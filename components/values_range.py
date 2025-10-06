from typing import Optional
from PySide6.QtWidgets import QWidget, QLabel, QComboBox, QVBoxLayout
from PySide6.QtGui import (QFont)

class ValuesRange():
    def __init__(self, parent: QVBoxLayout, font: Optional[QFont] = None):
        self._label = QLabel("Valor")
        self._input = QComboBox(placeholderText=u"Selecione um valor")
        if font != None:
            self._label.setFont(font)
        
        parent.addWidget(self._label)
        parent.addWidget(self._input)
    
    def reset_periods(self):
        self._input.clear()