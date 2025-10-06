from models.bid_model import BidModel
import requests
from PySide6.QtWidgets import (QPushButton, QLabel, QDialog, QHBoxLayout, QVBoxLayout)
from PySide6.QtCore import (Qt, QSize,QMargins, )
from PySide6.QtGui import (QFont, QPixmap)

class BidDetails(QDialog):
    def __init__(self, data: BidModel):
        super().__init__()
        self.setWindowTitle("Detalhes do Lote")
        self.setMinimumSize(800, 500)

        main_layout = QHBoxLayout(self)

        image_layout = QVBoxLayout()
        self.main_image = QLabel()
        self.loadImageFromUrl(self.main_image, data.url_image_cover)
        self.main_image.setFixedSize(300, 300)
        self.main_image.setScaledContents(True)
        image_layout.addWidget(self.main_image)

        thumbs_layout = QHBoxLayout()
        for thumb_url in [
            data.url_image_front_small,
            data.url_image_back_small
        ]:
            thumb = QLabel()
            self.loadImageFromUrl(thumb, thumb_url)
            thumb.setFixedSize(80, 80)
            thumb.setScaledContents(True)
            thumbs_layout.addWidget(thumb)
        image_layout.addLayout(thumbs_layout)
        main_layout.addLayout(image_layout)

        right_layout = QVBoxLayout()
        price = QLabel(f"Valor do lance mínimo: {data.value}")
        price.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        right_layout.addWidget(price)

        desc_title = QLabel("Descrição:")
        desc_title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        right_layout.addWidget(desc_title)

        description = QLabel(data.contract_description)
        description.setWordWrap(True)
        right_layout.addWidget(description)

        info_labels = {
            "Número do lote:": data.batch_number,
            "Número do contrato:": data.contract_number,
            "Centralizadora:": data.centralizing_name,
            "Data do Lance:": data.bid_date,
            "Resultado:": data.result_date,
            "Local da Retirada:": data.local_adress_description
        }

        for key, value in info_labels.items():
            hbox = QHBoxLayout()
            key_label = QLabel(key)
            key_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            value_label = QLabel(value)
            hbox.addWidget(key_label)
            hbox.addWidget(value_label)
            hbox.addStretch()
            right_layout.addLayout(hbox)

        # button_layout = QHBoxLayout()
        # btn_dar_lance = QPushButton("Como dar seu lance")
        # btn_edital = QPushButton("Baixar Edital")
        # btn_catalogo = QPushButton("Baixar Catálogo")
        # button_layout.addWidget(btn_dar_lance)
        # button_layout.addWidget(btn_edital)
        # button_layout.addWidget(btn_catalogo)

        # right_layout.addLayout(button_layout)
        main_layout.addLayout(right_layout)

    def loadImageFromUrl(self, label: QLabel, url: str):
        try:
            request = requests.get(f"https://servicebus2.caixa.gov.br/vitrinearquivos/fotos{url}")
            pixmap = QPixmap()
            pixmap.loadFromData(request.content)
            label.setPixmap(pixmap)
        except Exception as e:
            label.setText("Erro ao carregar imagem")