import os
import sqlite3

class LorcanaDataLoader:
    def __init__(self, db_name="data/processed/lorcana.db"):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
    
    def database_exists(self):
        """Check if the SQLite database exists."""
        return os.path.exists(self.db_name)

def main():
  loader = LorcanaDataLoader()

  # Check if the database exists
  if loader.database_exists():
    print(f"Database '{loader.db_name}' exists.")
  else:
    print(f"Database '{loader.db_name}' does not exist.")
