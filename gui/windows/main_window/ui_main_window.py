#Import qt core
from qt_core import *

#Main Window
class UI_MainWindow(object):
    def setup_ui(self, parent):
        if not parent.objectName():
            parent.setObjectName("MainWindow")

            #Set Initial window Parameters
            parent.resize(800,500)
            parent.setMinimumSize(800,500)



            #Central Frame Widget
            self.central_frame = QFrame()
            self.central_frame.setStyleSheet("background-color: #6ab0d2")

            #Main Layout
            self.main_layout = QHBoxLayout(self.central_frame)

            #Top Menu
            self.top_menu = QFrame()
            self.top_menu.setStyleSheet("background-color: #2d7ca4")


            # Set central Widget
            parent.setCentralWidget(self.central_frame)