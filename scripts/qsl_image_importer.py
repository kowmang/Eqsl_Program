import os
import sqlite3
import re
from datetime import datetime

class QslImageImporter:
    """
    Responsible for importing image files (.jpg, .png)
    and assigning them to QSO entries in the SQLite database.
    """
    
    # Example filename: Callsign=IK1ICF_VisitorCallsign=OE4VMB_QSODate=2025-09-02_12_19_00_0_Band=20M_Mode=FT8.jpg
    # REGEX pattern to extract QSO keys from the filename
    FILENAME_PATTERN = re.compile(
        r'Callsign=(?P<CALL>.*?)_'
        r'VisitorCallsign=(?P<V_CALL>.*?)_'
        r'QSODate=(?P<QSO_DATE_STR>\d{4}-\d{2}-\d{2})_'
        r'(?P<QSO_TIME_STR>\d{2}_\d{2}_\d{2})_\d+_' 
        r'Band=(?P<BAND>.*?)_'
        r'Mode=(?P<MODE>.*)'
    )

    # IMPORTANT: 'table_name' MUST be passed during instantiation (e.g., 'eqsl_data')
    def __init__(self, db_filepath: str, table_name: str = "eqsl_data"):
        self.db_filepath = db_filepath
        self.table_name = table_name

    def _get_db_connection(self):
        """Establishes a connection to the SQLite database."""
        if not self.db_filepath or not os.path.exists(self.db_filepath):
            raise FileNotFoundError(f"Database file not found: {self.db_filepath}")
        
        return sqlite3.connect(self.db_filepath)

    def _parse_filename(self, filename: str) -> dict | None:
        """Extracts QSO keys from the filename."""
        # Remove the file extension for parsing
        base_name = os.path.splitext(filename)[0]
        match = self.FILENAME_PATTERN.match(base_name)
        
        if not match:
            return None
            
        data = match.groupdict()

        try:
            # Prepare QSO_DATE (YYYYMMDD) and QSO_TIME (HHMMSS) for the query (data is still parsed)
            qso_date_str = data['QSO_DATE_STR'].replace('-', '') 
            qso_time_str = data['QSO_TIME_STR'].replace('_', '') 

            return {
                'qso_date': qso_date_str,
                'qso_time': qso_time_str,
                'call1': data['CALL'].upper(),
                'call2': data['V_CALL'].upper(),
                'mode': data['MODE'].upper(),
                'band': data['BAND'].upper()
                }

        except Exception as e:
            print(f"Error parsing data from filename '{filename}': {e}")
            return None


    def _get_qso_id(self, conn: sqlite3.Connection, qso_data: dict) -> int | None:
        """
        Finds the ROWID of the QSO entry based on the keys (CALL, QSO_DATE, BAND, and MODE).
        """
        
        # 1. Prepare data
        band_val = qso_data['band'].replace('M', '').replace('CM', '')
        
        # 2. SQL query
        # The query looks for (Call1 OR Call2) AND QSO_DATE AND BAND AND MODE.
        sql = f"""
        SELECT ROWID FROM {self.table_name}
        WHERE (UPPER(CALL) = ? OR UPPER(CALL) = ?)
        AND QSO_DATE = ? 
        AND BAND = ? 
        AND UPPER(MODE) = ? 
        LIMIT 1
        """
        
        # 3. Parameter list for the query (5 values: Call1, Call2, Date, Band, Mode)
        params = (
            qso_data['call1'], 
            qso_data['call2'],
            qso_data['qso_date'],  # <-- NEW: Third value for QSO_DATE
            band_val,              # <-- Fourth value for BAND
            qso_data['mode']       # <-- Fifth value for MODE
        )
        
        try:
            cursor = conn.execute(sql, params)
            result = cursor.fetchone()
            # print(f"-> Success: QSO found with ID {result[0]} (CALL, DATE, BAND, and MODE match)") # Optional: Debug output
            return result[0] if result else None
        except Exception as e:
            # Hopefully this error no longer occurs, but the output remains
            print(f"Error during DB query for {qso_data['call1']}/{qso_data['call2']}: {e}")
            return None

    def _image_to_blob(self, image_path: str) -> bytes | None:
        """Converts an image file to a BLOB (bytes)."""
        try:
            with open(image_path, 'rb') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading image file {image_path}: {e}")
            return None
            
    def _is_image_present(self, conn: sqlite3.Connection, qso_id: int) -> bool:
        """Checks if an image is already present for the entry."""
        sql = f"SELECT EQSL_IMAGE_BLOB FROM {self.table_name} WHERE ROWID = ?"
        cursor = conn.execute(sql, (qso_id,))
        result = cursor.fetchone()
        
        # True if the column is not NULL
        return result is not None and result[0] is not None
        
    def _update_qso_with_blob(self, conn: sqlite3.Connection, qso_id: int, blob_data: bytes):
        """Stores the BLOB in the database."""
        sql = f"UPDATE {self.table_name} SET EQSL_IMAGE_BLOB = ? WHERE ROWID = ?"
        conn.execute(sql, (blob_data, qso_id))
        conn.commit()

    def bulk_import_images(self, directory_path: str) -> dict:
        """
        Performs the bulk import:
        1. Searches the directory for .jpg/.png files.
        2. Parses filenames, finds QSO ID, converts image to BLOB, stores it.
        """
        results = {
            'total_files': 0,
            'imported': 0,
            'already_present': 0,
            'not_found': 0,
            'parse_error': 0,
            'file_error': 0
        }
        
        if not os.path.isdir(directory_path):
            print(f"Error: '{directory_path}' is not a valid directory.")
            return results

        file_list = [f for f in os.listdir(directory_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        results['total_files'] = len(file_list)
        
        if not file_list:
            print("No relevant image files (.jpg, .png) found in the directory.")
            return results

        try:
            conn = self._get_db_connection()
            
            for filename in file_list:
                full_path = os.path.join(directory_path, filename)
                # print(f"Processing: {filename}") 
                
                # 1. Parse filename
                qso_data = self._parse_filename(filename)
                if not qso_data:
                    results['parse_error'] += 1
                    continue
                    
                # 2. Find QSO ID
                qso_id = self._get_qso_id(conn, qso_data)
                
                if qso_id is None:
                    # print(f"-> QSO not found: {qso_data['call1']}/{qso_data['call2']} (CALL, DATE, BAND and MODE match)")
                    results['not_found'] += 1
                    continue
                    
                # 3. Check if image is already present
                if self._is_image_present(conn, qso_id):
                    results['already_present'] += 1
                    continue
                    
                # 4. Convert image to BLOB
                blob_data = self._image_to_blob(full_path)
                if not blob_data:
                    results['file_error'] += 1
                    continue
                    
                # 5. DB-Update
                self._update_qso_with_blob(conn, qso_id, blob_data)
                results['imported'] += 1
                
            conn.close()
            
        except FileNotFoundError as e:
            print(f"Critical error: {e}")
        except Exception as e:
            print(f"Unknown import error: {e}")
        
        # Print summary of the import
        print("\n--- Bulk Card Import Summary ---")
        print(f"Total files: {results['total_files']}")
        print(f"Imported: {results['imported']} NEW images saved.")
        print(f"Already present: {results['already_present']}")
        print(f"QSO not found in DB: {results['not_found']}")
        print(f"Parse errors: {results['parse_error']}")
        print(f"File errors (reading): {results['file_error']}")
            
        return results