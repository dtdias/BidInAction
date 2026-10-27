from dataclasses import replace

from PySide6.QtCore import QObject, QRunnable, QSize, Qt, QThreadPool, Signal
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from components.bid_details import BidDetails
from models.bid_model import BidModel, BidSearchResult
from models.bid_query_model import BidQueryModel
from services.request_service import RequesterService


class ImageSignals(QObject):
    loaded = Signal(QImage)
    failed = Signal()


class ImageLoader(QRunnable):
    def __init__(self, lot: BidModel):
        super().__init__()
        self.lot = lot
        self.signals = ImageSignals()
        self.setAutoDelete(False)

    def run(self):
        try:
            if not self.lot.photos:
                raise ValueError("Lote sem fotos")
            image = QImage.fromData(self.lot.photos[0].bytes())
            if image.isNull():
                raise ValueError("Imagem inválida")
            self.signals.loaded.emit(image)
        except Exception:
            self.signals.failed.emit()


class PageSignals(QObject):
    loaded = Signal(object)
    failed = Signal(str)


class PageTask(QRunnable):
    def __init__(self, requester: RequesterService, query: BidQueryModel):
        super().__init__()
        self.requester = requester
        self.query = query
        self.signals = PageSignals()

    def run(self):
        try:
            self.signals.loaded.emit(self.requester.request_lots(self.query))
        except Exception as error:
            self.signals.failed.emit(str(error))


class BidCard(QPushButton):
    def __init__(self, lot: BidModel, requester: RequesterService):
        super().__init__()
        self.setObjectName("bidCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMinimumSize(QSize(210, 250))
        self.lot = lot
        self.requester = requester
        self._image_loader = None
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(8)
        header = QHBoxLayout()
        lot_label = QLabel(f"Lote {lot.batch_number}")
        lot_label.setObjectName("cardCaption")
        uf_label = QLabel(lot.uf_acronym)
        uf_label.setObjectName("cardCaption")
        header.addWidget(lot_label)
        header.addStretch(1)
        header.addWidget(uf_label)
        layout.addLayout(header)
        self.img_label = QLabel("Carregando imagem...")
        self.img_label.setObjectName("cardImage")
        self.img_label.setMinimumSize(QSize(180, 145))
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.img_label)
        value = QLabel(lot.value)
        value.setObjectName("cardValue")
        layout.addWidget(value)
        self.clicked.connect(self._show_details)

    def _show_details(self):
        BidDetails(self.lot, self.requester).exec()

    def load_image(self, thread_pool: QThreadPool):
        self._image_loader = ImageLoader(self.lot)
        self._image_loader.signals.loaded.connect(self._on_image_loaded)
        self._image_loader.signals.failed.connect(self._render_image_fail)
        thread_pool.start(self._image_loader)

    def _on_image_loaded(self, image: QImage):
        pixmap = QPixmap.fromImage(image)
        self.img_label.setText("")
        self.img_label.setPixmap(
            pixmap.scaled(220, 155, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        )

    def _render_image_fail(self):
        self.img_label.setText("Imagem indisponível")


class ResultWindow(QDialog):
    def __init__(self, result: BidSearchResult, requester: RequesterService, query: BidQueryModel):
        super().__init__()
        self.setWindowTitle("Lotes encontrados | Caixa")
        self.setMinimumSize(820, 600)
        self.resize(1040, 720)
        self.requester = requester
        self.query = query
        self.result = result
        self.cards: list[BidCard] = []
        self._thread_pool = QThreadPool(self)
        self._tasks = []
        self._build_ui()
        self._render_result(result)

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 24, 26, 26)
        header = QHBoxLayout()
        title = QLabel("Lotes encontrados")
        title.setObjectName("dialogTitle")
        header.addWidget(title)
        header.addStretch(1)
        self.total_label = QLabel()
        self.total_label.setObjectName("dialogMeta")
        header.addWidget(self.total_label)
        layout.addLayout(header)
        self.status_label = QLabel()
        self.status_label.setObjectName("dialogMeta")
        layout.addWidget(self.status_label)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        container = QWidget()
        self.grid_layout = QGridLayout(container)
        self.grid_layout.setContentsMargins(4, 4, 4, 4)
        self.grid_layout.setHorizontalSpacing(16)
        self.grid_layout.setVerticalSpacing(16)
        self.scroll.setWidget(container)
        layout.addWidget(self.scroll, 1)
        controls = QHBoxLayout()
        self.previous_button = QPushButton("Anterior")
        self.next_button = QPushButton("Próxima")
        self.previous_button.setObjectName("secondaryButton")
        self.next_button.setObjectName("secondaryButton")
        self.previous_button.clicked.connect(lambda: self._load_page(self.query.page - 1))
        self.next_button.clicked.connect(lambda: self._load_page(self.query.page + 1))
        controls.addWidget(self.previous_button)
        controls.addWidget(self.next_button)
        controls.addStretch(1)
        layout.addLayout(controls)

    def _render_result(self, result: BidSearchResult):
        self.result = result
        self.total_label.setText(f"{result.total} lote(s)")
        self.status_label.setText(f"Página {self.query.page} de {max(1, -(-result.total // self.query.limit))}")
        self.previous_button.setEnabled(self.query.page > 1)
        self.next_button.setEnabled(self.query.page * self.query.limit < result.total)
        for card in self.cards:
            card.deleteLater()
        self.cards.clear()
        while self.grid_layout.count():
            self.grid_layout.takeAt(0)
        for lot in result.lots:
            card = BidCard(lot, self.requester)
            self.cards.append(card)
            card.load_image(self._thread_pool)
        self._relayout_cards()

    def _load_page(self, page: int):
        if page < 1:
            return
        self.query = replace(self.query, page=page)
        self.previous_button.setEnabled(False)
        self.next_button.setEnabled(False)
        self.status_label.setText("Carregando página...")
        task = PageTask(self.requester, self.query)
        task.signals.loaded.connect(self._render_result)
        task.signals.failed.connect(self._page_failed)
        self._tasks.append(task)
        self._thread_pool.start(task)

    def _page_failed(self, error: str):
        self.status_label.setText(f"Falha ao carregar página: {error}")
        self.previous_button.setEnabled(self.query.page > 1)
        self.next_button.setEnabled(self.query.page * self.query.limit < self.result.total)

    def _relayout_cards(self):
        cols = max(1, min(4, self.scroll.viewport().width() // 250))
        for index, card in enumerate(self.cards):
            self.grid_layout.addWidget(card, index // cols, index % cols)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.cards:
            while self.grid_layout.count():
                self.grid_layout.takeAt(0)
            self._relayout_cards()

    def closeEvent(self, event):
        self._thread_pool.clear()
        super().closeEvent(event)
