from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar, QHBoxLayout
from PySide6.QtCore import Qt, QTimer

class LoaderDialog(QDialog):
    def __init__(self, text="Carregando...", parent=None):
        super().__init__(parent)
        self.setModal(True)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setWindowTitle("Aguarde")
        
        layout = QVBoxLayout(self)
        lbl = QLabel(text, self)
        lbl.setAlignment(Qt.AlignCenter)
        
        # Container horizontal para barra + percentual
        bar_row = QHBoxLayout()
        self.bar = QProgressBar(self)
        self.bar.setRange(0, 100)  # determinístico
        self.bar.setValue(0)
        
        self.percent_lbl = QLabel("0%", self)
        self.percent_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.percent_lbl.setMinimumWidth(45)
        
        bar_row.addWidget(self.bar)
        bar_row.addWidget(self.percent_lbl)
        
        layout.addWidget(lbl)
        layout.addLayout(bar_row)
        self.setFixedSize(320, 140)
        
        # Timer para simular progresso
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(80)  # atualiza a cada 80ms
    
    def _tick(self):
        v = self.bar.value()
        if v < 90:  # para em 90% até terminar de verdade
            self.set_progress(v + 1)
    
    def set_progress(self, value: int):
        v = max(0, min(100, int(value)))
        self.bar.setValue(v)
        self.percent_lbl.setText(f"{v}%")
    
    def stop_and_fill(self):
        """Para o timer e completa a barra em 100%"""
        self._timer.stop()
        self.set_progress(100)