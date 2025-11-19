import sys
import os
import re 
from PySide6.QtWidgets import (QApplication, QMainWindow, QMessageBox, QFileDialog)
from PySide6.QtCore import (Slot, QSortFilterProxyModel, QItemSelection, QItemSelectionModel, 
                            QModelIndex, Qt, QByteArray, QDir)
from PySide6.QtSql import QSqlDatabase, QSqlTableModel
from PySide6.QtGui import QPixmap 

# Korrekte Imports (basierend auf Ihrer Struktur)
from .gui_data.frm_main_window_ui import Ui_frm_main_window 
from .scripts.gui_manager import GuiManager 
from .scripts.settings_manager import SettingsManager 
from .scripts.image_viewer_dialog import ImageViewerDialog 

# Definition der Spalten-Indizes (0-basiert)
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

# Liste der durchsuchbaren Spalten
SEARCHABLE_COLUMN_INDICES = [
    COL_CALL, COL_QSO_DATE, COL_TIME_ON, COL_BAND, COL_MODE, 
    COL_SUB_MODE, COL_COUNTRY, COL_FREQ, COL_CQZ, COL_ITUZ, COL_GRID
]


# ======================================================================
# Benutzerdefiniertes Proxy-Modell für Multi-Spalten-ODER-Filterung
# ======================================================================
class MultiColumnFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None, searchable_indices=None):
        super().__init__(parent)
        self.search_terms = []
        self.searchable_indices = searchable_indices if searchable_indices is not None else []

    def setFilterString(self, text: str):
        """
        Setzt den Suchtext. Leerzeichen dienen nun als ODER-Trenner.
        """
        # Teilt den Text in Begriffe auf und konvertiert in Kleinbuchstaben
        self.search_terms = [term.strip().lower() for term in text.split() if term.strip()]
        # Filterung neu starten
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        """
        Implementiert die ODER-Logik: Zeile wird akzeptiert, wenn EINER der Suchbegriffe 
        in EINER der definierten Spalten gefunden wird.
        """
        if not self.search_terms:
            return True 

        source_model = self.sourceModel()
        
        # ODER-Logik
        for term in self.search_terms:
            for col_index in self.searchable_indices:
                index = source_model.index(source_row, col_index, source_parent)
                data = source_model.data(index, Qt.ItemDataRole.DisplayRole)
                
                if data is None:
                    continue
                
                try:
                    data_str = str(data).lower()
                    if term in data_str:
                        # Begriff gefunden => Zeile akzeptieren (ODER-Bedingung erfüllt)
                        return True 
                except:
                    continue

        # Keiner der Suchbegriffe wurde gefunden => Zeile ablehnen
        return False


# ======================================================================
# EqslMainWindow
# ======================================================================
class EqslMainWindow(QMainWindow):
    
    def __init__(self, db_conn: QSqlDatabase, settings_manager: SettingsManager): 
        super().__init__()
        
        self.db = db_conn
        self.settings_manager = settings_manager 
        
        # NEU: Speichervariable für die Standard-Pixmap
        self.default_pixmap = QPixmap() 
        
        self.gui_manager = GuiManager(
            db_conn=self.db, 
            settings_manager=self.settings_manager,
            main_window=self 
        ) 

        self.ui = Ui_frm_main_window()
        self.ui.setupUi(self)
        self.setWindowTitle("eQSL Programm (Hauptfenster)")

        self._setup_models()
        self._setup_ui_elements()
        
        self._setup_connections()

    def _setup_models(self):
        table_name = self.settings_manager.settings.get("table_name", "eqsl_data")
        
        # 1. QSqlTableModel initialisieren
        self.source_model = QSqlTableModel(db=self.db)
        self.source_model.setTable(table_name)
        self.source_model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        
        # Spaltenüberschriften setzen
        self.source_model.setHeaderData(COL_CALL, Qt.Orientation.Horizontal, "Call")
        self.source_model.setHeaderData(COL_QSO_DATE, Qt.Orientation.Horizontal, "Date")
        self.source_model.setHeaderData(COL_TIME_ON, Qt.Orientation.Horizontal, "Time")
        self.source_model.setHeaderData(COL_BAND, Qt.Orientation.Horizontal, "Band")
        self.source_model.setHeaderData(COL_MODE, Qt.Orientation.Horizontal, "Mode")
        self.source_model.setHeaderData(COL_FREQ, Qt.Orientation.Horizontal, "Frequenz")
        self.source_model.setHeaderData(COL_ITUZ, Qt.Orientation.Horizontal, "ITU Zone")
        self.source_model.setHeaderData(COL_CQZ, Qt.Orientation.Horizontal, "CQ Zone")
        self.source_model.setHeaderData(COL_GRID, Qt.Orientation.Horizontal, "Grid")
        
        # Statische Vorfilterung: Nur Einträge mit einem Bild anzeigen
        self.source_model.setFilter(f"EQSL_IMAGE_BLOB IS NOT NULL")
        self.source_model.select()

        # 2. MultiColumnFilterProxyModel initialisieren
        self.proxy_model = MultiColumnFilterProxyModel(self, searchable_indices=SEARCHABLE_COLUMN_INDICES) 
        self.proxy_model.setSourceModel(self.source_model)
        
        # 3. View setzen
        self.ui.tbl_data_view_main.setModel(self.proxy_model)
        self.ui.tbl_data_view_main.setSelectionBehavior(self.ui.tbl_data_view_main.SelectionBehavior.SelectRows)
        self.ui.tbl_data_view_main.setSortingEnabled(True)

        # Spalten ausblenden
        total_columns = self.source_model.columnCount()
        visible_indices = set(SEARCHABLE_COLUMN_INDICES + [COL_IMAGE_BLOB]) 

        for col_index in range(total_columns):
            if col_index not in visible_indices or col_index == COL_IMAGE_BLOB:
                self.ui.tbl_data_view_main.setColumnHidden(col_index, True)
            else:
                self.ui.tbl_data_view_main.setColumnHidden(col_index, False)


    def _setup_ui_elements(self):
        """Konfiguriert UI-Elemente und lädt das Standardbild."""
        # Preview Label für die Bildanzeige konfigurieren
        self.ui.lb_preview_image_main.setScaledContents(True)
        self.ui.lb_preview_image_main.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # NEU: Standardbild laden
        # HINWEIS: Passen Sie diesen Pfad an, falls Ihr Standardbild woanders liegt!
        # Beispiel: 'support_data/default_preview.png'
        default_image_path = os.path.join(os.path.dirname(__file__), 'support_data', 'default_preview.png')
        
        if self.default_pixmap.load(default_image_path):
             self._set_default_preview()
        else:
             self.ui.lb_preview_image_main.setText("Kein Bild ausgewählt. (Default-Bild fehlt.)")


    def _set_default_preview(self):
        """Hilfsfunktion, um das skalierte Standardbild zu setzen."""
        if not self.default_pixmap.isNull():
             # Bild proportional skalieren, um in das Label zu passen
             scaled_pixmap = self.default_pixmap.scaled(
                 self.ui.lb_preview_image_main.size(),
                 Qt.AspectRatioMode.KeepAspectRatio,
                 Qt.TransformationMode.SmoothTransformation
             )
             self.ui.lb_preview_image_main.setPixmap(scaled_pixmap)
        else:
            self.ui.lb_preview_image_main.setText("Kein Bild ausgewählt.")


    def _setup_connections(self):
        """Verbindet die UI-Elemente mit dem GuiManager oder lokalen Slots."""
        
        # Filterung
        self.ui.btn_search_main.clicked.connect(lambda: self.filter_data_flex(self.ui.txt_search_field_main.text()))
        self.ui.btn_reset_main.clicked.connect(self.reset_filter) # ANGEPASST
        
        # Selektion
        self.ui.btn_markall_main.clicked.connect(self.mark_all)
        self.ui.btn_unmarkall_main.clicked.connect(self.unmark_all) # ANGEPASST
        
        # Aktionen für Bilder
        self.ui.btn_show_image.clicked.connect(self.show_selected_images)
        self.ui.btn_export_image.clicked.connect(self.download_selected_images)
        
        # Vorschau bei Auswahländerung
        self.ui.tbl_data_view_main.selectionModel().currentChanged.connect(self.show_preview)
        
        # Menü-Aktionen (zum GuiManager)
        if hasattr(self.ui, 'actionSettings'):
            self.ui.actionSettings.triggered.connect(self.gui_manager.open_settings)
        if hasattr(self.ui, 'actionSingle_Card_Import'):
            self.ui.actionSingle_Card_Import.triggered.connect(self.gui_manager.open_single_import)
        if hasattr(self.ui, 'actionBulk_Card_Import'):
            self.ui.actionBulk_Card_Import.triggered.connect(self.gui_manager.open_bulk_import)
        if hasattr(self.ui, 'actionManual'):
            self.ui.actionManual.triggered.connect(self.gui_manager.open_help) 
        if hasattr(self.ui, 'actionVersion_Info'):
            self.ui.actionVersion_Info.triggered.connect(self.gui_manager.open_version_info)
        if hasattr(self.ui, 'actionExit'):
            self.ui.actionExit.triggered.connect(self.close)

        # DB-Pfad-Änderung & Datenaktualisierung
        self.settings_manager.db_path_selected.connect(self._handle_db_path_changed)
        self.gui_manager.qso_data_updated.connect(self._refresh_model)


    # ----------------------------------------------------------------------
    # LOKALE SLOTS
    # ----------------------------------------------------------------------
    
    @Slot()
    def filter_data_flex(self, text: str):
        """Übergibt den Suchtext an das benutzerdefinierte Proxy-Modell zur Multi-Spalten-ODER-Suche."""
        self.proxy_model.setFilterString(text)
        
    @Slot()
    def reset_filter(self):
        """Setzt das Textfeld zurück, entfernt den dynamischen Filter UND setzt die Vorschau zurück."""
        self.ui.txt_search_field_main.clear()
        self.filter_data_flex("") 
        
        # NEU: Auswahl löschen und Default-Bild setzen
        self.ui.tbl_data_view_main.selectionModel().clearSelection()
        self._set_default_preview()
        
    @Slot()
    def mark_all(self):
        """Wählt alle aktuell sichtbaren Zeilen aus."""
        # Das Löschen der Auswahl ist am Anfang nötig, da sonst die Auswahl im SelectionModel bestehen bleibt
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
        """Hebt die gesamte Auswahl auf UND setzt die Vorschau zurück."""
        self.ui.tbl_data_view_main.selectionModel().clearSelection()
        # NEU: Default-Bild setzen, nachdem die Auswahl aufgehoben wurde
        self._set_default_preview()


    @Slot(QModelIndex, QModelIndex)
    def show_preview(self, current_index: QModelIndex, previous_index: QModelIndex):
        """Zeigt das Bild des aktuell ausgewählten Datensatzes oder das Standardbild an."""
        
        # Wichtig: Wenn current_index ungültig ist (z.B. nach Filter-Reset), wird der Default gesetzt
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
                 # Fehler beim Laden des Bildformats, zeige Standardbild
                self.ui.lb_preview_image_main.setText("Fehler beim Laden des Bildformats.")
                self._set_default_preview() 
        else:
            # Kein Bild vorhanden oder BLOB leer, zeige Standardbild
            self._set_default_preview()


    @Slot()
    def show_selected_images(self):
        """Öffnet die Galerie mit allen markierten Bildern."""
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
            QMessageBox.information(self, "Keine Auswahl", "Bitte markieren Sie Datensätze mit Bildern.")

    @Slot()
    def download_selected_images(self):
        """Lädt ausgewählte Bilder in den Settings-definierten Ordner herunter."""
        
        download_folder = self.settings_manager.get_current_download_dir()
        
        if not download_folder or not os.path.isdir(download_folder):
            QMessageBox.critical(self, "Download-Fehler", 
                                 "Der Download-Pfad ist in den Settings nicht gesetzt oder ungültig. Bitte prüfen Sie die Einstellungen.")
            return
        
        file_format = "PNG" 

        selected_rows = self.ui.tbl_data_view_main.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Keine Auswahl", "Bitte markieren Sie Datensätze zum Export.")
            return

        success_count = 0
        for proxy_index in selected_rows:
            source_index = self.proxy_model.mapToSource(proxy_index)
            
            # Datenfelder für den Dateinamen abrufen
            call = self.source_model.data(self.source_model.index(source_index.row(), COL_CALL))
            date = self.source_model.data(self.source_model.index(source_index.row(), COL_QSO_DATE))
            time = self.source_model.data(self.source_model.index(source_index.row(), COL_TIME_ON))
            band = self.source_model.data(self.source_model.index(source_index.row(), COL_BAND))
            mode = self.source_model.data(self.source_model.index(source_index.row(), COL_MODE))
            
            # Bild-BLOB abrufen
            blob_index = self.source_model.index(source_index.row(), COL_IMAGE_BLOB)
            blob_data = self.source_model.data(blob_index)

            if not isinstance(blob_data, QByteArray) or blob_data.isEmpty():
                continue

            # Dateinamen erstellen und bereinigen
            filename_base = f"{call}_{date}_{time}_{band}_{mode}"
            safe_filename = re.sub(r'[^\w\-]', '_', str(filename_base)) 
            
            file_path = os.path.join(download_folder, f"{safe_filename}.{file_format.lower()}")

            # Speichern
            pixmap = QPixmap()
            if pixmap.loadFromData(blob_data):
                success = pixmap.save(file_path, file_format) 
                if success:
                    success_count += 1
            
        QMessageBox.information(self, "Export Abgeschlossen", 
                                f"{success_count} von {len(selected_rows)} Datensätzen erfolgreich exportiert. (Ziel: {download_folder})")

    @Slot()
    def _refresh_model(self):
        """Aktualisiert das Datenmodell, z.B. nach einem Import."""
        self.source_model.select()
        print("EqslMainWindow: Datenmodell nach Import aktualisiert.")
        QMessageBox.information(self, "Aktualisierung", "Die Datenansicht wurde erfolgreich aktualisiert.")


    @Slot(str)
    def _handle_db_path_changed(self, new_db_path: str):
        """
        Wird aufgerufen, wenn der DB-Pfad über die Settings geändert wird.
        """
        QMessageBox.information(self, "Datenbankwechsel", 
                                f"Versuche, die Datenbankverbindung zu wechseln: {new_db_path}")
        
        # 1. Alte Verbindung schließen
        if self.db.isOpen():
            self.db.close()
            
        # 2. Datenbanknamen im QSqlDatabase-Objekt ändern
        self.db.setDatabaseName(new_db_path)
        
        # 3. Neue Verbindung öffnen
        if self.db.open():
            # 4. Modell neu initialisieren 
            table_name = self.settings_manager.settings.get("table_name", "eqsl_data")
            
            self.source_model.setTable(table_name)
            self.source_model.setFilter(f"EQSL_IMAGE_BLOB IS NOT NULL")
            self.source_model.select()
            
            self.ui.tbl_data_view_main.setModel(self.proxy_model) 
            
            # Spalten erneut ausblenden.
            total_columns = self.source_model.columnCount()
            visible_indices = set(SEARCHABLE_COLUMN_INDICES + [COL_IMAGE_BLOB])
            
            for col_index in range(total_columns):
                 if col_index not in visible_indices or col_index == COL_IMAGE_BLOB:
                    self.ui.tbl_data_view_main.setColumnHidden(col_index, True)
                 else:
                    self.ui.tbl_data_view_main.setColumnHidden(col_index, False)
                    
            self.setWindowTitle(f"eQSL Programm (Hauptfenster) - DB: {os.path.basename(new_db_path)}")
            QMessageBox.information(self, "Datenbankwechsel", 
                                    "Datenbankverbindung erfolgreich gewechselt und Ansicht aktualisiert.")
        else:
            QMessageBox.critical(self, "Datenbankfehler", 
                                 f"Konnte neue Datenbank '{new_db_path}' nicht öffnen. Behalte alten Zustand bei (falls möglich).")


# ----------------------------------------------------------------------
# main() Funktion für den Programmstart 
# ----------------------------------------------------------------------

def main():
    """Definierte Startfunktion für die Anwendung und Datenbankverbindung."""
    app = QApplication(sys.argv)
    
    # 1. Settings Manager initialisieren und Pfade abrufen
    try:
        settings_manager = SettingsManager()
    except Exception as e:
        QMessageBox.critical(None, "Startfehler", 
                             f"Konnte SettingsManager nicht initialisieren: {e}")
        sys.exit(1) 
        
    db_path = settings_manager.get_current_db_path() 
    
    # 2. Datenbankverbindung herstellen
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(db_path) 
    
    db_ok = True
    if not db_path:
        QMessageBox.critical(None, "Datenbankfehler", 
                             "Datenbankpfad in Settings.json nicht definiert. Bitte in den Settings festlegen. Die Anwendung startet ohne Datenzugriff.")
        db_ok = False
        
    if db_path and not db.open():
        QMessageBox.critical(None, "Datenbankfehler", 
                             f"Konnte Datenbank '{db_path}' nicht öffnen. Bitte überprüfen Sie den Pfad in den Settings. Die Anwendung startet ohne Datenzugriff.")
        db_ok = False
        
    # 3. Hauptfenster mit DB-Verbindung UND Settings Manager instanziieren
    main_window = EqslMainWindow(db, settings_manager) 
    
    # 4. GUI anzeigen
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()