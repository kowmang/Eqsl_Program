import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox

# Korrekter relativer Import für Ihre saubere Struktur.
# Die Datei 'eqsl_main_prog.py' und der Ordner 'gui_data' sind auf derselben Ebene.
from .gui_data.frm_main_window_ui import Ui_frm_main_window 
from .gui_data.frm_sql_create_ui import Ui_frm_sql_create
from .gui_data.frm_settings_ui import Ui_frm_settings
from .gui_data.frm_upload_ui import Ui_frm_upload
from .gui_data.frm_image_view_ui import Ui_frm_image_view
from .gui_data.frm_help_view_ui import Ui_frm_help_view
from .gui_data.frm_version_ui import Ui_frm_version


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
#-----------------------------------------------------------
# Test der anderen Fensterklassen

class EqslSqlCreateWindow(QMainWindow):
    """
    Klasse zur Initialisierung des SQL-Erstellungsfensters.
    Sie erbt von QMainWindow und bindet die kompilierte UI-Klasse ein.
    """
    def __init__(self):
        super().__init__()
        
        # UI-Klasse instanziieren (das Objekt erstellen)
        self.ui = Ui_frm_sql_create()
        
        # UI auf dieses QMainWindow-Objekt anwenden (Fenster wird gezeichnet)
        self.ui.setupUi(self)
        
        self.setWindowTitle("eQSL Programm (SQL-Erstellungsfenster)")


class EqslSettingsWindow(QMainWindow):
    """
    Klasse zur Initialisierung des Einstellungsfensters.
    Sie erbt von QMainWindow und bindet die kompilierte UI-Klasse ein.
    """
    def __init__(self):
        super().__init__()
        
        # UI-Klasse instanziieren (das Objekt erstellen)
        self.ui = Ui_frm_settings()
        
        # UI auf dieses QMainWindow-Objekt anwenden (Fenster wird gezeichnet)
        self.ui.setupUi(self)
        
        self.setWindowTitle("eQSL Programm (Einstellungsfenster)")


class EqslUploadWindow(QMainWindow):
    """
    Klasse zur Initialisierung des Upload-Fensters.
    Sie erbt von QMainWindow und bindet die kompilierte UI-Klasse ein.
    """
    def __init__(self):
        super().__init__()
        
        # UI-Klasse instanziieren (das Objekt erstellen)
        self.ui = Ui_frm_upload()
        
        # UI auf dieses QMainWindow-Objekt anwenden (Fenster wird gezeichnet)
        self.ui.setupUi(self)
        
        self.setWindowTitle("eQSL Programm (Upload-Fenster)")


class EqslImageViewWindow(QWidget):     
    """
    Klasse zur Initialisierung des Bildbetrachter-Fensters.
    Sie erbt von QMainWindow und bindet die kompilierte UI-Klasse ein.
    """
    def __init__(self):
        super().__init__()
        
        # UI-Klasse instanziieren (das Objekt erstellen)
        self.ui = Ui_frm_image_view()
        
        # UI auf dieses QMainWindow-Objekt anwenden (Fenster wird gezeichnet)
        self.ui.setupUi(self)
        
        self.setWindowTitle("eQSL Programm (Bildbetrachter-Fenster)")

class EqslHelpViewWindow(QWidget):     
    """
    Klasse zur Initialisierung des Hilfefensters.
    Sie erbt von QMainWindow und bindet die kompilierte UI-Klasse ein.
    """
    def __init__(self):
        super().__init__()
        
        # UI-Klasse instanziieren (das Objekt erstellen)
        self.ui = Ui_frm_help_view()
        
        # UI auf dieses QMainWindow-Objekt anwenden (Fenster wird gezeichnet)
        self.ui.setupUi(self)
        
        self.setWindowTitle("eQSL Programm (Hilfefenster)")

class EqslVersionWindow(QWidget):     
    """
    Klasse zur Initialisierung des Versionsfensters.
    Sie erbt von QMainWindow und bindet die kompilierte UI-Klasse ein.
    """
    def __init__(self):
        super().__init__()
        
        # UI-Klasse instanziieren (das Objekt erstellen)
        self.ui = Ui_frm_version()
        
        # UI auf dieses QMainWindow-Objekt anwenden (Fenster wird gezeichnet)
        self.ui.setupUi(self)
        
        self.setWindowTitle("eQSL Programm (Versionsfenster)")

# -----------------------------------------------------------
# ANWENDUNGSSTARTER UND KORREKTE AUSFÜHRUNG
# -----------------------------------------------------------

if __name__ == "__main__":
    # 1. QApplication Instanz erstellen
    app = QApplication(sys.argv)
    
    # 2. Instanz des Hauptfensters erstellen
    window1 = EqslMainWindow()
    window2 = EqslSqlCreateWindow()
    window3 = EqslSettingsWindow()  
    window4 = EqslUploadWindow()
    window5 = EqslImageViewWindow()
    window6 = EqslHelpViewWindow()
    window7 = EqslVersionWindow()
    
    # 3. Fenster anzeigen
    window1.show()
    window2.show()
    window3.show()  
    window4.show()
    window5.show()
    window6.show()
    window7.show()
    
    # 4. Anwendungsschleife starten
    sys.exit(app.exec())