# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_settings.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QWidget)

class Ui_frm_settings(object):
    def setupUi(self, frm_settings):
        if not frm_settings.objectName():
            frm_settings.setObjectName(u"frm_settings")
        frm_settings.resize(800, 600)
        self.centralwidget = QWidget(frm_settings)
        self.centralwidget.setObjectName(u"centralwidget")
        self.le_database_selection = QLineEdit(self.centralwidget)
        self.le_database_selection.setObjectName(u"le_database_selection")
        self.le_database_selection.setGeometry(QRect(40, 70, 300, 30))
        font = QFont()
        font.setPointSize(11)
        self.le_database_selection.setFont(font)
        self.le_dxcc_list_import = QLineEdit(self.centralwidget)
        self.le_dxcc_list_import.setObjectName(u"le_dxcc_list_import")
        self.le_dxcc_list_import.setGeometry(QRect(40, 190, 300, 30))
        self.le_dxcc_list_import.setFont(font)
        self.le_downloadfolder_image = QLineEdit(self.centralwidget)
        self.le_downloadfolder_image.setObjectName(u"le_downloadfolder_image")
        self.le_downloadfolder_image.setGeometry(QRect(40, 310, 300, 30))
        self.le_downloadfolder_image.setFont(font)
        self.btn_restore_frm_settings = QPushButton(self.centralwidget)
        self.btn_restore_frm_settings.setObjectName(u"btn_restore_frm_settings")
        self.btn_restore_frm_settings.setGeometry(QRect(40, 490, 85, 27))
        font1 = QFont()
        font1.setPointSize(11)
        font1.setBold(True)
        self.btn_restore_frm_settings.setFont(font1)
        self.btn_cancel_frm_settings = QPushButton(self.centralwidget)
        self.btn_cancel_frm_settings.setObjectName(u"btn_cancel_frm_settings")
        self.btn_cancel_frm_settings.setGeometry(QRect(530, 490, 85, 27))
        self.btn_cancel_frm_settings.setFont(font1)
        self.btn_Save_frm_settings = QPushButton(self.centralwidget)
        self.btn_Save_frm_settings.setObjectName(u"btn_Save_frm_settings")
        self.btn_Save_frm_settings.setGeometry(QRect(660, 490, 85, 27))
        self.btn_Save_frm_settings.setFont(font1)
        self.lb_database_selection = QLabel(self.centralwidget)
        self.lb_database_selection.setObjectName(u"lb_database_selection")
        self.lb_database_selection.setGeometry(QRect(40, 40, 301, 27))
        self.lb_database_selection.setFont(font)
        self.lb_database_selection.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lb_dxcc_list_import = QLabel(self.centralwidget)
        self.lb_dxcc_list_import.setObjectName(u"lb_dxcc_list_import")
        self.lb_dxcc_list_import.setGeometry(QRect(40, 160, 301, 27))
        self.lb_dxcc_list_import.setFont(font)
        self.lb_dxcc_list_import.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lb_downloadfolder_image = QLabel(self.centralwidget)
        self.lb_downloadfolder_image.setObjectName(u"lb_downloadfolder_image")
        self.lb_downloadfolder_image.setGeometry(QRect(40, 280, 301, 27))
        self.lb_downloadfolder_image.setFont(font)
        self.lb_downloadfolder_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.btn_search_database = QPushButton(self.centralwidget)
        self.btn_search_database.setObjectName(u"btn_search_database")
        self.btn_search_database.setGeometry(QRect(370, 70, 85, 27))
        self.btn_search_database.setFont(font1)
        self.btn_search_dxcc_list_import = QPushButton(self.centralwidget)
        self.btn_search_dxcc_list_import.setObjectName(u"btn_search_dxcc_list_import")
        self.btn_search_dxcc_list_import.setGeometry(QRect(370, 190, 85, 27))
        self.btn_search_dxcc_list_import.setFont(font1)
        self.btn_search_downloadfolder_image = QPushButton(self.centralwidget)
        self.btn_search_downloadfolder_image.setObjectName(u"btn_search_downloadfolder_image")
        self.btn_search_downloadfolder_image.setGeometry(QRect(370, 310, 85, 27))
        self.btn_search_downloadfolder_image.setFont(font1)
        frm_settings.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(frm_settings)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 33))
        frm_settings.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(frm_settings)
        self.statusbar.setObjectName(u"statusbar")
        frm_settings.setStatusBar(self.statusbar)

        self.retranslateUi(frm_settings)

        QMetaObject.connectSlotsByName(frm_settings)
    # setupUi

    def retranslateUi(self, frm_settings):
        frm_settings.setWindowTitle(QCoreApplication.translate("frm_settings", u"MainWindow", None))
        self.btn_restore_frm_settings.setText(QCoreApplication.translate("frm_settings", u"Restore", None))
        self.btn_cancel_frm_settings.setText(QCoreApplication.translate("frm_settings", u"Cancel", None))
        self.btn_Save_frm_settings.setText(QCoreApplication.translate("frm_settings", u"Save", None))
        self.lb_database_selection.setText(QCoreApplication.translate("frm_settings", u"Database Selection", None))
        self.lb_dxcc_list_import.setText(QCoreApplication.translate("frm_settings", u"DXCC List Import", None))
        self.lb_downloadfolder_image.setText(QCoreApplication.translate("frm_settings", u"Downloadfolder for Image Download", None))
        self.btn_search_database.setText(QCoreApplication.translate("frm_settings", u"Search", None))
        self.btn_search_dxcc_list_import.setText(QCoreApplication.translate("frm_settings", u"Search", None))
        self.btn_search_downloadfolder_image.setText(QCoreApplication.translate("frm_settings", u"Search", None))
    # retranslateUi

