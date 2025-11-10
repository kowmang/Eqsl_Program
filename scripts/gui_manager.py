from PySide6.QtWidgets import QMainWindow, QWidget
from PySide6.QtCore import Slot

# Die kompilierten UI-Klassen werden hier importiert (relativ zum 'scripts' Ordner)
# Wir müssen eine Ebene höher (..) und dann in den gui_data Ordner gehen.
from ..gui_data.frm_settings_ui import Ui_frm_settings
from ..gui_data.frm_upload_ui import Ui_frm_upload
from ..gui_data.frm_help_view_ui import Ui_frm_help_view
from ..gui_data.frm_version_ui import Ui_frm_version


# ----------------------------------------------------
# 1. DEFINITION DER UNTERFENSTER (SettingsWindow)
# ----------------------------------------------------

class EqslSettingsWindow(QMainWindow):
    """Das separate Fenster für die Einstellungen."""
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_frm_settings()
        self.ui.setupUi(self)
        self.setWindowTitle("eQSL Programm (Settings)")
        # Fügen Sie hier später die Logik für Einstellungs-Widgets hinzu
        self._setup_connections() 

    def _setup_connections(self):
        # Verbindungen für dieses Fenster
        pass

class EqslUploadWindow(QMainWindow):
    """Das separate Fenster für die Einstellungen."""
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_frm_upload()
        self.ui.setupUi(self)
        self.setWindowTitle("eQSL Programm (QSL Upload)")
        # Fügen Sie hier später die Logik für Einstellungs-Widgets hinzu
        self._setup_connections() 

    def _setup_connections(self):
        # Verbindungen für dieses Fenster
        pass

class EqslHelpWindow(QWidget):
    """Das separate Fenster für die Einstellungen."""
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_frm_help_view()
        self.ui.setupUi(self)
        self.setWindowTitle("eQSL Programm (Manual)")
        # Fügen Sie hier später die Logik für Einstellungs-Widgets hinzu
        self._setup_connections() 

    def _setup_connections(self):
        # Verbindungen für dieses Fenster
        pass

class EqslVersionWindow(QWidget):
    """Das separate Fenster für die Einstellungen."""
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_frm_version()
        self.ui.setupUi(self)
        self.setWindowTitle("eQSL Programm (Version Info)")
        # Fügen Sie hier später die Logik für Einstellungs-Widgets hinzu
        self._setup_connections() 

    def _setup_connections(self):
        # Verbindungen für dieses Fenster
        pass

# ----------------------------------------------------
# 2. MANAGER-KLASSE ZUR KONTROLLE DER FENSTER
# ----------------------------------------------------

class GuiManager:
    """Verwaltet die Instanzen aller sekundären Fenster."""
    def __init__(self):
        self.settings_window = None # Speichert die Instanz
        self.upload_window = None
        self.help_window = None 
        self.version_window = None
        
    @Slot()
    def open_settings(self):
        """Öffnet das Einstellungsfenster und bringt es in den Vordergrund."""
        
        if self.settings_window is None:
            # Erstellt die Instanz nur, wenn sie noch nicht existiert
            self.settings_window = EqslSettingsWindow()
        
        self.settings_window.show()

    @Slot()
    def open_upload(self):
        """Öffnet das Einstellungsfenster und bringt es in den Vordergrund."""
        
        if self.upload_window is None:
            # Erstellt die Instanz nur, wenn sie noch nicht existiert
            self.upload_window = EqslUploadWindow()
        
        self.upload_window.show()

    @Slot()
    def open_help(self):
        """Öffnet das Einstellungsfenster und bringt es in den Vordergrund."""
        
        if self.help_window is None:
            # Erstellt die Instanz nur, wenn sie noch nicht existiert
            self.help_window = EqslHelpWindow()
        
        self.help_window.show()

    @Slot()
    def open_version_info(self):    
        """Öffnet das Einstellungsfenster und bringt es in den Vordergrund."""
        
        if self.version_window is None:
            # Erstellt die Instanz nur, wenn sie noch nicht existiert
            self.version_window = EqslVersionWindow()
        
        self.version_window.show()


# Sie können hier weitere Methoden hinzufügen, z.B. open_upload(), open_help()