# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_version.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QSizePolicy, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_frm_version(object):
    def setupUi(self, frm_version):
        if not frm_version.objectName():
            frm_version.setObjectName(u"frm_version")
        frm_version.resize(500, 500)
        self.verticalLayout = QVBoxLayout(frm_version)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.txt_version_credits = QTextEdit(frm_version)
        self.txt_version_credits.setObjectName(u"txt_version_credits")

        self.verticalLayout.addWidget(self.txt_version_credits)


        self.retranslateUi(frm_version)

        QMetaObject.connectSlotsByName(frm_version)
    # setupUi

    def retranslateUi(self, frm_version):
        frm_version.setWindowTitle(QCoreApplication.translate("frm_version", u"Dialog", None))
    # retranslateUi

