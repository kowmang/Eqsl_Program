import os
from PySide6.QtWidgets import QMainWindow, QWidget, QDialog
from PySide6.QtWidgets import QTextBrowser, QVBoxLayout
from PySide6.QtGui import QFont
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

class EqslSettingsWindow(QDialog):
    """Das separate Fenster für die Einstellungen."""
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_frm_settings()
        self.ui.setupUi(self)
        self.setWindowTitle("eQSL Programm (Settings)")
        # Fügen Sie hier später die Logik für Einstellungs-Widgets hinzu
        self._setup_connections() 

    def _setup_connections(self):
        # ANNAHME: Button im Designer heißt 'btn_cancel'
        if hasattr(self.ui, 'btn_cancel_frm_settings'):
            # Verbindet den Klick des Buttons direkt mit der close()-Methode des Dialogs
            self.ui.btn_cancel_frm_settings.clicked.connect(self.reject)
        # Wenn Sie eine QDialogButtonBox verwenden, ist die Verbindung anders (siehe unten)
        pass

class EqslUploadWindow(QDialog):
    """Das separate Fenster für die Einstellungen."""
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_frm_upload()
        self.ui.setupUi(self)
        self.setWindowTitle("eQSL Programm (QSL Upload)")
        # Fügen Sie hier später die Logik für Einstellungs-Widgets hinzu
        self._setup_connections() 

    def _setup_connections(self):
        if hasattr(self.ui, 'btn_cancel_frm_upload'):
            # Verbindet den Klick des Buttons direkt mit der close()-Methode des Dialogs
            self.ui.btn_cancel_frm_upload.clicked.connect(self.reject)
        # Verbindungen für dieses Fenster
        pass

class EqslHelpWindow(QDialog):
    """Das separate Fenster für die Einstellungen."""
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_frm_help_view()
        self.ui.setupUi(self)
        self.setWindowTitle("eQSL Programm (Manual)")
        # Fügen Sie hier später die Logik für Einstellungs-Widgets hinzu
        self._load_version_content() 
        self._setup_connections() 
    
    def _load_version_content(self):
        """
        Lädt den Inhalt der version.html aus support_data und zeigt ihn an.
        """
        # Pfad zur version.html relativ zum Hauptverzeichnis
        # Der Pfad ist von 'Eqsl_Program/scripts' aus: '../../support_data/version.html'
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Springt zwei Ebenen hoch (Eqsl_Program) und dann in support_data
        html_path = os.path.join(base_dir, '..', 'support_data', 'manual.html')

        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
        except FileNotFoundError:
            html_content = (
                f"<h1>Fehler: version.html nicht gefunden!</h1>"
                f"<p>Erwarteter Pfad: <code>{html_path}</code></p>"
            )
        
        # QTextBrowser erstellen, um den HTML-Inhalt anzuzeigen
        browser = QTextBrowser(self)
        browser.setHtml(html_content)
        browser.setFont(QFont("Arial", 10))

        # Das ui-Objekt wird in QDialog nur als Container betrachtet.
        # Wir müssen das Layout manuell setzen, da setupUi() hier wahrscheinlich
        # nur die Steuerelemente initialisiert hat, aber nicht das gesamte Layout.
        
        # Sicherstellen, dass ein Layout gesetzt ist, um den Browser zu platzieren.
        if self.layout() is None:
            layout = QVBoxLayout(self)
            self.setLayout(layout)
        else:
             layout = self.layout()

        # Fügen Sie den Browser zum Layout hinzu (falls er nicht schon im Designer war)
        layout.addWidget(browser)

    def _setup_connections(self):
        # Verbindungen für dieses Fenster
        pass

class EqslVersionWindow(QDialog): # Geändert auf QDialog
    """Das separate Fenster für die Versionsinformationen."""
    def __init__(self):
        super().__init__()

        self.ui = Ui_frm_version()
        self.ui.setupUi(self) 
        self.setWindowTitle("eQSL Programm (Version Info)")
        
        # Die Methode, die den HTML-Inhalt lädt und anzeigt
        self._load_version_content() 
        self._setup_connections() 
    
    def _load_version_content(self):
        """
        Lädt den Inhalt der version.html aus support_data und zeigt ihn an.
        """
        # Pfad zur version.html relativ zum Hauptverzeichnis
        # Der Pfad ist von 'Eqsl_Program/scripts' aus: '../../support_data/version.html'
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Springt zwei Ebenen hoch (Eqsl_Program) und dann in support_data
        html_path = os.path.join(base_dir, '..', 'support_data', 'version.html')

        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
        except FileNotFoundError:
            html_content = (
                f"<h1>Fehler: version.html nicht gefunden!</h1>"
                f"<p>Erwarteter Pfad: <code>{html_path}</code></p>"
            )
        
        # QTextBrowser erstellen, um den HTML-Inhalt anzuzeigen
        browser = QTextBrowser(self)
        browser.setHtml(html_content)
        browser.setFont(QFont("Arial", 10))

        # Das ui-Objekt wird in QDialog nur als Container betrachtet.
        # Wir müssen das Layout manuell setzen, da setupUi() hier wahrscheinlich
        # nur die Steuerelemente initialisiert hat, aber nicht das gesamte Layout.
        
        # Sicherstellen, dass ein Layout gesetzt ist, um den Browser zu platzieren.
        if self.layout() is None:
            layout = QVBoxLayout(self)
            self.setLayout(layout)
        else:
             layout = self.layout()

        # Fügen Sie den Browser zum Layout hinzu (falls er nicht schon im Designer war)
        layout.addWidget(browser)

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