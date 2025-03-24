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