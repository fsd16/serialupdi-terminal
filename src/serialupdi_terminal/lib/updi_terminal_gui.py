# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'updi_terminal.ui'
##
## Created by: Qt User Interface Compiler version 6.7.1
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QLabel,
    QLineEdit, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QStatusBar,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMouseTracking(False)
        MainWindow.setDocumentMode(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 1, 3, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 5, 3, 1, 1)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 3, 4, 1, 1, Qt.AlignmentFlag.AlignBottom)

        self.browse = QPushButton(self.centralwidget)
        self.browse.setObjectName(u"browse")

        self.gridLayout.addWidget(self.browse, 1, 2, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 4, 0, 1, 1)

        self.select_section_type = QComboBox(self.centralwidget)
        self.select_section_type.setObjectName(u"select_section_type")

        self.gridLayout.addWidget(self.select_section_type, 4, 1, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_5, 2, 3, 1, 1)

        self.select_section = QComboBox(self.centralwidget)
        self.select_section.setObjectName(u"select_section")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.select_section.sizePolicy().hasHeightForWidth())
        self.select_section.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.select_section, 2, 1, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_3, 3, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 2, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_4, 4, 5, 1, 1)

        self.map_file = QLineEdit(self.centralwidget)
        self.map_file.setObjectName(u"map_file")

        self.gridLayout.addWidget(self.map_file, 1, 1, 1, 1)

        self.set_update_freq = QSpinBox(self.centralwidget)
        self.set_update_freq.setObjectName(u"set_update_freq")

        self.gridLayout.addWidget(self.set_update_freq, 4, 4, 1, 1)

        self.monitor = QPushButton(self.centralwidget)
        self.monitor.setObjectName(u"monitor")

        self.gridLayout.addWidget(self.monitor, 2, 4, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_6, 4, 3, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 2, 5, 1, 1)

        self.set_port = QComboBox(self.centralwidget)
        self.set_port.setObjectName(u"set_port")
        self.set_port.setFrame(True)

        self.gridLayout.addWidget(self.set_port, 0, 1, 1, 1)

        self.serial_connect = QPushButton(self.centralwidget)
        self.serial_connect.setObjectName(u"serial_connect")

        self.gridLayout.addWidget(self.serial_connect, 0, 2, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Update Frequency", None))
        self.browse.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.select_section_type.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Select Section Type", None))
        self.select_section.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Select Section", None))
        self.monitor.setText(QCoreApplication.translate("MainWindow", u"Monitor", None))
        self.set_port.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Select COM Port", None))
        self.serial_connect.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
    # retranslateUi

