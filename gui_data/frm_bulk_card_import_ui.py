# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_bulk_card_import.ui'
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

class Ui_frm_bulk_card_import(object):
    def setupUi(self, frm_bulk_card_import):
        if not frm_bulk_card_import.objectName():
            frm_bulk_card_import.setObjectName(u"frm_bulk_card_import")
        frm_bulk_card_import.resize(800, 600)
        self.btn_select_path_bulkcard_upload = QPushButton(frm_bulk_card_import)
        self.btn_select_path_bulkcard_upload.setObjectName(u"btn_select_path_bulkcard_upload")
        self.btn_select_path_bulkcard_upload.setGeometry(QRect(390, 340, 85, 27))
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.btn_select_path_bulkcard_upload.setFont(font)
        self.btn_import_bulkcard = QPushButton(frm_bulk_card_import)
        self.btn_import_bulkcard.setObjectName(u"btn_import_bulkcard")
        self.btn_import_bulkcard.setGeometry(QRect(660, 340, 85, 27))
        self.btn_import_bulkcard.setFont(font)
        self.btn_reset_bulkcard = QPushButton(frm_bulk_card_import)
        self.btn_reset_bulkcard.setObjectName(u"btn_reset_bulkcard")
        self.btn_reset_bulkcard.setGeometry(QRect(540, 340, 85, 27))
        self.btn_reset_bulkcard.setFont(font)
        self.lb_path_bulkcard = QLabel(frm_bulk_card_import)
        self.lb_path_bulkcard.setObjectName(u"lb_path_bulkcard")
        self.lb_path_bulkcard.setGeometry(QRect(70, 310, 301, 27))
        font1 = QFont()
        font1.setPointSize(11)
        self.lb_path_bulkcard.setFont(font1)
        self.lb_path_bulkcard.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.txt_path_bulkcard = QLineEdit(frm_bulk_card_import)
        self.txt_path_bulkcard.setObjectName(u"txt_path_bulkcard")
        self.txt_path_bulkcard.setGeometry(QRect(70, 340, 300, 30))
        self.txt_path_bulkcard.setFont(font1)
        self.lb_warning_bulk_upload_1 = QLabel(frm_bulk_card_import)
        self.lb_warning_bulk_upload_1.setObjectName(u"lb_warning_bulk_upload_1")
        self.lb_warning_bulk_upload_1.setGeometry(QRect(88, 105, 671, 161))
        self.lb_bulk_card_upload_section = QLabel(frm_bulk_card_import)
        self.lb_bulk_card_upload_section.setObjectName(u"lb_bulk_card_upload_section")
        self.lb_bulk_card_upload_section.setGeometry(QRect(110, 50, 601, 27))
        self.lb_bulk_card_upload_section.setFont(font1)
        self.lb_bulk_card_upload_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.btn_cancel_frm_bulk_import = QPushButton(frm_bulk_card_import)
        self.btn_cancel_frm_bulk_import.setObjectName(u"btn_cancel_frm_bulk_import")
        self.btn_cancel_frm_bulk_import.setGeometry(QRect(360, 550, 85, 27))
        self.btn_cancel_frm_bulk_import.setFont(font)

        self.retranslateUi(frm_bulk_card_import)

        QMetaObject.connectSlotsByName(frm_bulk_card_import)
    # setupUi

    def retranslateUi(self, frm_bulk_card_import):
        frm_bulk_card_import.setWindowTitle(QCoreApplication.translate("frm_bulk_card_import", u"Dialog", None))
        self.btn_select_path_bulkcard_upload.setText(QCoreApplication.translate("frm_bulk_card_import", u"Select", None))
        self.btn_import_bulkcard.setText(QCoreApplication.translate("frm_bulk_card_import", u"Import", None))
        self.btn_reset_bulkcard.setText(QCoreApplication.translate("frm_bulk_card_import", u"Reset", None))
        self.lb_path_bulkcard.setText(QCoreApplication.translate("frm_bulk_card_import", u"Path for Bulk Card Upload", None))
        self.lb_warning_bulk_upload_1.setText(QCoreApplication.translate("frm_bulk_card_import", u"<html><head/><body><p align=\"center\">Warning! Images for upload must have a filename defined by the AC9HP downloader,<br>which should be like this and the .jpg or .png format: <br><br><br>\n"
"<span style=\" font-size:10pt; font-weight:700;\">Callsign=EA2BHE_VisitorCallsign=OE4VMB_QSODate=2025-09-01_15_23_00_0_Band=20M_Mode=FT8</span></p><p><br/></p><p><br/></p></body></html>", None))
        self.lb_bulk_card_upload_section.setText(QCoreApplication.translate("frm_bulk_card_import", u"Bulk Card Import for Eqsl downloaded by AC9HP Downloader", None))
        self.btn_cancel_frm_bulk_import.setText(QCoreApplication.translate("frm_bulk_card_import", u"Cancel", None))
    # retranslateUi

