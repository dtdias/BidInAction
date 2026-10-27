from pathlib import Path

from PySide6.QtCore import QObject, QRunnable, Qt, QThreadPool, Signal
from PySide6.QtGui import QDoubleValidator, QPixmap
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from components.pdf_exporter import export_bid_details_to_pdf
from components.image_viewer import ImageViewer
from models.bid_model import BidDetail, BidModel, PublishedFile
from services.request_service import DownloadedFile, RequesterService


class DetailSignals(QObject):
    loaded = Signal(object)
    failed = Signal(str)


class DetailTask(QRunnable):
    def __init__(self, requester: RequesterService, auction_code: str, contract_number: str):
        super().__init__()
        self.requester = requester
        self.auction_code = auction_code
        self.contract_number = contract_number
        self.signals = DetailSignals()

    def run(self):
        try:
            self.signals.loaded.emit(
                self.requester.request_lot_detail(self.auction_code, self.contract_number)
            )
        except Exception as error:
            self.signals.failed.emit(str(error))


class DownloadSignals(QObject):
    loaded = Signal(object)
    failed = Signal(str)


class DownloadTask(QRunnable):
    def __init__(self, requester: RequesterService, documents: list[PublishedFile]):
        super().__init__()
        self.requester = requester
        self.documents = documents
        self.signals = DownloadSignals()

    def run(self):
        try:
            self.signals.loaded.emit(self.requester.download_documents(self.documents))
        except Exception as error:
            self.signals.failed.emit(str(error))


class ClickableImageLabel(QLabel):
    clicked = Signal()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.pixmap() and not self.pixmap().isNull():
            self.clicked.emit()
            event.accept()
            return
        super().mousePressEvent(event)


class BidDetails(QDialog):
    def __init__(self, data: BidModel, requester: RequesterService):
        super().__init__()
        self.setWindowTitle("Detalhes do lote | Caixa")
        self.setMinimumSize(900, 600)
        self.resize(1040, 700)
        self.data = data
        self.requester = requester
        self._pool = QThreadPool(self)
        self._tasks = []
        self._build_ui()
        self._render_photos()
        self._load_detail()

    def _build_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)
        media_panel = QFrame()
        media_panel.setObjectName("mediaPanel")
        media_layout = QVBoxLayout(media_panel)
        media_layout.setContentsMargins(18, 18, 18, 18)
        media_layout.addWidget(self._label("Galeria do lote", "subsectionTitle"))
        self.main_image = ClickableImageLabel("Imagem indisponível")
        self.main_image.setObjectName("cardImage")
        self.main_image.setFixedSize(360, 280)
        self.main_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_image.setCursor(Qt.CursorShape.PointingHandCursor)
        self.main_image.setToolTip("Clique para ampliar. Use a roda do mouse para zoom.")
        self.main_image.clicked.connect(lambda: self._open_image(0))
        media_layout.addWidget(self.main_image)
        self.thumb_row = QHBoxLayout()
        self.thumb_row.setSpacing(10)
        self.thumb_labels: list[QLabel] = []
        self.photo_pixmaps: list[QPixmap] = []
        self.thumb_row.addStretch(1)
        media_layout.addLayout(self.thumb_row)
        media_layout.addStretch(1)
        main_layout.addWidget(media_panel)

        panel = QFrame()
        panel.setObjectName("detailsPanel")
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(20, 18, 20, 18)
        actions = QHBoxLayout()
        actions.addWidget(self._label("Acréscimo", "fieldLabel"))
        self.input_additional = QLineEdit()
        self.input_additional.setObjectName("percentInput")
        self.input_additional.setPlaceholderText("0,00")
        self.input_additional.setFixedWidth(86)
        validator = QDoubleValidator(0.0, 100.0, 2, self)
        self.input_additional.setValidator(validator)
        actions.addWidget(self.input_additional)
        actions.addWidget(self._label("%", "fieldLabel"))
        actions.addStretch(1)
        self.btn_documents = QPushButton("Documentos oficiais")
        self.btn_documents.setObjectName("secondaryButton")
        self.btn_documents.setEnabled(bool(self.data.published_files))
        self.btn_documents.clicked.connect(self._choose_documents)
        actions.addWidget(self.btn_documents)
        self.btn_download = QPushButton("Exportar PDF")
        self.btn_download.setObjectName("secondaryButton")
        self.btn_download.setEnabled(False)
        self.btn_download.clicked.connect(self.on_download_pdf)
        actions.addWidget(self.btn_download)
        panel_layout.addLayout(actions)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        content = QWidget()
        details_layout = QVBoxLayout(content)
        details_layout.setContentsMargins(0, 8, 8, 8)
        details_layout.setSpacing(12)
        details_layout.addWidget(self._label("Detalhes do lote", "detailTitle"))
        self.price = self._label(f"Valor do lance mínimo: {self.data.value}", "priceLabel")
        self.price.setWordWrap(True)
        details_layout.addWidget(self.price)
        details_layout.addWidget(self._label("Descrição", "subsectionTitle"))
        self.description = self._label("Carregando detalhes...", "descriptionLabel")
        self.description.setWordWrap(True)
        details_layout.addWidget(self.description)
        details_layout.addWidget(self._label("Informações do lote", "subsectionTitle"))
        self.info_labels = {
            "Número do lote:": self.data.batch_number,
            "Número do contrato:": self.data.contract_number,
            "Centralizadora:": self.data.centralizing_name,
            "Data do Lance:": self.data.bid_date,
            "Resultado:": self.data.result_date,
            "Local da Retirada:": self.data.local_address_description,
        }
        self._info_values: dict[str, QLabel] = {}
        for key, value in self.info_labels.items():
            row = QHBoxLayout()
            key_label = self._label(key, "infoKey")
            key_label.setMinimumWidth(140)
            value_label = self._label(str(value or "N/A"), "infoValue")
            value_label.setWordWrap(True)
            row.addWidget(key_label)
            row.addWidget(value_label, 1)
            details_layout.addLayout(row)
            self._info_values[key] = value_label
        details_layout.addStretch(1)
        scroll.setWidget(content)
        panel_layout.addWidget(scroll, 1)
        main_layout.addWidget(panel, 1)

    def _label(self, text: str, object_name: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName(object_name)
        return label

    def _render_photos(self):
        images: list[QPixmap] = []
        for photo in self.data.photos:
            try:
                pixmap = QPixmap()
                if pixmap.loadFromData(photo.bytes()):
                    images.append(pixmap)
            except (ValueError, TypeError):
                continue
        if images:
            self.photo_pixmaps = images
            self.main_image.setText("")
            self.main_image.setPixmap(
                images[0].scaled(
                    self.main_image.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        for index, pixmap in enumerate(images[1:], 1):
            thumbnail = ClickableImageLabel()
            thumbnail.setObjectName("cardImage")
            thumbnail.setFixedSize(112, 88)
            thumbnail.setAlignment(Qt.AlignmentFlag.AlignCenter)
            thumbnail.setCursor(Qt.CursorShape.PointingHandCursor)
            thumbnail.setToolTip("Clique para ampliar")
            thumbnail.setPixmap(
                pixmap.scaled(
                    thumbnail.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
            thumbnail.clicked.connect(lambda index=index: self._open_image(index))
            self.thumb_row.insertWidget(self.thumb_row.count() - 1, thumbnail)
            self.thumb_labels.append(thumbnail)

    def _open_image(self, index: int):
        if index < len(self.photo_pixmaps):
            ImageViewer(self.photo_pixmaps[index], f"Foto {index + 1} do lote", self).exec()

    def _load_detail(self):
        task = DetailTask(self.requester, self.data.bid_code, self.data.contract_number)
        task.signals.loaded.connect(self._apply_detail)
        task.signals.failed.connect(self._detail_failed)
        self._tasks.append(task)
        self._pool.start(task)

    def _apply_detail(self, detail: BidDetail):
        self.data.contract_description = detail.description
        self.data.value = detail.value or self.data.value
        self.data.batch_number = detail.lot_number or self.data.batch_number
        self.data.result_date = detail.result_date
        self.data.local_address_description = detail.pickup_address
        self.price.setText(f"Valor do lance mínimo: {self.data.value}")
        self.description.setText(self.data.contract_description or "N/A")
        self.info_labels.update(
            {
                "Número do lote:": self.data.batch_number,
                "Número do contrato:": self.data.contract_number,
                "Resultado:": self.data.result_date,
                "Local da Retirada:": self.data.local_address_description,
            }
        )
        for key, label in self._info_values.items():
            label.setText(str(self.info_labels[key] or "N/A"))
        self.btn_download.setEnabled(True)

    def _detail_failed(self, error: str):
        self.description.setText(f"Não foi possível carregar detalhes: {error}")
        self.btn_download.setEnabled(True)

    def _choose_documents(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Documentos oficiais")
        layout = QVBoxLayout(dialog)
        checks: list[tuple[QCheckBox, PublishedFile]] = []
        for document in self.data.published_files:
            check = QCheckBox(document.file_type)
            check.setToolTip(document.name)
            layout.addWidget(check)
            checks.append((check, document))
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Save)
        buttons.rejected.connect(dialog.reject)
        buttons.accepted.connect(dialog.accept)
        layout.addWidget(buttons)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        selected = [document for check, document in checks if check.isChecked()]
        if not selected:
            QMessageBox.warning(self, "Documentos", "Selecione ao menos um documento.")
            return
        self.btn_documents.setEnabled(False)
        task = DownloadTask(self.requester, selected)
        task.signals.loaded.connect(self._save_documents)
        task.signals.failed.connect(self._document_failed)
        self._tasks.append(task)
        self._pool.start(task)

    def _save_documents(self, download: DownloadedFile):
        self.btn_documents.setEnabled(True)
        filename = Path(download.filename).name or "Documentos.zip"
        filter_text = "PDF (*.pdf)" if "pdf" in download.content_type.lower() else "Arquivo compactado (*.zip)"
        path, _ = QFileDialog.getSaveFileName(self, "Salvar documentos", filename, filter_text)
        if not path:
            return
        try:
            self.requester.save_download(download, path)
            QMessageBox.information(self, "Documentos", "Documentos salvos com sucesso.")
        except OSError as error:
            QMessageBox.critical(self, "Documentos", f"Falha ao salvar documentos:\n{error}")

    def _document_failed(self, error: str):
        self.btn_documents.setEnabled(True)
        QMessageBox.critical(self, "Documentos", f"Falha ao baixar documentos:\n{error}")

    def on_download_pdf(self):
        text = self.input_additional.text().strip()
        try:
            percent_multiplier = float(text.replace(",", ".")) / 100 if text else 0
        except ValueError:
            percent_multiplier = 0
        path, _ = QFileDialog.getSaveFileName(
            self, "Salvar PDF", f"Lote_{self.data.batch_number or 'detalhes'}.pdf", "PDF (*.pdf)"
        )
        if not path:
            return
        try:
            export_bid_details_to_pdf(self, path, percent_multiplier)
            QMessageBox.information(self, "Sucesso", "PDF gerado com sucesso.")
        except Exception as error:
            QMessageBox.critical(self, "Erro", f"Falha ao gerar PDF:\n{error}")

    def closeEvent(self, event):
        self._pool.clear()
        super().closeEvent(event)
