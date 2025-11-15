import sqlite3
import os
import json 
import shutil 
from PySide6.QtCore import Slot

class SettingsManager:
    """
    Verwaltet das Speichern und Laden der Programmeinstellungen (z.B. Pfade) 
    und ist für die Erstellung neuer Datenbanken zuständig.
    """
    def __init__(self):
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
        return self.settings.get("download_directory", "") # NEU
    
    def get_current_adif_path(self) -> str:
        """Gibt den aktuell in den Einstellungen gespeicherten ADIF-Pfad zurück."""
        return self.settings.get("adif_path", "")

    def load_settings(self) -> dict:
        """Lädt Einstellungen aus settings.json oder gibt Standardwerte zurück."""
        default_settings = {
            "database": "",         
            "table_name": "eqsl_data", 
            "last_upload_dir": "",
            "download_directory": "",
            "adif_path": ""  # NEU: Standardpfad für ADIF-Import
        }
        
        # STANDARD-STRUKTUR (Hinzugefügt: download_directory)
        default_settings = { 
            "database": "",       
            "table_name": "eqsl_data", 
            "last_upload_dir": "",
            "download_directory": "" # NEU
        }

        if os.path.exists(self.config_filepath):
            try:
                with open(self.config_filepath, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    print(f"Settings loaded from: {self.config_filepath}")
                    
                    # Merge mit Defaults, um fehlende Schlüssel zu vermeiden
                    default_settings.update(settings)
                    return default_settings
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading settings file: {e}. Using default settings.")
        
        return default_settings

    def save_settings(self):
        """Speichert die aktuellen Einstellungen in settings.json."""
        try:
            with open(self.config_filepath, 'w', encoding='utf-8') as f:
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
            print("Database path successfully reset to empty string.")
        else:
            print("Database path was already empty. No reset needed.")
            
       # Slot für Download-Ordner (NEU)
    @Slot(str)
    def handle_new_download_dir(self, dir_path: str):
        """
        Speichert den ausgewählten Download-Ordner in den Einstellungen.
        """
        if not os.path.isdir(dir_path):
             print(f"Error: Selected path is not a valid directory: {dir_path}")
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
    def handle_new_db_path(self, db_filepath: str):
        """
        Erstellt die Datenbankdatei, das Schema und speichert den Pfad unter 'database'.
        """
        if not db_filepath.lower().endswith(('.db', '.sqlite')):
            print(f"Error: Database file path '{db_filepath}' does not have a valid extension.")
            return

        print(f"Attempting to create new database and schema at: {db_filepath}")

        success = self._create_db_with_schema(db_filepath)

        if success:
            # 2. Datenbankpfad in den Einstellungen unter dem Schlüssel 'database' aktualisieren
            self.settings["database"] = db_filepath
            
            # 3. Einstellungen speichern (Automatisches Speichern)
            self.save_settings()

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
        
        # 1. Datenbankpfad in den Einstellungen unter dem Schlüssel 'database' aktualisieren
        self.settings["database"] = db_filepath
        
        # 2. Einstellungen speichern (Automatisches Speichern)
        self.save_settings()

        print(f"New default database set to: {db_filepath}")


    def _create_db_with_schema(self, db_filepath: str) -> bool:
        """
        Stellt eine Verbindung zur Datenbank her und erstellt alle notwendigen Tabellen.
        """

        # SQL-Befehl für die hochgeladenen eQSL-Daten
        EQSL_DATA_SQL = """
        CREATE TABLE IF NOT EXISTS eqsl_data (
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
            LAT REAL,                   -- Breitengrad (N050 51.151)
            LON REAL,                   -- Längengrad (E004 49.287)

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
            EQSL_IMAGE_BLOB BLOB,        -- eQSL Bild als BLOB  

           
            -- DX-INDEXES (Wenn gewünscht, z.B. SOTA/POTA/IOTA)
            SOTA_REF TEXT,              -- Obwohl in der Datei nicht explizit, beibehalten falls benötigt
            POTA_REF TEXT,              -- Dito
            IOTA_REF TEXT,              -- Dito
    
            -- UNIQUE Constraint zur Duplikat-Erkennung (wichtig!)
            UNIQUE(CALL, QSO_DATE, TIME_ON) 
        );
        """

        try:
            # Stellt Verbindung her und aktiviert Foreign Keys (wichtig für SQLite)
            conn = sqlite3.connect(db_filepath)
            cursor = conn.cursor()
            
            # Foreign Keys MÜSSEN direkt nach dem Verbindungsaufbau aktiviert werden
            cursor.execute("PRAGMA foreign_keys = OFF;")
            
            # Tabellen erstellen
            cursor.execute(EQSL_DATA_SQL)
            
            # Speichert die Änderungen und schließt die Verbindung
            conn.commit()
            conn.close()
            print("Schema created: eqsl_data tables are now defined.")
            return True
            
        except sqlite3.Error as e:
            print(f"SQLite Error during schema creation: {e}")
            return False