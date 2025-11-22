# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_help_view.ui'
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
    QPalette, QPixmap, QRadialGradient, QTransform,
    QTextCharFormat, QTextFormat) 
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QSizePolicy,
    QTextBrowser, QWidget)

class Ui_frm_help_view(object):
    def setupUi(self, frm_help_view):
        if not frm_help_view.objectName():
            frm_help_view.setObjectName(u"frm_help_view")
        frm_help_view.resize(900, 700)
        self.horizontalLayout = QHBoxLayout(frm_help_view)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.textBrowser = QTextBrowser(frm_help_view)
        self.textBrowser.setObjectName(u"textBrowser")

        # NEUE KORREKTUREN FÜR DEN TEXTBROWSER START
        
        # Cursor des QTextBrowser-Dokuments holen
        cursor = self.textBrowser.textCursor()
        
        # 1. Zeichen-Formatierung anpassen (Setzt die Standard-Schrift)
        char_format = QTextCharFormat()
        char_format.setFontFamily("Arial")
        cursor.setCharFormat(char_format)
        
        # 2. Block-Formatierung anpassen, um die Zeilenhöhe zu erzwingen
        block_format = cursor.blockFormat()
        
        # KORREKTUR: Ersetzt QTextFormat.ProportionalHeight (welches einen Fehler warf)
        # durch seinen Integer-Wert 3. Dies erzwingt die proportionale Zeilenhöhe von 160%.
        block_format.setLineHeight(160, 3) 
        
        cursor.setBlockFormat(block_format)

        # 3. Das gesamte Dokument mit den neuen Formaten aktualisieren
        self.textBrowser.setCurrentCharFormat(char_format)
        self.textBrowser.setTextCursor(cursor)
        
        # NEUE KORREKTUREN FÜR DEN TEXTBROWSER ENDE

        self.horizontalLayout.addWidget(self.textBrowser)


        self.retranslateUi(frm_help_view)

        QMetaObject.connectSlotsByName(frm_help_view)
    # setupUi

    def retranslateUi(self, frm_help_view):
        frm_help_view.setWindowTitle(QCoreApplication.translate("frm_help_view", u"Dialog", None))
    # retranslateUi