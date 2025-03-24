import sys
import os

from qt_core import *


from gui.windows.main_window.ui_main_window import *

#Main Window

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #Setup main Window
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)


        #Exibi a aplicação
        self.show()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())