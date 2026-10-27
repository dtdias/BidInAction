from datetime import date

from PySide6.QtCore import QObject, QRunnable, QThread, QSize, Qt, QThreadPool, Signal
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from components.bit_period import BidPeriod
from components.pick_up_location import PickUpLocation
from components.search_filter import SearchFilter
from components.title import Title
from components.values_range import ValuesRange
from models.auction_model import AuctionModel
from models.bid_query_model import BidQueryModel
from services.request_service import RequesterService
from services.storage_service import StorageService
from services.workers import SearchWorker
from utils.resources import resource_path
from views.loader_dialog import LoaderDialog
from views.result_window import ResultWindow


MONTHS = [
    "janeiro", "fevereiro", "março", "abril", "maio", "junho",
    "julho", "agosto", "setembro", "outubro", "novembro", "dezembro",
]


class ScheduleSignals(QObject):
    completed = Signal(int, object)
    failed = Signal(int, str)


class ScheduleTask(QRunnable):
    def __init__(self, requester: RequesterService, request_id: int, year: int, month: int):
        super().__init__()
        self.requester = requester
        self.request_id = request_id
        self.year = year
        self.month = month
        self.signals = ScheduleSignals()
        self.setAutoDelete(False)

    def run(self):
        try:
            self.signals.completed.emit(
                self.request_id, self.requester.request_schedule(self.year, self.month)
            )
        except Exception as error:
            self.signals.failed.emit(self.request_id, str(error))


class ScrollComboBox(QComboBox):
    popup_opened = Signal()

    def showPopup(self):
        self.popup_opened.emit()
        super().showPopup()


class SearchWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.requester = RequesterService()
        self.storage = StorageService()
        self._lookup_pool = QThreadPool(self)
        self._schedule_tasks = []
        self._schedule_request_id = 0
        self._schedule: dict = {}
        self._auctions: list[AuctionModel] = []
        self._schedule_loading = False
        self._thread = None
        self._loader = None
        self.resize(900, 760)
        self.setMinimumSize(QSize(720, 620))
        self.setWindowTitle("Leilão Vitrine de Joias | CAIXA")
        self._build_ui()
        self._request_schedule()

    def _build_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(32, 28, 32, 32)
        layout.setSpacing(20)
        scroll.setWidget(content)
        self.setCentralWidget(scroll)

        hero = QFrame()
        hero.setObjectName("heroPanel")
        hero_layout = QVBoxLayout(hero)
        hero_layout.setContentsMargins(24, 20, 24, 22)
        banner = QLabel()
        banner.setObjectName("brandLogo")
        banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo = QPixmap(resource_path("assets/logo_vitrine_de_joias.png"))
        if not logo.isNull():
            banner.setPixmap(
                logo.scaled(
                    680,
                    86,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        else:
            banner.setText("Leilão Vitrine de Joias")
        hero_layout.addWidget(banner)
        hero_layout.addWidget(self._label("CAIXA  •  LEILÃO VITRINE DE JOIAS", "heroKicker"))
        subtitle = self._label(
            "Consulte cronograma, lotes, imagens e documentos oficiais da CAIXA.",
            "heroSubtitle",
        )
        subtitle.setWordWrap(True)
        hero_layout.addWidget(subtitle)
        layout.addWidget(hero)

        card = QFrame()
        card.setObjectName("searchCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(18)
        self.title = Title(card_layout)

        grid = QGridLayout()
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(16)
        schedule_group = QFrame()
        schedule_layout = QHBoxLayout(schedule_group)
        schedule_layout.setContentsMargins(0, 0, 0, 0)
        self.year_input = self._combo("Ano")
        self.month_input = self._combo("Mês")
        today = date.today()
        self.year_input.addItem(str(today.year), today.year)
        self.month_input.addItem(MONTHS[today.month - 1].capitalize(), today.month)
        self.year_input.setCurrentIndex(0)
        self.month_input.setCurrentIndex(0)
        self.year_input.popup_opened.connect(self._refresh_year_options)
        self.year_input.currentIndexChanged.connect(self._request_schedule)
        self.month_input.currentIndexChanged.connect(self._request_schedule)
        schedule_layout.addWidget(self._field("Ano", self.year_input))
        schedule_layout.addWidget(self._field("Mês", self.month_input))

        search_group, self.wgSearchFilter = self._make_field_group(SearchFilter)
        location_group, self.wgPickUpLocation = self._make_field_group(PickUpLocation)
        auction_group, self.wgBidPeriod = self._make_field_group(BidPeriod)
        value_group, self.wgValuesRange = self._make_field_group(ValuesRange)
        self.wgValuesRange._input.addItems(list(self.storage.values_range.keys()))
        self.wgPickUpLocation._inputUf.currentTextChanged.connect(self._update_cities)
        self.wgPickUpLocation._inputCity.currentTextChanged.connect(self._update_auctions)
        for dropdown in (
            self.wgPickUpLocation._inputUf,
            self.wgPickUpLocation._inputCity,
            self.wgBidPeriod._input,
            self.wgValuesRange._input,
        ):
            self._configure_dropdown(dropdown)

        grid.addWidget(schedule_group, 0, 0, 1, 2)
        grid.addWidget(search_group, 1, 0, 1, 2)
        grid.addWidget(location_group, 2, 0)
        grid.addWidget(auction_group, 2, 1)
        grid.addWidget(value_group, 3, 0, 1, 2)
        card_layout.addLayout(grid)

        footer = QHBoxLayout()
        self.status_label = self._label("Carregando cronograma...", "formStatus")
        self.status_label.setWordWrap(True)
        footer.addWidget(self.status_label, 1)
        self.retry_button = QPushButton("Tentar novamente")
        self.retry_button.setObjectName("secondaryButton")
        self.retry_button.clicked.connect(self._request_schedule)
        self.retry_button.hide()
        footer.addWidget(self.retry_button)
        self.wgSubmitButton = QPushButton("Buscar lotes")
        self.wgSubmitButton.setObjectName("primaryButton")
        self.wgSubmitButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.wgSubmitButton.clicked.connect(self.on_submit_query)
        footer.addWidget(self.wgSubmitButton)
        card_layout.addLayout(footer)
        layout.addWidget(card)
        layout.addStretch(1)
        self.wgSearchFilter._input.returnPressed.connect(self.on_submit_query)
        self._set_filters_enabled(False)

    def _label(self, text: str, object_name: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName(object_name)
        return label

    def _combo(self, placeholder: str) -> ScrollComboBox:
        combo = ScrollComboBox()
        combo.setPlaceholderText(placeholder)
        self._configure_dropdown(combo)
        return combo

    def _configure_dropdown(self, combo: QComboBox):
        combo.setMaxVisibleItems(8)
        combo.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        combo.view().setMaximumHeight(260)
        combo.view().setUniformItemSizes(True)

    def _field(self, label: str, widget: QWidget) -> QWidget:
        container = QFrame()
        field_layout = QVBoxLayout(container)
        field_layout.setContentsMargins(0, 0, 0, 0)
        field_layout.setSpacing(7)
        field_layout.addWidget(self._label(label, "fieldLabel"))
        field_layout.addWidget(widget)
        return container

    def _make_field_group(self, component_type):
        group = QFrame()
        field_layout = QVBoxLayout(group)
        field_layout.setContentsMargins(0, 0, 0, 0)
        field_layout.setSpacing(7)
        return group, component_type(field_layout)

    def _set_status(self, text: str, state: str = "ready"):
        self.status_label.setText(text)
        self.status_label.setProperty("state", state)
        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)

    def _set_filters_enabled(self, enabled: bool):
        for widget in (
            self.wgPickUpLocation._inputUf,
            self.wgPickUpLocation._inputCity,
            self.wgBidPeriod._input,
            self.wgValuesRange._input,
            self.wgSubmitButton,
        ):
            widget.setEnabled(enabled)

    def _refresh_year_options(self):
        if self._schedule:
            self._populate_schedule_options(self._schedule)
        elif not self._schedule_loading:
            self._request_schedule()

    def _request_schedule(self, *_):
        if not self.year_input.currentData() or not self.month_input.currentData():
            return
        self._schedule_request_id += 1
        request_id = self._schedule_request_id
        self._schedule_loading = True
        self._set_filters_enabled(False)
        self.retry_button.hide()
        self._set_status("Carregando cronograma...", "loading")
        task = ScheduleTask(
            self.requester, request_id, int(self.year_input.currentData()), int(self.month_input.currentData())
        )
        task.signals.completed.connect(self._on_schedule_loaded)
        task.signals.failed.connect(self._on_schedule_failed)
        self._schedule_tasks.append(task)
        self._lookup_pool.start(task)

    def _on_schedule_loaded(self, request_id: int, schedule: dict):
        if request_id != self._schedule_request_id:
            return
        self._schedule_loading = False
        self._schedule = schedule
        self._populate_schedule_options(schedule)
        self._auctions = [AuctionModel.from_api(item) for item in schedule.get("leiloes", [])]
        self.wgPickUpLocation._inputUf.blockSignals(True)
        self.wgPickUpLocation._inputUf.clear()
        self.wgPickUpLocation._inputUf.addItems(sorted({item.uf for item in self._auctions if item.uf}))
        self.wgPickUpLocation._inputUf.blockSignals(False)
        self._update_cities(self.wgPickUpLocation._inputUf.currentText())
        self._set_filters_enabled(bool(self._auctions))
        self._set_status(
            "Selecione UF, cidade e leilão." if self._auctions else "Nenhum leilão neste período.",
            "ready" if self._auctions else "error",
        )

    def _on_schedule_failed(self, request_id: int, error: str):
        if request_id != self._schedule_request_id:
            return
        self._schedule_loading = False
        self._set_filters_enabled(False)
        self.retry_button.show()
        self._set_status(f"Falha ao carregar cronograma: {error}", "error")

    def _populate_schedule_options(self, schedule: dict):
        selected_year = self.year_input.currentData()
        selected_month = self.month_input.currentData()
        years = schedule.get("anos", [])
        months = schedule.get("meses", [])
        self.year_input.blockSignals(True)
        self.year_input.clear()
        for year in years:
            self.year_input.addItem(str(year), int(year))
        self.year_input.setCurrentIndex(max(0, self.year_input.findData(selected_year)))
        self.year_input.blockSignals(False)
        self.month_input.blockSignals(True)
        self.month_input.clear()
        for index, month in enumerate(months, 1):
            self.month_input.addItem(str(month).capitalize(), index)
        self.month_input.setCurrentIndex(max(0, self.month_input.findData(selected_month)))
        self.month_input.blockSignals(False)

    def _update_cities(self, uf: str):
        cities = sorted({item.city for item in self._auctions if item.uf == uf})
        self.wgPickUpLocation._inputCity.blockSignals(True)
        self.wgPickUpLocation._inputCity.clear()
        self.wgPickUpLocation._inputCity.addItems(cities)
        self.wgPickUpLocation._inputCity.blockSignals(False)
        self._update_auctions(self.wgPickUpLocation._inputCity.currentText())

    def _update_auctions(self, city: str):
        uf = self.wgPickUpLocation._inputUf.currentText()
        auctions = [item for item in self._auctions if item.uf == uf and item.city == city]
        self.wgBidPeriod._input.clear()
        for auction in auctions:
            self.wgBidPeriod._input.addItem(auction.label, auction)

    def on_submit_query(self):
        auction = self.wgBidPeriod._input.currentData()
        if not isinstance(auction, AuctionModel):
            self._set_status("Selecione um leilão.", "error")
            return
        values = self.storage.values_range[self.wgValuesRange._input.currentText()]
        text = self.wgSearchFilter._input.text().strip()
        query = BidQueryModel(
            auction_code=auction.code,
            min_value=values.get("min", 0),
            max_value=values.get("max", 0),
            lot_number=text if text.replace(".", "").replace("-", "").isdigit() else "",
            description="" if text.replace(".", "").replace("-", "").isdigit() else text,
        )
        self._active_query = query
        self._set_status("Consultando lotes na CAIXA...", "loading")
        self.wgSubmitButton.setEnabled(False)
        self._loader = LoaderDialog("Consultando catálogo de lotes", self)
        self._loader.show()
        self._thread = QThread(self)
        self._worker = SearchWorker(query)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.finished.connect(self._on_search_finished)
        self._worker.failed.connect(self._on_search_failed)
        self._worker.finished.connect(self._thread.quit)
        self._worker.failed.connect(self._thread.quit)
        self._thread.finished.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)
        self._thread.start()

    def _close_loader(self):
        if self._loader:
            self._loader.stop_and_fill()
            self._loader.close()
            self._loader = None
        self.wgSubmitButton.setEnabled(True)

    def _on_search_finished(self, result):
        self._close_loader()
        if not result.lots:
            self._set_status("Nenhum lote encontrado.", "ready")
            return
        self._set_status(f"{result.total} lotes encontrados.", "success")
        ResultWindow(result, self.requester, self._active_query).exec()

    def _on_search_failed(self, error: str):
        self._close_loader()
        self._set_status(f"Falha na busca: {error}", "error")
