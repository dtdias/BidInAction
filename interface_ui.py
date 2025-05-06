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
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QWidget)

class Ui_interface(object):
    def setupUi(self, interface):
        if not interface.objectName():
            interface.setObjectName(u"interface")
        interface.resize(650, 500)
        interface.setMaximumSize(QSize(650, 500))
        interface.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.centralwidget = QWidget(interface)
        self.centralwidget.setObjectName(u"centralwidget")
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(120, 100, 431, 31))
        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(120, 180, 69, 31))
        self.comboBox_2 = QComboBox(self.centralwidget)
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setGeometry(QRect(200, 180, 351, 31))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(120, 140, 131, 31))
        font = QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(120, 240, 131, 31))
        self.label_2.setFont(font)
        self.comboBox_4 = QComboBox(self.centralwidget)
        self.comboBox_4.setObjectName(u"comboBox_4")
        self.comboBox_4.setGeometry(QRect(120, 280, 431, 31))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(120, 330, 101, 31))
        self.label_3.setFont(font)
        self.comboBox_5 = QComboBox(self.centralwidget)
        self.comboBox_5.setObjectName(u"comboBox_5")
        self.comboBox_5.setGeometry(QRect(120, 370, 431, 31))
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(120, 440, 75, 31))
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(120, 30, 311, 31))
        self.label_4.setFont(font)
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(120, 60, 371, 31))
        font1 = QFont()
        font1.setPointSize(10)
        self.label_5.setFont(font1)
        interface.setCentralWidget(self.centralwidget)

        self.retranslateUi(interface)

        QMetaObject.connectSlotsByName(interface)
    # setupUi

    def retranslateUi(self, interface):
        interface.setWindowTitle(QCoreApplication.translate("interface", u"BUSCADOR DE LEIL\u00d5ES DE JOIAS DA CAIXA", None))
#if QT_CONFIG(tooltip)
        self.lineEdit.setToolTip(QCoreApplication.translate("interface", u"Busque por numero de lote ou contrato", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.comboBox.setToolTip(QCoreApplication.translate("interface", u"UF", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.comboBox_2.setToolTip(QCoreApplication.translate("interface", u"Cidade", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("interface", u"Local de retirada*", None))
        self.label_2.setText(QCoreApplication.translate("interface", u"Per\u00edodo de lance*", None))
#if QT_CONFIG(tooltip)
        self.comboBox_4.setToolTip(QCoreApplication.translate("interface", u"Per\u00edodo de lance", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("interface", u"Valor", None))
#if QT_CONFIG(tooltip)
        self.comboBox_5.setToolTip(QCoreApplication.translate("interface", u"Selecione", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pushButton.setToolTip(QCoreApplication.translate("interface", u"Continuar", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton.setText(QCoreApplication.translate("interface", u"Continuar", None))
        self.label_4.setText(QCoreApplication.translate("interface", u"FILTROS", None))
        self.label_5.setText(QCoreApplication.translate("interface", u"Busque por n\u00famero de contrato e/ou lote ou utilize os filtros.", None))
    # retranslateUi

