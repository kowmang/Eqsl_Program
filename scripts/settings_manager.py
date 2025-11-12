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
        
    def get_current_dxcc_path(self) -> str:
        """Gibt den aktuell in den Einstellungen gespeicherten DXCC-Listenpfad zurück."""
        return self.settings.get("dxcc_lookup_path", "")

    def get_current_download_dir(self) -> str:
        """Gibt den aktuell in den Einstellungen gespeicherten Download-Pfad zurück."""
        return self.settings.get("download_directory", "") # NEU

    def load_settings(self) -> dict:
        """Lädt Einstellungen aus settings.json oder gibt Standardwerte zurück."""
        
        # STANDARD-STRUKTUR (Hinzugefügt: download_directory)
        default_settings = {
            "dxcc_lookup_path": "", 
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
            
    # Slot für DXCC-Pfad
    @Slot(str)
    def handle_new_dxcc_path(self, source_filepath: str):
        """
        Kopiert die ausgewählte DXCC-CSV-Datei in den support_data-Ordner und speichert 
        den internen Pfad in den Einstellungen, außer die Datei ist bereits dort.
        """
        if not source_filepath or not os.path.exists(source_filepath):
            print(f"Error: DXCC source file not found: {source_filepath}")
            return
            
        if not source_filepath.lower().endswith('.csv'):
            print(f"Error: Selected file '{source_filepath}' is not a CSV file.")
            return

        # Sicherstellen, dass der Zielordner existiert
        if not os.path.exists(self.support_data_dir):
            os.makedirs(self.support_data_dir, exist_ok=True)

        # 1. Zielpfad definieren (immer 'dxcc_lookup.csv' im support_data Ordner)
        destination_filepath = os.path.join(self.support_data_dir, 'dxcc_lookup.csv')
        
        # Prüfung, ob Quelle und Ziel identisch sind (Absolutpfad-Vergleich)
        if os.path.abspath(source_filepath) == os.path.abspath(destination_filepath):
            print("DXCC list is already in the target location. Skipping copy operation.")
            self.settings["dxcc_lookup_path"] = destination_filepath
            self.save_settings()
            return
        
        # --- Kopiervorgang (nur wenn nötig) ---
        try:
            # 2. Datei kopieren (shutil.copy2 stellt sicher, dass Metadaten kopiert werden)
            shutil.copy2(source_filepath, destination_filepath)
            print(f"DXCC list copied from {source_filepath} to {destination_filepath}")

            # 3. Internen Pfad in den Einstellungen speichern
            self.settings["dxcc_lookup_path"] = destination_filepath
            self.save_settings()
            print("New DXCC lookup path set and saved.")

        except Exception as e:
            print(f"Error during DXCC file copy: {e}")

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
        
        # SQL-Befehl für die Nachschlagetabelle der DXCC-Länder
        DXCC_LIST_SQL = """
        CREATE TABLE IF NOT EXISTS dxcc_list (
            dxcc_number INTEGER PRIMARY KEY NOT NULL,
            prefix TEXT NOT NULL,
            continent TEXT,
            itu_zone INTEGER,
            cq_zone INTEGER,
            dxcc_name TEXT NOT NULL UNIQUE
        );
        """

        # SQL-Befehl für die hochgeladenen eQSL-Daten
        EQSL_DATA_SQL = """
        CREATE TABLE IF NOT EXISTS eqsl_data (
            primarykey TEXT PRIMARY KEY NOT NULL,
            callsign TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            year INTEGER NOT NULL,
            band TEXT,
            mode TEXT,
            itu_zone INTEGER,
            cq_zone INTEGER,
            
            -- Fremdschlüssel: Moderne SQLite-Definition
            dxcc_number INTEGER REFERENCES dxcc_list(dxcc_number), 
            
            dxcc_name TEXT,
            prefix TEXT,
            continent TEXT
        );
        """

        try:
            # Stellt Verbindung her und aktiviert Foreign Keys (wichtig für SQLite)
            conn = sqlite3.connect(db_filepath)
            cursor = conn.cursor()
            
            # Foreign Keys MÜSSEN direkt nach dem Verbindungsaufbau aktiviert werden
            cursor.execute("PRAGMA foreign_keys = ON;")
            
            # Tabellen erstellen
            cursor.execute(DXCC_LIST_SQL)
            cursor.execute(EQSL_DATA_SQL)
            
            # Speichert die Änderungen und schließt die Verbindung
            conn.commit()
            conn.close()
            print("Schema created: dxcc_list and eqsl_data tables are now defined.")
            return True
            
        except sqlite3.Error as e:
            print(f"SQLite Error during schema creation: {e}")
            return False