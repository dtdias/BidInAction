from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QPushButton, QDialog, QLabel, QMessageBox
)
from PySide6.QtCore import (Qt, QSize, QMargins, QThread)
from PySide6.QtGui import (QFont, QPixmap)

from components.bit_period import BidPeriod
from components.pick_up_location import PickUpLocation
from components.search_filter import SearchFilter
from components.title import Title
from components.values_range import ValuesRange
from models.bid_query_model import BidQueryModel
from services.request_service import RequesterService
from services.storage_service import StorageService
from services.workers import SearchWorker
from views.result_window import ResultWindow
from views.loader_dialog import LoaderDialog
import os
from utils.resources import resource_path

class SearchWindow(QMainWindow):
    fontMedium = QFont()
    fontDefault = QFont()
    requester = RequesterService()
    city_by_uf: dict[str, list[dict]] = dict()
    bid_period_by_city: dict[str, list[dict]] = dict()
    storage = StorageService()
    wgSearchFilter: SearchFilter
    wgPickUpLocation: PickUpLocation
    wgBidPeriod: BidPeriod
    wgValuesRange: ValuesRange
    wgSubmitButton: QPushButton

    def __init__(self):
        super().__init__()
        self.main_view = QWidget()
        self.main_layout = QVBoxLayout(self.main_view)
        self.resize(650, 500)
        self.setMaximumSize(QSize(650, 500))
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.setWindowTitle(u"BUSCADOR VITRINE DE JOIAS CAIXA")
        self.setCentralWidget(self.main_view)
        self.initialize_fonts()

        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.setSpacing(15)
        self.main_view.setContentsMargins(QMargins(100, 40, 100, 0))

        # Topper image (logo)
        self.logo_label = QLabel(self.main_view)
        self.logo_label.setAlignment(Qt.AlignCenter)
        logo_path = resource_path(os.path.join("assets", "logo_vitrine_de_joias.png"))
        pix = QPixmap(logo_path)
        if not pix.isNull():
            # Redimensiona mantendo proporção (ajuste target_width conforme necessário)
            scaled = pix.scaledToWidth(500, Qt.SmoothTransformation)
            scaled = pix.scaledToHeight(60, Qt.SmoothTransformation)
            self.logo_label.setPixmap(scaled)
        else:
            self.logo_label.setText("Logo não encontrada")
        
        self.main_layout.addWidget(self.logo_label)

        self.wgTitle = Title(self.main_layout)
        self.wgTitle._label.setFont(self.fontMedium)

        self.wgSearchFilter = SearchFilter(self.main_layout)

        self.wgPickUpLocation = PickUpLocation(self.main_layout)
        self.wgPickUpLocation._label.setFont(self.fontMedium)
        self.wgPickUpLocation._inputUf.addItems([x.acronym for x in self.requester.request_uf_list()])

        from threading import Thread
        self.wgPickUpLocation._inputUf.currentTextChanged.connect(lambda o: Thread(target=self.onChangeUf, args=(o,)).start())
        self.wgPickUpLocation._inputCity.currentTextChanged.connect(lambda o: Thread(target=self.onChangeCity, args=(o,)).start())

        self.wgBidPeriod = BidPeriod(self.main_layout)
        self.wgBidPeriod._label.setFont(self.fontMedium)

        self.wgValuesRange = ValuesRange(self.main_layout)
        self.wgValuesRange._label.setFont(self.fontMedium)
        self.wgValuesRange._input.addItems(list(self.storage.values_range.keys()))

        self.wgSubmitButton = QPushButton(u"Continuar")
        self.wgSubmitButton.clicked.connect(self.onSubmitQuery)
        self.main_layout.addWidget(self.wgSubmitButton)

        # Placeholders para thread/loader
        self._thread = None
        self._loader = None

    def onChangeUf(self, uf: str):
        self.wgPickUpLocation.reset_inputCity()
        self.wgBidPeriod.reset_periods()

        cities = self.storage.cities
        if cities.get(uf) is None:
            cities[uf] = {}
            for city in self.requester.request_cities_list(uf):
                if cities[uf].get(city.name) is not None:
                    continue
                cities[uf][city.name] = city

        self.wgPickUpLocation._inputCity.addItems(list(cities[uf].keys()))

    def onChangeCity(self, city_name: str):
        if not city_name:
            return
        self.wgBidPeriod.reset_periods()

        periods = self.storage.periods
        uf = self.wgPickUpLocation._inputUf.currentText()
        city = self.storage.cities[uf][city_name]

        for period in self.requester.request_bid_period(city.code):
            if periods.get(city.name) is None:
                periods[city.name] = {}
            periods[city.name][period.bid_period] = period

        self.wgBidPeriod._input.addItems(list(periods[city_name].keys()))

    def onSubmitQuery(self):
        def warn_issue(issue: str):
            toasty = QDialog(self)
            layout = QVBoxLayout(toasty)
            layout.addWidget(QLabel(issue))
            toasty.setLayout(layout)
            toasty.exec()
            self.wgSubmitButton.setText("Continuar")

        filter_text = self.wgSearchFilter._input.text()
        uf = self.wgPickUpLocation._inputUf.currentText()
        if uf == "":
            return warn_issue("Selecione uma UF")

        city = self.wgPickUpLocation._inputCity.currentText()
        if city == "":
            return warn_issue("Selecione uma cidade")

        period_key = self.wgBidPeriod._input.currentText()
        if period_key == "":
            return warn_issue("Selecione um período de lance")
        period = self.storage.periods[city][period_key].start_date

        values_range_key = self.wgValuesRange._input.currentText()
        if values_range_key == "":
            return warn_issue("Selecione uma faixa de valor")
        values_range = self.storage.values_range[values_range_key]

        # Monta query
        query = BidQueryModel(filter_text, uf, self.storage.cities[uf][city].code, period, values_range)

        # Mostra loader e desabilita botão
        self.wgSubmitButton.setEnabled(False)
        self.wgSubmitButton.setText("Carregando...")
        self._loader = LoaderDialog("Buscando lotes, aguarde...", self)
        self._loader.show()

        # Cria worker + thread
        self._thread = QThread(self)
        self._worker = SearchWorker(query)
        self._worker.moveToThread(self._thread)

        # Conexões
        self._thread.started.connect(self._worker.run)
        self._worker.finished.connect(self._on_search_finished)
        self._worker.failed.connect(self._on_search_failed)

        # Encerramento limpo
        self._worker.finished.connect(self._thread.quit)
        self._worker.failed.connect(self._thread.quit)
        self._thread.finished.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)

        # Inicia
        self._thread.start()

    def _close_loader_and_restore_button(self):
        if self._loader is not None:
            self._loader.stop_and_fill()  # completa a barra em 100%
            self._loader.close()
            self._loader = None
        self.wgSubmitButton.setEnabled(True)
        self.wgSubmitButton.setText("Continuar")
        self.wgSubmitButton.setMinimumHeight(80)
        self.wgSubmitButton.setStyleSheet("""
    QPushButton {
        padding: 10px 16px;      /* padding interno do botão */
        font-size: 14px;         /* opcional: aumenta fonte */
        border-radius: 6px;      /* opcional: cantos arredondados */
    }
""")

    def _on_search_finished(self, result_list: list):
        self._close_loader_and_restore_button()
        if not result_list:
            # Nenhum resultado
            dlg = QDialog(self)
            layout = QVBoxLayout(dlg)
            layout.addWidget(QLabel("Nenhum resultado encontrado"))
            dlg.setLayout(layout)
            dlg.exec()
            return

        # Abre a janela de resultados modal (como já fazia)
        dialog = ResultWindow(result_list)
        dialog.exec()

    def _on_search_failed(self, error_msg: str):
        self._close_loader_and_restore_button()
        QMessageBox.critical(self, "Erro na busca", error_msg)

    def initialize_fonts(self):
        self.fontMedium.setPointSize(12)
        self.fontDefault.setPointSize(10)