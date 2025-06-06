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
        
        # Create the tables if they don't exist
        self.create_sets_table()
        self.create_cards_table()
        self.create_card_images_table()
        self.create_inks_table()
        self.create_card_types_table()
        self.create_card_classifications_table()
        self.create_card_legalities_table()
        self.create_prices_table()

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

    def insert_or_update_card_data(self, card_data):
        """Insert or update card data into the cards and related tables."""
        if not card_data:
            print("No card data to insert or update.")
            return

        for card in card_data:
            # Insert into cards table
            self.cursor.execute('''
                INSERT OR REPLACE INTO cards (id, name, version, layout, released_at, cost, inkwell, 
                                              strength, willpower, lore, rarity, collector_number, lang, 
                                              flavor_text, tcgplayer_id, move_cost)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                card['id'], card['name'], card['version'], card['layout'], card['released_at'], 
                card['cost'], card['inkwell'], card['strength'], card['willpower'], card['lore'], 
                card['rarity'], card['collector_number'], card['lang'], card['flavor_text'], 
                card['tcgplayer_id'], card.get('move_cost', None)
            ))

            # Insert card images
            image_uris = card['image_uris']['digital']
            self.cursor.execute('''
                INSERT INTO card_images (card_id, small, normal, large) 
                VALUES (?, ?, ?, ?)
            ''', (card['id'], image_uris['small'], image_uris['normal'], image_uris['large']))

            # Insert inks
            for ink in card['inks']:
                self.cursor.execute('''
                    INSERT INTO inks (card_id, ink_color) 
                    VALUES (?, ?)
                ''', (card['id'], ink))

            # Insert card types
            for card_type in card['type']:
                self.cursor.execute('''
                    INSERT INTO card_types (card_id, type) 
                    VALUES (?, ?)
                ''', (card['id'], card_type))

            # Insert card classifications
            for classification in card['classifications']:
                self.cursor.execute('''
                    INSERT INTO card_classifications (card_id, classification) 
                    VALUES (?, ?)
                ''', (card['id'], classification))

            # Insert legalities
            legalities = card['legalities']
            self.cursor.execute('''
                INSERT INTO card_legalities (card_id, core_legal) 
                VALUES (?, ?)
            ''', (card['id'], legalities.get('core', 'unknown')))

            # Insert prices
            prices = card['prices']
            self.cursor.execute('''
                INSERT INTO prices (card_id, usd, usd_foil) 
                VALUES (?, ?, ?)
            ''', (card['id'], prices.get('usd', '0.00'), prices.get('usd_foil', '0.00')))

        self.connection.commit()
        print(f"Upserted {len(card_data)} rows into the 'cards' and related tables.")

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

    def create_cards_table(self):
        """Create the 'cards' table if it doesn't exist."""
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS cards (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            version TEXT,
            layout TEXT,
            released_at TEXT,
            cost INTEGER,
            inkwell BOOLEAN,
            strength INTEGER,
            willpower INTEGER,
            lore INTEGER,
            rarity TEXT,
            collector_number TEXT,
            lang TEXT,
            flavor_text TEXT,
            tcgplayer_id INTEGER,
            move_cost INTEGER
        );
        '''
        self.cursor.execute(create_table_sql)
        self.connection.commit()

    def create_card_images_table(self):
        """Create the 'card_images' table if it doesn't exist."""
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS card_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_id TEXT,
            small TEXT,
            normal TEXT,
            large TEXT,
            FOREIGN KEY (card_id) REFERENCES cards(id)
        );
        '''
        self.cursor.execute(create_table_sql)
        self.connection.commit()

    def create_inks_table(self):
        """Create the 'inks' table if it doesn't exist."""
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS inks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_id TEXT,
            ink_color TEXT,
            FOREIGN KEY (card_id) REFERENCES cards(id)
        );
        '''
        self.cursor.execute(create_table_sql)
        self.connection.commit()

    def create_card_types_table(self):
        """Create the 'card_types' table if it doesn't exist."""
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS card_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_id TEXT,
            type TEXT,
            FOREIGN KEY (card_id) REFERENCES cards(id)
        );
        '''
        self.cursor.execute(create_table_sql)
        self.connection.commit()

    def create_card_classifications_table(self):
        """Create the 'card_classifications' table if it doesn't exist."""
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS card_classifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_id TEXT,
            classification TEXT,
            FOREIGN KEY (card_id) REFERENCES cards(id)
        );
        '''
        self.cursor.execute(create_table_sql)
        self.connection.commit()

    def create_card_legalities_table(self):
        """Create the 'card_legalities' table if it doesn't exist."""
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS card_legalities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_id TEXT,
            core_legal TEXT,
            FOREIGN KEY (card_id) REFERENCES cards(id)
        );
        '''
        self.cursor.execute(create_table_sql)
        self.connection.commit()

    def create_prices_table(self):
        """Create the 'prices' table if it doesn't exist."""
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_id TEXT,
            usd TEXT,
            usd_foil TEXT,
            FOREIGN KEY (card_id) REFERENCES cards(id)
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
        
        # Process all card files under the latest folder
        cards_folder = os.path.join(loader.raw_data_path, latest_folder, 'sets')
        for filename in os.listdir(cards_folder):
            if filename.endswith('.json') and filename.startswith('crd_'):  # Only card files
                card_json_path = os.path.join(cards_folder, filename)
                # Load and process each card
                card_data = loader.load_json_from_file(card_json_path)
                if card_data:
                    loader.insert_or_update_card_data([card_data])  # Each card is a single entry
                else:
                    print(f"Failed to load {filename}.")
    else:
        print("Could not determine the latest folder.")

    # Close the database connection
    loader.close()

if __name__ == "__main__":
    main()
