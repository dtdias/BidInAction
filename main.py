import os, sys
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from views.search_window import SearchWindow

def Resource_path(rel_path: str) -> str:
    # Suporta execução normal e empacotado via PyInstaller
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, rel_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    icon_path = Resource_path("icon/app_Caixa.ico")
    app.setWindowIcon(QIcon(icon_path))

    window = SearchWindow()
    # Opcional, se quiser forçar na janela
    # window.setWindowIcon(QIcon(icon_path))
    window.show()
    sys.exit(app.exec())