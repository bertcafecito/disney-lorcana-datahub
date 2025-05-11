import os
import sqlite3

class LorcanaDataLoader:
    def __init__(self, db_name="data/processed/lorcana.db"):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def get_latest_folder(path):
        """Get the latest folder based on date format YYYY-MM-DD."""
        # List all directories in the base path
        try:
            all_folders = [folder for folder in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, folder))]
            
            # Filter folders that match the date format YYYY-MM-DD
            date_folders = []
            for folder in all_folders:
                try:
                    # Attempt to convert the folder name to a datetime object
                    folder_date = datetime.strptime(folder, '%Y-%m-%d')
                    date_folders.append((folder, folder_date))
                except ValueError:
                    # Ignore folders that do not match the date format
                    continue
            
            if not date_folders:
                print("No valid date folders found.")
                return None
            
            # Sort folders by date (latest date first)
            latest_folder = max(date_folders, key=lambda x: x[1])[0]
            return latest_folder
    
    def check_if_table_exists(self, table_name):
        """Check if a table exists in the database."""
        self.cursor.execute('''
        SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name=?
        ''', (table_name,))
        return self.cursor.fetchone()[0] == 1

    def close(self):
        """Close the database connection."""
        self.connection.close()

def main():
    path = 'data/raw/lorcast'
    loader = LorcanaDataLoader()

    latest_folder = loader.get_latest_folder(path)
    if latest_folder:
        print(f"The latest folder is: {latest_folder}")
    else:
        print("Could not determine the latest folder.")

    # Check if the 'sets' table exists
    if loader.check_if_table_exists('sets'):
        print("Table 'sets' exists.")
    else:
        print("Table 'sets' does not exist.")
        
    loader.close()

if __name__ == "__main__":
    main()


