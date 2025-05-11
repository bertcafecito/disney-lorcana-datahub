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

    def check_if_table_exists(self, table_name):
        """Check if a table exists in the SQLite database."""
        self.cursor.execute('''
        SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name=?
        ''', (table_name,))
        return self.cursor.fetchone()[0] == 1

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
