from concurrent.futures import ThreadPoolExecutor
import os
import sys

from components.bid_details import BidDetails
from requests import Session
from models.bid_model import BidModel
import requests
from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout,
    QScrollArea, QDialog, QPushButton
)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt

class BidCard(QPushButton):
    lote_info: BidModel
    def __init__(self, lote_info: BidModel, session: Session):
        super().__init__()
        layout = QVBoxLayout()
        layout.setSpacing(4)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.session =session
        self.lote_info = lote_info
        lote_label = QLabel(f"Nº lote {lote_info.batch_number}")
        uf_label = QLabel(lote_info.uf_acronym)
        valor_label = QLabel(lote_info.value)

        lote_label.setFont(QFont("Arial", 9))
        uf_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        uf_label.setFont(QFont("Arial", 9))
        valor_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        valor_label.setStyleSheet("color: #0077cc")

        top_row = QHBoxLayout()
        top_row.addWidget(lote_label)
        top_row.addWidget(uf_label)
        layout.addLayout(top_row)

        self.img_label = QLabel()
        self.img_label.setFixedSize(160, 120)
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.img_label)
        layout.addWidget(valor_label)

        self.setLayout(layout)
        self.setFixedSize(180, 200)
        self.clicked.connect(self.on_bid_has_choosen)
        
    def on_bid_has_choosen(self):
        details = BidDetails(self.lote_info)
        details.exec()
        
    def render_image(self):
        if self.lote_info.url_image_cover:
            try:
                response = self.session.get(f"https://servicebus2.caixa.gov.br/vitrinearquivos/fotos{self.lote_info.url_image_cover}")
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)   
                
                if not pixmap.isNull():
                    self.img_label.setPixmap(pixmap.scaled(160, 120, Qt.AspectRatioMode.KeepAspectRatio))
                else:
                    self.img_label.setText("Indisponível")
                    self.img_label.setFont(QFont("Arial", 10))
                    self.img_label.setStyleSheet("color: #888;")
            except:
                self.img_label.setText("Erro na imagem")
        else:
            self.img_label.setText("Indisponível")
            self.img_label.setFont(QFont("Arial", 10))
            self.img_label.setStyleSheet("color: #888;")

class ResultWindow(QDialog):
    cols = 3
    def __init__(self, data: list[BidModel]):
        super().__init__()
        self.setWindowTitle("Vitrine de Lotes")
        self.setMinimumSize(800, 600)

        scroll = QScrollArea()
        container = QWidget()
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(20)

        container.setLayout(self.grid_layout)
        scroll.setWidgetResizable(True)
        scroll.setWidget(container)
        main_layout = QHBoxLayout(self)
        main_layout.addWidget(scroll)
        self.render_cards(data)    

    def render_cards(self, data):
        session = requests.Session()
        pool = ThreadPoolExecutor()
        for i, lote in enumerate(data):
            row = i // self.cols
            col = i % self.cols
            card = BidCard(lote, session)
            self.grid_layout.addWidget(card, row, col)
            pool.submit(card.render_image)
        pool.shutdown()
            
            