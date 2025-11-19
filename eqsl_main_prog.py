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

# Definition der Spalten-Indizes (0-basiert, basierend auf der 31er Liste)
COL_CALL = 0
COL_QSO_DATE = 1
COL_TIME_ON = 2
COL_BAND = 3
COL_MODE = 4
COL_IMAGE_BLOB = 28 # EQSL_IMAGE_BLOB ist die 29. Spalte -> Index 28

class EqslMainWindow(QMainWindow):
    
    # Konstruktor akzeptiert DB und SettingsManager
    def __init__(self, db_conn: QSqlDatabase, settings_manager: SettingsManager): 
        super().__init__()
        
        self.db = db_conn
        self.settings_manager = settings_manager 
        
        # 1. KORREKTUR: Instanziierung des GuiManagers MUSS mit seinen Abhängigkeiten 
        # UND dem Hauptfenster (self) erfolgen!
        self.gui_manager = GuiManager(
            db_conn=self.db, 
            settings_manager=self.settings_manager,
            main_window=self # <--- KRITISCHE ÄNDERUNG: Übergabe des Hauptfensters
        ) 

        # 2. UI-Klasse instanziieren und anwenden
        self.ui = Ui_frm_main_window()
        self.ui.setupUi(self)
        self.setWindowTitle("eQSL Programm (Hauptfenster)")

        # 3. NEU: Models und UI-Elemente initialisieren
        self._setup_models()
        self._setup_ui_elements()
       
        # 4. Verbindungen zur Logik einrichten
        self._setup_connections()

    def _setup_models(self):
        table_name = self.settings_manager.settings.get("table_name", "eqsl_data")
        
        # 1. QSqlTableModel initialisieren
        self.source_model = QSqlTableModel(db=self.db)
        self.source_model.setTable(table_name)
        self.source_model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        
        # Statische Vorfilterung: Nur Einträge mit einem Bild anzeigen
        self.source_model.setFilter(f"EQSL_IMAGE_BLOB IS NOT NULL")
        self.source_model.select()

        # 2. QSortFilterProxyModel initialisieren
        self.proxy_model = QSortFilterProxyModel(self)
        self.proxy_model.setSourceModel(self.source_model)
        self.proxy_model.setFilterKeyColumn(COL_CALL) 
        
        # 3. View setzen
        self.ui.tbl_data_view_main.setModel(self.proxy_model)
        self.ui.tbl_data_view_main.setSelectionBehavior(self.ui.tbl_data_view_main.SelectionBehavior.SelectRows)
        self.ui.tbl_data_view_main.setSortingEnabled(True)

    def _setup_ui_elements(self):
        # Preview Label für die Bildanzeige konfigurieren
        self.ui.lb_preview_image_main.setScaledContents(True)
        self.ui.lb_preview_image_main.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ui.lb_preview_image_main.setText("Wählen Sie eine Zeile, um die Bildvorschau zu sehen.")

    def _setup_connections(self):
        """Verbindet die UI-Elemente mit dem GuiManager oder lokalen Slots (inkl. neuer Logik)."""
        
        # ----------------------------------------------------------------------
        # A) LOKALE AKTIONEN (Filterung, Markierung, Export)
        # ----------------------------------------------------------------------
        
        # Filterung
        self.ui.btn_search_main.clicked.connect(lambda: self.filter_data_flex(self.ui.txt_search_field_main.text()))
        self.ui.btn_reset_main.clicked.connect(self.reset_filter)

        # Selektion
        self.ui.btn_markall_main.clicked.connect(self.mark_all)
        self.ui.btn_unmarkall_main.clicked.connect(self.unmark_all)
        
        # Aktionen für Bilder
        self.ui.btn_show_image.clicked.connect(self.show_selected_images)
        self.ui.btn_export_image.clicked.connect(self.download_selected_images)
        
        # Vorschau bei Auswahländerung
        self.ui.tbl_data_view_main.selectionModel().currentChanged.connect(self.show_preview)
        
        # ----------------------------------------------------------------------
        # B) KRITISCHE AKTIONEN (Menü-Bar) ZUM GuiManager
        # ----------------------------------------------------------------------
        
        # Settings
        if hasattr(self.ui, 'actionSettings'):
            self.ui.actionSettings.triggered.connect(self.gui_manager.open_settings)
            
        # Single Card Import
        if hasattr(self.ui, 'actionSingle_Card_Import'):
            self.ui.actionSingle_Card_Import.triggered.connect(self.gui_manager.open_single_import)
            
        # Bulk Import
        if hasattr(self.ui, 'actionBulk_Card_Import'):
            self.ui.actionBulk_Card_Import.triggered.connect(self.gui_manager.open_bulk_import)
            
        # Hilfe
        if hasattr(self.ui, 'actionManual'):
            self.ui.actionManual.triggered.connect(self.gui_manager.open_help) 
            
        # Version
        if hasattr(self.ui, 'actionVersion_Info'):
            self.ui.actionVersion_Info.triggered.connect(self.gui_manager.open_version_info)
        
        # Exit (Annahme: actionExit existiert)
        if hasattr(self.ui, 'actionExit'):
            self.ui.actionExit.triggered.connect(self.close)

        # ----------------------------------------------------------------------
        # C) NEUE KRITISCHE VERBINDUNG: DB-PFAD-ÄNDERUNG
        # ----------------------------------------------------------------------
        
        # **WICHTIG:** Wenn der DB-Pfad in den Settings geändert wird, muss 
        # das Hauptfenster darauf reagieren.
        self.settings_manager.db_path_selected.connect(self._handle_db_path_changed)

        # Zusätzlich das Signal des GuiManagers für Datenaktualisierung verbinden
        self.gui_manager.qso_data_updated.connect(self._refresh_model)



    # ----------------------------------------------------------------------
    # LOKALE SLOTS (Unverändert)
    # ----------------------------------------------------------------------
 
    @Slot()
    def filter_data_flex(self, text: str):
        """Implementiert UND/ODER-Filterlogik mittels regulärer Ausdrücke."""
        terms = [term.strip() for term in text.split() if term.strip()]
        
        if not terms:
            regex = ""
        else:
            # Erstellt einen Lookahead-Ausdruck für UND-Logik: (?=.*Begriff1)(?=.*Begriff2)...
            lookaheads = "".join(f"(?=.*{re.escape(term)})" for term in terms)
            regex = lookaheads
        
        self.proxy_model.setFilterRegularExpression(regex)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        
    @Slot()
    def reset_filter(self):
        """Setzt das Textfeld zurück und entfernt den dynamischen Filter."""
        self.ui.txt_search_field_main.clear()
        self.filter_data_flex("") 
        
    @Slot()
    def mark_all(self):
        """Wählt alle aktuell sichtbaren Zeilen aus."""
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
        """Hebt die gesamte Auswahl auf."""
        self.ui.tbl_data_view_main.selectionModel().clearSelection()

    @Slot(QModelIndex, QModelIndex)
    def show_preview(self, current_index: QModelIndex, previous_index: QModelIndex):
        """Zeigt das Bild des aktuell ausgewählten Datensatzes in der Vorschau an."""
        if not current_index.isValid():
            self.ui.lb_preview_image_main.clear()
            self.ui.lb_preview_image_main.setText("Kein Bild ausgewählt.")
            return

        source_index = self.proxy_model.mapToSource(current_index)
        
        # Daten abrufen (Spalte 28 EQSL_IMAGE_BLOB)
        blob_index = self.source_model.index(source_index.row(), COL_IMAGE_BLOB)
        blob_data = self.source_model.data(blob_index) 

        if isinstance(blob_data, QByteArray) and not blob_data.isEmpty():
            pixmap = QPixmap()
            if pixmap.loadFromData(blob_data):
                self.ui.lb_preview_image_main.setPixmap(pixmap)
            else:
                self.ui.lb_preview_image_main.setText("Fehler beim Laden des Bildformats.")
        else:
            self.ui.lb_preview_image_main.clear()
            self.ui.lb_preview_image_main.setText("Kein Bild vorhanden.")

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
        
        # 1. Download-Pfad aus den Settings holen
        download_folder = self.settings_manager.get_current_download_dir()
        
        # 2. Prüfen, ob der Download-Pfad gesetzt und gültig ist
        if not download_folder or not os.path.isdir(download_folder):
            QMessageBox.critical(self, "Download-Fehler", 
                                 "Der Download-Pfad ist in den Settings nicht gesetzt oder ungültig. Bitte prüfen Sie die Einstellungen.")
            return
        
        # ANNAHME: Das Exportformat muss fest im Code oder in den Settings definiert sein.
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
            
            # Pfad mit os.path.join() erstellen (besser für OS-Kompatibilität)
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
        # WICHTIG: select() muss aufgerufen werden, damit das QSqlTableModel die DB neu abfragt.
        self.source_model.select()
        print("EqslMainWindow: Datenmodell nach Import aktualisiert.")
        QMessageBox.information(self, "Aktualisierung", "Die Datenansicht wurde erfolgreich aktualisiert.")


    @Slot(str)
    def _handle_db_path_changed(self, new_db_path: str):
        """
        **NEUER SLOT:** Wird aufgerufen, wenn der DB-Pfad über die Settings geändert wird.
        Schließt die alte Verbindung und versucht, die neue zu öffnen.
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
            # 4. Modell neu initialisieren (muss mit neuer DB-Verbindung arbeiten)
            # Das QSqlTableModel muss neu initialisiert oder zumindest neu selektiert werden
            table_name = self.settings_manager.settings.get("table_name", "eqsl_data")
            
            # Da self.db ein Singleton ist, sollte ein einfaches select() funktionieren,
            # aber zur Sicherheit initialisieren wir das Model neu.
            
            self.source_model.setTable(table_name)
            self.source_model.setFilter(f"EQSL_IMAGE_BLOB IS NOT NULL")
            self.source_model.select()
            
            self.ui.tbl_data_view_main.setModel(self.proxy_model) # View muss das ProxyModel wieder erhalten
            self.setWindowTitle(f"eQSL Programm (Hauptfenster) - DB: {os.path.basename(new_db_path)}")
            QMessageBox.information(self, "Datenbankwechsel", 
                                    "Datenbankverbindung erfolgreich gewechselt und Ansicht aktualisiert.")
        else:
            QMessageBox.critical(self, "Datenbankfehler", 
                                 f"Konnte neue Datenbank '{new_db_path}' nicht öffnen. Behalte alten Zustand bei (falls möglich).")
            # Fehlerbehandlung: Wenn möglich, müsste hier die alte Verbindung wiederhergestellt werden.
            # Da das kritisch ist, ist es besser, den Fehler zu melden.




# ----------------------------------------------------------------------
# main() Funktion für den Programmstart (Unverändert)
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
    
    if not db_path:
        QMessageBox.critical(None, "Datenbankfehler", 
                             "Datenbankpfad in Settings.json nicht definiert. Bitte in den Settings festlegen.")
        sys.exit(1)

    # 2. Datenbankverbindung herstellen
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(db_path) 
    
    if not db.open():
        QMessageBox.critical(None, "Datenbankfehler", 
                             f"Konnte Datenbank '{db_path}' nicht öffnen. Beende Programm.")
        sys.exit(1)

    # 3. Hauptfenster mit DB-Verbindung UND Settings Manager instanziieren
    main_window = EqslMainWindow(db, settings_manager) 
    
    # 4. GUI anzeigen
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()