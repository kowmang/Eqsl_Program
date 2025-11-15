import os
import sys
# WICHTIGE ÄNDERUNG: Importiere Qt, um die WindowModality explizit setzen zu können.
from PySide6.QtWidgets import QMainWindow, QDialog, QVBoxLayout, QTextBrowser, QFileDialog, QMessageBox
from PySide6.QtCore import Slot, Signal, QObject, Qt 
from PySide6.QtGui import QFont
import os.path

# Die kompilierten UI-Klassen werden hier importiert (relativ zum 'scripts' Ordner)
from ..gui_data.frm_settings_ui import Ui_frm_settings
from ..gui_data.frm_single_card_import_ui import Ui_frm_single_card_import
from ..gui_data.frm_help_view_ui import Ui_frm_help_view
from ..gui_data.frm_version_ui import Ui_frm_version
from ..gui_data.frm_bulk_card_import_ui import Ui_frm_bulk_card_import

# Importieren des Logik-Managers
from .settings_manager import SettingsManager 
# Importieren des ADIF_Importer
from .adif_importer import AdifImporter

# ----------------------------------------------------
# 1. DEFINITION DER UNTERFENSTER
# ----------------------------------------------------

class EqslSettingsWindow(QDialog):
    """
    Das separate Fenster für die Einstellungen. 
    WICHTIG: Setzt die Modalität explizit auf ApplicationModal.
    """

    new_db_selected = Signal(str)
    existing_db_selected = Signal(str)
    new_download_dir_selected = Signal(str) 
    adif_import_requested = Signal(str)
    new_adif_selected = Signal(str)

    def __init__(self, settings_manager: SettingsManager, parent=None):
        super().__init__(parent)
        self.ui = Ui_frm_settings()
        self.ui.setupUi(self)
        self.setWindowTitle("eQSL Programm (Settings)")
        
        # FIX: Setze die Modalität explizit auf ApplicationModal.
        # Dies blockiert ALLE Fenster der Anwendung, bis dieser Dialog geschlossen wird,
        # und hält ihn garantiert im Vordergrund.
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        
        self.settings_manager = settings_manager
        self.selected_adif_path = self.settings_manager.get_current_adif_path()
        self._setup_ui_state() 
        self._setup_connections() 

    def _setup_ui_state(self):
        """Initialisiert den Zustand der UI-Elemente basierend auf den Einstellungen."""
        
        # --- 1. Datenbank-Pfad ---
        current_db_path = self.settings_manager.get_current_db_path()
        if hasattr(self.ui, 'txt_db_selection'):
            if current_db_path and os.path.exists(current_db_path):
                self.ui.txt_db_selection.setText(current_db_path)
            else:
                self.ui.txt_db_selection.setText("Bitte wählen Sie eine Datenbank aus...")
            self.ui.txt_db_selection.setReadOnly(True)

        # --- 3. Download-Ordner Pfad ---
        current_download_dir = self.settings_manager.get_current_download_dir()
        if hasattr(self.ui, 'txt_download_dir'):
            if current_download_dir and os.path.isdir(current_download_dir):
                self.ui.txt_download_dir.setText(current_download_dir)
            else:
                self.ui.txt_download_dir.setText("Bitte wählen Sie den Download-Ordner aus...")
            self.ui.txt_download_dir.setReadOnly(True)
            
        # --- 4. ADIF-Listen-Pfad ---
        current_adif_path = self.settings_manager.get_current_adif_path()
        if hasattr(self.ui, 'txt_adif_selection'):
            if current_adif_path:
                self.ui.txt_adif_selection.setText(current_adif_path)
                self.selected_adif_path = current_adif_path 
            else:
                self.ui.txt_adif_selection.setText("Bitte wählen Sie die ADIF-Datei aus...")
            self.ui.txt_adif_selection.setReadOnly(True)

    def _setup_connections(self):
        # Verbindung für 'Abbrechen'
        if hasattr(self.ui, 'btn_cancel_frm_settings'):
            self.ui.btn_cancel_frm_settings.clicked.connect(self.reject)
            
        # Datenbank-Verbindungen
        if hasattr(self.ui, 'btn_new_db'):
            self.ui.btn_new_db.clicked.connect(self._open_new_db_dialog)
            
        if hasattr(self.ui, 'btn_search_db'):
            self.ui.btn_search_db.clicked.connect(self._open_existing_db_dialog)
            
        if hasattr(self.ui, 'btn_reset_db'):
            self.ui.btn_reset_db.clicked.connect(self._handle_reset_db)
            
        # Download-Ordner Verbindungen 
        if hasattr(self.ui, 'btn_search_download_dir'): 
            self.ui.btn_search_download_dir.clicked.connect(self._open_download_dir_dialog)

        # ADIF-Import Verbindung
        if hasattr(self.ui, 'btn_search_adif'): 
             self.ui.btn_search_adif.clicked.connect(self._open_adif_select_dialog)
             
        if hasattr(self.ui, 'btn_import_adif'): 
            self.ui.btn_import_adif.clicked.connect(self._handle_adif_import_click)

    # --- HELPER FUNKTIONEN ---

    def _get_default_db_directory(self) -> str:
        """Berechnet das Standardverzeichnis 'database_sql'."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        default_dir = os.path.join(base_dir, '..', 'database_sql')
        
        if not os.path.exists(default_dir):
            os.makedirs(default_dir, exist_ok=True)
            
        return default_dir
        
    # --- SLOTS (Datenbank) ---

    @Slot()
    def _open_new_db_dialog(self):
        """Öffnet den 'Speichern unter'-Dialog für eine neue Datenbank."""
        default_dir = self._get_default_db_directory()
        default_filepath = os.path.join(default_dir, 'qsl_log.db')

        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Wählen Sie einen Speicherort für die neue Datenbank",
            default_filepath, 
            "SQLite Database Files (*.db *.sqlite);;Alle Dateien (*)"
        )

        if filepath:
            self.new_db_selected.emit(filepath)
            self._setup_ui_state() 

    @Slot()
    def _open_existing_db_dialog(self):
        """Öffnet den 'Öffnen'-Dialog, um eine bestehende Datenbank auszuwählen."""
        current_db_path = self.settings_manager.get_current_db_path()
        
        start_dir = os.path.dirname(current_db_path) if current_db_path and os.path.exists(current_db_path) else self._get_default_db_directory()

        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Wählen Sie eine bestehende Datenbankdatei",
            start_dir,
            "SQLite Database Files (*.db *.sqlite);;Alle Dateien (*)"
        )

        if filepath:
            self.existing_db_selected.emit(filepath)
            self._setup_ui_state() 
            
    @Slot()
    def _handle_reset_db(self):
        """Ruft die Reset-Logik für den DB-Pfad auf und aktualisiert die UI."""
        self.settings_manager.reset_db_path()
        self._setup_ui_state()

    # --- SLOTS (Download-Ordner) ---
    
    @Slot()
    def _open_download_dir_dialog(self):
        """Öffnet den Dialog zur Auswahl des Download-Ordners."""
        current_dir = self.settings_manager.get_current_download_dir()
        start_dir = current_dir if current_dir and os.path.isdir(current_dir) else os.path.expanduser("~")
        
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "Wählen Sie den Standard-Download-Ordner",
            start_dir,
            QFileDialog.ShowDirsOnly
        )

        if dir_path:
            self.new_download_dir_selected.emit(dir_path)
            self._setup_ui_state()

    # --- SLOTS (ADIF-Import) ---
    @Slot()
    def _open_adif_select_dialog(self):
        """Öffnet den QFileDialog, sendet den Pfad zum Speichern und aktualisiert das Textfeld."""
        start_dir = os.path.dirname(self.selected_adif_path) if self.selected_adif_path and os.path.exists(self.selected_adif_path) else os.path.expanduser("~") 

        filepath, _ = QFileDialog.getOpenFileName(
             self,
             "Wählen Sie die ADIF-Datei zum Importieren",
             start_dir, 
             "ADIF Files (*.adif *.adi);;Alle Dateien (*)"
        )
        
        if filepath:
            self.selected_adif_path = filepath
            self.new_adif_selected.emit(filepath) 
            self.ui.txt_adif_selection.setText(filepath)
            
    @Slot()
    def _handle_adif_import_click(self):
        """Sendet den aktuell ausgewählten/gespeicherten Pfad an den GuiManager, um den Import zu starten."""
        if not self.selected_adif_path or not os.path.exists(self.selected_adif_path):
            QMessageBox.warning(self, "Import Fehler", "Bitte zuerst eine gültige ADIF-Datei auswählen.")
            return

        self.adif_import_requested.emit(self.selected_adif_path)


class EqslSingleImportWindow(QDialog): 
    """Fenster für den einzelnen QSO-Import."""
    def __init__(self, parent=None): 
        super().__init__(parent)
        self.ui = Ui_frm_single_card_import()
        self.ui.setupUi(self)
        self.setWindowTitle("eQSL Programm (Single Card Import)")
        self._setup_connections() 

        self.setWindowModality(Qt.WindowModality.ApplicationModal)

    def _setup_connections(self):
        if hasattr(self.ui, 'btn_cancel_frm_single_import'):
            self.ui.btn_cancel_frm_single_import.clicked.connect(self.reject)
        pass 

class EqslBulkImportWindow(QDialog): 
    """Fenster für den Bulk-Import von QSL-Karten."""
    def __init__(self, parent=None): 
        super().__init__(parent)
        self.ui = Ui_frm_bulk_card_import()
        self.ui.setupUi(self)
        self.setWindowTitle("eQSL Programm (Bulk Card Import)")
        self._setup_connections()

        self.setWindowModality(Qt.WindowModality.ApplicationModal) 

    def _setup_connections(self):
        if hasattr(self.ui, 'btn_cancel_frm_bulk_import'):
            self.ui.btn_cancel_frm_bulk_import.clicked.connect(self.reject)
        pass

class EqslHelpWindow(QDialog): 
    """Fenster für die Manual-Anzeige."""
    def __init__(self, parent=None): 
        super().__init__(parent)
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
    """Fenster für die Versionsinformationen."""
    def __init__(self, parent=None): 
        super().__init__(parent)
        self.ui = Ui_frm_version()
        self.ui.setupUi(self) 
        self.setWindowTitle("eQSL Programm (Version Info)")
        
        self._load_version_content() 
        self._setup_connections() 

        self.setWindowModality(Qt.WindowModality.WindowModal)
    
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

class GuiManager(QObject): 
    """Verwaltet die Instanzen aller sekundären Fenster und die Logik-Manager."""
    
    qso_data_updated = Signal(int)

    def __init__(self, main_window: QMainWindow = None): 
        super().__init__() 
        self.main_window = main_window 
        self.settings_window = None 
        self.single_import_window = None
        self.bulk_import_window = None
        self.help_window = None 
        self.version_window = None 
        
        self.settings_manager = SettingsManager() 
        
        initial_db_path = self.settings_manager.get_current_db_path()
        self.adif_importer = AdifImporter(initial_db_path)

    @Slot(str)
    def _handle_adif_import_from_settings(self, adif_filepath: str):
        """
        Interne Methode, die vom SettingsWindow aufgerufen wird, 
        um den Import über den AdifImporter zu starten.
        """
        # Holen Sie den AKTUELLEN Datenbankpfad JEDES MAL, bevor Sie importieren.
        db_path = self.settings_manager.get_current_db_path()
        
        if not db_path:
            QMessageBox.critical(self.settings_window, "Import Fehler", "Keine Datenbank ausgewählt. Import abgebrochen.")
            return

        if not adif_filepath or not os.path.exists(adif_filepath):
             QMessageBox.critical(self.settings_window, "Import Fehler", "Der ausgewählte ADIF-Pfad ist ungültig oder nicht vorhanden.")
             return
             
        # SICHERHEITS-UPDATE: Stellen Sie sicher, dass der AdifImporter den aktuellen Pfad verwendet.
        self.adif_importer.db_filepath = db_path 

        new_records = self.adif_importer.import_adif_file(adif_filepath)
        
        self.qso_data_updated.emit(new_records)

    @Slot()
    def open_settings(self):
        """Öffnet das Einstellungsfenster und verbindet die Signale. (MODAL mit exec)"""
        if self.settings_window is None:
            # Das Hauptfenster (self.main_window) wird als Parent übergeben
            self.settings_window = EqslSettingsWindow(self.settings_manager, parent=self.main_window) 
            
            # DB-Verbindungen
            self.settings_window.new_db_selected.connect(
                self.settings_manager.handle_new_db_path
            )
            self.settings_window.existing_db_selected.connect(
                self.settings_manager.handle_existing_db_path
            )
        
            # Download-Ordner Verbindung 
            self.settings_window.new_download_dir_selected.connect(
                self.settings_manager.handle_new_download_dir
            )
            
            # ADIF Import Verbindungen
            self.settings_window.adif_import_requested.connect(
                self._handle_adif_import_from_settings
            )
            
            self.settings_window.new_adif_selected.connect(
                self.settings_manager.handle_new_adif_path
            )
            
        self.settings_window._setup_ui_state() 
        
        # Durch .exec() wird die Ausführung blockiert, bis der Dialog geschlossen wird, 
        # und in Kombination mit ApplicationModal bleibt er definitiv im Vordergrund.
        self.settings_window.exec() 

    @Slot()
    def open_single_import(self):
        """Öffnet das Fenster für den einzelnen Import."""
        if self.single_import_window is None:
            self.single_import_window = EqslSingleImportWindow(parent=self.main_window)
        self.single_import_window.exec() 

    @Slot()
    def open_bulk_import(self):
        """Öffnet das Fenster für den Bulk-Import."""
        if self.bulk_import_window is None:
            self.bulk_import_window = EqslBulkImportWindow(parent=self.main_window)
        self.bulk_import_window.exec() 

    @Slot()
    def open_help(self):
        """Öffnet das Hilfefenster."""
        if self.help_window is None:
            self.help_window = EqslHelpWindow(parent=self.main_window)
        self.help_window.show() 

    @Slot()
    def open_version_info(self):
        """Öffnet das Versionsfenster."""
        if self.version_window is None:
            self.version_window = EqslVersionWindow(parent=self.main_window)
        self.version_window.exec()