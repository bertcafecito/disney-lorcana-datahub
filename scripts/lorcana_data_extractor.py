import os
import json
from datetime import datetime
from inkcollector.cli import InkcollectorCLI
from inkcollector.lorcast import LorcastAPI

class LorcanaExtractor:
    """
    A class to extract Lorcana sets and cards data.
    """
    
    def __init__(self, output_dir=None):
        # Generate date-based directory structure
        if output_dir is None:
            current_date = datetime.now().strftime("%Y-%m-%d")
            # Get the repository root (parent of scripts directory)
            script_dir = os.path.dirname(os.path.abspath(__file__))
            repo_root = os.path.dirname(script_dir)
            output_dir = os.path.join(repo_root, "data", "raw", "lorcast", current_date)
        
        self.output_dir = output_dir
        self.sets_dir = os.path.join(output_dir)
        self.cards_dir = os.path.join(output_dir, "sets")
        
        # Create directories
        self._setup_directories()
        
        # Initialize CLI and LorcastAPI
        self.cli = InkcollectorCLI()
        self.api = LorcastAPI()
    
    def _setup_directories(self):
        """Create necessary directories."""
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.sets_dir, exist_ok=True)
        os.makedirs(self.cards_dir, exist_ok=True)
    
    def extract_all_sets_and_cards(self):
        """Extract all sets and their cards."""
        print(f"Starting extraction of all Lorcana sets and cards...")
        print(f"Output directory: {self.output_dir}")
        
        # Get all sets using the API (CLI doesn't have a method to return sets data)
        sets = self.api.get_sets()
        print(f"Found {len(sets)} sets.")
        
        # Save all sets data
        self._save_all_sets(sets)
        
        # Process each set
        for set_data in sets:
            set_id = set_data.get("id")
            set_name = set_data.get("name", set_id)
            
            if not set_id:
                print(f"Skipping set without ID: {set_name}")
                continue
            
            print(f"\nProcessing set: {set_name} ({set_id})")
            
            # Extract cards for this set
            self._extract_set_cards(set_id)
    
    def _save_all_sets(self, sets):
        """Save all sets data to JSON file."""
        sets_file = os.path.join(self.sets_dir, "sets.json")
        with open(sets_file, "w", encoding="utf-8") as f:
            json.dump(sets, f, ensure_ascii=False, indent=2)
        print(f"Saved all sets data to {sets_file}")
    
    def _extract_set_cards(self, set_id):
        """Extract cards data for a specific set."""
        # Get cards data using the API directly
        cards = self.api.get_cards(set_id)
        
        # Save cards data to our desired location
        self._save_cards_to_custom_location(cards, set_id)
    
    def _save_cards_to_custom_location(self, cards, set_id):
        """Save cards data to our custom location."""
        file_path = os.path.join(self.cards_dir, f"{set_id}.json")
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(cards, f, ensure_ascii=False, indent=2)
            print(f"Cards data saved to {file_path}")
        except Exception as e:
            print(f"Error saving cards data to {file_path}: {e}")


def main():
    """Main function to run the extraction."""
    extractor = LorcanaExtractor()
    extractor.extract_all_sets_and_cards()
    print("\nExtraction completed!")


if __name__ == "__main__":
    main()
