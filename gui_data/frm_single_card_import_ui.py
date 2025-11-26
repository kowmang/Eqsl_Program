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
        self.txt_date_single = QLineEdit(frm_single_card_import)
        self.txt_date_single.setObjectName(u"txt_date_single")
        self.txt_date_single.setGeometry(QRect(260, 150, 111, 30))
        self.btn_reset_path_single = QPushButton(frm_single_card_import)
        self.btn_reset_path_single.setObjectName(u"btn_reset_path_single")
        self.btn_reset_path_single.setGeometry(QRect(500, 330, 85, 27))
        self.btn_reset_path_single.setFont(font)
        self.lb_mode_single = QLabel(frm_single_card_import)
        self.lb_mode_single.setObjectName(u"lb_mode_single")
        self.lb_mode_single.setGeometry(QRect(630, 120, 101, 27))
        font1 = QFont()
        font1.setPointSize(11)
        self.lb_mode_single.setFont(font1)
        self.lb_mode_single.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.txt_mode_single = QLineEdit(frm_single_card_import)
        self.txt_mode_single.setObjectName(u"txt_mode_single")
        self.txt_mode_single.setGeometry(QRect(630, 150, 101, 30))
        self.lb_band_single = QLabel(frm_single_card_import)
        self.lb_band_single.setObjectName(u"lb_band_single")
        self.lb_band_single.setGeometry(QRect(450, 120, 101, 27))
        self.lb_band_single.setFont(font1)
        self.lb_band_single.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.btn_select_path_single = QPushButton(frm_single_card_import)
        self.btn_select_path_single.setObjectName(u"btn_select_path_single")
        self.btn_select_path_single.setGeometry(QRect(390, 330, 85, 27))
        self.btn_select_path_single.setFont(font)
        self.btn_singlecard_import = QPushButton(frm_single_card_import)
        self.btn_singlecard_import.setObjectName(u"btn_singlecard_import")
        self.btn_singlecard_import.setGeometry(QRect(650, 330, 85, 27))
        self.btn_singlecard_import.setFont(font)
        self.lb_date_single = QLabel(frm_single_card_import)
        self.lb_date_single.setObjectName(u"lb_date_single")
        self.lb_date_single.setGeometry(QRect(250, 120, 127, 27))
        self.lb_date_single.setFont(font1)
        self.lb_date_single.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.txt_callsign_single = QLineEdit(frm_single_card_import)
        self.txt_callsign_single.setObjectName(u"txt_callsign_single")
        self.txt_callsign_single.setGeometry(QRect(70, 150, 111, 30))
        self.lb_path_singlecard = QLabel(frm_single_card_import)
        self.lb_path_singlecard.setObjectName(u"lb_path_singlecard")
        self.lb_path_singlecard.setGeometry(QRect(60, 300, 301, 27))
        self.lb_path_singlecard.setFont(font1)
        self.lb_path_singlecard.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.txt_path_singlecard_import = QLineEdit(frm_single_card_import)
        self.txt_path_singlecard_import.setObjectName(u"txt_path_singlecard_import")
        self.txt_path_singlecard_import.setGeometry(QRect(70, 330, 300, 30))
        self.txt_path_singlecard_import.setFont(font1)
        self.lb_single_card_upload_section = QLabel(frm_single_card_import)
        self.lb_single_card_upload_section.setObjectName(u"lb_single_card_upload_section")
        self.lb_single_card_upload_section.setGeometry(QRect(100, 50, 601, 27))
        self.lb_single_card_upload_section.setFont(font1)
        self.lb_single_card_upload_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lb_callsign_single = QLabel(frm_single_card_import)
        self.lb_callsign_single.setObjectName(u"lb_callsign_single")
        self.lb_callsign_single.setGeometry(QRect(60, 120, 127, 27))
        self.lb_callsign_single.setFont(font1)
        self.lb_callsign_single.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.txt_band_single = QLineEdit(frm_single_card_import)
        self.txt_band_single.setObjectName(u"txt_band_single")
        self.txt_band_single.setGeometry(QRect(450, 150, 101, 30))
        QWidget.setTabOrder(self.txt_callsign_single, self.txt_date_single)
        QWidget.setTabOrder(self.txt_date_single, self.txt_band_single)
        QWidget.setTabOrder(self.txt_band_single, self.txt_mode_single)
        QWidget.setTabOrder(self.txt_mode_single, self.txt_path_singlecard_import)
        QWidget.setTabOrder(self.txt_path_singlecard_import, self.btn_select_path_single)
        QWidget.setTabOrder(self.btn_select_path_single, self.btn_reset_path_single)
        QWidget.setTabOrder(self.btn_reset_path_single, self.btn_singlecard_import)
        QWidget.setTabOrder(self.btn_singlecard_import, self.btn_cancel_frm_single_import)

        self.retranslateUi(frm_single_card_import)

        QMetaObject.connectSlotsByName(frm_single_card_import)
    # setupUi

    def retranslateUi(self, frm_single_card_import):
        frm_single_card_import.setWindowTitle(QCoreApplication.translate("frm_single_card_import", u"Dialog", None))
        self.btn_cancel_frm_single_import.setText(QCoreApplication.translate("frm_single_card_import", u"Back", None))
        self.btn_reset_path_single.setText(QCoreApplication.translate("frm_single_card_import", u"Reset", None))
        self.lb_mode_single.setText(QCoreApplication.translate("frm_single_card_import", u"Mode", None))
        self.lb_band_single.setText(QCoreApplication.translate("frm_single_card_import", u"Band", None))
        self.btn_select_path_single.setText(QCoreApplication.translate("frm_single_card_import", u"Select", None))
        self.btn_singlecard_import.setText(QCoreApplication.translate("frm_single_card_import", u"Import", None))
        self.lb_date_single.setText(QCoreApplication.translate("frm_single_card_import", u"Date", None))
        self.lb_path_singlecard.setText(QCoreApplication.translate("frm_single_card_import", u"Path for Single Card Import", None))
        self.lb_single_card_upload_section.setText(QCoreApplication.translate("frm_single_card_import", u"Single Card Import", None))
        self.lb_callsign_single.setText(QCoreApplication.translate("frm_single_card_import", u"Callsign", None))
    # retranslateUi

