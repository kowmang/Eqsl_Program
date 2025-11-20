import os
from PySide6.QtWidgets import (
    QMainWindow, QDialog, QVBoxLayout, QTextBrowser, 
    QFileDialog, QMessageBox, QWidget, QTextEdit
)
from PySide6.QtCore import Slot, Signal, QObject, Qt 
from PySide6.QtGui import QFont
import os.path

# Typing Imports
from typing import Optional, Union, TYPE_CHECKING, Any
# NEW: Import QMainWindow here if it cannot find Pylance in the TYPE_CHECKING block.
# from PySide6.QtWidgets import QMainWindow 
if TYPE_CHECKING:
    from PySide6.QtWidgets import QMainWindow # FFor type safety
    from ..gui_data.frm_settings_ui import Ui_frm_settings
    from ..gui_data.frm_single_card_import_ui import Ui_frm_single_card_import
    from ..gui_data.frm_help_view_ui import Ui_frm_help_view
    from ..gui_data.frm_version_ui import Ui_frm_version
    from ..gui_data.frm_bulk_card_import_ui import Ui_frm_bulk_card_import

# The compiled UI classes are imported here (relative to the 'scripts' folder)
from ..gui_data.frm_settings_ui import Ui_frm_settings
from ..gui_data.frm_single_card_import_ui import Ui_frm_single_card_import
from ..gui_data.frm_help_view_ui import Ui_frm_help_view
from ..gui_data.frm_version_ui import Ui_frm_version
from ..gui_data.frm_bulk_card_import_ui import Ui_frm_bulk_card_import

# Importing the logic managers
from .settings_manager import SettingsManager 
from .adif_importer import AdifImporter
from .qsl_image_importer import QslImageImporter 
from .qsl_single_image_importer import QslSingleImageImporter 

# ----------------------------------------------------
# 1. DEFINITION OF SUBWINDOWS (Classes remain unchanged)
# ----------------------------------------------------

class EqslSettingsWindow(QDialog):
    new_db_selected = Signal(str)
    existing_db_selected = Signal(str)
    new_download_dir_selected = Signal(str) 
    adif_import_requested = Signal(str)
    new_adif_selected = Signal(str)

    def __init__(self, settings_manager: SettingsManager, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.ui: Ui_frm_settings = Ui_frm_settings()
        self.ui.setupUi(self) # type: ignore
        self.setWindowTitle("eQSL Programm (Settings)")
        
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        
        self.settings_manager = settings_manager
        self.selected_adif_path = self.settings_manager.get_current_adif_path()
        self.setup_ui_state() 
        self.setup_connections() 

    def setup_ui_state(self):
        """Initializes the state of the UI elements based on the settings."""
        # ... (Logic as before) ...
        current_db_path = self.settings_manager.get_current_db_path()
        if hasattr(self.ui, 'txt_db_selection'):
            if current_db_path and os.path.exists(current_db_path):
                self.ui.txt_db_selection.setText(current_db_path)
            else:
                self.ui.txt_db_selection.setText("Please select a database...")
            self.ui.txt_db_selection.setReadOnly(True)

        current_download_dir = self.settings_manager.get_current_download_dir()
        if hasattr(self.ui, 'txt_download_dir'):
            if current_download_dir and os.path.isdir(current_download_dir):
                self.ui.txt_download_dir.setText(current_download_dir)
            else:
                self.ui.txt_download_dir.setText("Please select the download directory...")
            self.ui.txt_download_dir.setReadOnly(True)
            
        current_adif_path = self.settings_manager.get_current_adif_path()
        if hasattr(self.ui, 'txt_adif_selection'):
            if current_adif_path:
                self.ui.txt_adif_selection.setText(current_adif_path)
                self.selected_adif_path = current_adif_path 
            else:
                self.ui.txt_adif_selection.setText("Please select the ADIF file...")
            self.ui.txt_adif_selection.setReadOnly(True)

    def setup_connections(self):
        # Connection for 'Cancel'
        if hasattr(self.ui, 'btn_cancel_frm_settings'):
            self.ui.btn_cancel_frm_settings.clicked.connect(self.close)
            
        # Database connections
        if hasattr(self.ui, 'btn_new_db'):
            self.ui.btn_new_db.clicked.connect(self._open_new_db_dialog)
            
        if hasattr(self.ui, 'btn_search_db'):
            self.ui.btn_search_db.clicked.connect(self._open_existing_db_dialog)
            
        if hasattr(self.ui, 'btn_reset_db'):
            self.ui.btn_reset_db.clicked.connect(self._handle_reset_db)
            
        # Download directory connections
        if hasattr(self.ui, 'btn_search_download_dir'): 
            self.ui.btn_search_download_dir.clicked.connect(self._open_download_dir_dialog)

        # ADIF import connection
        if hasattr(self.ui, 'btn_search_adif'): 
             self.ui.btn_search_adif.clicked.connect(self._open_adif_select_dialog)
             
        if hasattr(self.ui, 'btn_import_adif'): 
            self.ui.btn_import_adif.clicked.connect(self._handle_adif_import_click)

    # ... (Rest of the EqslSettingsWindow methods _get_default_db_directory, _open_new_db_dialog, 
    # _open_existing_db_dialog, _handle_reset_db, _open_download_dir_dialog, 
    # _open_adif_select_dialog, _handle_adif_import_click remain unchanged) ...

    def _get_default_db_directory(self) -> str:
        """Calculates the default 'database_sql' directory."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        default_dir = os.path.join(base_dir, '..', 'database_sql')
        
        if not os.path.exists(default_dir):
            os.makedirs(default_dir, exist_ok=True)
            
        return default_dir
        
    @Slot()
    def _open_new_db_dialog(self):
        """Opens the 'Save As' dialog for a new database."""
        default_dir = self._get_default_db_directory()
        default_filepath = os.path.join(default_dir, 'qsl_log.db')

        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Select a location to save the new database",
            default_filepath, 
            "SQLite Database Files (*.db *.sqlite);;All Files (*)"
        )

        if filepath:
            self.new_db_selected.emit(filepath)
            self.setup_ui_state()

    @Slot()
    def _open_existing_db_dialog(self):
        """Opens the 'Open' dialog to select an existing database."""
        current_db_path = self.settings_manager.get_current_db_path()
        
        start_dir = os.path.dirname(current_db_path) if current_db_path and os.path.exists(current_db_path) else self._get_default_db_directory()

        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Select an existing database file",
            start_dir,
            "SQLite Database Files (*.db *.sqlite);;All Files (*)"
        )

        if filepath:
            self.existing_db_selected.emit(filepath)
            self.setup_ui_state()
            
    @Slot()
    def _handle_reset_db(self):
        """Calls the reset logic for the DB path and updates the UI."""
        self.settings_manager.reset_db_path()
        self.setup_ui_state()

    @Slot()
    def _open_download_dir_dialog(self):
        """Opens the dialog to select the download directory."""
        current_dir = self.settings_manager.get_current_download_dir()
        start_dir = current_dir if current_dir and os.path.isdir(current_dir) else os.path.expanduser("~")
        
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "Select the default download directory",
            start_dir,
            QFileDialog.ShowDirsOnly # type: ignore
        )

        if dir_path:
            self.new_download_dir_selected.emit(dir_path)
            self.setup_ui_state()

    @Slot()
    def _open_adif_select_dialog(self):
        """Opens the QFileDialog, sends the path for saving, and updates the text field."""
        start_dir = os.path.dirname(self.selected_adif_path) if self.selected_adif_path and os.path.exists(self.selected_adif_path) else os.path.expanduser("~") 

        filepath, _ = QFileDialog.getOpenFileName(
             self,
             "Select the ADIF file to import",
             start_dir, 
             "ADIF Files (*.adif *.adi);;All Files (*)"
        )
        
        if filepath:
            self.selected_adif_path = filepath
            self.new_adif_selected.emit(filepath) 
            self.ui.txt_adif_selection.setText(filepath)
            
    @Slot()
    def _handle_adif_import_click(self):
        """Sends the currently selected/saved path to the GuiManager to start the import."""
        if not self.selected_adif_path or not os.path.exists(self.selected_adif_path):
            QMessageBox.warning(self, "Import Error", "Please select a valid ADIF file first.")
            return

        self.adif_import_requested.emit(self.selected_adif_path)


class EqslSingleImportWindow(QDialog): 
    single_card_import_requested = Signal(str, str, str, str, str) # Call, Date, Band, Mode, Path
    
    def __init__(self, parent: Optional[QWidget] = None): 
        super().__init__(parent)
        self.ui: Ui_frm_single_card_import = Ui_frm_single_card_import()
        self.ui.setupUi(self) # type: ignore
        self.setWindowTitle("eQSL Programm (Single Card Import)")
        
        self.setWindowModality(Qt.WindowModality.ApplicationModal) 
        
        self._setup_connections() 
    
    def _setup_connections(self):
        if hasattr(self.ui, 'btn_cancel_frm_single_import'):
            self.ui.btn_cancel_frm_single_import.clicked.connect(self.close)
            
        if hasattr(self.ui, 'btn_select_path_single'):
            self.ui.btn_select_path_single.clicked.connect(self._open_select_path_dialog)

        if hasattr(self.ui, 'btn_singlecard_import'):
            self.ui.btn_singlecard_import.clicked.connect(self._handle_single_import_request)
            
        if hasattr(self.ui, 'btn_reset_path_single'):
            self.ui.btn_reset_path_single.clicked.connect(self._reset_all_fields)

    @Slot()
    def _reset_all_fields(self):
        """Resets all input fields in the single import window."""
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
        """Opens the file dialog to select the image path and sets the text field."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select Image File", 
            "", 
            "Image Files (*.jpg *.jpeg *.png);;All Files (*)"
        )
        if file_path and hasattr(self.ui, 'txt_path_singlecard_import'):
            self.ui.txt_path_singlecard_import.setText(file_path)

    @Slot()
    def _handle_single_import_request(self):
        """Collects data from the text fields and sends the import signal."""
        
        if not (hasattr(self.ui, 'txt_callsign_single') and 
                hasattr(self.ui, 'txt_date_single') and
                hasattr(self.ui, 'txt_band_single') and
                hasattr(self.ui, 'txt_mode_single') and
                hasattr(self.ui, 'txt_path_singlecard_import')):
            QMessageBox.critical(self, "Error", "UI elements are not properly defined.")
            return

        callsign = self.ui.txt_callsign_single.text().strip()
        date = self.ui.txt_date_single.text().strip()
        band = self.ui.txt_band_single.text().strip()
        mode = self.ui.txt_mode_single.text().strip()
        image_path = self.ui.txt_path_singlecard_import.text().strip()

        if not all([callsign, date, band, mode, image_path]):
            QMessageBox.warning(self, "Import error", "Please fill in all fields and select an image path.")
            return
            
        self.single_card_import_requested.emit(callsign, date, band, mode, image_path)


class EqslBulkImportWindow(QDialog): 
    new_bulk_card_dir_selected = Signal(str)
    bulk_card_dir_reset = Signal()
    bulk_card_import_requested = Signal(str)
    
    def __init__(self, settings_manager: SettingsManager, parent: Optional[QWidget] = None): 
        super().__init__(parent)
        self.ui: Ui_frm_bulk_card_import = Ui_frm_bulk_card_import()
        self.ui.setupUi(self) # type: ignore
        self.setWindowTitle("eQSL Programm (Bulk Card Import)")
        
        self.settings_manager = settings_manager
        
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        
        self._setup_ui_state()
        self._setup_connections() 
        
    def _setup_ui_state(self):
        """Initializes the state of the UI elements based on the settings."""
        
        try:
            current_bulk_card_directory = self.settings_manager.get_bulk_card_dir()
        except AttributeError:
            current_bulk_card_directory = ""

        if hasattr(self.ui, 'txt_path_bulkcard'):
            if current_bulk_card_directory:
                self.ui.txt_path_bulkcard.setText(current_bulk_card_directory)
            else:
                self.ui.txt_path_bulkcard.setText("Please select the folder for QSL images...")
            self.ui.txt_path_bulkcard.setReadOnly(True)

    def _setup_connections(self):
        if hasattr(self.ui, 'btn_cancel_frm_bulk_import'):
            self.ui.btn_cancel_frm_bulk_import.clicked.connect(self.close)
        
        if hasattr(self.ui, 'btn_select_path_bulkcard_upload'): # Assumption: Corrected name
             self.ui.btn_select_path_bulkcard_upload.clicked.connect(self._open_select_dir_dialog)
             
        if hasattr(self.ui, 'btn_reset_bulkcard'):
            self.ui.btn_reset_bulkcard.clicked.connect(self._handle_reset)
            
        if hasattr(self.ui, 'btn_import_bulkcard'):
            self.ui.btn_import_bulkcard.clicked.connect(self._handle_import_request)
            
    @Slot()
    def _open_select_dir_dialog(self):
        """Opens the QFileDialog to select the directory."""
        try:
            current_dir = self.settings_manager.get_bulk_card_dir()
        except AttributeError:
            current_dir = ""

        start_dir = current_dir if current_dir and os.path.isdir(current_dir) else os.path.expanduser("~")
        
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "Select the folder with QSL images",
            start_dir,
            QFileDialog.ShowDirsOnly # type: ignore
        )

        if dir_path:
            self.new_bulk_card_dir_selected.emit(dir_path)
            self._setup_ui_state()
            
    @Slot()
    def _handle_reset(self):
        """Resets the path and updates the UI."""
        self.bulk_card_dir_reset.emit()
        self._setup_ui_state()

    @Slot()
    def _handle_import_request(self):
        """Starts the import process if a valid path is set."""
        try:
            current_dir = self.settings_manager.get_bulk_card_dir()
        except AttributeError:
            current_dir = ""
        
        if not current_dir or not os.path.isdir(current_dir):
            QMessageBox.warning(self, "Import error", "Please select a valid directory first.")
            return

        self.bulk_card_import_requested.emit(current_dir)


class EqslHelpWindow(QDialog): 
    def __init__(self, parent: Optional[QWidget] = None): 
        super().__init__(parent)
        self.ui: Ui_frm_help_view = Ui_frm_help_view()
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
                f"<h1>Error: manual.html not found!</h1>"
                f"<p>Expected path: <code>{html_path}</code></p>"
            )
        else:
            try:
                with open(html_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
            except Exception as e:
                html_content = f"<h1>Error reading the file!</h1><p>{e}</p>"
        
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
            if self.layout() is not None:
                self.layout().addWidget(browser)

    def _setup_connections(self):
        pass

class EqslVersionWindow(QDialog): 
    def __init__(self, parent: Optional[QWidget] = None): 
        # Since you defined the class outside the global scope, 
        # we need to keep the type imports.
        super().__init__(parent)
        self.ui: Ui_frm_version = Ui_frm_version()
        self.ui.setupUi(self) # type: ignore
        
        # Set the title according to your preference
        self.setWindowTitle("eQSL Program (Version and Credits)")
        
        # NEW: Direct assignment of the formatted content
        self._setup_text_content() 
        self._setup_connections() 
        
    def _setup_text_content(self):
        """Configures the QTextEdit widget and loads the fixed, formatted content."""
        
        # 1. Check and configure the QTextEdit widget ('txt_version_credits')
        if hasattr(self.ui, 'txt_version_credits') and isinstance(self.ui.txt_version_credits, QTextEdit):
            text_edit: QTextEdit = self.ui.txt_version_credits
            
            # Important: Make read-only
            text_edit.setReadOnly(True) 
            text_edit.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            
            # 2. Format the desired text as HTML (centered and styled)
            html_content = """
            <div align='center'>
                <h1 style='font-size: 18pt; margin-bottom: 5px; color: #0078D4;'>
                    eQSL Program
                </h1>
                <h2 style='font-size: 14pt; margin-top: 0;'>
                    Version 0.1.0
                </h2>
                <p>
                    <b>Release Datum:</b> 19. November 2025
                </p>
                <hr width='70%' style='border: 1px solid #ccc;'>

                <h3 style='font-weight: bold;'>New Function in 0.1.0:</h3>
                <p>
                    First public release,<br>
                    for info read manual<br>
                    or readme<br>
                </p>
                
                <br>
                
                <h3 style='font-weight: bold; color: #555;'>Created by</h3>
                <p style='font-size: 12pt; font-weight: bold; color: #0078D4;'>
                    SuccuS
                </p>
                
                <br>
                
                <h3 style='font-weight: bold;'>Credits to:</h3>
                <p>
                    Text to fill in at<br>
                    first public release
                </p>
            </div>
            """
            
            # 3. Assign content
            text_edit.setHtml(html_content)
            
            # You can set the base font if desired (optional)
            text_edit.setFont(QFont("Arial", 10)) 

        else:
            # If the widget is named differently or missing in the UI code.
            print("ERROR: QTextEdit 'txt_version_credits' not found or is of the wrong type.")
            QMessageBox.critical(self, "UI Error", "The version text field could not be found.")

    # The _setup_connections method can remain empty as no logic is needed in the version window.
    def _setup_connections(self):
        pass


# ----------------------------------------------------
# 2. MANAGER CLASS FOR WINDOW CONTROL
# ----------------------------------------------------

class GuiManager(QObject): 
    """Manages instances of all secondary windows and the logic managers."""
    
    qso_data_updated = Signal(int)

    # CORRECTED __init__
    def __init__(self, db_conn=None, settings_manager=None, main_window: Optional['QMainWindow'] = None, parent=None):
        super().__init__(parent) 
        
        # 1. CORRECTION: Store the passed dependencies
        self.db_conn = db_conn
        self.settings_manager: SettingsManager = settings_manager 
        self.main_window = main_window # <--- CRITICAL: Stores the main window

        print("GuiManager: Initializing with DB Connection and Settings Manager.")
        
        # 2. Window instances (Keep lazy initialization as they are used in open_... slots)
        self.settings_window: Optional['EqslSettingsWindow'] = None 
        self.single_import_window: Optional['EqslSingleImportWindow'] = None
        self.bulk_import_window: Optional['EqslBulkImportWindow'] = None
        self.help_window: Optional['EqslHelpWindow'] = None 
        self.version_window: Optional['EqslVersionWindow'] = None 
        
        # 3. CORRECTION: Remove the duplicate initialization of the SettingsManager!
        # self.settings_manager = SettingsManager() 
        
        # 4. Importer initialization (remains the same)
        initial_db_path = self.settings_manager.get_current_db_path()
        self.adif_importer = AdifImporter(initial_db_path)
        self.image_importer = QslImageImporter(initial_db_path) 
        self.single_image_importer = QslSingleImageImporter(initial_db_path) 
        
        # 5. Connection (remains the same)
        try:
            self.settings_manager.db_path_selected.connect(self._update_importers_db_path)
        except AttributeError:
            print("ERROR: SettingsManager.db_path_selected signal not found! Importers will not be updated.")
        
    @Slot(str)
    def _update_importers_db_path(self, db_path: str):
        """Updates the DB path in all logic services."""
        self.adif_importer.db_filepath = db_path
        self.image_importer.db_filepath = db_path
        self.single_image_importer.db_filepath = db_path 
        print(f"GuiManager: DB path for importers updated to: {db_path}")
    @Slot(str)
    def _handle_adif_import_from_settings(self, adif_filepath: str):
        """
        Internal method called by the SettingsWindow 
        to start the import via the AdifImporter.
        """
        db_path = self.settings_manager.get_current_db_path()
        
        if not db_path:
            QMessageBox.critical(self.settings_window, "Import Error", "No database selected. Import aborted.")
            return

        if not adif_filepath or not os.path.exists(adif_filepath):
             QMessageBox.critical(self.settings_window, "Import Error", "The selected ADIF path is invalid or does not exist.")
             return
             
        self.adif_importer.db_filepath = db_path 

        new_records = self.adif_importer.import_adif_file(adif_filepath)
        
        self.qso_data_updated.emit(new_records)
        
    @Slot(str, str, str, str, str)
    def _handle_single_card_import_request(self, callsign: str, date: str, band: str, mode: str, image_path: str):
        """
        Performs the actual single import of images.
        """
        db_path = self.settings_manager.get_current_db_path()
        
        if not db_path:
            QMessageBox.critical(self.single_import_window, "Import Error", "No database selected. Import aborted.")
            return
            
        self.single_image_importer.db_filepath = db_path 

        results: dict[str, Union[str, int, bool]] = self.single_image_importer.import_single_image(callsign, date, band, mode, image_path)
        
        if results['success']:
            QMessageBox.information(
                self.single_import_window, 
                "Import successful", 
                str(results['message'])
            )
            if self.single_import_window is not None:
                self.single_import_window.close()
            
            if results.get('qso_id'):
                self.qso_data_updated.emit(1)
                
        else:
             QMessageBox.warning(
                 self.single_import_window, 
                 "Import failed", 
                 f"{results['message']}\n\nDetails: {results['reason']}"
             )

    @Slot(str)
    def _handle_bulk_card_import_request(self, dir_path: str):
        """
        Performs the actual bulk import of images.
        """
        db_path = self.settings_manager.get_current_db_path()
        
        if not db_path:
            QMessageBox.critical(self.bulk_import_window, "Import Error", "No database selected. Import aborted.")
            return

        QMessageBox.information(self.bulk_import_window, "Bulk Import started", f"Starting import of images from:\n{dir_path}")
        
        self.image_importer.db_filepath = db_path 

        results: dict[str, Union[str, int, bool]] = self.image_importer.bulk_import_images(dir_path)
        
        # Show the results
        if results.get('imported', 0) > 0:
            QMessageBox.information(
                self.bulk_import_window, 
                "Import completed", 
                f"Bulk import completed successfully.\n"
                f"Total files: {results.get('total_files', 0)}\n"
                f"New images imported: {results.get('imported', 0)}\n"
                f"Images already present: {results.get('already_present', 0)}\n"
                f"Errors (parsing/file): {results.get('parse_error', 0) + results.get('file_error', 0)}"
            )
            self.qso_data_updated.emit(results['imported']) # type: ignore
        else:
             QMessageBox.warning(
                 self.bulk_import_window, 
                 "Import completed", 
                 f"Bulk import completed, but no new images were imported.\n"
                 f"Details:\n"
                 f"Total files: {results.get('total_files', 0)}\n"
                 f"Images already present: {results.get('already_present', 0)}\n"
                 f"QSO not found: {results.get('not_found', 0)}"
             )


    # --- OPPENING-SLOTS (MODAL) ---

    @Slot()
    def open_settings(self):
        """Opens the settings window (MODAL: ApplicationModal + .exec())."""
        # NEW: Check if the window exists, otherwise initialize it
        if self.settings_window is None:
            self.settings_window = EqslSettingsWindow(self.settings_manager, parent=self.main_window) 
            
            # DB connections
            self.settings_window.new_db_selected.connect(
                self.settings_manager.handle_new_db_path
            )
            self.settings_window.existing_db_selected.connect(
                self.settings_manager.handle_existing_db_path
            )
            
            # Download folder connection 
            self.settings_window.new_download_dir_selected.connect(
                self.settings_manager.handle_new_download_dir
            )
            
            # ADIF import connections
            self.settings_window.adif_import_requested.connect(
                self._handle_adif_import_from_settings
            )
            
            self.settings_window.new_adif_selected.connect(
                self.settings_manager.handle_new_adif_path
            )
            
        self.settings_window.setup_ui_state() 
        self.settings_window.exec() 

    @Slot()
    def open_single_import(self):
        """Opens the window for single import (MODAL: WindowModal + .exec())."""
        if self.single_import_window is None:
            self.single_import_window = EqslSingleImportWindow(parent=self.main_window)
            
            # NEW: Connection for single import request
            self.single_import_window.single_card_import_requested.connect(
                self._handle_single_card_import_request
            )
            
        self.single_import_window.exec() 

    @Slot()
    def open_bulk_import(self):
        """Opens the window for bulk import (MODAL: WindowModal + .exec())."""
        if self.bulk_import_window is None:
            self.bulk_import_window = EqslBulkImportWindow(self.settings_manager, parent=self.main_window)
            
            # Connect bulk import signals
            try:
                self.bulk_import_window.new_bulk_card_dir_selected.connect(
                    self.settings_manager.handle_new_bulk_card_dir
                )
                self.bulk_import_window.bulk_card_dir_reset.connect(
                    self.settings_manager.reset_bulk_card_dir
                )
            except AttributeError as e:
                print(f"WARNING: Slots for bulk card settings in SettingsManager are missing. {e}")
                
            self.bulk_import_window.bulk_card_import_requested.connect(
                self._handle_bulk_card_import_request
            )
            
        self.bulk_import_window._setup_ui_state()
        self.bulk_import_window.exec() 

    # --- OPENING-SLOTS (NON-MODAL) ---

    @Slot()
    def open_help(self):
        """Opens the help window (Remains non-modal)."""
        if self.help_window is None:
            self.help_window = EqslHelpWindow(parent=self.main_window)
        self.help_window.show() 

    @Slot()
    def open_version_info(self):
        """Opens the version window (Remains non-modal)."""
        if self.version_window is None:
            self.version_window = EqslVersionWindow(parent=self.main_window)
        self.version_window.show()

        