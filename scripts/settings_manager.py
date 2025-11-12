from PySide6.QtCore import Slot

class SettingsManager:
    """
    Handles all application settings, including loading/saving the settings.json
    and managing the path to the current SQLite database.
    """
    def __init__(self):
        # Initialisierung des Einstellungszustands
        # Später können hier die Einstellungen aus settings.json geladen werden.
        print("SettingsManager initialized.")

    @Slot(str)
    def handle_new_db_path(self, db_path: str):
        """
        Slot method called when the Settings Window emits a new database path.

        Args:
            db_path (str): The full path where the new database should be created.
        """
        print(f"Received signal for new DB path: {db_path}")

        # 1. Datenbankerstellung (Logik)
        success = self._create_database_file(db_path)

        if success:
            # 2. Speichern in settings.json (Konfiguration)
            self._save_default_db_path(db_path)
            print("Database created and path saved successfully.")
        else:
            print("Error: Could not create the database.")


    def _create_database_file(self, path: str) -> bool:
        """
        Placeholder for the database creation logic (using sqlite3 later).
        Returns True on success.
        """
        try:
            # Beispiel-Logik: Erstellt eine leere Datei zur Simulation
            with open(path, 'w') as f:
                f.write("# SQLite placeholder file")
            # Später: Hier würde der sqlite3-Code die Tabellen erstellen.
            return True
        except Exception as e:
            print(f"Error creating file: {e}")
            return False

    def _save_default_db_path(self, path: str):
        """
        Placeholder: Saves the path to the persistent settings (settings.json).
        """
        # Später: Logik zum Speichern des Pfades in einer JSON-Datei.
        print(f"Saved default DB path to settings: {path}")