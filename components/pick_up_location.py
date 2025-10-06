from typing import Optional
from PySide6.QtWidgets import QLabel, QComboBox, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QFont
class PickUpLocation():
    def __init__(self, parent: QVBoxLayout, font: Optional[QFont] = None):
        self._row = QHBoxLayout()
        self._label = QLabel( u"Local de retirada*")
        
        self._inputUf = QComboBox(placeholderText="UF")
        self._inputUf.setToolTip("UF")
        
        self._inputCity = QComboBox(placeholderText="Cidade")
        self._inputUf.setToolTip("Cidade")
        
        self._row.addWidget(self._inputUf)
        self._row.addWidget(self._inputCity)
        if font != None:
            self._label.setFont(font)
                
        parent.addWidget(self._label)
        parent.addLayout(self._row)        
        
    def reset_inputCity(self):
        self._inputCity.clear()