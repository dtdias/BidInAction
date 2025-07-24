from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout

class SearchFilter():
    def __init__(self, parent: QVBoxLayout):
        self._label = QLabel(u"Busque por n\u00famero de contrato e/ou lote ou utilize os filtros.")
        self._input = QLineEdit()
        self._input.setToolTip(u"Busque por numero de lote ou contrato")
        
        parent.addWidget(self._label)
        parent.addWidget(self._input)