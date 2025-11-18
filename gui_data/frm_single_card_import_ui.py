# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_single_card_import.ui'
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

class Ui_frm_single_card_import(object):
    def setupUi(self, frm_single_card_import):
        if not frm_single_card_import.objectName():
            frm_single_card_import.setObjectName(u"frm_single_card_import")
        frm_single_card_import.setEnabled(True)
        frm_single_card_import.resize(800, 600)
        self.btn_cancel_frm_single_import = QPushButton(frm_single_card_import)
        self.btn_cancel_frm_single_import.setObjectName(u"btn_cancel_frm_single_import")
        self.btn_cancel_frm_single_import.setGeometry(QRect(340, 550, 85, 27))
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.btn_cancel_frm_single_import.setFont(font)
        self.lb_time_1 = QLabel(frm_single_card_import)
        self.lb_time_1.setObjectName(u"lb_time_1")
        self.lb_time_1.setGeometry(QRect(300, 100, 111, 27))
        font1 = QFont()
        font1.setPointSize(11)
        self.lb_time_1.setFont(font1)
        self.lb_time_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.le_date_1 = QLineEdit(frm_single_card_import)
        self.le_date_1.setObjectName(u"le_date_1")
        self.le_date_1.setGeometry(QRect(190, 130, 111, 30))
        self.btn_reset_singlecard = QPushButton(frm_single_card_import)
        self.btn_reset_singlecard.setObjectName(u"btn_reset_singlecard")
        self.btn_reset_singlecard.setGeometry(QRect(530, 440, 85, 27))
        self.btn_reset_singlecard.setFont(font)
        self.lb_mode_1 = QLabel(frm_single_card_import)
        self.lb_mode_1.setObjectName(u"lb_mode_1")
        self.lb_mode_1.setGeometry(QRect(520, 100, 101, 27))
        self.lb_mode_1.setFont(font1)
        self.lb_mode_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.le_callsign_5 = QLineEdit(frm_single_card_import)
        self.le_callsign_5.setObjectName(u"le_callsign_5")
        self.le_callsign_5.setGeometry(QRect(520, 130, 101, 30))
        self.le_dxcc_number_1 = QLineEdit(frm_single_card_import)
        self.le_dxcc_number_1.setObjectName(u"le_dxcc_number_1")
        self.le_dxcc_number_1.setGeometry(QRect(630, 130, 111, 30))
        self.lb_band_1 = QLabel(frm_single_card_import)
        self.lb_band_1.setObjectName(u"lb_band_1")
        self.lb_band_1.setGeometry(QRect(410, 100, 101, 27))
        self.lb_band_1.setFont(font1)
        self.lb_band_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.le_time_1 = QLineEdit(frm_single_card_import)
        self.le_time_1.setObjectName(u"le_time_1")
        self.le_time_1.setGeometry(QRect(310, 130, 91, 30))
        self.btn_search_path_singlecard_upload = QPushButton(frm_single_card_import)
        self.btn_search_path_singlecard_upload.setObjectName(u"btn_search_path_singlecard_upload")
        self.btn_search_path_singlecard_upload.setGeometry(QRect(390, 440, 85, 27))
        self.btn_search_path_singlecard_upload.setFont(font)
        self.btn_upload_singlecard = QPushButton(frm_single_card_import)
        self.btn_upload_singlecard.setObjectName(u"btn_upload_singlecard")
        self.btn_upload_singlecard.setGeometry(QRect(650, 440, 85, 27))
        self.btn_upload_singlecard.setFont(font)
        self.lb_date_1 = QLabel(frm_single_card_import)
        self.lb_date_1.setObjectName(u"lb_date_1")
        self.lb_date_1.setGeometry(QRect(180, 100, 127, 27))
        self.lb_date_1.setFont(font1)
        self.lb_date_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.le_callsign_1 = QLineEdit(frm_single_card_import)
        self.le_callsign_1.setObjectName(u"le_callsign_1")
        self.le_callsign_1.setGeometry(QRect(70, 130, 111, 30))
        self.lb_path_singlecard = QLabel(frm_single_card_import)
        self.lb_path_singlecard.setObjectName(u"lb_path_singlecard")
        self.lb_path_singlecard.setGeometry(QRect(60, 410, 301, 27))
        self.lb_path_singlecard.setFont(font1)
        self.lb_path_singlecard.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.le_path_singlecard = QLineEdit(frm_single_card_import)
        self.le_path_singlecard.setObjectName(u"le_path_singlecard")
        self.le_path_singlecard.setGeometry(QRect(70, 440, 300, 30))
        self.le_path_singlecard.setFont(font1)
        self.lb_dxcc_number_1 = QLabel(frm_single_card_import)
        self.lb_dxcc_number_1.setObjectName(u"lb_dxcc_number_1")
        self.lb_dxcc_number_1.setGeometry(QRect(630, 100, 111, 27))
        self.lb_dxcc_number_1.setFont(font1)
        self.lb_dxcc_number_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lb_single_card_upload_section = QLabel(frm_single_card_import)
        self.lb_single_card_upload_section.setObjectName(u"lb_single_card_upload_section")
        self.lb_single_card_upload_section.setGeometry(QRect(110, 50, 601, 27))
        self.lb_single_card_upload_section.setFont(font1)
        self.lb_single_card_upload_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lb_callsign_1 = QLabel(frm_single_card_import)
        self.lb_callsign_1.setObjectName(u"lb_callsign_1")
        self.lb_callsign_1.setGeometry(QRect(70, 100, 127, 27))
        self.lb_callsign_1.setFont(font1)
        self.lb_callsign_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.le_mode_1 = QLineEdit(frm_single_card_import)
        self.le_mode_1.setObjectName(u"le_mode_1")
        self.le_mode_1.setGeometry(QRect(410, 130, 101, 30))

        self.retranslateUi(frm_single_card_import)

        QMetaObject.connectSlotsByName(frm_single_card_import)
    # setupUi

    def retranslateUi(self, frm_single_card_import):
        frm_single_card_import.setWindowTitle(QCoreApplication.translate("frm_single_card_import", u"Dialog", None))
        self.btn_cancel_frm_single_import.setText(QCoreApplication.translate("frm_single_card_import", u"Cancel", None))
        self.lb_time_1.setText(QCoreApplication.translate("frm_single_card_import", u"Time", None))
        self.btn_reset_singlecard.setText(QCoreApplication.translate("frm_single_card_import", u"Reset", None))
        self.lb_mode_1.setText(QCoreApplication.translate("frm_single_card_import", u"Mode", None))
        self.lb_band_1.setText(QCoreApplication.translate("frm_single_card_import", u"Band", None))
        self.btn_search_path_singlecard_upload.setText(QCoreApplication.translate("frm_single_card_import", u"Search", None))
        self.btn_upload_singlecard.setText(QCoreApplication.translate("frm_single_card_import", u"Upload", None))
        self.lb_date_1.setText(QCoreApplication.translate("frm_single_card_import", u"Date", None))
        self.lb_path_singlecard.setText(QCoreApplication.translate("frm_single_card_import", u"Path for Single Card Upload", None))
        self.lb_dxcc_number_1.setText(QCoreApplication.translate("frm_single_card_import", u"DXCC Number", None))
        self.lb_single_card_upload_section.setText(QCoreApplication.translate("frm_single_card_import", u"Single Card Import", None))
        self.lb_callsign_1.setText(QCoreApplication.translate("frm_single_card_import", u"Callsign", None))
    # retranslateUi

