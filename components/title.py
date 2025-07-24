from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout
from PySide6.QtCore import Qt

class Title():
    def __init__(self, parent: QVBoxLayout):
        self._label = QLabel(u"FILTROS")
        parent.addWidget(self._label)
        
        
        