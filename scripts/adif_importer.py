import sqlite3
import os
import re
import sys
from typing import List, Dict, Tuple

# --------------------------------------------------------------------------------
# KONFIGURATION & STRUKTUR
# --------------------------------------------------------------------------------

# PASSEN SIE DIESE PFADE AN IHRE ECHTE UMGEBUNG AN!
# Der ADIF-Pfad aus Ihrer letzten Konsolenausgabe:
DEFAULT_ADIF_PATH = "C:/Users/oe4vm/Desktop/Proggen/test.adi"
# Der DB-Pfad aus Ihrer letzten Konsolenausgabe:
DEFAULT_DB_PATH = "C:/Users/oe4vm/Desktop/Proggen/eqsl_program/Eqsl_Program/database_sql/new_test_db_51.db"

# Liste der Spalten, die in die Datenbank eingefügt werden sollen.
DB_COLUMNS = [
    'CALL', 'QSO_DATE', 'TIME_ON', 'BAND', 'MODE', 'SUBMODE', 'FREQ', 'RST_SENT', 'RST_RCVD',
    'TX_PWR', 'CONT', 'COUNTRY', 'DXCC', 'PFX', 'CQZ', 'ITUZ', 'GRIDSQUARE', 'LAT', 'LON',
    'NAME', 'QTH', 'ADDRESS', 'EMAIL', 'AGE', 'EQSL_QSL_SENT', 'EQSL_QSLS_DATE', 'EQSL_QSL_RCVD',
    'EQSL_QSLR_DATE', 'EQSL_IMAGE_BLOB', 'SOTA_REF', 'POTA_REF', 'IOTA_REF'
]

# Regulärer Ausdruck zur Extraktion von ADIF-Tags: <TAG:LÄNGE>WERT
# (Die Tag-Namen werden hierbei in Großbuchstaben umgewandelt)
ADIF_REGEX = re.compile(r'<(\w+):(\d+)>([^<]+)', re.IGNORECASE) 

# --------------------------------------------------------------------------------
# KLASSEN FÜR PARSING UND IMPORT
# --------------------------------------------------------------------------------

class AdifParsingError(Exception):
    """Benutzerdefinierte Ausnahme für ADIF-Parsing-Fehler."""
    pass

class AdifFileIO:
    """Liest und parst eine tatsächliche ADIF-Datei."""
    @staticmethod
    def read_from_file(filepath: str) -> Tuple[List[Dict[str, str]], Dict[str, str]]:
        """
        Liest eine ADIF-Datei, parst die QSOs und gibt sie als Liste von Dictionaries zurück.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Die ADIF-Datei wurde nicht gefunden: {filepath}")

        print(f"[DEBUG] Lese Datei: {filepath}")
        try:
            # Versuche, die Datei mit verschiedenen Codierungen zu lesen (häufiges Problem bei ADIF)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().upper()
        except Exception as e:
            raise AdifParsingError(f"Fehler beim Lesen der Datei: {e}")

        qso_records = []
        is_header = True

        # ADIF-Daten nach dem End of Record Tag trennen
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
                # Bereinige den Wert und stelle sicher, dass der Tag großgeschrieben wird
                tag = tag.upper()
                value = value.strip()
                
                if tag in ['EOZ', 'ADIF_VER', 'CREATOR', 'PROGRAMID']:
                    continue
                
                # Prüfen, ob wir nach dem Header in den QSO-Teil gewechselt sind
                if tag in ['CALL', 'QSO_DATE', 'TIME_ON']:
                    is_header = False
                    record_is_qso = True # Markiere diesen Datensatz als potenzielles QSO

                if record_is_qso and tag in DB_COLUMNS:
                    current_qso[tag] = value

            if record_is_qso:
                # Stellen Sie sicher, dass die minimalen UNIQUE-Felder vorhanden sind
                if all(key in current_qso for key in ['CALL', 'QSO_DATE', 'TIME_ON']):
                    qso_records.append(current_qso)
                else:
                    print(f"[WARNUNG] QSO ignoriert (fehlende Schlüssel): {current_qso.get('CALL', 'NOCALL')}")

        if not qso_records:
            print("[WARNUNG] Der Parser fand keine gültigen QSO-Einträge in der Datei.")
            
        return qso_records, {}


class AdifImporter:
    """Importiert QSOs aus einer ADIF-Datei in eine SQLite-Datenbank."""
    
    def __init__(self, db_filepath: str):
        self.db_filepath = db_filepath
        self.table_name = "eqsl_data"

    def _create_schema(self, conn: sqlite3.Connection):
        """Erstellt die eqsl_data Tabelle, falls sie noch nicht existiert."""
        cursor = conn.cursor()
        # HIER IST DER SCHUTZ VOR DUPLIKATEN:
        # Nur Kombinationen von CALL, QSO_DATE und TIME_ON, die noch nicht existieren, werden eingefügt.
        sql_create_table = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
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
        cursor.execute(sql_create_table)
        conn.commit()
        print(f"[INFO] Datenbank-Schema ({self.table_name}) geprüft und erstellt.")


    def import_adif_file(self, adif_filepath: str) -> int:
        """Führt den Import-Prozess durch."""
        conn = None 
        
        try:
            # 1. ADIF-Datei parsen
            qso_records, _ = AdifFileIO.read_from_file(adif_filepath)
            
            if not qso_records:
                print("[INFO] Der Parser fand keine Datensätze zum Importieren. Ende.")
                return 0
                
            print(f"[INFO] Es wurden {len(qso_records)} potenzielle QSOs gefunden.")

            # 2. Verbindung zur Datenbank herstellen
            conn = sqlite3.connect(self.db_filepath)
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            
            # 2b. Schema prüfen/erstellen
            self._create_schema(conn)

            # 3. DATENEINFÜGUNG
            data_for_insert = []
            for record in qso_records:
                full_record = {}
                for col in DB_COLUMNS:
                    # Stelle sicher, dass jeder Datensatz alle Spalten enthält (fehlende als leere Strings)
                    full_record[col] = record.get(col, '')
                data_for_insert.append(full_record)

            placeholders = ', '.join([f':{col}' for col in DB_COLUMNS])
            columns = ', '.join(DB_COLUMNS)
            
            # WICHTIG: INSERT OR IGNORE führt dazu, dass Duplikate STILLSCHWEIGEND ignoriert werden.
            sql_insert = f"""
            INSERT OR IGNORE INTO {self.table_name} ({columns}) 
            VALUES ({placeholders})
            """
            
            cursor.executemany(sql_insert, data_for_insert)
            
            inserted_count = cursor.rowcount
            conn.commit() 
            
            print(f"\n[ERFOLG] ADIF-Import abgeschlossen. {inserted_count} NEUE Datensätze eingefügt.")
            print(f"[HINWEIS] {len(qso_records) - inserted_count} Datensätze wurden als Duplikate ignoriert.")

            return inserted_count
            
        except FileNotFoundError as e:
            print(f"[FEHLER] Dateifehler: {e}")
            return 0
        except AdifParsingError as e:
            print(f"[FEHLER] Parsing-Fehler: {e}")
            return 0
        except sqlite3.Error as e:
            if conn:
                conn.rollback() 
            print(f"[KRITISCH] SQLite Datenbankfehler (Rollback durchgeführt): {e}")
            return 0
        except Exception as e:
            print(f"[KRITISCH] Ein unerwarteter Fehler ist aufgetreten: {e}")
            return 0
        finally:
             if conn:
                conn.close()


def main():
    """Führt den Importprozess mit den Standardpfaden aus."""
    print("--- ADIF Import Debug-Modus ---")
    print(f"ADIF-Pfad: {DEFAULT_ADIF_PATH}")
    print(f"DB-Pfad:   {DEFAULT_DB_PATH}")
    print("-------------------------------")

    # Stellen Sie sicher, dass die Datenbank existiert, falls sie nicht im Pfad liegt
    db_dir = os.path.dirname(DEFAULT_DB_PATH)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
        
    importer = AdifImporter(DEFAULT_DB_PATH)
    importer.import_adif_file(DEFAULT_ADIF_PATH)


if __name__ == "__main__":
    main()