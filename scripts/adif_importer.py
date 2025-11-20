import sqlite3
import os
import re

from typing import List, Dict, Tuple

# --------------------------------------------------------------------------------
# CONFIGURATION & STRUCTURE
# --------------------------------------------------------------------------------

# ADJUST THESE PATHS TO YOUR ACTUAL ENVIRONMENT!
# The ADIF path from your last console output:
DEFAULT_ADIF_PATH = "C:/Users/oe4vm/Desktop/Proggen/test.adi"
# The DB path from your last console output:
DEFAULT_DB_PATH = "C:/Users/oe4vm/Desktop/Proggen/eqsl_program/Eqsl_Program/database_sql/new_test_db_51.db"

# List of columns to be inserted into the database.
DB_COLUMNS = [
    'CALL', 'QSO_DATE', 'TIME_ON', 'BAND', 'MODE', 'SUBMODE', 'FREQ', 'RST_SENT', 'RST_RCVD',
    'TX_PWR', 'CONT', 'COUNTRY', 'DXCC', 'PFX', 'CQZ', 'ITUZ', 'GRIDSQUARE', 'LAT', 'LON',
    'NAME', 'QTH', 'ADDRESS', 'EMAIL', 'AGE', 'EQSL_QSL_SENT', 'EQSL_QSLS_DATE', 'EQSL_QSL_RCVD',
    'EQSL_QSLR_DATE', 'EQSL_IMAGE_BLOB', 'SOTA_REF', 'POTA_REF', 'IOTA_REF'
]

# Regular expression to extract ADIF tags: <TAG:LENGTH>VALUE
# (Tag names are converted to uppercase)
ADIF_REGEX = re.compile(r'<(\w+):(\d+)>([^<]+)', re.IGNORECASE) 

# --------------------------------------------------------------------------------
# CLASSES FOR PARSING AND IMPORT
# --------------------------------------------------------------------------------

class AdifParsingError(Exception):
  """User-defined exception for ADIF parsing errors."""
  pass

class AdifFileIO:
  """Reads and parses an actual ADIF file."""
  @staticmethod
  def read_from_file(filepath: str) -> Tuple[List[Dict[str, str]], Dict[str, str]]:
    """
    Reads an ADIF file, parses the QSOs, and returns them as a list of dictionaries.
    """
    if not os.path.exists(filepath):
      raise FileNotFoundError(f"ADIF File not found: {filepath}")

    print(f"[DEBUG] Reading file: {filepath}")
    try:
      # Try reading the file with different encodings (common issue with ADIF)
      with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read().upper()
    except Exception as e:
      raise AdifParsingError(f"Error reading file: {e}")
    qso_records = []
    is_header = True

    # Split ADIF data by the End of Record tag
    records = re.split(r'<EOR>', content)
    
    for record in records:
      if not record.strip():
        continue

      fields = ADIF_REGEX.findall(record)
      
      if not fields:
        continue

      current_qso = {}
      record_is_qso = False
      
      for tag, length_str, value in fields:
        # Clean the value and ensure the tag is uppercase
        tag = tag.upper()
        value = value.strip()
        
        if tag in ['EOZ', 'ADIF_VER', 'CREATOR', 'PROGRAMID']:
          continue
        
        # Check if we have moved from the header to the QSO section
        if tag in ['CALL', 'QSO_DATE', 'TIME_ON']:
          is_header = False
          record_is_qso = True # Mark this record as a potential QSO

        # Store all DB-relevant fields. 'FREQ' comes as a string and must be converted later
        if record_is_qso and tag in DB_COLUMNS:
          current_qso[tag] = value

      if record_is_qso:
        # Ensure that the minimum UNIQUE fields are present.
        if all(key in current_qso for key in ['CALL', 'QSO_DATE', 'TIME_ON']):
          qso_records.append(current_qso)
        else:
          print(f"[WARNING] QSO ignored (missing keys): {current_qso.get('CALL', 'NOCALL')}")

    if not qso_records:
      print("[WARNING] Parser found no valid QSO entries in the file.")
      
    return qso_records, {}


class AdifImporter:
  """Imports QSOs from an ADIF file into a SQLite database."""
  
  # 1. NEW BAND MAPPING TABLE (Frequency in MHz)
  # Definition of amateur radio bands and their frequency ranges. 
  # Sorted from highest frequency to lowest for correct assignment.
  FREQUENCY_TO_BAND_MAP = [
    (144.0000, 146.0000, "2"),    # 2m
    (50.0000, 54.0000, "6"),      # 6m
    (28.0000, 29.7000, "10"),     # 10m
    (24.8900, 24.9900, "12"),     # 12m
    (21.0000, 21.4500, "15"),     # 15m
    (18.0680, 18.1680, "17"),     # 17m
    (14.0000, 14.3500, "20"),     # 20m
    (10.1000, 10.1500, "30"),     # 30m
    (7.0000, 7.2000, "40"),       # 40m
    (3.5000, 3.8000, "80"),       # 80m
    (1.8100, 2.0000, "160"),      # 160m
    # Additional bands (UHF/VHF) can be added here if needed:
    # (430.0000, 440.0000, "70cm"),
  ]
  
  def __init__(self, db_filepath: str):
    self.db_filepath = db_filepath
    self.table_name = "eqsl_data"

  # 2. NEW FUNCTION FOR FREQUENCY-TO-BAND MAPPING
  def _get_band_from_freq(self, freq_val: float) -> str:
    """
    Determines the amateur radio band (in meters) based on the frequency (in MHz).
    """
    for freq_min, freq_max, band_name in self.FREQUENCY_TO_BAND_MAP:
      # Checks if the frequency value is within the defined range (inclusive)
      if freq_min <= freq_val <= freq_max:
        return band_name
    return "" # Return an empty string if no band is found

  def _create_schema(self, conn: sqlite3.Connection):
    """Creates the eqsl_data table if it does not already exist."""
    cursor = conn.cursor()
    # HERE IS THE PROTECTION AGAINST DUPLICATES:
    # Only combinations of CALL, QSO_DATE, and TIME_ON that do not already exist will be inserted.
    sql_create_table = f"""
    CREATE TABLE IF NOT EXISTS {self.table_name} (
      qso_id INTEGER PRIMARY KEY,
  
      -- IMPORTANT QSO DATA FOR UNIQUE KEY
      CALL TEXT NOT NULL,       -- Call sign of the QSO partner
      QSO_DATE TEXT NOT NULL,   -- Date (YYYYMMDD)
      TIME_ON TEXT NOT NULL,    -- Start time (HHMMSS)
  
      -- GENERAL QSO DATA
      BAND TEXT,                -- Band (e.g., 20)
      MODE TEXT,                -- Mode (e.g., FT8)
      SUBMODE TEXT,             -- Submode (e.g., FT4)
      FREQ REAL,                -- Frequency (e.g., 14.0764)
      RST_SENT TEXT,            -- Sent RST
      RST_RCVD TEXT,            -- Received RST
      TX_PWR REAL,              -- Transmit Power (e.g., 30.0)
  
      -- GEOGRAPHICAL DATA OF THE PARTNER
      CONT TEXT,                -- Continent
      COUNTRY TEXT,             -- Land (Name)
      DXCC INTEGER,             -- DXCC-Nummer
      PFX TEXT,                 -- Prefix
      CQZ INTEGER,              -- CQ Zone
      ITUZ INTEGER,             -- ITU Zone
      GRIDSQUARE TEXT,          -- Locator (e.g., JO55RM)
      LAT REAL,                 -- Latitude (N050 51.151)
      LON REAL,                 -- Longitude (E004 49.287)

      -- PERSONAL DATA OF THE PARTNER
      NAME TEXT,            -- Name (First and Last)
      QTH TEXT,             -- Location/City
      ADDRESS TEXT,         -- Complete Address
      EMAIL TEXT,
      AGE INTEGER,
  
      -- eQSL-STATUS
      EQSL_QSL_SENT TEXT,
      EQSL_QSLS_DATE TEXT,      -- Sent Date (YYYYMMDD)
      EQSL_QSL_RCVD TEXT,
      EQSL_QSLR_DATE TEXT,      -- Received Date (YYYYMMDD)
      EQSL_IMAGE_BLOB BLOB,     -- eQSL Image as BLOB  

      
      -- DX-INDEXES (If desired, e.g., SOTA/POTA/IOTA)
      SOTA_REF TEXT,      -- Although not explicitly in the file, retained if needed
      POTA_REF TEXT,      -- Ditto
      IOTA_REF TEXT,      -- Dito
  
      -- UNIQUE constraint for duplicate detection (important!)
      UNIQUE(CALL, QSO_DATE, TIME_ON) 
    );
    """
    cursor.execute(sql_create_table)
    conn.commit()
    print(f"[INFO] database schema ({self.table_name}) checked and created.")


  def import_adif_file(self, adif_filepath: str) -> int:
    """Performs the import process."""
    conn = None 
    
    try:
      # 1. ADIF-Datei parsen
      qso_records, _ = AdifFileIO.read_from_file(adif_filepath)
      
      if not qso_records:
        print("[INFO] Parser found no records to import. Ending.")
        return 0
        
      print(f"[INFO] Found {len(qso_records)} potential QSOs.")

      # 2. Connect to the database
      conn = sqlite3.connect(self.db_filepath)
      cursor = conn.cursor()
      cursor.execute("PRAGMA foreign_keys = ON;")
      
      # 2b. Check/create schema
      self._create_schema(conn)

      # 3. DATA INSERTION AND PREPARATION (including frequency/band logic)
      data_for_insert = []
      for record in qso_records:
        full_record = {}
        
        # Preprocessing frequency (must be a float for band logic)
        freq_val_str = record.get('FREQ', '')
        freq_float = None
        if freq_val_str:
          try:
            # The FREQ in ADIF format is typically in MHz (e.g., 14.074).
            freq_float = float(freq_val_str)
          except ValueError:
            print(f"[WARNING] Invalid FREQ format '{freq_val_str}' for QSO {record.get('CALL')}. Ignoring FREQ/BAND.")
            freq_float = None # Set to None to avoid errors.
        # Band determination
        band_from_adif = record.get('BAND', '').strip()
        
        # HERE IS THE NEW LOGIC: If BAND is missing, try to determine it from FREQ
        if not band_from_adif and freq_float is not None:
          calculated_band = self._get_band_from_freq(freq_float)
          
          if calculated_band:
            # Set the determined band in the record
            record['BAND'] = calculated_band
            # print(f"[DEBUG] Band for {freq_float} MHz set to {calculated_band}.") # Optional debugging

        # Assemble the final record
        for col in DB_COLUMNS:
          value = record.get(col, '')
          
          # Special handling for frequency and BLOB
          if col == 'FREQ':
            # Set FREQ in the database as REAL (Float)
            full_record[col] = freq_float
          elif col == 'EQSL_IMAGE_BLOB' and value == '':
            full_record[col] = None
          # FFor all other columns
          else:
            full_record[col] = value
            
        data_for_insert.append(full_record)

      placeholders = ', '.join([f':{col}' for col in DB_COLUMNS])
      columns = ', '.join(DB_COLUMNS)
      
      # IMPORTANT: INSERT OR IGNORE causes duplicates to be SILENTLY ignored.
      sql_insert = f"""
      INSERT OR IGNORE INTO {self.table_name} ({columns}) 
      VALUES ({placeholders})
      """
      
      cursor.executemany(sql_insert, data_for_insert)
      
      inserted_count = cursor.rowcount
      conn.commit() 
      
      print(f"\n[SUCCESS] ADIF import completed. {inserted_count} NEW records inserted.")
      print(f"[NOTE] {len(qso_records) - inserted_count} records were ignored as duplicates.")

      return inserted_count
      
    except FileNotFoundError as e:
      print(f"[ERROR] File error: {e}")
      return 0
    except AdifParsingError as e:
      print(f"[ERROR] Parsing error: {e}")
      return 0
    except sqlite3.Error as e:
      if conn:
        conn.rollback() 
      print(f"[CRITICAL] SQLite database error (rollback performed): {e}")
      return 0
    except Exception as e:
      print(f"[CRITICAL] An unexpected error occurred: {e}")
      return 0
    finally:
      if conn:
        conn.close()


def main():
  """Runs the import process with the default paths."""
  print("--- ADIF Import Debug Mode ---")
  print(f"ADIF-Path: {DEFAULT_ADIF_PATH}")
  print(f"DB-Path:   {DEFAULT_DB_PATH}")
  print("-------------------------------")

  # Ensure the database directory exists if it is not in the path
  db_dir = os.path.dirname(DEFAULT_DB_PATH)
  if db_dir and not os.path.exists(db_dir):
    os.makedirs(db_dir)
    
  importer = AdifImporter(DEFAULT_DB_PATH)
  importer.import_adif_file(DEFAULT_ADIF_PATH)


if __name__ == "__main__":
  main()