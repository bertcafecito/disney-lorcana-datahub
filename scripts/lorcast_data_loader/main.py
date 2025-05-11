import json
import os
import sqlite3
from datetime import datetime

class LorcanaDataLoader:
    def __init__(self, db_name="data/processed/lorcana.db", raw_data_path='data/raw/lorcast'):
        """Initialize the loader with database name and raw data path."""
        self.db_name = db_name
        self.raw_data_path = raw_data_path
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        
        # Create the table if it doesn't exist
        self.create_sets_table()

    def get_latest_folder(self):
        """Get the latest folder based on the date format YYYY-MM-DD."""
        all_folders = self._get_all_folders()
        date_folders = self._filter_date_folders(all_folders)
        
        if not date_folders:
            print("No valid date folders found.")
            return None
        
        latest_folder = max(date_folders, key=lambda x: x[1])[0]
        return latest_folder

    def _get_all_folders(self):
        """Get all subdirectories in the raw data path."""
        try:
            return [folder for folder in os.listdir(self.raw_data_path)
                    if os.path.isdir(os.path.join(self.raw_data_path, folder))]
        except FileNotFoundError:
            print(f"Error: The directory '{self.raw_data_path}' does not exist.")
            return []
        except Exception as e:
            print(f"Error: {e}")
            return []

    def _filter_date_folders(self, folders):
        """Filter folders that match the YYYY-MM-DD date format."""
        date_folders = []
        for folder in folders:
            try:
                folder_date = datetime.strptime(folder, '%Y-%m-%d')
                date_folders.append((folder, folder_date))
            except ValueError:
                continue  # Skip non-date folders
        return date_folders

    def load_json_from_file(self, file_path):
        """Load JSON data from a file."""
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON in the file: {file_path}")
        except Exception as e:
            print(f"Unexpected error while loading JSON: {e}")
        return None

    def insert_or_update_sets_data(self, sets_data):
        """Insert or update the sets data into the SQLite database (upsert)."""
        if not sets_data:
            print("No sets data to insert or update.")
            return
        
        # Assuming sets_data is a list of dictionaries where each dictionary represents a set
        for set_item in sets_data:
            self.cursor.execute('''
                INSERT OR REPLACE INTO sets (code, name, release_date, description)
                VALUES (?, ?, ?, ?)
            ''', (set_item.get('code'), set_item.get('name'), set_item.get('release_date'), set_item.get('description')))
        
        self.connection.commit()
        print(f"Upserted {len(sets_data)} rows into the 'sets' table.")

    def check_if_table_exists(self, table_name):
        """Check if a table exists in the SQLite database."""
        self.cursor.execute('''
        SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name=?
        ''', (table_name,))
        return self.cursor.fetchone()[0] == 1

    def create_sets_table(self):
        """Create the 'sets' table if it doesn't exist."""
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS sets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            release_date TEXT,
            description TEXT
        );
        '''
        self.cursor.execute(create_table_sql)
        self.connection.commit()

    def close(self):
        """Close the database connection."""
        self.connection.close()

def main():
    """Main function to execute the workflow."""
    loader = LorcanaDataLoader()

    # Get the latest folder based on date format
    latest_folder = loader.get_latest_folder()
    if latest_folder:
        print(f"The latest folder is: {latest_folder}")
        sets_json_path = os.path.join(loader.raw_data_path, latest_folder, 'sets.json')
        
        # Load the sets.json data
        sets_data = loader.load_json_from_file(sets_json_path)
        if sets_data:
            # Upsert the data into the 'sets' table
            loader.insert_or_update_sets_data(sets_data)
        else:
            print("Failed to load sets.json.")
    else:
        print("Could not determine the latest folder.")

    # Check if the 'sets' table exists
    if loader.check_if_table_exists('sets'):
        print("Table 'sets' exists.")
    else:
        print("Table 'sets' does not exist.")
        
    # Close the database connection
    loader.close()

if __name__ == "__main__":
    main()
