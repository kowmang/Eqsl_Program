import sqlite3
import os
import adif_io
from PySide6.QtCore import Slot

class AdifImporter:
    """
    Verantwortlich für das Einlesen von ADIF-Dateien, das Parsen der QSOs 
    und das Einfügen neuer Einträge in die SQLite-Datenbank.
    """
    
    # Der Importer benötigt Zugriff auf den SettingsManager, um den DB-Pfad zu bekommen
    def __init__(self, settings_manager):
        self.settings_manager = settings_manager

    @Slot(str)
    def import_adif_file(self, adif_filepath: str) -> int:
        """
        Liest eine ADIF-Datei ein und fügt nur neue QSOs in die 'eqsl_data'-Tabelle ein.
        
        :param adif_filepath: Pfad zur ADIF-Datei.
        :return: Anzahl der neu eingefügten Datensätze.
        """
        db_filepath = self.settings_manager.get_current_db_path()
        table_name = self.settings_manager.settings.get("table_name", "eqsl_data")
        
        if not db_filepath or not os.path.exists(db_filepath):
            print("Error: Datenbankpfad ist nicht gesetzt oder Datei existiert nicht.")
            return 0
        
        if not os.path.exists(adif_filepath):
            print(f"Error: ADIF-Datei nicht gefunden: {adif_filepath}")
            return 0
            
        try:
            # 1. ADIF-Datei parsen
            print(f"Starte Parsing der ADIF-Datei: {adif_filepath}...")
            qso_records, _ = adif_io.read_from_file(adif_filepath)
            print(f"Es wurden {len(qso_records)} QSOs in der ADIF-Datei gefunden.")

            if not qso_records:
                return 0

            # 2. Verbindung zur Datenbank herstellen
            conn = sqlite3.connect(db_filepath)
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")

            inserted_count = 0
            
            # Die Liste der DB-Spalten (muss der Reihenfolge in der SQL-Definition entsprechen!)
            DB_COLUMNS = [
                'CALL', 'QSO_DATE', 'TIME_ON', 
                'BAND', 'MODE', 'SUBMODE', 'FREQ', 'RST_SENT', 'RST_RCVD', 'TX_PWR',
                'CONT', 'COUNTRY', 'DXCC', 'PFX', 'CQZ', 'ITUZ', 'GRIDSQUARE', 'LAT', 'LON',
                'NAME', 'QTH', 'ADDRESS', 'EMAIL', 'AGE',
                'EQSL_QSL_SENT', 'EQSL_QSLS_DATE', 'EQSL_QSL_RCVD', 'EQSL_QSLR_DATE', 
                'EQSL_IMAGE_BLOB', # <-- WICHTIG: Hier kommt das BLOB-Feld
                'SOTA_REF', 'POTA_REF', 'IOTA_REF',
                'QSO_COMPLETE', 'TIME_OFF', 'QSO_DATE_OFF'
            ]
            
            # Wir verwenden die Spaltennamen direkt als ADIF-Tags (alles GROSS)
            # Das fields_map-Dictionary ist hier nicht mehr nötig,
            # da die DB-Spalten exakt den ADIF-Tags entsprechen.

            for record in qso_records:
                
                # Stelle sicher, dass die wichtigsten Duplikat-Schlüssel existieren
                if not record.get('CALL') or not record.get('QSO_DATE') or not record.get('TIME_ON'):
                    continue
                
                # Daten für den INSERT-Befehl in der korrekten Reihenfolge vorbereiten
                values = []
                for col in DB_COLUMNS:
                    raw_value = record.get(col)
                    
                    if raw_value is not None:
                        # Bereinigung des Strings
                        if isinstance(raw_value, str):
                             raw_value = raw_value.strip()

                    # ----------------------------------------------------
                    # 1. Spezielle Konvertierung für numerische Felder
                    # ----------------------------------------------------
                    if col in ['FREQ', 'TX_PWR', 'LAT', 'LON']:
                        try:
                            values.append(float(raw_value) if raw_value else None)
                        except ValueError:
                            values.append(None)
                            
                    elif col in ['DXCC', 'CQZ', 'ITUZ', 'AGE']:
                        try:
                            # Wir setzen DXCC, CQZ, ITUZ, AGE als INTEGER
                            values.append(int(raw_value) if raw_value else None)
                        except ValueError:
                            values.append(None)

                    # ----------------------------------------------------
                    # 2. Spezieller Eintrag für BLOB
                    # ----------------------------------------------------
                    elif col == 'EQSL_IMAGE_BLOB':
                        # Da das ADIF-File selbst keine Bilddaten enthält, 
                        # wird das Feld initial auf None gesetzt (NULL in SQLite).
                        values.append(None) 
                        
                    # ----------------------------------------------------
                    # 3. Standard Text-Felder
                    # ----------------------------------------------------
                    else:
                        values.append(raw_value)


                # 3. Datenbankabfrage zum Einfügen mit IGNORE
                placeholders = ', '.join(['?'] * len(DB_COLUMNS))
                columns = ', '.join(DB_COLUMNS)
                
                insert_sql = f"""
                INSERT OR IGNORE INTO {table_name} ({columns})
                VALUES ({placeholders})
                """
                
                try:
                    cursor.execute(insert_sql, tuple(values))
                    
                    # lastrowid != 0 bedeutet, dass eine Zeile eingefügt wurde (kein Duplikat)
                    if cursor.lastrowid != 0:
                        inserted_count += 1
                        
                except sqlite3.Error as e:
                    print(f"DB Error beim Einfügen von {record.get('CALL')}/{record.get('QSO_DATE')}: {e}")
                    
            conn.commit()
            conn.close()
            print(f"ADIF-Import abgeschlossen. {inserted_count} neue Datensätze eingefügt.")
            return inserted_count
            
        except adif_io.AdifParsingError as e:
            print(f"Fehler beim Parsen der ADIF-Datei: {e}")
            return 0
        except sqlite3.Error as e:
            print(f"SQLite Verbindungs- oder Commit-Fehler: {e}")
            return 0
        except Exception as e:
            print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
            return 0