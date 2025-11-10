import sys
from PySide6.QtWidgets import QApplication, QMainWindow

# Korrekter relativer Import für Ihre saubere Struktur.
# Die Datei 'eqsl_main_prog.py' und der Ordner 'gui_data' sind auf derselben Ebene.
from .gui_data.frm_main_window_ui import Ui_frm_main_window 

class EqslMainWindow(QMainWindow):
    """
    Klasse zur Initialisierung des Hauptfensters.
    Sie erbt von QMainWindow und bindet die kompilierte UI-Klasse ein.
    """
    def __init__(self):
        super().__init__()
        
        # UI-Klasse instanziieren (das Objekt erstellen)
        self.ui = Ui_frm_main_window()
        
        # UI auf dieses QMainWindow-Objekt anwenden (Fenster wird gezeichnet)
        self.ui.setupUi(self)
        
        self.setWindowTitle("eQSL Programm (Hauptfenster)")

        # Die Verbindungen lassen wir für diesen Test weg
        # self._setup_connections() 

# -----------------------------------------------------------
# ANWENDUNGSSTARTER UND KORREKTE AUSFÜHRUNG
# -----------------------------------------------------------

if __name__ == "__main__":
    # 1. QApplication Instanz erstellen
    app = QApplication(sys.argv)
    
    # 2. Instanz des Hauptfensters erstellen
    window = EqslMainWindow()
    
    # 3. Fenster anzeigen
    window.show()
    
    # 4. Anwendungsschleife starten
    sys.exit(app.exec())