import sys
import os
import re 
from PySide6.QtWidgets import (QApplication, QMainWindow, QMessageBox, QFileDialog)
from PySide6.QtCore import (Slot, QSortFilterProxyModel, QItemSelection, QItemSelectionModel, 
                            QModelIndex, Qt, QByteArray, QDir)
from PySide6.QtSql import QSqlDatabase, QSqlTableModel
from PySide6.QtGui import QPixmap 

# Correct imports (based on your structure)
from gui_data.frm_main_window_ui import Ui_frm_main_window 
from scripts.gui_manager import GuiManager 
from scripts.settings_manager import SettingsManager 
from scripts.image_viewer_dialog import ImageViewerDialog


# Definition of column indexes (0-based)
COL_CALL = 1
COL_QSO_DATE = 2
COL_TIME_ON = 3
COL_BAND = 4
COL_MODE = 5
COL_SUB_MODE = 6
COL_FREQ = 7        
COL_COUNTRY = 12    
COL_CQZ = 15        
COL_ITUZ = 16       
COL_GRID = 17       

COL_IMAGE_BLOB = 29 

# List of searchable columns
SEARCHABLE_COLUMN_INDICES = [
    COL_CALL, COL_QSO_DATE, COL_TIME_ON, COL_BAND, COL_MODE, 
    COL_SUB_MODE, COL_COUNTRY, COL_FREQ, COL_CQZ, COL_ITUZ, COL_GRID
]


# ======================================================================
# Custom proxy model for multi-column OR filtering
# ======================================================================
class MultiColumnFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None, searchable_indices=None):
        super().__init__(parent)
        self.search_terms = []
        self.searchable_indices = searchable_indices if searchable_indices is not None else []

    def setFilterString(self, text: str):
        """
        Sets the filter string. Spaces now act as OR separators.
        """
        # Split the text into terms and convert to lowercase
        self.search_terms = [term.strip().lower() for term in text.split() if term.strip()]
        # Restart filtering
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        """
        Implements the OR logic: a row is accepted if ANY of the search terms 
        in ANY of the defined columns is found.
        """
        if not self.search_terms:
            return True 

        source_model = self.sourceModel()
        
        # OR logic
        for term in self.search_terms:
            for col_index in self.searchable_indices:
                index = source_model.index(source_row, col_index, source_parent)
                data = source_model.data(index, Qt.ItemDataRole.DisplayRole)
                
                if data is None:
                    continue
                
                try:
                    data_str = str(data).lower()
                    if term in data_str:
                        # Term found => accept row (OR condition met)
                        return True 
                except:
                    continue

        # None of the search terms were found => reject row
        return False


# ======================================================================
# EqslMainWindow
# ======================================================================
class EqslMainWindow(QMainWindow):
    
    def __init__(self, db_conn: QSqlDatabase, settings_manager: SettingsManager): 
        super().__init__()
        
        self.db = db_conn
        self.settings_manager = settings_manager 
        
        # NEW: Storage variable for the default pixmap
        self.default_pixmap = QPixmap() 
        
        self.gui_manager = GuiManager(
            db_conn=self.db, 
            settings_manager=self.settings_manager,
            main_window=self 
        ) 

        self.ui = Ui_frm_main_window()
        self.ui.setupUi(self)
        self.setWindowTitle("eQSL Program (Main Window)")

        self._setup_models()
        self._setup_ui_elements()
        
        self._setup_connections()

    def _setup_models(self):
        table_name = self.settings_manager.settings.get("table_name", "eqsl_data")
        
        # 1. Initialize QSqlTableModel
        self.source_model = QSqlTableModel(db=self.db)
        self.source_model.setTable(table_name)
        self.source_model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        
        # Set column headers
        self.source_model.setHeaderData(COL_CALL, Qt.Orientation.Horizontal, "Call")
        self.source_model.setHeaderData(COL_QSO_DATE, Qt.Orientation.Horizontal, "Date")
        self.source_model.setHeaderData(COL_TIME_ON, Qt.Orientation.Horizontal, "Time")
        self.source_model.setHeaderData(COL_BAND, Qt.Orientation.Horizontal, "Band")
        self.source_model.setHeaderData(COL_MODE, Qt.Orientation.Horizontal, "Mode")
        self.source_model.setHeaderData(COL_FREQ, Qt.Orientation.Horizontal, "Frequenz")
        self.source_model.setHeaderData(COL_ITUZ, Qt.Orientation.Horizontal, "ITU Zone")
        self.source_model.setHeaderData(COL_CQZ, Qt.Orientation.Horizontal, "CQ Zone")
        self.source_model.setHeaderData(COL_GRID, Qt.Orientation.Horizontal, "Grid")
        
        # Static pre-filtering: Only show entries with an image
        self.source_model.setFilter(f"EQSL_IMAGE_BLOB IS NOT NULL")
        self.source_model.select()

        # 2. Initialize MultiColumnFilterProxyModel
        self.proxy_model = MultiColumnFilterProxyModel(self, searchable_indices=SEARCHABLE_COLUMN_INDICES) 
        self.proxy_model.setSourceModel(self.source_model)
        
        # 3. Set view
        self.ui.tbl_data_view_main.setModel(self.proxy_model)
        self.ui.tbl_data_view_main.setSelectionBehavior(self.ui.tbl_data_view_main.SelectionBehavior.SelectRows)
        self.ui.tbl_data_view_main.setSortingEnabled(True)

        # Hide columns
        total_columns = self.source_model.columnCount()
        visible_indices = set(SEARCHABLE_COLUMN_INDICES + [COL_IMAGE_BLOB]) 

        for col_index in range(total_columns):
            if col_index not in visible_indices or col_index == COL_IMAGE_BLOB:
                self.ui.tbl_data_view_main.setColumnHidden(col_index, True)
            else:
                self.ui.tbl_data_view_main.setColumnHidden(col_index, False)


    def _setup_ui_elements(self):
        """Configures UI elements and loads the default image."""
        # Configure preview label for image display
        self.ui.lb_preview_image_main.setScaledContents(True)
        self.ui.lb_preview_image_main.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # NEW: Load default image
        # NOTE: Adjust this path if your default image is located elsewhere!
        # Example: 'support_data/default_preview.png'
        default_image_path = os.path.join(os.path.dirname(__file__), 'support_data', 'default_preview.png')
        
        if self.default_pixmap.load(default_image_path):
             self._set_default_preview()
        else:
             self.ui.lb_preview_image_main.setText("No image selected. (Default image missing.)")


    def _set_default_preview(self):
        """Helper function to set the scaled default image."""
        if not self.default_pixmap.isNull():
             # Scale image proportionally to fit the label
             scaled_pixmap = self.default_pixmap.scaled(
                 self.ui.lb_preview_image_main.size(),
                 Qt.AspectRatioMode.KeepAspectRatio,
                 Qt.TransformationMode.SmoothTransformation
             )
             self.ui.lb_preview_image_main.setPixmap(scaled_pixmap)
        else:
            self.ui.lb_preview_image_main.setText("No image selected.")


    def _setup_connections(self):
        """Connects UI elements to the GuiManager or local slots."""
        
        # Filtering
        self.ui.btn_search_main.clicked.connect(lambda: self.filter_data_flex(self.ui.txt_search_field_main.text()))
        self.ui.btn_reset_main.clicked.connect(self.reset_filter) # ADJUSTED
        
        # Selection
        self.ui.btn_markall_main.clicked.connect(self.mark_all)
        self.ui.btn_unmarkall_main.clicked.connect(self.unmark_all) # ADJUSTED
        
        # Actions for images
        self.ui.btn_show_image.clicked.connect(self.show_selected_images)
        self.ui.btn_export_image.clicked.connect(self.download_selected_images)
        
        # Preview on selection change
        self.ui.tbl_data_view_main.selectionModel().currentChanged.connect(self.show_preview)
        
        # Menu actions (to GuiManager)
        if hasattr(self.ui, 'actionSettings'):
            self.ui.actionSettings.triggered.connect(self.gui_manager.open_settings)
        # HIER IST DIE KORREKTUR
        if hasattr(self.ui, 'actionSingle_Card_Import'):
            self.ui.actionSingle_Card_Import.triggered.connect(self.gui_manager.open_single_card_import) 
        if hasattr(self.ui, 'actionBulk_Card_Import'):
            self.ui.actionBulk_Card_Import.triggered.connect(self.gui_manager.open_bulk_import)
        if hasattr(self.ui, 'actionManual'):
            self.ui.actionManual.triggered.connect(self.gui_manager.open_help) 
        if hasattr(self.ui, 'actionVersionInfo'):
            self.ui.actionVersionInfo.triggered.connect(self.gui_manager.open_version_info)
        if hasattr(self.ui, 'actionExit'):
            self.ui.actionExit.triggered.connect(self.close)
        if hasattr(self.ui, 'btn_edit'):
            self.ui.btn_edit.clicked.connect(self._handle_edit_qso) # <-- NEU


        # DB path change & data update
        self.settings_manager.db_path_selected.connect(self._handle_db_path_changed)
        self.gui_manager.qso_data_updated.connect(self._refresh_model)


    # ----------------------------------------------------------------------
    # LOCAL SLOTS
    # ----------------------------------------------------------------------
    
    @Slot()
    def filter_data_flex(self, text: str):
        """Passes the search text to the custom proxy model for multi-column OR search."""
        self.proxy_model.setFilterString(text)
        
    @Slot()
    def reset_filter(self):
        """Resets the text field, removes the dynamic filter, AND resets the preview."""
        self.ui.txt_search_field_main.clear()
        self.filter_data_flex("") 
        
        # NEW: Clear selection and set default image
        self.ui.tbl_data_view_main.selectionModel().clearSelection()
        self._set_default_preview()
        
    @Slot()
    def mark_all(self):
        """Selects all currently visible rows."""
        # Clearing the selection at the beginning is necessary because otherwise the selection remains in the SelectionModel
        self.ui.tbl_data_view_main.selectionModel().clearSelection() 
        
        row_count = self.proxy_model.rowCount()
        if row_count > 0:
            top_left = self.proxy_model.index(0, 0)
            bottom_right = self.proxy_model.index(row_count - 1, self.proxy_model.columnCount() - 1)
            
            selection = QItemSelection(top_left, bottom_right)
            self.ui.tbl_data_view_main.selectionModel().select(
                selection, 
                QItemSelectionModel.SelectionFlag.Select
            )

    @Slot()
    def unmark_all(self):
        """Clears the entire selection AND resets the preview."""
        self.ui.tbl_data_view_main.selectionModel().clearSelection()
        # NEW: Set default image after clearing the selection
        self._set_default_preview()


    @Slot(QModelIndex, QModelIndex)
    def show_preview(self, current_index: QModelIndex, previous_index: QModelIndex):
        """Shows the image of the currently selected record or the default image."""
        
        # Important: If current_index is invalid (e.g., after filter reset), set the default
        if not current_index.isValid():
            self._set_default_preview() 
            return

        source_index = self.proxy_model.mapToSource(current_index)
        blob_index = self.source_model.index(source_index.row(), COL_IMAGE_BLOB)
        blob_data = self.source_model.data(blob_index, Qt.ItemDataRole.DisplayRole)

        if isinstance(blob_data, QByteArray) and not blob_data.isEmpty():
            pixmap = QPixmap()
            
            if pixmap.loadFromData(blob_data):
                scaled_pixmap = pixmap.scaled(
                    self.ui.lb_preview_image_main.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.ui.lb_preview_image_main.setPixmap(scaled_pixmap)
            else:
                 # Error loading image format, show default image
                self.ui.lb_preview_image_main.setText("Error loading image format.")
                self._set_default_preview() 
        else:
            # No image available or BLOB empty, show default image
            self._set_default_preview()


    @Slot()
    def show_selected_images(self):
        """Opens the gallery with all selected images."""
        selected_rows = self.ui.tbl_data_view_main.selectionModel().selectedRows()
        
        image_list = []
        for proxy_index in selected_rows:
            source_index = self.proxy_model.mapToSource(proxy_index)
            blob_index = self.source_model.index(source_index.row(), COL_IMAGE_BLOB)
            blob_data = self.source_model.data(blob_index)
            
            if isinstance(blob_data, QByteArray) and not blob_data.isEmpty():
                image_list.append(blob_data)

        if image_list:
            viewer = ImageViewerDialog(image_list, self)
            viewer.exec()
        else:
            QMessageBox.information(self, "No Selection", "Please select records with images.")

    @Slot()
    def download_selected_images(self):
        """Downloads selected images to the folder defined in the settings."""
        
        download_folder = self.settings_manager.get_current_download_dir()
        
        if not download_folder or not os.path.isdir(download_folder):
            QMessageBox.critical(self, "Download Error", 
                                 "The download path is not set or invalid in the settings. Please check the settings.")
            return
        
        file_format = "PNG" 

        selected_rows = self.ui.tbl_data_view_main.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select records to export.")
            return

        success_count = 0
        for proxy_index in selected_rows:
            source_index = self.proxy_model.mapToSource(proxy_index)
            
            # Retrieve data fields for the filename
            call = self.source_model.data(self.source_model.index(source_index.row(), COL_CALL))
            date = self.source_model.data(self.source_model.index(source_index.row(), COL_QSO_DATE))
            time = self.source_model.data(self.source_model.index(source_index.row(), COL_TIME_ON))
            band = self.source_model.data(self.source_model.index(source_index.row(), COL_BAND))
            mode = self.source_model.data(self.source_model.index(source_index.row(), COL_MODE))
            
            # Retrieve image BLOB
            blob_index = self.source_model.index(source_index.row(), COL_IMAGE_BLOB)
            blob_data = self.source_model.data(blob_index)

            if not isinstance(blob_data, QByteArray) or blob_data.isEmpty():
                continue

            # Create and sanitize filename
            filename_base = f"{call}_{date}_{time}_{band}_{mode}"
            safe_filename = re.sub(r'[^\w\-]', '_', str(filename_base)) 
            
            file_path = os.path.join(download_folder, f"{safe_filename}.{file_format.lower()}")

            # Save
            pixmap = QPixmap()
            if pixmap.loadFromData(blob_data):
                success = pixmap.save(file_path, file_format) 
                if success:
                    success_count += 1
            
        QMessageBox.information(self, "Export Completed", 
                                f"{success_count} of {len(selected_rows)} records successfully exported. (Destination: {download_folder})")

    @Slot()
    def _refresh_model(self):
        """Refreshes the data model, e.g., after an import."""
        self.source_model.select()
        print("EqslMainWindow: Data model refreshed after import.")
        QMessageBox.information(self, "Update", "The data view has been successfully refreshed.")

    @Slot()
    def _handle_edit_qso(self):
        """Verarbeitet den Klick auf den 'Edit'-Button, ruft die QSO-Daten ab und öffnet das Importfenster zum Bearbeiten."""
        selection_model = self.ui.tbl_data_view_main.selectionModel()
        selected_indices = selection_model.selectedRows()

        if not selected_indices:
            QMessageBox.warning(self, "Auswahlfehler", "Bitte wählen Sie einen Eintrag in der Tabelle aus, den Sie bearbeiten möchten.")
            return
    
    # Nur die erste ausgewählte Zeile verwenden
        proxy_index = selected_indices[0] 
        source_index = self.proxy_model.mapToSource(proxy_index)
        source_model = self.source_model
    
    # WICHTIG: Die ROWID (interne ID) ist für das Update nötig. Sie ist normalerweise Spalte 0.
        qso_id = source_model.data(source_model.index(source_index.row(), 0), Qt.ItemDataRole.DisplayRole)
        if not qso_id:
            QMessageBox.critical(self, "Fehler", "Konnte die interne Datensatz-ID (ROWID) nicht abrufen.")
            return
        
    # Abrufen der anzuzeigenden Daten
    # Definierte Spaltenindizes aus eqsl_main_prog.py verwenden
        COL_MAP = {
            'callsign': COL_CALL,
            'qso_date': COL_QSO_DATE, # Format: YYYYMMDD
            'band': COL_BAND,
            'mode': COL_MODE,
            }
    
        qso_data = {'rowid': int(qso_id)} # ROWID speichern
    
        for key, col_index in COL_MAP.items():
            data = source_model.data(source_model.index(source_index.row(), col_index), Qt.ItemDataRole.DisplayRole)
            qso_data[key] = str(data) if data is not None else ""
    
    # Öffnet das Importfenster im "Edit"-Modus mit den Daten
        self.gui_manager.open_single_card_import(qso_data=qso_data)    

    @Slot(str)
    def _handle_db_path_changed(self, new_db_path: str):
        """
        Called when the DB path is changed via the settings.
        """
        QMessageBox.information(self, "Database Change", 
                                f"Attempting to change the database connection to: {new_db_path}")
        
        # 1. Close old connection
        if self.db.isOpen():
            self.db.close()
            
        # 2. Change database name in QSqlDatabase object
        self.db.setDatabaseName(new_db_path)
        
        # 3. Open new connection
        if self.db.open():
            # 4. Reinitialize model 
            table_name = self.settings_manager.settings.get("table_name", "eqsl_data")
            
            self.source_model.setTable(table_name)
            self.source_model.setFilter(f"EQSL_IMAGE_BLOB IS NOT NULL")
            self.source_model.select()
            
            self.ui.tbl_data_view_main.setModel(self.proxy_model) 
            
            # Hide columns again.
            total_columns = self.source_model.columnCount()
            visible_indices = set(SEARCHABLE_COLUMN_INDICES + [COL_IMAGE_BLOB])
            
            for col_index in range(total_columns):
                 if col_index not in visible_indices or col_index == COL_IMAGE_BLOB:
                    self.ui.tbl_data_view_main.setColumnHidden(col_index, True)
                 else:
                    self.ui.tbl_data_view_main.setColumnHidden(col_index, False)
                    
            self.setWindowTitle(f"eQSL Program (Main Window) - DB: {os.path.basename(new_db_path)}")
            QMessageBox.information(self, "Database Change", 
                                    "Database connection successfully changed and view updated.")
        else:
            QMessageBox.critical(self, "Database Error", 
                                 f"Could not open new database '{new_db_path}'. Retaining old state if possible.")


# ----------------------------------------------------------------------
# main() Function for program start 
# ----------------------------------------------------------------------

def main():
    """Defined start function for the application and database connection."""
    app = QApplication(sys.argv)
    
    # 1. Initialize Settings Manager and retrieve paths
    try:
        settings_manager = SettingsManager()
    except Exception as e:
        QMessageBox.critical(None, "Startup Error", 
                             f"Could not initialize SettingsManager: {e}")
        sys.exit(1) 
        
    db_path = settings_manager.get_current_db_path() 
    
    # 2. Establish database connection
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(db_path) 
    
    db_ok = True
    if not db_path:
        QMessageBox.critical(None, "Database Error", 
                             "Database path not defined in Settings.json. Please set it in the settings. The application will start without data access.")
        db_ok = False
        
    if db_path and not db.open():
        QMessageBox.critical(None, "Database Error", 
                             f"Could not open database '{db_path}'. Please check the path in the settings. The application will start without data access.")
        db_ok = False
        
    # 3. Instantiate main window with DB connection AND Settings Manager
    main_window = EqslMainWindow(db, settings_manager) 
    
    # 4. Show GUI
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()