from typing import Optional

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel, QComboBox, QVBoxLayout


class BidPeriod:
    def __init__(self, parent: QVBoxLayout, font: Optional[QFont] = None):
        self._label = QLabel("Leilão*")
        self._label.setObjectName("fieldLabel")
        self._input = QComboBox()
        self._input.setObjectName("auctionInput")
        self._input.setPlaceholderText("Selecione um leilão")
        self._input.setToolTip("Leilão disponível no cronograma selecionado")
        if font is not None:
            self._label.setFont(font)
        parent.addWidget(self._label)
        parent.addWidget(self._input)

    def reset_periods(self):
        self._input.clear()
