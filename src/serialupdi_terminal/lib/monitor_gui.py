# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'monitor.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGridLayout, QPushButton, QSizePolicy, QSpinBox,
    QStackedWidget, QTextEdit, QVBoxLayout, QWidget)

from pyqtgraph import PlotWidget

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 300)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.view_mode = QPushButton(Dialog)
        self.view_mode.setObjectName(u"view_mode")

        self.verticalLayout.addWidget(self.view_mode)

        self.stackedWidget = QStackedWidget(Dialog)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.text_page = QWidget()
        self.text_page.setObjectName(u"text_page")
        self.gridLayout = QGridLayout(self.text_page)
        self.gridLayout.setObjectName(u"gridLayout")
        self.text_widget = QTextEdit(self.text_page)
        self.text_widget.setObjectName(u"text_widget")

        self.gridLayout.addWidget(self.text_widget, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.text_page)
        self.plot_page = QWidget()
        self.plot_page.setObjectName(u"plot_page")
        self.gridLayout_2 = QGridLayout(self.plot_page)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.plot_widget = PlotWidget(self.plot_page)
        self.plot_widget.setObjectName(u"plot_widget")

        self.gridLayout_2.addWidget(self.plot_widget, 1, 0, 1, 1)

        self.plot_length = QSpinBox(self.plot_page)
        self.plot_length.setObjectName(u"plot_length")

        self.gridLayout_2.addWidget(self.plot_length, 0, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.stackedWidget.addWidget(self.plot_page)

        self.verticalLayout.addWidget(self.stackedWidget)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Close)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.accept)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.view_mode.setText(QCoreApplication.translate("Dialog", u"Value", None))
    # retranslateUi

