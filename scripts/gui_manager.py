import os
import sys
from PySide6.QtWidgets import QMainWindow, QDialog, QVBoxLayout, QTextBrowser, QFileDialog
from PySide6.QtCore import Slot, Signal
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
    """Das separate Fenster für die Einstellungen."""

    new_db_selected = Signal(str)
    existing_db_selected = Signal(str)
    new_download_dir_selected = Signal(str) # NEUES Signal für Download-Ordner
    adif_import_requested = Signal(str)
    new_adif_selected = Signal(str)

    def __init__(self, settings_manager: SettingsManager):
        super().__init__()
        self.ui = Ui_frm_settings()
        self.ui.setupUi(self)
        self.setWindowTitle("eQSL Programm (Settings)")
        self.settings_manager = settings_manager
        self.selected_adif_path = self.settings_manager.get_current_adif_path()
        self._setup_ui_state() # Zeigt den aktuellen Pfad an
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

        # --- 3. Download-Ordner Pfad (NEU) ---
        current_download_dir = self.settings_manager.get_current_download_dir()
        if hasattr(self.ui, 'txt_download_dir'):
            if current_download_dir and os.path.isdir(current_download_dir):
                self.ui.txt_download_dir.setText(current_download_dir)
            else:
                self.ui.txt_download_dir.setText("Bitte wählen Sie den Download-Ordner aus...")
            self.ui.txt_download_dir.setReadOnly(True)
            
        # --- 4. ADIF-Listen-Pfad (NEU) ---
        current_adif_path = self.settings_manager.get_current_adif_path()
        if hasattr(self.ui, 'txt_adif_selection'):
            if current_adif_path:
                self.ui.txt_adif_selection.setText(current_adif_path)
                self.selected_adif_path = current_adif_path # Lokalen Pfad setzen
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
        if hasattr(self.ui, 'btn_search_adif'): # NEU: Für die Pfadauswahl
             self.ui.btn_search_adif.clicked.connect(self._open_adif_select_dialog)
             
        if hasattr(self.ui, 'btn_import_adif'): 
            # Der Import-Button ruft NICHT den Dialog auf, sondern löst den Import aus
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
        else:
            print("Erstellung der neuen DB vom Benutzer abgebrochen.")

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
        else:
            print("Auswahl einer bestehenden DB vom Benutzer abgebrochen.")
            
    @Slot()
    def _handle_reset_db(self):
        """Ruft die Reset-Logik für den DB-Pfad auf und aktualisiert die UI."""
        self.settings_manager.reset_db_path()
        self._setup_ui_state()
        print("Datenbankpfad wurde zurückgesetzt.")

    # --- SLOTS (Download-Ordner) NEU ---
    
    @Slot()
    def _open_download_dir_dialog(self):
        """
        Öffnet den Dialog zur Auswahl des Download-Ordners.
        """
        current_dir = self.settings_manager.get_current_download_dir()
        # Startverzeichnis: Aktueller Ordner oder Benutzer-Home
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
        else:
            print("Auswahl des Download-Ordners vom Benutzer abgebrochen.")

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
            # 1. Speichert den Pfad lokal und sendet ihn an den SettingsManager
            self.selected_adif_path = filepath
            self.new_adif_selected.emit(filepath) 
            
            # 2. Aktualisiert das Textfeld sofort
            self.ui.txt_adif_selection.setText(filepath)
            
            print(f"ADIF-Pfad ausgewählt und gespeichert: {filepath}")
        else:
            print("ADIF-Auswahl abgebrochen.")

    @Slot()
    def _handle_adif_import_click(self):
        """Sendet den aktuell ausgewählten/gespeicherten Pfad an den GuiManager, um den Import zu starten."""
        if not self.selected_adif_path or not os.path.exists(self.selected_adif_path):
            print("Import Error: Bitte zuerst eine gültige ADIF-Datei auswählen.")
            return

        # Signal an den GuiManager senden, um den Import zu starten
        self.adif_import_requested.emit(self.selected_adif_path)

# ... (Klassen EqslUploadWindow, EqslHelpWindow, EqslVersionWindow bleiben unverändert) ...
class EqslSingleImportWindow(QDialog): 
    # ... (Klasse bleibt unverändert) ...
    def __init__(self):
        super().__init__()
        self.ui = Ui_frm_single_card_import()
        self.ui.setupUi(self)
        self.setWindowTitle("eQSL Programm (Single Card Import)")
        self._setup_connections() 

    def _setup_connections(self):
        if hasattr(self.ui, 'btn_cancel_frm_single_import'):
            self.ui.btn_cancel_frm_single_import.clicked.connect(self.reject)
        pass 

class EqslBulkImportWindow(QDialog): 
    # ... (Klasse bleibt unverändert) ...
    def __init__(self):
        super().__init__()
        self.ui = Ui_frm_bulk_card_import()
        self.ui.setupUi(self)
        self.setWindowTitle("eQSL Programm (Bulk Card Import)")
        self._setup_connections() 

    def _setup_connections(self):
        if hasattr(self.ui, 'btn_cancel_frm_bulk_import'):
            self.ui.btn_cancel_frm_bulk_import.clicked.connect(self.reject)
        pass     

class EqslHelpWindow(QDialog): 
    # ... (Klasse bleibt unverändert) ...
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
    # ... (Klasse bleibt unverändert) ...
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
        self.single_import_window = None  
        self.bulk_import_window = None
        self.help_window = None     
        self.version_window = None  
        
        self.settings_manager = SettingsManager() 

        self.adif_importer = AdifImporter(self.settings_manager)

    @Slot(str)
    def _handle_adif_import_from_settings(self, adif_filepath: str):
        """
        Interne Methode, die vom SettingsWindow aufgerufen wird, 
        um den Import über den AdifImporter zu starten (verwendet den GESPEICHERTEN Pfad).
        """
        db_path = self.settings_manager.get_current_db_path()
        if not db_path:
            print("Import Error: Keine Datenbank ausgewählt.")
            return

        if not adif_filepath or not os.path.exists(adif_filepath):
             print("Import Error: Der ausgewählte ADIF-Pfad ist ungültig oder nicht vorhanden.")
             return
             
        print(f"ADIF-Import gestartet für Datei: {adif_filepath}")
        new_records = self.adif_importer.import_adif_file(adif_filepath)
        print(f"ADIF-Import aus Settings beendet. {new_records} neue QSOs.")
        # TODO: Signal an das Hauptfenster senden, um die Datenansicht zu aktualisieren.

    @Slot()
    def open_settings(self):
        """Öffnet das Einstellungsfenster und verbindet die Signale."""
        if self.settings_window is None:
            self.settings_window = EqslSettingsWindow(self.settings_manager)
            
            # DB-Verbindungen
            self.settings_window.new_db_selected.connect(
                self.settings_manager.handle_new_db_path
            )
            self.settings_window.existing_db_selected.connect(
                self.settings_manager.handle_existing_db_path
            )
    
            # Download-Ordner Verbindung (NEU)
            self.settings_window.new_download_dir_selected.connect(
                self.settings_manager.handle_new_download_dir
            )
            
            self.settings_window.adif_import_requested.connect(
                self._handle_adif_import_from_settings
            )
            
        self.settings_window._setup_ui_state() 
        self.settings_window.show()

    @Slot()
    def open_single_import(self):
        """Öffnet das Upload-Fenster."""
        if self.single_import_window is None:
            self.single_import_window = EqslSingleImportWindow()
        self.single_import_window.show() 

    @Slot()
    def open_bulk_import(self):
        """Öffnet das Upload-Fenster."""
        if self.bulk_import_window is None:
            self.bulk_import_window = EqslBulkImportWindow()
        self.bulk_import_window.show() 

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