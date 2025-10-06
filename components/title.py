from typing import Optional
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout
from PySide6.QtGui import QFont

class Title():
    def __init__(self, parent: QVBoxLayout, font: Optional[QFont] = None):
        self._label = QLabel(u"FILTROS")
        if font != None:
            self._label.setFont(font)
        parent.addWidget(self._label)
        
        
        