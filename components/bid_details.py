# bid_details.py
from models.bid_model import BidModel
import requests
from requests.adapters import HTTPAdapter, Retry
from PySide6.QtWidgets import (
    QPushButton, QLabel, QDialog, QHBoxLayout, QVBoxLayout, QFileDialog, QMessageBox, QLineEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap, QDoubleValidator

from components.pdf_exporter import export_bid_details_to_pdf  # importa o módulo novo

IMG_BASE = "https://servicebus2.caixa.gov.br/vitrinearquivos/fotos"

def make_session_with_retry(total=2, backoff=0.3):
    s = requests.Session()
    retries = Retry(
        total=total,
        backoff_factor=backoff,
        status_forcelist=(500, 502, 503, 504),
        allowed_methods=["GET"],
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retries)
    s.mount("http://", adapter)
    s.mount("https://", adapter)
    return s

class BidDetails(QDialog):
    def __init__(self, data: BidModel):
        super().__init__()
        self.setWindowTitle("Detalhes do Lote")
        self.setMinimumSize(800, 500)
        self.data = data
        self.http = make_session_with_retry()

        main_layout = QHBoxLayout(self)

        # Imagens à esquerda
        image_layout = QVBoxLayout()
        self.main_image = QLabel()
        self.loadImageFromUrl(self.main_image, data.url_image_cover)
        self.main_image.setFixedSize(300, 300)
        self.main_image.setScaledContents(True)
        image_layout.addWidget(self.main_image)

        thumbs_layout = QHBoxLayout()
        self.thumb_labels = []
        for thumb_url in [data.url_image_front_small, data.url_image_back_small]:
            thumb = QLabel()
            self.loadImageFromUrl(thumb, thumb_url)
            thumb.setFixedSize(140, 140)
            thumb.setScaledContents(True)
            thumbs_layout.addWidget(thumb)
            self.thumb_labels.append(thumb)
        image_layout.addLayout(thumbs_layout)
        main_layout.addLayout(image_layout)

        # Info + botão download à direita
        right_layout = QVBoxLayout()

        # Linha superior: Adicional (%) + botão Baixar
        top_row = QHBoxLayout()
        # Campo de adicional (percentual)
        lbl_add = QLabel("Adicional %:")
        lbl_add.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.input_additional = QLineEdit()
        self.input_additional.setPlaceholderText("0")  # em porcentagem, ex.: 5 para 5%
        self.input_additional.setFixedWidth(80)
        # Aceitar apenas números (0 a 100, com 2 casas decimais)
        validator = QDoubleValidator(0.0, 100.0, 2, self)
        validator.setNotation(QDoubleValidator.StandardNotation)
        self.input_additional.setValidator(validator)
        # Alinhar conteúdo à direita
        self.input_additional.setAlignment(Qt.AlignRight)

        top_row.addWidget(lbl_add)
        top_row.addWidget(self.input_additional)
        top_row.addStretch()

        self.btn_download = QPushButton("Baixar")
        self.btn_download.setToolTip("Baixar PDF desta página")
        self.btn_download.clicked.connect(self.on_download_pdf)
        top_row.addWidget(self.btn_download)

        right_layout.addLayout(top_row)

        price = QLabel(f"Valor do lance mínimo: {data.value}")
        price.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        right_layout.addWidget(price)

        desc_title = QLabel("Descrição:")
        desc_title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        right_layout.addWidget(desc_title)

        self.description = QLabel(data.contract_description)
        self.description.setWordWrap(True)
        right_layout.addWidget(self.description)

        self.info_labels = {
            "Número do lote:": data.batch_number,
            "Número do contrato:": data.contract_number,
            "Centralizadora:": data.centralizing_name,
            "Data do Lance:": data.bid_date,
            "Resultado:": data.result_date,
            "Local da Retirada:": data.local_adress_description,
        }

        for key, value in self.info_labels.items():
            row = QHBoxLayout()
            key_label = QLabel(key)
            key_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            val_label = QLabel(value)
            val_label.setWordWrap(True)
            row.addWidget(key_label)
            row.addWidget(val_label, 1)
            row.addStretch()
            right_layout.addLayout(row)

        main_layout.addLayout(right_layout)

    def loadImageFromUrl(self, label: QLabel, url: str):
        try:
            if not url:
                label.setText("Imagem indisponível")
                return
            full_url = f"{IMG_BASE}{url}"
            resp = self.http.get(full_url, timeout=10)
            if resp.status_code >= 500:
                alt_url = self._try_alt_image_url(full_url)
                if alt_url:
                    resp = self.http.get(alt_url, timeout=10)
            if resp.status_code != 200 or not resp.content:
                label.setText("Imagem indisponível")
                return
            pixmap = QPixmap()
            pixmap.loadFromData(resp.content)
            if pixmap.isNull():
                label.setText("Imagem indisponível")
            else:
                label.setPixmap(pixmap)
        except Exception:
            label.setText("Imagem indisponível")

    def _try_alt_image_url(self, full_url: str) -> str | None:
        try:
            if full_url.upper().endswith("FRENTEP.JPG"):
                return full_url[:-5] + ".JPG"
            if full_url.endswith(".JPG"):
                return full_url[:-4] + ".jpg"
        except Exception:
            pass
        return None

    def on_download_pdf(self):
        # Lê o percentual informado (em %), converte para fração
        text = (self.input_additional.text() or "").strip()
        try:
            percent_multiplier = float(text.replace(",", ".")) / 100.0 if text else 0.0
        except ValueError:
            percent_multiplier = 0.0

        suggested = f"Lote_{self.data.batch_number or 'detalhes'}.pdf"
        file_path, _ = QFileDialog.getSaveFileName(self, "Salvar PDF", suggested, "PDF (*.pdf)")
        if not file_path:
            return
        try:
            export_bid_details_to_pdf(self, file_path, percent_multiplier=percent_multiplier)
            QMessageBox.information(self, "Sucesso", "PDF gerado com sucesso.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao gerar PDF:\n{e}")