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
        frm_settings.setWindowModality(Qt.WindowModality.WindowModal)
        frm_settings.resize(800, 596)
        self.lb_database_selection = QLabel(frm_settings)
        self.lb_database_selection.setObjectName(u"lb_database_selection")
        self.lb_database_selection.setGeometry(QRect(40, 60, 301, 27))
        font = QFont()
        font.setPointSize(11)
        self.lb_database_selection.setFont(font)
        self.lb_database_selection.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.btn_reset_db = QPushButton(frm_settings)
        self.btn_reset_db.setObjectName(u"btn_reset_db")
        self.btn_reset_db.setGeometry(QRect(40, 510, 85, 27))
        font1 = QFont()
        font1.setPointSize(11)
        font1.setBold(True)
        self.btn_reset_db.setFont(font1)
        self.lb_downloadfolder_image = QLabel(frm_settings)
        self.lb_downloadfolder_image.setObjectName(u"lb_downloadfolder_image")
        self.lb_downloadfolder_image.setGeometry(QRect(40, 340, 301, 27))
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
        self.btn_search_download_dir.setGeometry(QRect(370, 370, 85, 27))
        self.btn_search_download_dir.setFont(font1)
        self.btn_search_db = QPushButton(frm_settings)
        self.btn_search_db.setObjectName(u"btn_search_db")
        self.btn_search_db.setGeometry(QRect(370, 90, 85, 27))
        self.btn_search_db.setFont(font1)
        self.txt_download_dir = QLineEdit(frm_settings)
        self.txt_download_dir.setObjectName(u"txt_download_dir")
        self.txt_download_dir.setGeometry(QRect(40, 370, 300, 30))
        self.txt_download_dir.setFont(font)
        self.btn_new_db = QPushButton(frm_settings)
        self.btn_new_db.setObjectName(u"btn_new_db")
        self.btn_new_db.setGeometry(QRect(530, 90, 85, 27))
        self.btn_new_db.setFont(font1)
        self.txt_adif_selection = QLineEdit(frm_settings)
        self.txt_adif_selection.setObjectName(u"txt_adif_selection")
        self.txt_adif_selection.setGeometry(QRect(40, 230, 300, 30))
        self.txt_adif_selection.setFont(font)
        self.lb_adif_list_import = QLabel(frm_settings)
        self.lb_adif_list_import.setObjectName(u"lb_adif_list_import")
        self.lb_adif_list_import.setGeometry(QRect(40, 200, 301, 27))
        self.lb_adif_list_import.setFont(font)
        self.lb_adif_list_import.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.btn_search_adif = QPushButton(frm_settings)
        self.btn_search_adif.setObjectName(u"btn_search_adif")
        self.btn_search_adif.setGeometry(QRect(370, 230, 85, 27))
        self.btn_search_adif.setFont(font1)
        self.btn_import_adif = QPushButton(frm_settings)
        self.btn_import_adif.setObjectName(u"btn_import_adif")
        self.btn_import_adif.setGeometry(QRect(530, 230, 85, 27))
        self.btn_import_adif.setFont(font1)

        self.retranslateUi(frm_settings)

        QMetaObject.connectSlotsByName(frm_settings)
    # setupUi

    def retranslateUi(self, frm_settings):
        frm_settings.setWindowTitle(QCoreApplication.translate("frm_settings", u"Dialog", None))
        self.lb_database_selection.setText(QCoreApplication.translate("frm_settings", u"Database Selection", None))
        self.btn_reset_db.setText(QCoreApplication.translate("frm_settings", u"Reset", None))
        self.lb_downloadfolder_image.setText(QCoreApplication.translate("frm_settings", u"Downloadfolder for Image Download", None))
        self.txt_db_selection.setPlaceholderText(QCoreApplication.translate("frm_settings", u"Path to your database", None))
        self.btn_cancel_frm_settings.setText(QCoreApplication.translate("frm_settings", u"Back", None))
        self.btn_search_download_dir.setText(QCoreApplication.translate("frm_settings", u"Select", None))
        self.btn_search_db.setText(QCoreApplication.translate("frm_settings", u"Select", None))
        self.txt_download_dir.setPlaceholderText(QCoreApplication.translate("frm_settings", u"Path to your downloadfolder", None))
        self.btn_new_db.setText(QCoreApplication.translate("frm_settings", u"New DB", None))
        self.txt_adif_selection.setPlaceholderText(QCoreApplication.translate("frm_settings", u"Path to your adif file", None))
        self.lb_adif_list_import.setText(QCoreApplication.translate("frm_settings", u"ADIF List Import", None))
        self.btn_search_adif.setText(QCoreApplication.translate("frm_settings", u"Select", None))
        self.btn_import_adif.setText(QCoreApplication.translate("frm_settings", u"Import", None))
    # retranslateUi

