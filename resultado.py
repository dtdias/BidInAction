# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interface.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QSizePolicy,
    QWidget)

class Ui_interface(object):
    def setupUi(self, interface):
        if not interface.objectName():
            interface.setObjectName(u"interface")
        interface.resize(650, 500)
        interface.setMaximumSize(QSize(650, 500))
        interface.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.centralwidget = QWidget(interface)
        self.centralwidget.setObjectName(u"centralwidget")
        self.webEngineView = QWebEngineView(self.centralwidget)
        self.webEngineView.setObjectName(u"webEngineView")
        self.webEngineView.setGeometry(QRect(10, 40, 631, 451))
        self.webEngineView.setUrl(QUrl(u"about:blank"))
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(10, 10, 75, 24))
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(570, 10, 75, 24))
        interface.setCentralWidget(self.centralwidget)

        self.retranslateUi(interface)

        QMetaObject.connectSlotsByName(interface)
    # setupUi

    def retranslateUi(self, interface):
        interface.setWindowTitle(QCoreApplication.translate("interface", u"BUSCADOR DE LEIL\u00d5ES DE JOIAS DA CAIXA", None))
        self.pushButton.setText(QCoreApplication.translate("interface", u"VOLTAR", None))
        self.pushButton_2.setText(QCoreApplication.translate("interface", u"SAIR", None))
    # retranslateUi

