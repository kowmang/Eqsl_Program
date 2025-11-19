import os
# import sys  # WURDE ENTFERNT: Import \"sys\" is not accessed (Line 2)
# WICHTIGE ÄNDERUNG: Importiere Qt, um die WindowModality explizit setzen zu können.
from PySide6.QtWidgets import (
    QMainWindow, QDialog, QVBoxLayout, QTextBrowser, 
    QFileDialog, QMessageBox, QWidget # NEU: QWidget für Typisierung von 'parent'
)
from PySide6.QtCore import Slot, Signal, QObject, Qt 
from PySide6.QtGui import QFont
import os.path

# Typisierung Imports
from typing import Optional, Union, TYPE_CHECKING
# NEU: Nur importieren für Typ-Checking, um Zirkuläre Abhängigkeiten zu vermeiden (optional, aber gute Praxis)
if TYPE_CHECKING:
    # Nur für Typ-Checking, wenn die UI-Klassen nicht direkt importiert werden können
    from ..gui_data.frm_settings_ui import Ui_frm_settings
    from ..gui_data.frm_single_card_import_ui import Ui_frm_single_card_import
    from ..gui_data.frm_help_view_ui import Ui_frm_help_view
    from ..gui_data.frm_version_ui import Ui_frm_version
    from ..gui_data.frm_bulk_card_import_ui import Ui_frm_bulk_card_import

# Die kompilierten UI-Klassen werden hier importiert (relativ zum 'scripts' Ordner)
# Die Imports bleiben hier, um Laufzeit-Probleme zu vermeiden, aber wir verwenden TYPE_CHECKING für die UI-Typen unten.
from ..gui_data.frm_settings_ui import Ui_frm_settings
from ..gui_data.frm_single_card_import_ui import Ui_frm_single_card_import
from ..gui_data.frm_help_view_ui import Ui_frm_help_view
from ..gui_data.frm_version_ui import Ui_frm_version
from ..gui_data.frm_bulk_card_import_ui import Ui_frm_bulk_card_import

# Importieren der Logik-Manager
# Wir importieren die Klassen, um sie für die Typisierung nutzen zu können (z.B. SettingsManager)
from .settings_manager import SettingsManager 
from .adif_importer import AdifImporter
from .qsl_image_importer import QslImageImporter 
from .qsl_single_image_importer import QslSingleImageImporter 

# ----------------------------------------------------
# 1. DEFINITION DER UNTERFENSTER
# ----------------------------------------------------

class EqslSettingsWindow(QDialog):
    new_db_selected = Signal(str)
    existing_db_selected = Signal(str)
    new_download_dir_selected = Signal(str) 
    adif_import_requested = Signal(str)
    new_adif_selected = Signal(str)

    # TYPISIERUNG KORREKTUR (Line 35): parent ist Optional[QWidget]
    def __init__(self, settings_manager: SettingsManager, parent: Optional[QWidget] = None):
        # self.ui: Ui_frm_settings # NEU: Pylance weiß nun den Typ
        super().__init__(parent)
        self.ui: Ui_frm_settings = Ui_frm_settings() # NEU: Explizite Typ-Annotation für self.ui
        # self.ui.setupUi(self) 
        # TYPISIERUNG KORREKTUR (Line 38): Fügen Sie eine Typ-Ignorierung hinzu, da PySide6/PyQt5 UI-Klassen 
        # generierte Code-Stubs verwenden und Pylance den Parameter-Typ von setupUi oft nicht auflösen kann (reportUnknownMemberType).
        self.ui.setupUi(self) # type: ignore
        self.setWindowTitle("eQSL Programm (Settings)")
        
        # Einstellungen: ApplicationModal, um die gesamte App für kritische Änderungen zu blockieren.
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        
        self.settings_manager = settings_manager
        self.selected_adif_path = self.settings_manager.get_current_adif_path()
        # KORREKTUR (Lines 693, 735): Umbenennung in `setup_ui_state` und `setup_connections`
        self.setup_ui_state() 
        self.setup_connections() 

    # KORREKTUR: Umbenennung, um reportPrivateUsage zu vermeiden
    def setup_ui_state(self):
        """Initialisiert den Zustand der UI-Elemente basierend auf den Einstellungen."""
        # ... (Code bleibt unverändert) ...
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
            # Logik wie gewünscht: Zeige den gespeicherten Pfad immer an, wenn vorhanden.
            if current_adif_path:
                self.ui.txt_adif_selection.setText(current_adif_path)
                self.selected_adif_path = current_adif_path 
            else:
                self.ui.txt_adif_selection.setText("Bitte wählen Sie die ADIF-Datei aus...")
            self.ui.txt_adif_selection.setReadOnly(True)

    # KORREKTUR: Umbenennung, um reportPrivateUsage zu vermeiden
    def setup_connections(self):
        # Verbindung für 'Abbrechen'
        if hasattr(self.ui, 'btn_cancel_frm_settings'):
            self.ui.btn_cancel_frm_settings.clicked.connect(self.close)
            
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
            self.setup_ui_state() # KORREKTUR: Auf umbenannte Methode verweisen

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
            self.setup_ui_state() # KORREKTUR: Auf umbenannte Methode verweisen
            
    @Slot()
    def _handle_reset_db(self):
        """Ruft die Reset-Logik für den DB-Pfad auf und aktualisiert die UI."""
        self.settings_manager.reset_db_path()
        self.setup_ui_state() # KORREKTUR: Auf umbenannte Methode verweisen

    # --- SLOTS (Download-Ordner) ---
    
    @Slot()
    def _open_download_dir_dialog(self):
        """Öffnet den Dialog zur Auswahl des Download-Ordners."""
        current_dir = self.settings_manager.get_current_download_dir()
        start_dir = current_dir if current_dir and os.path.isdir(current_dir) else os.path.expanduser("~")
        
        # KORREKTUR (Lines 174, 381): Verwenden Sie den vollen Enum-Pfad für QFileDialog.Options oder verwenden Sie 
        # einen type: ignore, da QFileDialog.ShowDirsOnly von Pylance oft nicht korrekt aufgelöst wird.
        # Wir verwenden den korrekten vollen Pfad, der in PySide6/PyQt5 QFileDialog.Options.ShowDirsOnly wäre.
        # Da hier nur der Name verwendet wird, aber das Attribut ShowDirsOnly tatsächlich existiert (als Enum), 
        # fügen wir eine Type-Ignorierung hinzu, um die Funktionalität zu erhalten.
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "Wählen Sie den Standard-Download-Ordner",
            start_dir,
            QFileDialog.ShowDirsOnly # type: ignore
        )

        if dir_path:
            self.new_download_dir_selected.emit(dir_path)
            self.setup_ui_state() # KORREKTUR: Auf umbenannte Methode verweisen

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
    # ... (Unverändert) ...
    single_card_import_requested = Signal(str, str, str, str, str) # Call, Date, Band, Mode, Path
    
    # TYPISIERUNG KORREKTUR (Line 219): parent ist Optional[QWidget]
    def __init__(self, parent: Optional[QWidget] = None): 
        super().__init__(parent)
        self.ui: Ui_frm_single_card_import = Ui_frm_single_card_import() # NEU: Explizite Typ-Annotation für self.ui
        # TYPISIERUNG KORREKTUR (Line 222)
        self.ui.setupUi(self) # type: ignore
        self.setWindowTitle("eQSL Programm (Single Card Import)")
        
        self.setWindowModality(Qt.WindowModality.ApplicationModal) 
        
        self._setup_connections() 
    
    # ... (Rest der Klasse EqslSingleImportWindow bleibt unverändert) ...
    def _setup_connections(self):
        if hasattr(self.ui, 'btn_cancel_frm_single_import'):
            self.ui.btn_cancel_frm_single_import.clicked.connect(self.close)
            
        # NEU: Verbindung für den 'Select' Button (Pfadauswahl)
        if hasattr(self.ui, 'btn_select_path_single'):
            self.ui.btn_select_path_single.clicked.connect(self._open_select_path_dialog)

        # NEU: Verbindung für den 'Import' Button
        if hasattr(self.ui, 'btn_singlecard_import'):
            self.ui.btn_singlecard_import.clicked.connect(self._handle_single_import_request)
            
        # NEU: Verbindung für den 'Reset' Button
        if hasattr(self.ui, 'btn_reset_path_single'):
            # self.ui.btn_reset_path_single.clicked.connect(lambda: self.ui.txt_path_singlecard_import.setText("")) # ALTE ZEILE
            self.ui.btn_reset_path_single.clicked.connect(self._reset_all_fields) # NEUE ZEILE

    @Slot()
    def _reset_all_fields(self):
        """Setzt alle Eingabefelder im Einzelimport-Fenster zurück."""
        # Setzt Call, Date, Band, Mode und Path zurück
        if hasattr(self.ui, 'txt_callsign_single'):
            self.ui.txt_callsign_single.setText("")
        if hasattr(self.ui, 'txt_date_single'):
            self.ui.txt_date_single.setText("")
        if hasattr(self.ui, 'txt_band_single'):
            self.ui.txt_band_single.setText("")
        if hasattr(self.ui, 'txt_mode_single'):
            self.ui.txt_mode_single.setText("")
        if hasattr(self.ui, 'txt_path_singlecard_import'):
            self.ui.txt_path_singlecard_import.setText("")


    @Slot()
    def _open_select_path_dialog(self):
        """Öffnet den Dateidialog zur Auswahl des Bildpfads und setzt das Textfeld."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Bilddatei auswählen", 
            "", 
            "Image Files (*.jpg *.jpeg *.png);;Alle Dateien (*)"
        )
        if file_path and hasattr(self.ui, 'txt_path_singlecard_import'):
            self.ui.txt_path_singlecard_import.setText(file_path)


    @Slot()
    def _handle_single_import_request(self):
        """Sammelt Daten aus den Textfeldern und sendet das Import-Signal."""
        
        # Sicherstellen, dass die UI-Elemente existieren, bevor darauf zugegriffen wird
        if not (hasattr(self.ui, 'txt_callsign_single') and 
                hasattr(self.ui, 'txt_date_single') and
                hasattr(self.ui, 'txt_band_single') and
                hasattr(self.ui, 'txt_mode_single') and
                hasattr(self.ui, 'txt_path_singlecard_import')):
            QMessageBox.critical(self, "Fehler", "UI-Elemente sind nicht korrekt definiert.")
            return

        callsign = self.ui.txt_callsign_single.text().strip()
        date = self.ui.txt_date_single.text().strip()
        band = self.ui.txt_band_single.text().strip()
        mode = self.ui.txt_mode_single.text().strip()
        image_path = self.ui.txt_path_singlecard_import.text().strip()

        # Einfache Validierung vor dem Senden
        if not all([callsign, date, band, mode, image_path]):
            QMessageBox.warning(self, "Import Fehler", "Bitte alle Felder ausfüllen und einen Bildpfad auswählen.")
            return
            
        # Signal senden
        self.single_card_import_requested.emit(callsign, date, band, mode, image_path)


class EqslBulkImportWindow(QDialog): 
    # ... (Unverändert) ...
    # Signale für den GuiManager
    new_bulk_card_dir_selected = Signal(str)
    bulk_card_dir_reset = Signal()
    bulk_card_import_requested = Signal(str)
    
    # TYPISIERUNG KORREKTUR (Line 313): parent ist Optional[QWidget]
    def __init__(self, settings_manager: SettingsManager, parent: Optional[QWidget] = None): 
        super().__init__(parent)
        self.ui: Ui_frm_bulk_card_import = Ui_frm_bulk_card_import() # NEU: Explizite Typ-Annotation für self.ui
        # TYPISIERUNG KORREKTUR (Line 316)
        self.ui.setupUi(self) # type: ignore
        self.setWindowTitle("eQSL Programm (Bulk Card Import)")
        
        self.settings_manager = settings_manager
        
        # Sicherstellen, dass das Fenster modal ist
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        
        self._setup_ui_state()
        self._setup_connections() 
        
    def _setup_ui_state(self):
        """Initialisiert den Zustand der UI-Elemente basierend auf den Einstellungen."""
        
        # NEU: Konsistente Abfrage-Logik für den gespeicherten Pfad (wie bei ADIF)
        try:
            current_bulk_card_directory = self.settings_manager.get_bulk_card_dir()
            
            # --- DEBUGGING HINZUGEFÜGT ---
            print(f"DEBUG (Bulk Card Dir): settings_manager.get_bulk_card_dir() returned: '{current_bulk_card_directory}' (Type: {type(current_bulk_card_directory)})")
            # --- ENDE DEBUGGING ---
            
        except AttributeError:
            current_bulk_card_directory = ""
            print("DEBUG (Bulk Card Dir): settings_manager.get_bulk_card_dir() Methode fehlt (AttributeError).") 

        if hasattr(self.ui, 'txt_path_bulkcard'):
            if current_bulk_card_directory:
                self.ui.txt_path_bulkcard.setText(current_bulk_card_directory)
            else:
                self.ui.txt_path_bulkcard.setText("Bitte wählen Sie den Ordner für QSL-Bilder aus...")
            self.ui.txt_path_bulkcard.setReadOnly(True)

    def _setup_connections(self):
        # Cancel Button (bleibt)
        if hasattr(self.ui, 'btn_cancel_frm_bulk_import'):
            self.ui.btn_cancel_frm_bulk_import.clicked.connect(self.close)
        
        # Search/Select Button (umbenannt in der UI zu btn_search_path_bulkcard_upload)
        if hasattr(self.ui, 'btn_select_path_bulkcard_upload'):
             self.ui.btn_select_path_bulkcard_upload.clicked.connect(self._open_select_dir_dialog)
             
        # Reset Button
        if hasattr(self.ui, 'btn_reset_bulkcard'):
            self.ui.btn_reset_bulkcard.clicked.connect(self._handle_reset)
            
        # Upload/Import Button (umbenannt in der UI zu btn_upload_bulkcard)
        if hasattr(self.ui, 'btn_import_bulkcard'):
            self.ui.btn_import_bulkcard.clicked.connect(self._handle_import_request)
            
    @Slot()
    def _open_select_dir_dialog(self):
        """Öffnet den QFileDialog zur Auswahl des Ordners."""
        # ANNAHME: Die Methode get_bulk_card_dir() ist im SettingsManager vorhanden.
        try:
            current_dir = self.settings_manager.get_bulk_card_dir()
        except AttributeError:
            current_dir = ""

        start_dir = current_dir if current_dir and os.path.isdir(current_dir) else os.path.expanduser("~")
        
        # KORREKTUR (Lines 174, 381): Type-Ignorierung hinzufügen
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "Wählen Sie den Ordner mit den QSL-Bildern",
            start_dir,
            QFileDialog.ShowDirsOnly # type: ignore
        )

        if dir_path:
            # Signal an GuiManager senden, um den Pfad zu speichern
            self.new_bulk_card_dir_selected.emit(dir_path)
            self._setup_ui_state()
            
    @Slot()
    def _handle_reset(self):
        """Setzt den Pfad zurück und aktualisiert die UI."""
        self.bulk_card_dir_reset.emit()
        self._setup_ui_state()

    @Slot()
    def _handle_import_request(self):
        """Startet den Importvorgang, wenn ein gültiger Pfad gesetzt ist."""
        # ANNAHME: Die Methode get_bulk_card_dir() ist im SettingsManager vorhanden.
        try:
            current_dir = self.settings_manager.get_bulk_card_dir()
        except AttributeError:
            current_dir = ""
        
        if not current_dir or not os.path.isdir(current_dir):
            QMessageBox.warning(self.bulk_import_window, "Import Fehler", "Bitte zuerst einen gültigen Ordner auswählen.")
            return

        self.bulk_card_import_requested.emit(current_dir)


class EqslHelpWindow(QDialog): 
    # ... (Unverändert) ...
    # TYPISIERUNG KORREKTUR (Line 413): parent ist Optional[QWidget]
    def __init__(self, parent: Optional[QWidget] = None): 
        super().__init__(parent)
        self.ui: Ui_frm_help_view = Ui_frm_help_view() # NEU: Explizite Typ-Annotation für self.ui
        # TYPISIERUNG KORREKTUR (Line 416)
        self.ui.setupUi(self) # type: ignore
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
        
        # KORREKTUR (Lines 441, 443, 444, 447, 448): Fügen Sie Typ-Ignorierungen hinzu, 
        # da der Typ von self.ui.textBrowser/self.ui.textEdit/self.ui/setupUi
        # von Pylance nicht aufgelöst werden kann (reportUnknownMemberType, reportUnknownVariableType).
        widget: Optional[Union[QTextBrowser, 'QWidget']] = None
        if hasattr(self.ui, 'textBrowser'):
            widget = self.ui.textBrowser # type: ignore
        elif hasattr(self.ui, 'textEdit'):
            widget = self.ui.textEdit # type: ignore
            widget.setReadOnly(True) # type: ignore
        
        if widget:
            widget.setHtml(html_content) # type: ignore
            widget.setFont(QFont("Arial", 10)) # type: ignore
        else:
            browser = QTextBrowser(self)
            browser.setHtml(html_content)
            if self.layout() is None:
                layout = QVBoxLayout(self)
                self.setLayout(layout)
            # KORREKTUR (Line 455): Fügen Sie eine Sicherheitsprüfung für self.layout() ein
            # (reportOptionalMemberAccess: "addWidget" is not a known attribute of "None")
            if self.layout() is not None:
                self.layout().addWidget(browser)

    def _setup_connections(self):
        pass

class EqslVersionWindow(QDialog): 
    # ... (Unverändert) ...
    # TYPISIERUNG KORREKTUR (Line 462): parent ist Optional[QWidget]
    def __init__(self, parent: Optional[QWidget] = None): 
        super().__init__(parent)
        self.ui: Ui_frm_version = Ui_frm_version() # NEU: Explizite Typ-Annotation für self.ui
        # TYPISIERUNG KORREKTUR (Line 465)
        self.ui.setupUi(self) # type: ignore
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
        
        # KORREKTUR (Lines 490, 492, 493, 496, 497): Fügen Sie Typ-Ignorierungen hinzu.
        widget: Optional[Union[QTextBrowser, 'QWidget']] = None
        if hasattr(self.ui, 'textBrowser'):
            widget = self.ui.textBrowser # type: ignore
        elif hasattr(self.ui, 'textEdit'):
            widget = self.ui.textEdit # type: ignore
            widget.setReadOnly(True) # type: ignore
        
        if widget:
            widget.setHtml(html_content) # type: ignore
            widget.setFont(QFont("Arial", 10)) # type: ignore
        else:
            browser = QTextBrowser(self)
            browser.setHtml(html_content)
            if self.layout() is None:
                layout = QVBoxLayout(self)
                self.setLayout(layout)
            # KORREKTUR (Line 504): Fügen Sie eine Sicherheitsprüfung für self.layout() ein
            if self.layout() is not None:
                self.layout().addWidget(browser)
            
    def _setup_connections(self):
        pass


# ----------------------------------------------------
# 2. MANAGER-KLASSE ZUR KONTROLLE DER FENSTER
# ----------------------------------------------------

class GuiManager(QObject): 
    """Verwaltet die Instanzen aller sekundären Fenster und die Logik-Manager."""
    
    qso_data_updated = Signal(int)

    # TYPISIERUNG KORREKTUR (Line 519): main_window ist Optional[QMainWindow]
    # Pylance berichtete hier fälschlicherweise, dass `None` nicht an `QMainWindow` zugewiesen werden kann, 
    # aber in Python 3.7+ kann Optional[X] mit einem Standardwert von None verwendet werden.
    # Hier verwenden wir Optional[QMainWindow] als explizite Typisierung.
    def __init__(self, main_window: Optional[QMainWindow] = None): 
        super().__init__() 
        self.main_window = main_window 
        self.settings_window: Optional[EqslSettingsWindow] = None 
        self.single_import_window: Optional[EqslSingleImportWindow] = None
        self.bulk_import_window: Optional[EqslBulkImportWindow] = None
        self.help_window: Optional[EqslHelpWindow] = None 
        self.version_window: Optional[EqslVersionWindow] = None 
        
        self.settings_manager = SettingsManager() 
        
        initial_db_path = self.settings_manager.get_current_db_path()
        self.adif_importer = AdifImporter(initial_db_path)
        self.image_importer = QslImageImporter(initial_db_path) 
        self.single_image_importer = QslSingleImageImporter(initial_db_path) 
        
        # FIX: Das ist die Korrektur des ursprünglichen Fehlers.
        # Statt der Slots handle_new_db_path/handle_existing_db_path zu verwenden,
        # die keine connect-Methode haben, abonnieren wir das zentrale Signal 
        # db_path_selected vom SettingsManager, das bei jeder DB-Änderung gesendet wird.
        # ANNAHME: db_path_selected ist im SettingsManager als Signal(str) definiert.
        try:
            self.settings_manager.db_path_selected.connect(self._update_importers_db_path)
        except AttributeError:
             print("FEHLER: SettingsManager.db_path_selected Signal nicht gefunden! Importer werden nicht aktualisiert.")
            
        
    @Slot(str)
    def _update_importers_db_path(self, db_path: str):
        """Aktualisiert den DB-Pfad in allen Logik-Services."""
        self.adif_importer.db_filepath = db_path
        self.image_importer.db_filepath = db_path
        self.single_image_importer.db_filepath = db_path 
        print(f"GuiManager: DB Pfad für Importer aktualisiert auf: {db_path}")

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
        
    
    @Slot(str, str, str, str, str)
    def _handle_single_card_import_request(self, callsign: str, date: str, band: str, mode: str, image_path: str):
        """
        Führt den eigentlichen Einzelimport der Bilder durch.
        """
        db_path = self.settings_manager.get_current_db_path()
        
        if not db_path:
            QMessageBox.critical(self.single_import_window, "Import Fehler", "Keine Datenbank ausgewählt. Import abgebrochen.")
            return
            
        # Sicherstellen, dass der Importer den aktuellen Pfad verwendet.
        self.single_image_importer.db_filepath = db_path 

        # KORREKTUR (Line 636): Fügen Sie eine explizite Typ-Annotation hinzu, da der Rückgabewert des Importers 
        # ohne Typ-Annotation nicht aufgelöst wird (reportUnknownVariableType/reportUnknownMemberType).
        # Wir verwenden den Typ-Hinweis: dict[str, Any] (Any ist ein Platzhalter für unbekannte innere Typen)
        results: dict[str, Union[str, int, bool]] = self.single_image_importer.import_single_image(callsign, date, band, mode, image_path)
        
        # Zeige die Ergebnisse an und schließe den Dialog
        if results['success']:
            QMessageBox.information(
                self.single_import_window, 
                "Import erfolgreich", 
                str(results['message'])
            )
            # Schließe den Dialog nach Erfolg
            # KORREKTUR (Line 606): Prüfen Sie, ob das Fenster existiert.
            # Obwohl es unwahrscheinlich ist, wenn es gerade eine QMessageBox anzeigt, 
            # ist es für Pylance die sicherere Variante (reportOptionalMemberAccess: "close" is not a known attribute of "None").
            # Wir verwenden die logische Prüfung, dass self.single_import_window nicht None ist, bevor close() aufgerufen wird.
            if self.single_import_window is not None:
                self.single_import_window.close()
            
            # Emit Signal, falls Hauptfenster Aktualisierung benötigt
            if results.get('qso_id'):
                self.qso_data_updated.emit(1)
                
        else:
             QMessageBox.warning(
                 self.single_import_window, 
                 "Import fehlgeschlagen", 
                 f"{results['message']}\n\nDetails: {results['reason']}"
             )


    @Slot(str)
    def _handle_bulk_card_import_request(self, dir_path: str):
        """
        Führt den eigentlichen Bulk-Import der Bilder durch.
        """
        db_path = self.settings_manager.get_current_db_path()
        
        if not db_path:
            QMessageBox.critical(self.bulk_import_window, "Import Fehler", "Keine Datenbank ausgewählt. Import abgebrochen.")
            return

        QMessageBox.information(self.bulk_import_window, "Bulk Import gestartet", f"Starte den Import von Bildern aus:\n{dir_path}")
        
        # Sicherstellen, dass der Importer den aktuellen Pfad verwendet.
        self.image_importer.db_filepath = db_path 

        # KORREKTUR (Line 636): Fügen Sie eine explizite Typ-Annotation hinzu, da der Rückgabewert des Importers 
        # ohne Typ-Annotation nicht aufgelöst wird.
        results: dict[str, Union[str, int, bool]] = self.image_importer.bulk_import_images(dir_path)
        
        # Zeige die Ergebnisse an
        if results['imported'] > 0:
            QMessageBox.information(
                self.bulk_import_window, 
                "Import abgeschlossen", 
                f"Bulk-Import erfolgreich abgeschlossen.\n"
                f"Gesamtzahl Dateien: {results['total_files']}\n"
                f"Neue Bilder importiert: {results['imported']}\n"
                f"Bereits vorhandene Bilder: {results['already_present']}\n"
                f"Fehler (Parsen/Datei): {results['parse_error'] + results['file_error']}" # type: ignore
            )
            # Emit Signal, falls Hauptfenster Aktualisierung benötigt
            self.qso_data_updated.emit(results['imported'])
        else:
             QMessageBox.warning(
                 self.bulk_import_window, 
                 "Import abgeschlossen", 
                 f"Bulk-Import abgeschlossen, aber keine neuen Bilder importiert.\n"
                 f"Details:\n"
                 f"Gesamtzahl Dateien: {results['total_files']}\n"
                 f"Bereits vorhanden: {results['already_present']}\n"
                 f"QSO nicht gefunden: {results['not_found']}"
             )


    @Slot()
    def open_settings(self):
        """Öffnet das Einstellungsfenster (MODAL: ApplicationModal + .exec())."""
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
            
        self.settings_window.setup_ui_state() # KORREKTUR: Auf umbenannte Methode verweisen
        
        # NEU: .exec() blockiert die Ausführung.
        self.settings_window.exec() 

    @Slot()
    def open_single_import(self):
        """Öffnet das Fenster für den einzelnen Import (MODAL: WindowModal + .exec())."""
        if self.single_import_window is None:
            # Übergabe des Parent-Fensters ist wichtig für WindowModal
            self.single_import_window = EqslSingleImportWindow(parent=self.main_window)
            
            # NEU: Verbindung für den Einzelimport-Request
            self.single_import_window.single_card_import_requested.connect(
                self._handle_single_card_import_request
            )
            
        # NEU: .exec() blockiert die Ausführung.
        self.single_import_window.exec() 

    @Slot()
    def open_bulk_import(self):
        """Öffnet das Fenster für den Bulk-Import (MODAL: WindowModal + .exec())."""
        if self.bulk_import_window is None:
            self.bulk_import_window = EqslBulkImportWindow(self.settings_manager, parent=self.main_window)
            
            # Verbinde Bulk Import Signale
            try:
                # ANNAHME: Diese Slots sind im SettingsManager verfügbar
                self.bulk_import_window.new_bulk_card_dir_selected.connect(
                    self.settings_manager.handle_new_bulk_card_dir
                )
                self.bulk_import_window.bulk_card_dir_reset.connect(
                    self.settings_manager.reset_bulk_card_dir
                )
            except AttributeError as e:
                print(f"WARNUNG: Slots für Bulk Card Settings im SettingsManager fehlen. {e}")
                
            self.bulk_import_window.bulk_card_import_requested.connect(
                self._handle_bulk_card_import_request
            )
            
        self.bulk_import_window._setup_ui_state()
        
        # NEU: .exec() blockiert die Ausführung.
        self.bulk_import_window.exec() 

    @Slot()
    def open_help(self):
        """Öffnet das Hilfefenster (Bleibt non-modal)."""
        if self.help_window is None:
            self.help_window = EqslHelpWindow(parent=self.main_window)
        self.help_window.show() 

    @Slot()
    def open_version_info(self):
        """Öffnet das Versionsfenster (Bleibt non-modal)."""
        if self.version_window is None:
            self.version_window = EqslVersionWindow(parent=self.main_window)
        self.version_window.show()