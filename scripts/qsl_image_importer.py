import os
import sqlite3
import re
from datetime import datetime

class QslImageImporter:
    """
    Verantwortlich für das Einlesen von Bilddateien (.jpg, .png)
    und deren Zuordnung zu QSO-Einträgen in der SQLite-Datenbank.
    """
    
    # Beispiel Dateiname: Callsign=IK1ICF_VisitorCallsign=OE4VMB_QSODate=2025-09-02_12_19_00_0_Band=20M_Mode=FT8.jpg
    # REGEX-Muster zum Extrahieren der QSO-Schlüssel aus dem Dateinamen
    FILENAME_PATTERN = re.compile(
        r'Callsign=(?P<CALL>.*?)_'
        r'VisitorCallsign=(?P<V_CALL>.*?)_'
        r'QSODate=(?P<QSO_DATE_STR>\d{4}-\d{2}-\d{2})_'
        r'(?P<QSO_TIME_STR>\d{2}_\d{2}_\d{2})_\d+_' 
        r'Band=(?P<BAND>.*?)_'
        r'Mode=(?P<MODE>.*)'
    )

    # WICHTIG: 'table_name' MUSS beim Instanziieren übergeben werden (z.B. 'eqsl_data')
    def __init__(self, db_filepath: str, table_name: str = "eqsl_data"):
        self.db_filepath = db_filepath
        self.table_name = table_name

    def _get_db_connection(self):
        """Stellt eine Verbindung zur SQLite-Datenbank her."""
        if not self.db_filepath or not os.path.exists(self.db_filepath):
            raise FileNotFoundError(f"Datenbankdatei nicht gefunden: {self.db_filepath}")
        
        return sqlite3.connect(self.db_filepath)

    def _parse_filename(self, filename: str) -> dict | None:
        """Extrahiert QSO-Schlüssel aus dem Dateinamen."""
        # Entferne die Dateiendung für das Parsen
        base_name = os.path.splitext(filename)[0]
        match = self.FILENAME_PATTERN.match(base_name)
        
        if not match:
            return None
            
        data = match.groupdict()

        try:
            # QSO_DATE (YYYYMMDD) und QSO_TIME (HHMMSS) für die Abfrage vorbereiten (Daten werden trotzdem geparst)
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
            print(f"Fehler beim Parsen der Daten aus Dateiname '{filename}': {e}")
            return None


    def _get_qso_id(self, conn: sqlite3.Connection, qso_data: dict) -> int | None:
        """
        Findet die ROWID des QSO-Eintrags basierend auf den Schlüsseln (CALL, QSO_DATE, BAND und MODE).
        """
        
        # 1. Daten vorbereiten
        band_val = qso_data['band'].replace('M', '').replace('CM', '')
        
        # 2. SQL-Abfrage
        # Die Abfrage sucht nach (Call1 ODER Call2) UND QSO_DATE UND BAND UND MODE.
        sql = f"""
        SELECT ROWID FROM {self.table_name}
        WHERE (UPPER(CALL) = ? OR UPPER(CALL) = ?)
        AND QSO_DATE = ? 
        AND BAND = ? 
        AND UPPER(MODE) = ? 
        LIMIT 1
        """
        
        # 3. Parameterliste für die Abfrage (5 Werte: Call1, Call2, Date, Band, Mode)
        params = (
            qso_data['call1'], 
            qso_data['call2'],
            qso_data['qso_date'],  # <-- NEU: Dritter Wert für QSO_DATE
            band_val,              # <-- Vierter Wert für BAND
            qso_data['mode']       # <-- Fünfter Wert für MODE
        )
        
        try:
            cursor = conn.execute(sql, params)
            result = cursor.fetchone()
            # print(f"-> Erfolg: QSO gefunden mit ID {result[0]} (CALL, DATE, BAND und MODE-Abgleich)") # Optional: Debug-Ausgabe
            return result[0] if result else None
        except Exception as e:
            # Der Fehler tritt nun hoffentlich nicht mehr auf, aber die Ausgabe bleibt
            print(f"Fehler bei der DB-Abfrage für {qso_data['call1']}/{qso_data['call2']}: {e}")
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
        """Prüft, ob für den Eintrag bereits ein Bild vorhanden ist."""
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

    def bulk_import_images(self, directory_path: str) -> dict:
        """
        Führt den Massenimport durch:
        1. Durchsucht das Verzeichnis nach .jpg/.png.
        2. Parst Dateinamen, sucht QSO-ID, konvertiert Bild in BLOB, speichert.
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
            print(f"Fehler: '{directory_path}' ist kein gültiger Ordner.")
            return results

        file_list = [f for f in os.listdir(directory_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        results['total_files'] = len(file_list)
        
        if not file_list:
            print("Keine relevanten Bilddateien (.jpg, .png) im Ordner gefunden.")
            return results

        try:
            conn = self._get_db_connection()
            
            for filename in file_list:
                full_path = os.path.join(directory_path, filename)
                # print(f"Verarbeite: {filename}") 
                
                # 1. Dateiname parsen
                qso_data = self._parse_filename(filename)
                if not qso_data:
                    results['parse_error'] += 1
                    continue
                    
                # 2. QSO-ID finden
                qso_id = self._get_qso_id(conn, qso_data)
                
                if qso_id is None:
                    # print(f"-> QSO nicht gefunden: {qso_data['call1']}/{qso_data['call2']} (CALL, DATE, BAND und MODE-Abgleich)")
                    results['not_found'] += 1
                    continue
                    
                # 3. Prüfen, ob Bild bereits vorhanden
                if self._is_image_present(conn, qso_id):
                    results['already_present'] += 1
                    continue
                    
                # 4. Bild in BLOB konvertieren
                blob_data = self._image_to_blob(full_path)
                if not blob_data:
                    results['file_error'] += 1
                    continue
                    
                # 5. DB-Update
                self._update_qso_with_blob(conn, qso_id, blob_data)
                results['imported'] += 1
                
            conn.close()
            
        except FileNotFoundError as e:
            print(f"Kritischer Fehler: {e}")
        except Exception as e:
            print(f"Unbekannter Import-Fehler: {e}")
        
        # Zusammenfassung des Imports ausgeben
        print("\n--- Zusammenfassung Bulk Card Import ---")
        print(f"Gesamtdateien: {results['total_files']}")
        print(f"Importiert: {results['imported']} NEUE Bilder gespeichert.")
        print(f"Bereits vorhanden: {results['already_present']}")
        print(f"QSO nicht in DB gefunden: {results['not_found']}")
        print(f"Parse-Fehler: {results['parse_error']}")
        print(f"Datei-Fehler (Lesen): {results['file_error']}")
            
        return results