import os
import sqlite3
import re # Although not necessary for single import, it remains for the basic definition..
from datetime import datetime
from typing import Dict, Any

# --- BASE CLASS (Assuming it exists in a separate file or here) ---
# It provides the generic database and blob functions.
class QslImageImporterBasis:
    """
    Base class for QSL image imports, contains the generic
    functions for DB connection, QSO search, blob conversion, and update.
    """
    
    # Example filename: Callsign=IK1ICF_VisitorCallsign=OE4VMB_QSODate=2025-09-02_12_19_00_0_Band=20M_Mode=FT8.jpg
    # REGEX pattern is not used for single import, but remains for the base definition.
    FILENAME_PATTERN = re.compile(r'Callsign=(?P<CALL>.*?)_.*')

    def __init__(self, db_filepath: str, table_name: str = "eqsl_data"):
        self.db_filepath = db_filepath
        self.table_name = table_name

    def _get_db_connection(self):
        """Establishes a connection to the SQLite database."""
        if not self.db_filepath or not os.path.exists(self.db_filepath):
            # Allows raising an error that can be caught by the caller (e.g., the GUI).
            raise FileNotFoundError(f"Database file not found: {self.db_filepath}")
        return sqlite3.connect(self.db_filepath)

    def _get_qso_id(self, conn: sqlite3.Connection, qso_data: dict) -> int | None:
        """
        Finds the ROWID of the QSO entry based on the keys 
        (CALL, QSO_DATE, BAND and MODE) from the manually entered data.
        """
        
        # 1. Prepare data
        band_val = qso_data['band'].replace('M', '').replace('CM', '')
        call_val = qso_data['call'].upper()
        
        # 2. SQL query
        # The query looks for whether the entered call matches the CALL field in the log.
        # It might make sense to search for either the user's call OR the partner's call.
        # Here, only the main CALL field (partner) is checked, as the user enters the partner call.
        sql = f"""
        SELECT ROWID FROM {self.table_name}
        WHERE UPPER(CALL) = ?
        AND QSO_DATE = ? 
        AND BAND = ? 
        AND UPPER(MODE) = ? 
        LIMIT 1
        """
        
        # 3. Parameter list for the query (4 values: Call, Date, Band, Mode)
        params = (
            call_val,
            qso_data['qso_date'],  # Format: YYYYMMDD
            band_val,              # E.g., '20' for 20M
            qso_data['mode'].upper()
        )
        
        try:
            cursor = conn.execute(sql, params)
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            # Report error during query process
            print(f"Error during DB query for {call_val}: {e}")
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
        """Checks if an image is already present for the entry (EQSL_IMAGE_BLOB != NULL)."""
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

# --- NEW CLASS FOR MANUAL IMPORT ---

class QslSingleImageImporter(QslImageImporterBasis):
    """
    Imports a single QSL image based on manually entered
    QSO data (Call, Date, Band, Mode) and an image path.
    """
    
    def __init__(self, db_filepath: str, table_name: str = "eqsl_data"):
        # Calls the constructor of the base class to initialize DB path and table name
        super().__init__(db_filepath, table_name)
    
    def _validate_and_format_data(self, data: Dict[str, str]) -> Dict[str, str] | None:
        """Validates and formats the manually entered data for the DB query."""
        
        # 1. Check if all required fields are present
        required_fields = ['call', 'date', 'band', 'mode', 'path']
        if not all(field in data and data[field].strip() for field in required_fields):
            print("Error: All fields (Callsign, Date, Band, Mode, Path) must be filled.")
            return None
        
        # 2. Convert date to YYYYMMDD format (important for DB query)
        try:
            date_input = data['date'].strip()
            
            # Try to parse common formats (YYYY-MM-DD, DD.MM.YYYY)
            if re.match(r'\d{4}-\d{2}-\d{2}', date_input):
                date_obj = datetime.strptime(date_input, '%Y-%m-%d')
            elif re.match(r'\d{2}\.\d{2}\.\d{4}', date_input):
                date_obj = datetime.strptime(date_input, '%d.%m.%Y')
            else:
                print(f"Invalid date format: {date_input}. Expected YYYY-MM-DD or DD.MM.YYYY.")
                return None
                
            formatted_date = date_obj.strftime('%Y%m%d') # Format for the DB
            
        except ValueError as e:
            print(f"Error parsing date: {e}")
            return None


        # 3. Check path and file type
        file_path = data['path'].strip()
        if not os.path.exists(file_path):
            print(f"Error: File not found at: {file_path}")
            return None
            
        if not file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            print(f"Error: Invalid file type for {file_path}. Only .jpg and .png allowed.")
            return None
            
        # 4. Return cleaned data
        return {
            'call': data['call'].strip().upper(),
            'qso_date': formatted_date, # YYYYMMDD
            'band': data['band'].strip().upper(),
            'mode': data['mode'].strip().upper(),
            'path': file_path
        }

    def import_single_image(self, callsign: str, date: str, band: str, mode: str, image_path: str) -> Dict[str, Any]:
        """
        Performs the single import based on manual data.

        :param callsign: CALL field from the GUI
        :param date: DATE field from the GUI
        :param band: BAND field from the GUI
        :param mode: MODE field from the GUI
        :param image_path: Path to the image from the GUI
        :return: Result dictionary with 'success' and 'message'
        """
        
        results = {
            'success': False,
            'message': "Import failed.",
            'qso_id': None,
            'reason': ''
        }
        
        # 1. Validate and format data
        raw_data = {'call': callsign, 'date': date, 'band': band, 'mode': mode, 'path': image_path}
        qso_data = self._validate_and_format_data(raw_data)
        
        if qso_data is None:
            results['reason'] = "Error in data validation/formatting or invalid path."
            return results

        try:
            conn = self._get_db_connection()
            
            # 2. Find QSO-ID (match by Call, Date, Band, Mode)
            qso_id = self._get_qso_id(conn, qso_data)
            
            if qso_id is None:
                results['message'] = "QSO not found in the database."
                results['reason'] = f"Combination: CALL={qso_data['call']}, DATE={qso_data['qso_date']}, BAND={qso_data['band']}, MODE={qso_data['mode']}"
                conn.close()
                return results

            # 3. Check if image is already present
            if self._is_image_present(conn, qso_id):
                results['message'] = f"QSO found (ID {qso_id}), but an image is already present. (Not saved)"
                results['success'] = True 
                results['qso_id'] = qso_id
                conn.close()
                return results
                
            # 4. Convert image to BLOB
            blob_data = self._image_to_blob(qso_data['path'])
            if not blob_data:
                results['message'] = "Error converting image file to BLOB."
                results['reason'] = "The file could not be read."
                conn.close()
                return results
                
            # 5. DB-Update
            self._update_qso_with_blob(conn, qso_id, blob_data)
            
            results['success'] = True
            results['qso_id'] = qso_id
            results['message'] = f"Import successful! Image saved to QSO entry ID {qso_id}."
            
            conn.close()
            
        except FileNotFoundError as e:
            results['message'] = "Critical error: Database file not found."
            results['reason'] = str(e)
        except Exception as e:
            results['message'] = "Unknown error during import."
            results['reason'] = str(e)
            
        return results

# Example usage in a main script (optional, for illustration only)
if __name__ == '__main__':
    # WARNING: 'your_log_data.db' and 'eqsl_data' must be adapted to your actual environment!
    DB_PATH = "your_log_data.db" 
    TABLE_NAME = "eqsl_data"
    
    # Simulate a successful input
    CALL = "OE4VMB"
    DATE = "2025-09-02" 
    BAND = "20M"
    MODE = "FT8"
    # The path must point to an existing JPG/PNG image
    IMAGE_PATH = "/path/to/my/OE4VMB_QSL_image.jpg" 
    
    print(f"Starting single import for QSO: {CALL} on {DATE} on {BAND} in {MODE}...")
    
    try:
        # Here you would instantiate QslSingleImageImporter in the GUI controller
        importer = QslSingleImageImporter(DB_PATH, TABLE_NAME)
        
        # Perform the import
        import_result = importer.import_single_image(CALL, DATE, BAND, MODE, IMAGE_PATH)
        
        print("\n--- Import Result ---")
        print(f"Success: {import_result['success']}")
        print(f"Message: {import_result['message']}")
        if import_result.get('reason'):
             print(f"Reason: {import_result['reason']}")

    except FileNotFoundError as e:
        print(f"\nFATAL ERROR: {e}")
    except Exception as e:
        print(f"\nUnhandled error: {e}")