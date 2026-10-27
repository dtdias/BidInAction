from PySide6.QtGui import QColor, QFont, QPalette
from PySide6.QtWidgets import QApplication


def apply_theme(app: QApplication) -> None:
    """Apply shared visual language to every application window."""
    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#F4F7FB"))
    palette.setColor(QPalette.ColorRole.Base, QColor("#FFFFFF"))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#EEF3F8"))
    palette.setColor(QPalette.ColorRole.Text, QColor("#17324D"))
    palette.setColor(QPalette.ColorRole.WindowText, QColor("#17324D"))
    palette.setColor(QPalette.ColorRole.Button, QColor("#0B6EAA"))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor("#FFFFFF"))
    palette.setColor(QPalette.ColorRole.Highlight, QColor("#0B6EAA"))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#FFFFFF"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor("#7C91A5"))
    palette.setColor(QPalette.ColorRole.Link, QColor("#0B6EAA"))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#17324D"))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#FFFFFF"))
    app.setPalette(palette)
    app_font = QFont()
    app_font.setPointSize(10)
    app_font.setStyleHint(QFont.StyleHint.SansSerif)
    app.setFont(app_font)

    app.setStyleSheet(
        """
        QWidget {
            color: #17324D;
            font-size: 10pt;
        }

        QMainWindow, QDialog {
            background: #F4F7FB;
        }

        QScrollArea {
            background: transparent;
            border: none;
        }

        QFrame#heroPanel {
            background: #0B6EAA;
            border: 1px solid #0B6EAA;
            border-radius: 18px;
        }

        QFrame#searchCard,
        QFrame#mediaPanel,
        QFrame#detailsPanel,
        QFrame#loadingCard {
            background: #FFFFFF;
            border: 1px solid #DDE7F0;
            border-radius: 18px;
        }

        QLabel#heroKicker {
            color: #D8F0FF;
            font-size: 9pt;
            font-weight: 600;
            letter-spacing: 1px;
        }

        QLabel#heroSubtitle {
            color: #EAF7FF;
            font-size: 10pt;
        }

        QLabel#sectionTitle {
            color: #17324D;
            font-size: 18pt;
            font-weight: 700;
        }

        QLabel#sectionHint,
        QLabel#dialogMeta,
        QLabel#fieldHint {
            color: #71869A;
        }

        QLabel#fieldLabel {
            color: #36536B;
            font-size: 9pt;
            font-weight: 600;
        }

        QFrame#fieldGroup {
            background: transparent;
            border: none;
        }

        QLineEdit,
        QComboBox {
            min-height: 42px;
            padding: 0 12px;
            color: #17324D;
            background: #FCFDFE;
            border: 1px solid #C9D7E3;
            border-radius: 10px;
            selection-background-color: #0B6EAA;
        }

        QLineEdit:hover,
        QComboBox:hover {
            border-color: #86B5D2;
        }

        QLineEdit:focus,
        QComboBox:focus {
            background: #FFFFFF;
            border: 2px solid #0B6EAA;
        }

        QComboBox {
            padding-right: 32px;
        }

        QComboBox::drop-down {
            width: 30px;
            border: none;
        }

        QComboBox QAbstractItemView {
            color: #17324D;
            background: #FFFFFF;
            border: 1px solid #C9D7E3;
            selection-background-color: #E4F2FA;
            selection-color: #17324D;
            padding: 6px;
        }

        QPushButton#primaryButton,
        QPushButton#secondaryButton {
            min-height: 46px;
            padding: 0 22px;
            border-radius: 10px;
            font-weight: 700;
        }

        QPushButton#primaryButton {
            color: #FFFFFF;
            background: #0B6EAA;
            border: 1px solid #0B6EAA;
        }

        QPushButton#primaryButton:hover {
            background: #095C8F;
            border-color: #095C8F;
        }

        QPushButton#primaryButton:pressed {
            background: #074A74;
        }

        QPushButton#primaryButton:disabled {
            color: #A9C0D0;
            background: #DCE8F0;
            border-color: #DCE8F0;
        }

        QPushButton#secondaryButton {
            color: #0B6EAA;
            background: #EAF5FB;
            border: 1px solid #BBDCED;
        }

        QPushButton#secondaryButton:hover {
            background: #D9EEF9;
            border-color: #86B5D2;
        }

        QLabel#formStatus {
            padding: 10px 12px;
            color: #71869A;
            background: #F4F7FB;
            border: 1px solid #E0E9F0;
            border-radius: 8px;
        }

        QLabel#formStatus[state="error"] {
            color: #A12B26;
            background: #FFF1F0;
            border-color: #F3C1BD;
        }

        QLabel#formStatus[state="loading"] {
            color: #0B6EAA;
            background: #EAF5FB;
            border-color: #BBDCED;
        }

        QLabel#formStatus[state="success"] {
            color: #236B4A;
            background: #EEF9F3;
            border-color: #B9E2C9;
        }

        QLabel#dialogTitle,
        QLabel#detailTitle {
            color: #17324D;
            font-size: 18pt;
            font-weight: 700;
        }

        QLabel#subsectionTitle {
            color: #36536B;
            font-size: 11pt;
            font-weight: 700;
        }

        QLabel#priceLabel {
            color: #0B6EAA;
            font-size: 17pt;
            font-weight: 700;
        }

        QLabel#descriptionLabel {
            color: #36536B;
            line-height: 140%;
        }

        QLabel#infoKey {
            color: #71869A;
            font-size: 9pt;
            font-weight: 600;
        }

        QLabel#infoValue {
            color: #17324D;
        }

        QLabel#cardImage {
            min-height: 150px;
            background: #F1F5F8;
            border: 1px solid #E1EAF0;
            border-radius: 10px;
        }

        QLabel#cardValue {
            color: #0B6EAA;
            font-size: 12pt;
            font-weight: 700;
        }

        QLabel#cardCaption {
            color: #71869A;
            font-size: 9pt;
        }

        QPushButton#bidCard {
            min-width: 210px;
            min-height: 250px;
            padding: 14px;
            color: #17324D;
            text-align: left;
            background: #FFFFFF;
            border: 1px solid #DDE7F0;
            border-radius: 16px;
        }

        QPushButton#bidCard:hover {
            background: #F9FCFF;
            border: 2px solid #86B5D2;
        }

        QPushButton#bidCard:pressed {
            background: #EAF5FB;
        }

        QLabel#loaderTitle {
            color: #17324D;
            font-size: 15pt;
            font-weight: 700;
        }

        QLabel#loaderText {
            color: #71869A;
        }

        QProgressBar {
            min-height: 10px;
            max-height: 10px;
            background: #E7EFF5;
            border: none;
            border-radius: 5px;
            text-align: center;
        }

        QProgressBar::chunk {
            background: #0B6EAA;
            border-radius: 5px;
        }

        QToolTip {
            color: #FFFFFF;
            background: #17324D;
            border: 1px solid #17324D;
            padding: 6px;
        }

        QScrollBar:vertical {
            width: 10px;
            margin: 4px;
            background: transparent;
        }

        QScrollBar::handle:vertical {
            min-height: 30px;
            background: #B9CAD7;
            border-radius: 5px;
        }

        QScrollBar::handle:vertical:hover {
            background: #86B5D2;
        }

        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            height: 0;
        }
        """
    )
