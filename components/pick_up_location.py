from PySide6.QtWidgets import QLabel, QComboBox, QHBoxLayout, QVBoxLayout

class PickUpLocation():
    def __init__(self, parent: QVBoxLayout):
        self._row = QHBoxLayout()
        self._label = QLabel( u"Local de retirada*")
        
        self._inputUf = QComboBox(placeholderText="UF")
        self._inputUf.setToolTip("UF")
        
        self._inputCity = QComboBox(placeholderText="Cidade")
        self._inputUf.setToolTip("Cidade")
        
        self._row.addWidget(self._inputUf)
        self._row.addWidget(self._inputCity)
                
        parent.addWidget(self._label)
        parent.addLayout(self._row)        
        
    def reset_inputCity(self):
        self._inputCity.clear()