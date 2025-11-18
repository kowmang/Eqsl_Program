import sqlite3
import os
import json
# Importiere QObject und Signal, da die Klasse Signale aussenden soll
from PySide6.QtCore import Slot, QObject, Signal 


# SettingsManager muss von QObject erben, um Signale senden zu können
class SettingsManager(QObject):
    """
    Verwaltet das Speichern und Laden der Programmeinstellungen (z.B. Pfade) 
    und ist für die Erstellung neuer Datenbanken zuständig.
    """
    
    # Signal definieren, das den neuen Pfad überträgt, wenn die Datenbank gesetzt wurde
    db_path_selected = Signal(str)
    
    def __init__(self):
        # QObject-Initialisierung muss im Konstruktor aufgerufen werden, wenn man erbt
        super().__init__()
        print("SettingsManager initialized.")
        
        # Den Pfad zur Konfigurationsdatei relativ zum aktuellen Skript festlegen
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_filepath = os.path.join(base_dir, '..', 'settings.json')
        self.support_data_dir = os.path.join(base_dir, '..', 'support_data') 
        
        # Standardeinstellungen oder geladene Einstellungen
        self.settings = self.load_settings()

    def get_current_db_path(self) -> str:
        """Gibt den aktuell in den Einstellungen gespeicherten DB-Pfad zurück."""
        return self.settings.get("database", "")

    def get_current_download_dir(self) -> str:
        """Gibt den aktuell in den Einstellungen gespeicherten Download-Pfad zurück."""
        return self.settings.get("download_directory", "")
    
    def get_current_adif_path(self) -> str:
        """Gibt den aktuell in den Einstellungen gespeicherten ADIF-Pfad zurück."""
        return self.settings.get("adif_path", "")
    
    # GEÄNDERT: Von 'get_current_bulk_card_dir' zu 'get_bulk_card_dir', um den AttributeError zu beheben
    def get_bulk_card_dir(self) -> str:
        """Gibt den Pfad zum Bulk Card Verzeichnis zurück."""
        return self.settings.get("bulk_card_directory", "")

    def load_settings(self) -> dict:
        """Lädt Einstellungen aus settings.json oder gibt Standardwerte zurück."""
        
        # DEFINITION DER VOLLSTÄNDIGEN STANDARD-STRUKTUR
        default_settings = {
            "database": "",  # Pfad zur SQLite-Datenbank
            "table_name": "eqsl_data", 
            "last_upload_dir": "",# Letztes Verzeichnis für Uploads
            "download_directory": "", # Standard-Download-Verzeichnis
            "adif_path": "", # Standardpfad für ADIF-Import
            "bulk_card_directory": "" # Pfad für Bulk Card Settings
        }
        
        if os.path.exists(self.config_filepath):
            try:
                with open(self.config_filepath, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    print(f"Settings loaded from: {self.config_filepath}")
                    
                    # Merge mit Defaults, um sicherzustellen, dass alle Schlüssel vorhanden sind
                    default_settings.update(settings)
                    return default_settings
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading settings file: {e}. Using default settings.")
        
        # Erstellt das Verzeichnis, falls es fehlt, bevor die leere Datei gespeichert wird
        config_dir = os.path.dirname(self.config_filepath)
        if config_dir and not os.path.exists(config_dir):
            try:
                os.makedirs(config_dir, exist_ok=True)
            except OSError as e:
                print(f"Warning: Could not create config directory {config_dir}: {e}")
                
        return default_settings

    def save_settings(self):
        """Speichert die aktuellen Einstellungen in settings.json."""
        try:
            with open(self.config_filepath, 'w', encoding='utf-8') as f:
                # Speichert nur die aktuellen Einstellungen, nicht die default_settings
                json.dump(self.settings, f, indent=4)
            print(f"Settings successfully saved to: {self.config_filepath}")
        except IOError as e:
            print(f"Error saving settings file: {e}")

    @Slot()
    def reset_db_path(self):
        """
        Setzt den Datenbankpfad in den Einstellungen zurück auf einen leeren String und speichert.
        """
        if self.settings.get("database"):
            self.settings["database"] = ""
            self.save_settings()
            # Signal senden, dass der Pfad zurückgesetzt wurde (mit leerem String)
            self.db_path_selected.emit("") 
            print("Database path successfully reset to empty string.")
        else:
            print("Database path was already empty. No reset needed.")

    @Slot()
    def reset_bulk_card_dir(self):
        """
        Setzt den Bulk Card Verzeichnispfad in den Einstellungen zurück.
        """
        if self.settings.get("bulk_card_directory"):
            self.settings["bulk_card_directory"] = ""
            self.save_settings()
            print("Bulk card directory path successfully reset to empty string.")
        else:
            print("Bulk card directory path was already empty. No reset needed.")
            
    @Slot(str)
    def handle_new_download_dir(self, dir_path: str):
        """
        Speichert den ausgewählten Download-Ordner in den Einstellungen.
        """
        # Überprüfen, ob der Pfad ein gültiges Verzeichnis ist und existiert
        if not dir_path or not os.path.isdir(dir_path):
            print(f"Error: Selected path is not a valid directory or does not exist: {dir_path}")
            return
        
        print(f"Setting new default download directory to: {dir_path}")
        self.settings["download_directory"] = dir_path
        self.save_settings()
        print("Download directory successfully saved.")

    @Slot(str)
    def handle_new_adif_path(self, adif_filepath: str):
        """Speichert den Pfad zur ADIF-Datei in den Settings."""
        if not adif_filepath or not os.path.exists(adif_filepath):
            print(f"Error: Selected ADIF file does not exist: {adif_filepath}")
            return

        print(f"Setting new default ADIF path to: {adif_filepath}")
        self.settings["adif_path"] = adif_filepath
        self.save_settings()
        print("ADIF path successfully saved.")

    @Slot(str)
    def handle_new_bulk_card_dir(self, dir_path: str):
        """
        Speichert das ausgewählte Verzeichnis für die Bulk Card Settings.
        """
        if not dir_path or not os.path.isdir(dir_path):
            print(f"Error: Selected path is not a valid directory or does not exist: {dir_path}")
            return

        print(f"Setting new bulk card directory to: {dir_path}")
        self.settings["bulk_card_directory"] = dir_path
        self.save_settings()
        print("Bulk card directory successfully saved.")

    @Slot(str)
    def handle_new_db_path(self, db_filepath: str):
        """
        Erstellt die Datenbankdatei, das Schema und speichert den Pfad unter 'database'.
        Stellt sicher, dass das Zielverzeichnis existiert.
        """
        if not db_filepath.lower().endswith(('.db', '.sqlite')):
            print(f"Error: Database file path '{db_filepath}' does not have a valid extension.")
            return

        # Sicherstellen, dass das Verzeichnis existiert
        db_dir = os.path.dirname(db_filepath)
        if db_dir and not os.path.exists(db_dir):
            try:
                os.makedirs(db_dir, exist_ok=True)
                print(f"Created directory for new database: {db_dir}")
            except OSError as e:
                print(f"Error creating directory for database: {e}")
                return 

        print(f"Attempting to create new database and schema at: {db_filepath}")

        success = self._create_db_with_schema(db_filepath)

        if success:
            # Datenbankpfad in den Einstellungen unter dem Schlüssel 'database' aktualisieren
            self.settings["database"] = db_filepath
            self.save_settings()

            # Signal senden, dass der Pfad erfolgreich gesetzt wurde
            self.db_path_selected.emit(db_filepath) 

            print(f"New default database set to: {db_filepath}")
        else:
            print("Failed to create database schema. Check file permissions.")


    @Slot(str)
    def handle_existing_db_path(self, db_filepath: str):
        """
        Speichert einen bereits existierenden Datenbankpfad als Standard.
        """
        if not os.path.exists(db_filepath):
            print(f"Error: Selected file does not exist: {db_filepath}")
            return
            
        if not db_filepath.lower().endswith(('.db', '.sqlite')):
            print(f"Error: Database file path '{db_filepath}' does not have a valid extension.")
            return

        print(f"Setting existing database path to: {db_filepath}")
        
        # Datenbankpfad in den Einstellungen unter dem Schlüssel 'database' aktualisieren
        self.settings["database"] = db_filepath
        
        # Einstellungen speichern (Automatisches Speichern)
        self.save_settings()

        # Signal senden, dass der Pfad erfolgreich gesetzt wurde
        self.db_path_selected.emit(db_filepath)

        print(f"New default database set to: {db_filepath}")


    def _create_db_with_schema(self, db_filepath: str) -> bool:
        """
        Stellt eine Verbindung zur Datenbank her und erstellt alle notwendigen Tabellen.
        Liest den Tabellennamen aus den Settings.
        """
        # HINWEIS: Hier wird der Tabellenname aus den Settings gelesen (Fix vom letzten Mal)
        table_name = self.settings.get("table_name", "eqsl_data") 

        # SQL-Befehl für die hochgeladenen eQSL-Daten
        EQSL_DATA_SQL = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            qso_id INTEGER PRIMARY KEY,
    
            -- WICHTIGE QSO-DATEN FÜR UNIQUE KEY
            CALL TEXT NOT NULL,         -- Rufzeichen des QSO-Partners
            QSO_DATE TEXT NOT NULL,     -- Datum (YYYYMMDD)
            TIME_ON TEXT NOT NULL,      -- Startzeit (HHMMSS)
    
            -- ALLGEMEINE QSO-DATEN
            BAND TEXT,
            MODE TEXT,
            SUBMODE TEXT,
            FREQ REAL,                  -- Frequenz (z.B. 14.0764)
            RST_SENT TEXT,              -- Gesendetes Rapport
            RST_RCVD TEXT,              -- Empfangenes Rapport
            TX_PWR REAL,                -- Sendeleistung (z.B. 30.0)
    
            -- GEOGRAFISCHE DATEN DES PARTNERS
            CONT TEXT,                  -- Kontinent
            COUNTRY TEXT,               -- Land (Name)
            DXCC INTEGER,               -- DXCC-Nummer
            PFX TEXT,                   -- Präfix
            CQZ INTEGER,                -- CQ Zone
            ITUZ INTEGER,               -- ITU Zone
            GRIDSQUARE TEXT,            -- Locator (z.B. JO55RM)
            LAT REAL,                   -- Breitengrad
            LON REAL,                   -- Längengrad

            -- PERSÖNLICHE DATEN DES PARTNERS
            NAME TEXT,                  -- Name (Vor- und Nachname)
            QTH TEXT,                   -- Ort/City
            ADDRESS TEXT,               -- Komplette Adresse
            EMAIL TEXT,
            AGE INTEGER,
    
            -- eQSL-STATUS
            EQSL_QSL_SENT TEXT,
            EQSL_QSLS_DATE TEXT,        -- Sendedatum (YYYYMMDD)
            EQSL_QSL_RCVD TEXT,
            EQSL_QSLR_DATE TEXT,        -- Empfangsdatum (YYYYMMDD)
            EQSL_IMAGE_BLOB BLOB,       -- eQSL Bild als BLOB 

            
            -- DX-INDEXES 
            SOTA_REF TEXT, 
            POTA_REF TEXT,
            IOTA_REF TEXT,
    
            -- UNIQUE Constraint zur Duplikat-Erkennung (wichtig!)
            UNIQUE(CALL, QSO_DATE, TIME_ON) 
        );
        """

        try:
            # Stellt Verbindung her und aktiviert Foreign Keys (wichtig für SQLite)
            conn = sqlite3.connect(db_filepath)
            cursor = conn.cursor()
            
            # Tabellen erstellen
            cursor.execute(EQSL_DATA_SQL)
            
            # Speichert die Änderungen und schließt die Verbindung
            conn.commit()
            conn.close()
            print(f"Schema created: {table_name} table is now defined.")
            return True
            
        except sqlite3.Error as e:
            print(f"SQLite Error during schema creation: {e}")
            return False