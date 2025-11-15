import sys
# QApplication ist zwingend erforderlich, um das Qt-System zu starten!
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import Slot

# Korrekter relativer Import für die kompilierte Haupt-UI
from .gui_data.frm_main_window_ui import Ui_frm_main_window 

# Importiert den Fenster-Manager aus dem 'scripts' Unterpaket
from .scripts.gui_manager import GuiManager 


class EqslMainWindow(QMainWindow):
    """
    Klasse zur Initialisierung des Hauptfensters.
    """
    def __init__(self):
        super().__init__()
        
        # Instanziierung des GuiManagers. Er verwaltet alle Unterfenster.
        self.gui_manager = GuiManager() 

        # 1. UI-Klasse instanziieren
        self.ui = Ui_frm_main_window()
        
        # 2. UI auf dieses QMainWindow-Objekt anwenden
        self.ui.setupUi(self)
        
        self.setWindowTitle("eQSL Programm (Hauptfenster)")

        # 3. Verbindungen zur Logik einrichten
        self._setup_connections()

    def _setup_connections(self):
        """Verbindet die UI-Elemente (Menü, Buttons) mit dem GuiManager oder lokalen Slots."""
        if hasattr(self.ui, 'btn_exit_program'):
            self.ui.btn_exit_program.clicked.connect(self.close)
        
        # ----------------------------------------------------------------------
        # A) VERBINDUNGEN ZU UNTERFENSTERN (GuiManager)
        # ----------------------------------------------------------------------
        
        if hasattr(self.ui, 'actionSettings'):
            self.ui.actionSettings.triggered.connect(self.gui_manager.open_settings)
            
        if hasattr(self.ui, 'actionSingle_Card_Import'):
            self.ui.actionSingle_Card_Import.triggered.connect(self.gui_manager.open_single_import)

        if hasattr(self.ui, 'actionBulk_Card_Import'):
            self.ui.actionBulk_Card_Import.triggered.connect(self.gui_manager.open_bulk_import)

        if hasattr(self.ui, 'actionManual'):
            self.ui.actionManual.triggered.connect(self.gui_manager.open_help)

        if hasattr(self.ui, 'actionVersionInfo'):
            self.ui.actionVersionInfo.triggered.connect(self.gui_manager.open_version_info)
        
        if hasattr(self.ui, 'actionExit'):
            self.ui.actionExit.triggered.connect(self.close)
            
        # ----------------------------------------------------------------------
        # C) VERBINDUNG FÜR ADIF-IMPORT-ERGEBNISSE
        # ----------------------------------------------------------------------
        self.gui_manager.qso_data_updated.connect(self.handle_qso_update_notification)


        # ----------------------------------------------------------------------
        # B) VERBINDUNGEN ZU LOKALER LOGIK (Hauptfenster)
        # ----------------------------------------------------------------------
        
        if hasattr(self.ui, 'btn_search'):
            self.ui.btn_search.clicked.connect(self.handle_search_qsl)
            
    # ----------------------------------------------------------------------
    # LOKALE SLOTS
    # ----------------------------------------------------------------------
    
    @Slot(int)
    def handle_qso_update_notification(self, new_records: int):
        """
        Slot, der aufgerufen wird, wenn der ADIF-Import beendet ist.
        """
        # Status-Meldung anzeigen
        QMessageBox.information(
            self, 
            "ADIF Import Abgeschlossen", 
            f"Der ADIF-Import ist erfolgreich beendet.\n\nEs wurden {new_records} neue QSOs in die Datenbank eingefügt."
        )
        
        # HIER: Fügen Sie die Logik zum Neuladen/Aktualisieren der Daten im Hauptfenster ein.

    @Slot()
    def handle_search_qsl(self):
        """Logik für die QSL-Suche, die nur das Hauptfenster betrifft."""
        
        if hasattr(self.ui, 'le_callsign'):
            callsign = self.ui.le_callsign.text()
            # Führen Sie hier die eigentliche Suchlogik aus
            pass 
        

def main():
    """Definierte Startfunktion für die Anwendung."""
    app = QApplication(sys.argv)
    main_window = EqslMainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()