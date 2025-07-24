from PySide6.QtWidgets import QWidget, QLabel, QComboBox, QVBoxLayout

class BidPeriod():
    def __init__(self, parent: QVBoxLayout):
        self._label = QLabel(u"Per\u00edodo de lance*")
        self._input = QComboBox(placeholderText=u"Per\u00edodo de lance*")
        self._input.setToolTip(u"Busque por numero de lote ou contrato")
        
        parent.addWidget(self._label)
        parent.addWidget(self._input)
    
    def reset_periods(self):
        self._input.clear()