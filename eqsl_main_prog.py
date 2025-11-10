import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import Slot

# Korrekter relativer Import für Ihre saubere Struktur.
from .gui_data.frm_main_window_ui import Ui_frm_main_window 
from .gui_data.frm_settings_ui import Ui_frm_settings


class EqslSettingsWindow(QMainWindow):
    """
    Klasse zur Initialisierung des Einstellungsfensters.
    Sie erbt von QMainWindow und bindet die kompilierte UI-Klasse ein.
    """
    def __init__(self):
        super().__init__()
        
        # 1. UI-Klasse instanziieren
        self.ui = Ui_frm_settings()
        
        # 2. UI auf dieses QMainWindow-Objekt anwenden
        self.ui.setupUi(self)
        
        self.setWindowTitle("eQSL Programm (Einstellungen)")

        # Logik für das Einstellungsfenster kann hier hinzugefügt werden
        self._setup_connections()

    def _setup_connections(self):
        # Beispiel: Wenn Sie einen Schließen-Button im Settings-Fenster hätten
        # self.ui.btn_close.clicked.connect(self.close)
        pass





class EqslMainWindow(QMainWindow):
    """
    Klasse zur Initialisierung des Hauptfensters.
    Sie erbt von QMainWindow und bindet die kompilierte UI-Klasse ein.
    """
    def __init__(self):
        super().__init__()
        
        # Attribute zur Speicherung von Unterfenstern (verhindert Garbage Collection)
        self.settings_window = None 
        
        # 1. UI-Klasse instanziieren
        self.ui = Ui_frm_main_window()
        
        # 2. UI auf dieses QMainWindow-Objekt anwenden
        self.ui.setupUi(self)
        
        self.setWindowTitle("eQSL Programm (Hauptfenster)")

        # 3. Verbindungen zur Logik einrichten
        self._setup_connections()

    def _setup_connections(self):
        """Verbindet die UI-Elemente (Signale) mit den Methoden (Slots)."""
        # Annahme: Im Designer gibt es eine QAction namens 'actionSettings'
        if self.ui.actionSettings:
            self.ui.actionSettings.triggered.connect(self.open_settings_window)
        
        # Beispiel für einen Exit-Button
        # self.ui.actionExit.triggered.connect(self.close)

    @Slot()
    def open_settings_window(self):
        """Öffnet das Einstellungsfenster als separates QMainWindow."""
        
        if self.settings_window is None:
            # Erstellt die Instanz nur, wenn sie noch nicht existiert
            self.settings_window = EqslSettingsWindow()
        
        # Zeigt das Fenster an und bringt es in den Vordergrund
        self.settings_window.show()


if __name__ == "__main__":
    # 1. QApplication Instanz erstellen
    app = QApplication(sys.argv)
    
    # 2. Instanz des Hauptfensters erstellen
    window1 = EqslMainWindow()
    
    # 3. Fenster anzeigen
    window1.show()
    
    # 4. Anwendungsschleife starten
    sys.exit(app.exec())