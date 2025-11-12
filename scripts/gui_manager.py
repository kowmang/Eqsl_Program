import os
import sys
from PySide6.QtWidgets import QMainWindow, QDialog, QVBoxLayout, QTextBrowser, QFileDialog
from PySide6.QtCore import Slot, Signal
from PySide6.QtGui import QFont

# Die kompilierten UI-Klassen werden hier importiert (relativ zum 'scripts' Ordner)
from ..gui_data.frm_settings_ui import Ui_frm_settings
from ..gui_data.frm_upload_ui import Ui_frm_upload
from ..gui_data.frm_help_view_ui import Ui_frm_help_view
from ..gui_data.frm_version_ui import Ui_frm_version
# Importieren des Logik-Managers
from .settings_manager import SettingsManager 


# ----------------------------------------------------
# 1. DEFINITION DER UNTERFENSTER
# ----------------------------------------------------

class EqslSettingsWindow(QDialog):
    """Das separate Fenster für die Einstellungen."""

    new_db_selected = Signal(str)

    def __init__(self):
        super().__init__()
        self.ui = Ui_frm_settings()
        self.ui.setupUi(self)
        self.setWindowTitle("eQSL Programm (Settings)")
        self._setup_connections() 

    def _setup_connections(self):
        # Verbindung für 'Abbrechen'
        if hasattr(self.ui, 'btn_cancel_frm_settings'):
            self.ui.btn_cancel_frm_settings.clicked.connect(self.reject)
            
        # Verbindung für den "Neue Datenbank erstellen"-Button
        if hasattr(self.ui, 'btn_new_db'):
            self.ui.btn_new_db.clicked.connect(self._open_new_db_dialog)
        pass

    @Slot()
    def _open_new_db_dialog(self):
        """
        Öffnet den Dateidialog, um einen Speicherort für die neue Datenbank 
        auszuwählen und sendet das Signal. Schlägt den Ordner 'database_sql' vor.
        """
        # 1. Berechnet den Pfad zum Ordner 'database_sql' relativ zum aktuellen Skript.
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # Navigiert von 'scripts' in 'Eqsl_Program' und dann nach 'database_sql'
        default_dir = os.path.join(base_dir, '..', 'database_sql')
        default_filepath = os.path.join(default_dir, 'qsl_log.db')

        # Stellt sicher, dass der Ordner existiert (optional, aber gut für UX)
        if not os.path.exists(default_dir):
            os.makedirs(default_dir, exist_ok=True)
        
        # 2. Öffnet den 'Speichern unter'-Dialog mit vorgeschlagenem Pfad/Dateiname
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Select new database file location",
            default_filepath, # Startet im Ordner und schlägt den Dateinamen vor
            "SQLite Database Files (*.db *.sqlite);;All Files (*)"
        )

        if filepath:
            self.new_db_selected.emit(filepath)
        else:
            print("New DB creation cancelled by user.")


class EqslUploadWindow(QDialog): 
    """Das separate Fenster für den QSL-Upload."""
    def __init__(self):
        super().__init__()
        self.ui = Ui_frm_upload()
        self.ui.setupUi(self)
        self.setWindowTitle("eQSL Programm (QSL Upload)")
        self._setup_connections() 

    def _setup_connections(self):
        if hasattr(self.ui, 'btn_cancel'):
            self.ui.btn_cancel.clicked.connect(self.reject)
        pass 

class EqslHelpWindow(QDialog): 
    """Das separate Fenster für die Hilfe/das Handbuch."""
    def __init__(self):
        super().__init__()
        self.ui = Ui_frm_help_view()
        self.ui.setupUi(self) 
        self.setWindowTitle("eQSL Programm (Manual)")
        self.resize(900, 700)
        self._load_manual_content()
        self._setup_connections() 

    def _load_manual_content(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(base_dir, '..', 'support_data', 'manual.html')

        html_content = ""
        if not os.path.exists(html_path):
            html_content = (
                f"<h1>Fehler: manual.html nicht gefunden!</h1>"
                f"<p>Erwarteter Pfad: <code>{html_path}</code></p>"
            )
        else:
            try:
                with open(html_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
            except Exception as e:
                html_content = f"<h1>Fehler beim Lesen der Datei!</h1><p>{e}</p>"
        
        widget = None
        if hasattr(self.ui, 'textBrowser'):
            widget = self.ui.textBrowser
        elif hasattr(self.ui, 'textEdit'):
            widget = self.ui.textEdit
            widget.setReadOnly(True) 
        
        if widget:
            widget.setHtml(html_content)
            widget.setFont(QFont("Arial", 10))
        else:
            browser = QTextBrowser(self)
            browser.setHtml(html_content)
            if self.layout() is None:
                layout = QVBoxLayout(self)
                self.setLayout(layout)
            self.layout().addWidget(browser)

    def _setup_connections(self):
        pass

class EqslVersionWindow(QDialog): 
    """Das separate Fenster für die Versionsinformationen."""
    def __init__(self):
        super().__init__()
        self.ui = Ui_frm_version()
        self.ui.setupUi(self) 
        self.setWindowTitle("eQSL Programm (Version Info)")
        
        self._load_version_content() 
        self._setup_connections() 
    
    def _load_version_content(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(base_dir, '..', 'support_data', 'version.html')

        html_content = ""
        if not os.path.exists(html_path):
            html_content = (
                f"<h1>Fehler: version.html nicht gefunden!</h1>"
                f"<p>Erwarteter Pfad: <code>{html_path}</code></p>"
            )
        else:
            try:
                with open(html_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
            except Exception as e:
                html_content = f"<h1>Fehler beim Lesen der Datei!</h1><p>{e}</p>"
        
        widget = None
        if hasattr(self.ui, 'textBrowser'):
            widget = self.ui.textBrowser
        elif hasattr(self.ui, 'textEdit'):
            widget = self.ui.textEdit
            widget.setReadOnly(True) 
        
        if widget:
            widget.setHtml(html_content)
            widget.setFont(QFont("Arial", 10))
        else:
            browser = QTextBrowser(self)
            browser.setHtml(html_content)
            if self.layout() is None:
                layout = QVBoxLayout(self)
                self.setLayout(layout)
            self.layout().addWidget(browser)
        
    def _setup_connections(self):
        pass


# ----------------------------------------------------
# 2. MANAGER-KLASSE ZUR KONTROLLE DER FENSTER
# ----------------------------------------------------

class GuiManager:
    """Verwaltet die Instanzen aller sekundären Fenster und die Logik-Manager."""
    def __init__(self): 
        self.settings_window = None 
        self.upload_window = None  
        self.help_window = None     
        self.version_window = None  
        
        self.settings_manager = SettingsManager() 
        
    @Slot()
    def open_settings(self):
        """Öffnet das Einstellungsfenster und verbindet die Signale."""
        if self.settings_window is None:
            self.settings_window = EqslSettingsWindow()
            
            # SIGNAL VERBINDEN
            self.settings_window.new_db_selected.connect(
                self.settings_manager.handle_new_db_path
            )
            
        self.settings_window.show()

    @Slot()
    def open_upload(self):
        """Öffnet das Upload-Fenster."""
        if self.upload_window is None:
            self.upload_window = EqslUploadWindow()
        self.upload_window.show() 

    @Slot()
    def open_help(self):
        """Öffnet das Hilfefenster."""
        if self.help_window is None:
            self.help_window = EqslHelpWindow()
        self.help_window.show() 

    @Slot()
    def open_version_info(self):
        """Öffnet das Versionsfenster."""
        if self.version_window is None:
            self.version_window = EqslVersionWindow()
        self.version_window.show()