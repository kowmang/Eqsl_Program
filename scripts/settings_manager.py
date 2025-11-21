import sqlite3
import os
import json
# Import QObject and Signal, as the class should send signals.
from PySide6.QtCore import Slot, QObject, Signal 


# SettingsManager must inherit from QObject to be able to send signals
class SettingsManager(QObject):
    """
    Manages saving and loading program settings (e.g., paths) 
    and is responsible for creating new databases.
    """
    
    # Define signal that transmits the new path when the database is set
    db_path_selected = Signal(str)
    
    def __init__(self):
        # QObject initialization must be called in the constructor when inheriting
        super().__init__()
        print("SettingsManager initialized.")
        
        # Set the path to the configuration file relative to the current script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_filepath = os.path.join(base_dir, '..', 'settings.json')
        self.support_data_dir = os.path.join(base_dir, '..', 'support_data') 
        
        # Default settings or loaded settings
        self.settings = self.load_settings()

    def get_current_db_path(self) -> str:
        """Returns the currently stored DB path in the settings."""
        return self.settings.get("database", "")

    def get_current_download_dir(self) -> str:
        """Returns the currently stored download directory in the settings."""
        return self.settings.get("download_directory", "")
    
    def get_current_adif_path(self) -> str:
        """Returns the currently stored ADIF path in the settings."""
        return self.settings.get("adif_path", "")
    
    # CHANGED: From 'get_current_bulk_card_dir' to 'get_bulk_card_dir' to fix AttributeError
    def get_bulk_card_dir(self) -> str:
        """Returns the path to the Bulk Card directory."""
        return self.settings.get("bulk_card_directory", "")

    def load_settings(self) -> dict:
        """Loads settings from settings.json or returns default values."""
        
        # DEFINITION OF THE COMPLETE STANDARD STRUCTURE
        default_settings = {
            "database": "",  # Path to the SQLite database
            "table_name": "eqsl_data", 
            "last_upload_dir": "",# Last directory for uploads
            "download_directory": "", # Default download directory
            "adif_path": "", # Default path for ADIF import
            "bulk_card_directory": "" # Path for Bulk Card settings
        }
        
        if os.path.exists(self.config_filepath):
            try:
                with open(self.config_filepath, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    print(f"Settings loaded from: {self.config_filepath}")
                    
                    # Merge with defaults to ensure all keys are present
                    default_settings.update(settings)
                    return default_settings
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading settings file: {e}. Using default settings.")
        
        # Creates the directory if it is missing before saving the empty file
        config_dir = os.path.dirname(self.config_filepath)
        if config_dir and not os.path.exists(config_dir):
            try:
                os.makedirs(config_dir, exist_ok=True)
            except OSError as e:
                print(f"Warning: Could not create config directory {config_dir}: {e}")
                
        return default_settings

    def save_settings(self):
        """Saves the current settings to settings.json."""
        try:
            with open(self.config_filepath, 'w', encoding='utf-8') as f:
                # Saves only the current settings, not the default_settings
                json.dump(self.settings, f, indent=4)
            print(f"Settings successfully saved to: {self.config_filepath}")
        except IOError as e:
            print(f"Error saving settings file: {e}")

    @Slot()
    def reset_db_path(self):
        """
        Resets the database path in the settings to an empty string and saves.
        """
        if self.settings.get("database"):
            self.settings["database"] = ""
            self.save_settings()
            # Signal that the path has been reset (with an empty string)
            self.db_path_selected.emit("") 
            print("Database path successfully reset to empty string.")
        else:
            print("Database path was already empty. No reset needed.")

    @Slot()
    def reset_bulk_card_dir(self):
        """
        Resets the Bulk Card directory path in the settings to an empty string and saves.
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
        Saves the selected download directory in the settings.
        """
        # Check if the path is a valid directory and exists
        if not dir_path or not os.path.isdir(dir_path):
            print(f"Error: Selected path is not a valid directory or does not exist: {dir_path}")
            return
        
        print(f"Setting new default download directory to: {dir_path}")
        self.settings["download_directory"] = dir_path
        self.save_settings()
        print("Download directory successfully saved.")

    @Slot(str)
    def handle_new_adif_path(self, adif_filepath: str):
        """Saves the path to the ADIF file in the settings."""
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
        Saves the selected directory for the Bulk Card settings.
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
        Creates the database file, the schema, and saves the path under 'database'.
        Ensures that the target directory exists.
        """
        if not db_filepath.lower().endswith(('.db', '.sqlite')):
            print(f"Error: Database file path '{db_filepath}' does not have a valid extension.")
            return

        # Ensure the directory exists
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
            # Update the database path in the settings under the key 'database'
            self.settings["database"] = db_filepath
            self.save_settings()

            # Emit signal that the path was successfully set
            self.db_path_selected.emit(db_filepath) 

            print(f"New default database set to: {db_filepath}")
        else:
            print("Failed to create database schema. Check file permissions.")


    @Slot(str)
    def handle_existing_db_path(self, db_filepath: str):
        """
        Saves an already existing database path as the default.
        """
        if not os.path.exists(db_filepath):
            print(f"Error: Selected file does not exist: {db_filepath}")
            return
            
        if not db_filepath.lower().endswith(('.db', '.sqlite')):
            print(f"Error: Database file path '{db_filepath}' does not have a valid extension.")
            return

        print(f"Setting existing database path to: {db_filepath}")
        
        # Update the database path in the settings under the key 'database'
        self.settings["database"] = db_filepath
        
        # Save settings (automatic saving)
        self.save_settings()

        # Emit signal that the path was successfully set
        self.db_path_selected.emit(db_filepath)

        print(f"New default database set to: {db_filepath}")


    def _create_db_with_schema(self, db_filepath: str) -> bool:
        """
        Establishes a connection to the database and creates all necessary tables.
        Reads the table name from the settings.
        """
        # NOTE: The table name is read from the settings here (fix from last time)
        table_name = self.settings.get("table_name", "eqsl_data") 

        # SQL command for the uploaded eQSL data
        EQSL_DATA_SQL = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            qso_id INTEGER PRIMARY KEY,
    
            -- IMPORTANT QSO DATA FOR UNIQUE KEY
            CALL TEXT NOT NULL,         -- Call sign of the QSO partner
            QSO_DATE TEXT NOT NULL,     -- Date (YYYYMMDD)
            TIME_ON TEXT NOT NULL,      -- Start time (HHMMSS)
    
            -- GENERAL QSO DATA
            BAND TEXT,
            MODE TEXT,
            SUBMODE TEXT,
            FREQ REAL,                  -- Frequency (e.g., 14.0764)
            RST_SENT TEXT,              -- Sent report
            RST_RCVD TEXT,              -- Received report
            TX_PWR REAL,                -- Transmit power (e.g., 30.0)
    
            -- GEOGRAPHICAL DATA OF THE PARTNER
            CONT TEXT,                  -- Continent
            COUNTRY TEXT,               -- Country (Name)
            DXCC INTEGER,               -- DXCC Number
            PFX TEXT,                   -- Prefix
            CQZ INTEGER,                -- CQ Zone
            ITUZ INTEGER,               -- ITU Zone
            GRIDSQUARE TEXT,            -- Locator (e.g., JO55RM)
            LAT REAL,                   -- Latitude
            LON REAL,                   -- Longitude

            -- PERSONAL DATA OF THE PARTNER
            NAME TEXT,                  -- Name (First and Last)
            QTH TEXT,                   -- Location/City
            ADDRESS TEXT,               -- Complete address
            EMAIL TEXT,
            AGE INTEGER,
    
            -- eQSL-STATUS
            EQSL_QSL_SENT TEXT,
            EQSL_QSLS_DATE TEXT,        -- Sent date (YYYYMMDD)
            EQSL_QSL_RCVD TEXT,
            EQSL_QSLR_DATE TEXT,        -- Received date (YYYYMMDD)
            EQSL_IMAGE_BLOB BLOB,       -- eQSL image as BLOB 

            
            -- DX-INDEXES 
            SOTA_REF TEXT, 
            POTA_REF TEXT,
            IOTA_REF TEXT,
    
            -- UNIQUE Constraint for duplicate detection (important!)
            UNIQUE(CALL, QSO_DATE, TIME_ON) 
        );
        """

        try:
            # Establishes connection and enables Foreign Keys (important for SQLite)
            conn = sqlite3.connect(db_filepath)
            cursor = conn.cursor()
            
            # Create tables
            cursor.execute(EQSL_DATA_SQL)
            
            # Save changes and close the connection
            conn.commit()
            conn.close()
            print(f"Schema created: {table_name} table is now defined.")
            return True
            
        except sqlite3.Error as e:
            print(f"SQLite Error during schema creation: {e}")
            return False