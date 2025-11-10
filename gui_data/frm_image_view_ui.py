# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_image_view.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_frm_image_view(object):
    def setupUi(self, frm_image_view):
        if not frm_image_view.objectName():
            frm_image_view.setObjectName(u"frm_image_view")
        frm_image_view.resize(655, 460)
        self.verticalLayout = QVBoxLayout(frm_image_view)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lb_image_view = QLabel(frm_image_view)
        self.lb_image_view.setObjectName(u"lb_image_view")

        self.verticalLayout.addWidget(self.lb_image_view)


        self.retranslateUi(frm_image_view)

        QMetaObject.connectSlotsByName(frm_image_view)
    # setupUi

    def retranslateUi(self, frm_image_view):
        frm_image_view.setWindowTitle(QCoreApplication.translate("frm_image_view", u"Form", None))
        self.lb_image_view.setText("")
    # retranslateUi

