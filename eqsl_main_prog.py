import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Slot

# Korrekter relativer Import für die kompilierte Haupt-UI
from .gui_data.frm_main_window_ui import Ui_frm_main_window 

# Importiert den Fenster-Manager aus dem 'scripts' Unterpaket
from .scripts.gui_manager import GuiManager 


class EqslMainWindow(QMainWindow):
    """
    Klasse zur Initialisierung des Hauptfensters.
    Hauptverantwortung: Nur das Hauptfenster anzeigen und die Verbindung zur Logik herstellen.
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
        pass     
        # ----------------------------------------------------------------------
        # A) VERBINDUNGEN ZU UNTERFENSTERN (GuiManager)
        # ----------------------------------------------------------------------
        
        # Verbindung: Datei -> Einstellungen
        # WICHTIG: Ersetze 'actionSettings' durch den exakten objectName aus dem Designer
        if hasattr(self.ui, 'actionSettings'):
            self.ui.actionSettings.triggered.connect(self.gui_manager.open_settings)
            
        # Verbindung: Datei -> Single Card Import
        if hasattr(self.ui, 'actionSingle_Card_Import'):
            self.ui.actionSingle_Card_Import.triggered.connect(self.gui_manager.open_single_import)

        # Verbindung: Datei -> Bulk Card Import
        if hasattr(self.ui, 'actionBulk_Card_Import'):
            self.ui.actionBulk_Card_Import.triggered.connect(self.gui_manager.open_bulk_import)

        # Verbindung: Hilfe -> Manual
        if hasattr(self.ui, 'actionManual'):
            self.ui.actionManual.triggered.connect(self.gui_manager.open_help)

        # Verbindung: Hilfe -> Version Info
        if hasattr(self.ui, 'actionVersionInfo'):
            self.ui.actionVersionInfo.triggered.connect(self.gui_manager.open_version_info)
        
        # Verbindung: Datei -> Beenden
        if hasattr(self.ui, 'actionExit'):
            self.ui.actionExit.triggered.connect(self.close)

        # ----------------------------------------------------------------------
        # B) VERBINDUNGEN ZU LOKALER LOGIK (Hauptfenster)
        # ----------------------------------------------------------------------
        
        # Beispiel: Verbindung des Such-Buttons mit einer lokalen Methode
        if hasattr(self.ui, 'btn_search'):
            self.ui.btn_search.clicked.connect(self.handle_search_qsl)
            
    # ----------------------------------------------------------------------
    # LOKALE SLOTS
    # ----------------------------------------------------------------------
    
    @Slot()
    def handle_search_qsl(self):
        """Logik für die QSL-Suche, die nur das Hauptfenster betrifft."""
        
        if hasattr(self.ui, 'le_callsign'):
            callsign = self.ui.le_callsign.text()
            print(f"Suche gestartet für Callsign: {callsign}")
        


if __name__ == "__main__":
    # 1. QApplication Instanz erstellen
    app = QApplication(sys.argv)
    
    # 2. Instanz des Hauptfensters erstellen
    window1 = EqslMainWindow()
    
    # 3. Fenster anzeigen
    window1.show()
    
    # 4. Anwendungsschleife starten
    sys.exit(app.exec())