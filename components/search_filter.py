from typing import Optional
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout
from PySide6.QtGui import (QFont)
class SearchFilter():
    def __init__(self, parent: QVBoxLayout, font: Optional[QFont] = None):
        self._label = QLabel(u"Busque por n\u00famero de contrato e/ou lote ou utilize os filtros.")
        self._label.setObjectName("fieldLabel")
        self._input = QLineEdit()
        self._input.setObjectName("searchInput")
        self._input.setPlaceholderText(u"Número do lote ou contrato")
        self._input.setClearButtonEnabled(True)
        self._input.setToolTip(u"Busque por número de lote ou contrato")
        if font != None:
            self._label.setFont(font)
            
        parent.addWidget(self._label)
        parent.addWidget(self._input)
