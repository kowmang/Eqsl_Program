import os
import sqlite3
import re # Obwohl für Single-Import nicht nötig, bleibt es für die Basis-Definition.
from datetime import datetime
from typing import Dict, Any

# --- BASISKLASSE (Angenommen, sie existiert in einer separaten Datei oder hier) ---
# Sie stellt die generischen Datenbank- und Blob-Funktionen bereit.
class QslImageImporterBasis:
    """
    Basisklasse für QSL-Bild-Importe, enthält die generischen
    Funktionen für DB-Verbindung, QSO-Suche, Blob-Konvertierung und Update.
    """
    
    # Beispiel Dateiname: Callsign=IK1ICF_VisitorCallsign=OE4VMB_QSODate=2025-09-02_12_19_00_0_Band=20M_Mode=FT8.jpg
    # REGEX-Muster wird für den Single-Import nicht verwendet, bleibt aber für die Basis-Definition.
    FILENAME_PATTERN = re.compile(r'Callsign=(?P<CALL>.*?)_.*')

    def __init__(self, db_filepath: str, table_name: str = "eqsl_data"):
        self.db_filepath = db_filepath
        self.table_name = table_name

    def _get_db_connection(self):
        """Stellt eine Verbindung zur SQLite-Datenbank her."""
        if not self.db_filepath or not os.path.exists(self.db_filepath):
            # Erlaubt das Werfen eines Fehlers, der im Aufrufer (z.B. der GUI) gefangen wird.
            raise FileNotFoundError(f"Datenbankdatei nicht gefunden: {self.db_filepath}")
        return sqlite3.connect(self.db_filepath)

    def _get_qso_id(self, conn: sqlite3.Connection, qso_data: dict) -> int | None:
        """
        Findet die ROWID des QSO-Eintrags basierend auf den Schlüsseln 
        (CALL, QSO_DATE, BAND und MODE) aus den manuell eingegebenen Daten.
        """
        
        # 1. Daten vorbereiten
        band_val = qso_data['band'].replace('M', '').replace('CM', '')
        call_val = qso_data['call'].upper()
        
        # 2. SQL-Abfrage
        # Die Abfrage sucht, ob das eingegebene Call mit dem CALL-Feld im Log übereinstimmt.
        # Es kann sinnvoll sein, nach dem eigenen Call ODER dem Partner Call zu suchen.
        # Hier wird nur das Haupt-CALL-Feld (Partner) geprüft, da der Anwender den Partner Call eingibt.
        sql = f"""
        SELECT ROWID FROM {self.table_name}
        WHERE UPPER(CALL) = ?
        AND QSO_DATE = ? 
        AND BAND = ? 
        AND UPPER(MODE) = ? 
        LIMIT 1
        """
        
        # 3. Parameterliste für die Abfrage (4 Werte: Call, Date, Band, Mode)
        params = (
            call_val,
            qso_data['qso_date'],  # Format: YYYYMMDD
            band_val,              # Z.B. '20' für 20M
            qso_data['mode'].upper()
        )
        
        try:
            cursor = conn.execute(sql, params)
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            # Fehler im Abfrage-Prozess melden
            print(f"Fehler bei der DB-Abfrage für {call_val}: {e}")
            return None

    def _image_to_blob(self, image_path: str) -> bytes | None:
        """Konvertiert eine Bilddatei in ein BLOB (bytes)."""
        try:
            with open(image_path, 'rb') as f:
                return f.read()
        except Exception as e:
            print(f"Fehler beim Lesen der Bilddatei {image_path}: {e}")
            return None
            
    def _is_image_present(self, conn: sqlite3.Connection, qso_id: int) -> bool:
        """Prüft, ob für den Eintrag bereits ein Bild vorhanden ist (EQSL_IMAGE_BLOB != NULL)."""
        sql = f"SELECT EQSL_IMAGE_BLOB FROM {self.table_name} WHERE ROWID = ?"
        cursor = conn.execute(sql, (qso_id,))
        result = cursor.fetchone()
        
        # True, wenn die Spalte nicht NULL ist
        return result is not None and result[0] is not None
        
    def _update_qso_with_blob(self, conn: sqlite3.Connection, qso_id: int, blob_data: bytes):
        """Speichert das BLOB in der Datenbank."""
        sql = f"UPDATE {self.table_name} SET EQSL_IMAGE_BLOB = ? WHERE ROWID = ?"
        conn.execute(sql, (blob_data, qso_id))
        conn.commit()

# --- NEUE KLASSE FÜR MANUELLEN IMPORT ---

class QslSingleImageImporter(QslImageImporterBasis):
    """
    Importiert ein einzelnes QSL-Bild basierend auf manuell eingegebenen
    QSO-Daten (Call, Date, Band, Mode) und einem Bildpfad.
    """
    
    def __init__(self, db_filepath: str, table_name: str = "eqsl_data"):
        # Ruft den Konstruktor der Basisklasse auf, um DB-Pfad und Tabellennamen zu initialisieren
        super().__init__(db_filepath, table_name)
    
    def _validate_and_format_data(self, data: Dict[str, str]) -> Dict[str, str] | None:
        """Validiert und formatiert die manuell eingegebenen Daten für die DB-Abfrage."""
        
        # 1. Prüfen, ob alle notwendigen Felder vorhanden sind
        required_fields = ['call', 'date', 'band', 'mode', 'path']
        if not all(field in data and data[field].strip() for field in required_fields):
            print("Fehler: Alle Felder (Callsign, Date, Band, Mode, Path) müssen ausgefüllt sein.")
            return None
        
        # 2. Datum in YYYYMMDD Format konvertieren (wichtig für die DB-Abfrage)
        try:
            date_input = data['date'].strip()
            
            # Versuche, gängige Formate zu parsen (YYYY-MM-DD, TT.MM.YYYY)
            if re.match(r'\d{4}-\d{2}-\d{2}', date_input):
                date_obj = datetime.strptime(date_input, '%Y-%m-%d')
            elif re.match(r'\d{2}\.\d{2}\.\d{4}', date_input):
                date_obj = datetime.strptime(date_input, '%d.%m.%Y')
            else:
                print(f"Ungültiges Datumsformat: {date_input}. Erwarte YYYY-MM-DD oder TT.MM.YYYY.")
                return None
                
            formatted_date = date_obj.strftime('%Y%m%d') # Format für die DB
            
        except ValueError as e:
            print(f"Fehler beim Parsen des Datums: {e}")
            return None


        # 3. Pfad und Dateityp prüfen
        file_path = data['path'].strip()
        if not os.path.exists(file_path):
            print(f"Fehler: Datei nicht gefunden unter: {file_path}")
            return None
            
        if not file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            print(f"Fehler: Ungültiger Dateityp für {file_path}. Nur .jpg und .png erlaubt.")
            return None
            
        # 4. Bereinigte Daten zurückgeben
        return {
            'call': data['call'].strip().upper(),
            'qso_date': formatted_date, # YYYYMMDD
            'band': data['band'].strip().upper(),
            'mode': data['mode'].strip().upper(),
            'path': file_path
        }

    def import_single_image(self, callsign: str, date: str, band: str, mode: str, image_path: str) -> Dict[str, Any]:
        """
        Führt den Einzelimport basierend auf manuellen Daten durch.

        :param callsign: CALL-Feld aus der GUI
        :param date: DATE-Feld aus der GUI
        :param band: BAND-Feld aus der GUI
        :param mode: MODE-Feld aus der GUI
        :param image_path: Pfad zum Bild aus der GUI
        :return: Ergebnis-Dictionary mit 'success' und 'message'
        """
        
        results = {
            'success': False,
            'message': "Import fehlgeschlagen.",
            'qso_id': None,
            'reason': ''
        }
        
        # 1. Daten validieren und formatieren
        raw_data = {'call': callsign, 'date': date, 'band': band, 'mode': mode, 'path': image_path}
        qso_data = self._validate_and_format_data(raw_data)
        
        if qso_data is None:
            results['reason'] = "Fehler bei der Datenvalidierung/Formatierung oder ungültiger Pfad."
            return results

        try:
            conn = self._get_db_connection()
            
            # 2. QSO-ID finden (Abgleich über Call, Datum, Band, Mode)
            qso_id = self._get_qso_id(conn, qso_data)
            
            if qso_id is None:
                results['message'] = "QSO nicht in der Datenbank gefunden."
                results['reason'] = f"Kombination: CALL={qso_data['call']}, DATE={qso_data['qso_date']}, BAND={qso_data['band']}, MODE={qso_data['mode']}"
                conn.close()
                return results

            # 3. Prüfen, ob Bild bereits vorhanden
            if self._is_image_present(conn, qso_id):
                results['message'] = f"QSO gefunden (ID {qso_id}), aber es ist bereits ein Bild vorhanden. (Nicht gespeichert)"
                results['success'] = True 
                results['qso_id'] = qso_id
                conn.close()
                return results
                
            # 4. Bild in BLOB konvertieren
            blob_data = self._image_to_blob(qso_data['path'])
            if not blob_data:
                results['message'] = "Fehler beim Konvertieren der Bilddatei in BLOB."
                results['reason'] = "Die Datei konnte nicht gelesen werden."
                conn.close()
                return results
                
            # 5. DB-Update
            self._update_qso_with_blob(conn, qso_id, blob_data)
            
            results['success'] = True
            results['qso_id'] = qso_id
            results['message'] = f"Import erfolgreich! Bild zu QSO-Eintrag ID {qso_id} gespeichert."
            
            conn.close()
            
        except FileNotFoundError as e:
            results['message'] = "Kritischer Fehler: Datenbankdatei nicht gefunden."
            results['reason'] = str(e)
        except Exception as e:
            results['message'] = "Unbekannter Fehler während des Imports."
            results['reason'] = str(e)
            
        return results

# Beispiel für die Verwendung in einem Haupt-Skript (optional, nur zur Veranschaulichung)
if __name__ == '__main__':
    # ACHTUNG: 'your_log_data.db' und 'eqsl_data' müssen an Ihre tatsächliche Umgebung angepasst werden!
    DB_PATH = "your_log_data.db" 
    TABLE_NAME = "eqsl_data"
    
    # Simuliere eine erfolgreiche Eingabe
    CALL = "OE4VMB"
    DATE = "2025-09-02" 
    BAND = "20M"
    MODE = "FT8"
    # Der Pfad muss auf ein existierendes JPG/PNG-Bild zeigen
    IMAGE_PATH = "/path/to/my/OE4VMB_QSL_image.jpg" 
    
    print(f"Starte Einzelimport für QSO: {CALL} am {DATE} auf {BAND} in {MODE}...")
    
    try:
        # Hier würden Sie QslSingleImageImporter im GUI-Controller instanziieren
        importer = QslSingleImageImporter(DB_PATH, TABLE_NAME)
        
        # Führe den Import durch
        import_result = importer.import_single_image(CALL, DATE, BAND, MODE, IMAGE_PATH)
        
        print("\n--- Import Ergebnis ---")
        print(f"Erfolg: {import_result['success']}")
        print(f"Nachricht: {import_result['message']}")
        if import_result.get('reason'):
             print(f"Grund: {import_result['reason']}")

    except FileNotFoundError as e:
        print(f"\nFATALER FEHLER: {e}")
    except Exception as e:
        print(f"\nUnbehandelter Fehler: {e}")