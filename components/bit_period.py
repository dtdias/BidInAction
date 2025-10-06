from typing import Optional
from PySide6.QtWidgets import QWidget, QLabel, QComboBox, QVBoxLayout
from PySide6.QtGui import QFont
class BidPeriod():
    def __init__(self, parent: QVBoxLayout, font: Optional[QFont] = None):
        self._label = QLabel(u"Per\u00edodo de lance*")
        self._input = QComboBox(placeholderText=u"Per\u00edodo de lance")
        self._input.setToolTip(u"Busque por numero de lote ou contrato")
        if font != None:
            self._label.setFont(font)
        
        parent.addWidget(self._label)
        parent.addWidget(self._input)
    
    def reset_periods(self):
        self._input.clear()