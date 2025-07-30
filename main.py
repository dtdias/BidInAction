import sys
from PySide6.QtWidgets import (QApplication)
from views.search_window import SearchWindow

if __name__ == "__main__":
    app = QApplication([])
    SearchWindow().show()
    
    sys.exit(app.exec())
