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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_frm_settings(object):
    def setupUi(self, frm_settings):
        if not frm_settings.objectName():
            frm_settings.setObjectName(u"frm_settings")
        frm_settings.resize(800, 596)
        self.lb_database_selection = QLabel(frm_settings)
        self.lb_database_selection.setObjectName(u"lb_database_selection")
        self.lb_database_selection.setGeometry(QRect(40, 60, 301, 27))
        font = QFont()
        font.setPointSize(11)
        self.lb_database_selection.setFont(font)
        self.lb_database_selection.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.btn_search_dxcc = QPushButton(frm_settings)
        self.btn_search_dxcc.setObjectName(u"btn_search_dxcc")
        self.btn_search_dxcc.setGeometry(QRect(370, 210, 85, 27))
        font1 = QFont()
        font1.setPointSize(11)
        font1.setBold(True)
        self.btn_search_dxcc.setFont(font1)
        self.btn_reset_db = QPushButton(frm_settings)
        self.btn_reset_db.setObjectName(u"btn_reset_db")
        self.btn_reset_db.setGeometry(QRect(40, 510, 85, 27))
        self.btn_reset_db.setFont(font1)
        self.lb_downloadfolder_image = QLabel(frm_settings)
        self.lb_downloadfolder_image.setObjectName(u"lb_downloadfolder_image")
        self.lb_downloadfolder_image.setGeometry(QRect(40, 300, 301, 27))
        self.lb_downloadfolder_image.setFont(font)
        self.lb_downloadfolder_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.txt_db_selection = QLineEdit(frm_settings)
        self.txt_db_selection.setObjectName(u"txt_db_selection")
        self.txt_db_selection.setGeometry(QRect(40, 90, 300, 30))
        self.txt_db_selection.setFont(font)
        self.btn_cancel_frm_settings = QPushButton(frm_settings)
        self.btn_cancel_frm_settings.setObjectName(u"btn_cancel_frm_settings")
        self.btn_cancel_frm_settings.setGeometry(QRect(640, 510, 85, 27))
        self.btn_cancel_frm_settings.setFont(font1)
        self.btn_search_download_dir = QPushButton(frm_settings)
        self.btn_search_download_dir.setObjectName(u"btn_search_download_dir")
        self.btn_search_download_dir.setGeometry(QRect(370, 330, 85, 27))
        self.btn_search_download_dir.setFont(font1)
        self.lb_dxcc_list_import = QLabel(frm_settings)
        self.lb_dxcc_list_import.setObjectName(u"lb_dxcc_list_import")
        self.lb_dxcc_list_import.setGeometry(QRect(40, 180, 301, 27))
        self.lb_dxcc_list_import.setFont(font)
        self.lb_dxcc_list_import.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.txt_dxcc_selection = QLineEdit(frm_settings)
        self.txt_dxcc_selection.setObjectName(u"txt_dxcc_selection")
        self.txt_dxcc_selection.setGeometry(QRect(40, 210, 300, 30))
        self.txt_dxcc_selection.setFont(font)
        self.btn_search_db = QPushButton(frm_settings)
        self.btn_search_db.setObjectName(u"btn_search_db")
        self.btn_search_db.setGeometry(QRect(370, 90, 85, 27))
        self.btn_search_db.setFont(font1)
        self.txt_download_dir = QLineEdit(frm_settings)
        self.txt_download_dir.setObjectName(u"txt_download_dir")
        self.txt_download_dir.setGeometry(QRect(40, 330, 300, 30))
        self.txt_download_dir.setFont(font)
        self.btn_new_db = QPushButton(frm_settings)
        self.btn_new_db.setObjectName(u"btn_new_db")
        self.btn_new_db.setGeometry(QRect(530, 90, 85, 27))
        self.btn_new_db.setFont(font1)
        self.btn_import_dxcc = QPushButton(frm_settings)
        self.btn_import_dxcc.setObjectName(u"btn_import_dxcc")
        self.btn_import_dxcc.setGeometry(QRect(530, 330, 85, 27))
        self.btn_import_dxcc.setFont(font1)

        self.retranslateUi(frm_settings)

        QMetaObject.connectSlotsByName(frm_settings)
    # setupUi

    def retranslateUi(self, frm_settings):
        frm_settings.setWindowTitle(QCoreApplication.translate("frm_settings", u"Dialog", None))
        self.lb_database_selection.setText(QCoreApplication.translate("frm_settings", u"Database Selection", None))
        self.btn_search_dxcc.setText(QCoreApplication.translate("frm_settings", u"Select", None))
        self.btn_reset_db.setText(QCoreApplication.translate("frm_settings", u"Restore", None))
        self.lb_downloadfolder_image.setText(QCoreApplication.translate("frm_settings", u"Downloadfolder for Image Download", None))
        self.btn_cancel_frm_settings.setText(QCoreApplication.translate("frm_settings", u"Cancel", None))
        self.btn_search_download_dir.setText(QCoreApplication.translate("frm_settings", u"Select", None))
        self.lb_dxcc_list_import.setText(QCoreApplication.translate("frm_settings", u"DXCC List Import", None))
        self.btn_search_db.setText(QCoreApplication.translate("frm_settings", u"Select", None))
        self.btn_new_db.setText(QCoreApplication.translate("frm_settings", u"New DB", None))
        self.btn_import_dxcc.setText(QCoreApplication.translate("frm_settings", u"Import", None))
    # retranslateUi

