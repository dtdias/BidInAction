from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QFrame, QLabel, QProgressBar, QVBoxLayout


class LoaderDialog(QDialog):
    def __init__(self, text="Carregando...", parent=None):
        super().__init__(parent)
        self.setObjectName("loaderDialog")
        self.setModal(True)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setWindowTitle("Aguarde")
        self.setMinimumSize(420, 190)

        card = QFrame()
        card.setObjectName("loadingCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(28, 26, 28, 26)
        card_layout.setSpacing(12)

        title = QLabel("Buscando lotes")
        title.setObjectName("loaderTitle")
        card_layout.addWidget(title)

        message = QLabel(text)
        message.setObjectName("loaderText")
        message.setWordWrap(True)
        card_layout.addWidget(message)

        self.bar = QProgressBar()
        self.bar.setRange(0, 0)
        self.bar.setTextVisible(False)
        card_layout.addWidget(self.bar)

        self.percent_lbl = QLabel("Conectando...")
        self.percent_lbl.setObjectName("loaderText")
        self.percent_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        card_layout.addWidget(self.percent_lbl)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(card)

    def set_progress(self, value: int):
        if self.bar.maximum() == 0:
            self.bar.setRange(0, 100)
        bounded_value = max(0, min(100, int(value)))
        self.bar.setValue(bounded_value)
        self.percent_lbl.setText(f"{bounded_value}%")

    def stop_and_fill(self):
        """Complete progress before closing the dialog."""
        self.bar.setRange(0, 100)
        self.set_progress(100)
