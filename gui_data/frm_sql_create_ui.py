# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_sql_create.ui'
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
        frm_settings.resize(800, 350)
        self.centralwidget = QWidget(frm_settings)
        self.centralwidget.setObjectName(u"centralwidget")
        self.le_path_new_db = QLineEdit(self.centralwidget)
        self.le_path_new_db.setObjectName(u"le_path_new_db")
        self.le_path_new_db.setGeometry(QRect(40, 70, 300, 30))
        font = QFont()
        font.setPointSize(11)
        self.le_path_new_db.setFont(font)
        self.btn_restore_frm_sql_create = QPushButton(self.centralwidget)
        self.btn_restore_frm_sql_create.setObjectName(u"btn_restore_frm_sql_create")
        self.btn_restore_frm_sql_create.setGeometry(QRect(40, 220, 85, 27))
        font1 = QFont()
        font1.setPointSize(11)
        font1.setBold(True)
        self.btn_restore_frm_sql_create.setFont(font1)
        self.btn_cancel_frm_sql_create = QPushButton(self.centralwidget)
        self.btn_cancel_frm_sql_create.setObjectName(u"btn_cancel_frm_sql_create")
        self.btn_cancel_frm_sql_create.setGeometry(QRect(530, 220, 85, 27))
        self.btn_cancel_frm_sql_create.setFont(font1)
        self.btn_create_new_db = QPushButton(self.centralwidget)
        self.btn_create_new_db.setObjectName(u"btn_create_new_db")
        self.btn_create_new_db.setGeometry(QRect(660, 220, 85, 27))
        self.btn_create_new_db.setFont(font1)
        self.lb_path_new_db = QLabel(self.centralwidget)
        self.lb_path_new_db.setObjectName(u"lb_path_new_db")
        self.lb_path_new_db.setGeometry(QRect(40, 40, 301, 27))
        self.lb_path_new_db.setFont(font)
        self.lb_path_new_db.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.btn_search_path_new_db = QPushButton(self.centralwidget)
        self.btn_search_path_new_db.setObjectName(u"btn_search_path_new_db")
        self.btn_search_path_new_db.setGeometry(QRect(370, 70, 85, 27))
        self.btn_search_path_new_db.setFont(font1)
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
        self.btn_restore_frm_sql_create.setText(QCoreApplication.translate("frm_settings", u"Restore", None))
        self.btn_cancel_frm_sql_create.setText(QCoreApplication.translate("frm_settings", u"Cancel", None))
        self.btn_create_new_db.setText(QCoreApplication.translate("frm_settings", u"Create", None))
        self.lb_path_new_db.setText(QCoreApplication.translate("frm_settings", u"Path to new Database", None))
        self.btn_search_path_new_db.setText(QCoreApplication.translate("frm_settings", u"Search", None))
    # retranslateUi

