import os
import json
import glob
import argparse
from datetime import datetime
from pathlib import Path

class LorcanaDataProcessor:
    """Main processor for consolidating Lorcana data with timestamps"""
    
    def __init__(self, input_dir='data/raw/lorcast', output_dir='data/processed/lorcast'):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # File for tracking processed files
        self.tracking_file = self.output_dir / 'processing_history.json'
        self.processed_files = self.load_processing_history()
        
        # File for tracking card changes over time
        self.changes_file = self.output_dir / 'card_changes.json'
        self.card_changes = self.load_card_changes()
        
        # Mapping for friendly names to set IDs
        self.friendly_to_set_id = {
            'the_first_chapter': 'set_7ecb0e0c71af496a9e01110e23824e0a5',
            'rise_of_the_floodborn': 'set_142d2dfb5d4b4b739a1017dc4bb0fcd2',
            'into_the_inklands': 'set_10a1db03fe66417c9912494b94463e8e',
            'ursula\'s_return': 'set_8f4cbf5aef324eb295c4add5673e684f',
            'ursulas_return': 'set_8f4cbf5aef324eb295c4add5673e684f',
            'shimmering_skies': 'set_c64f092e725a4f66966f43af3aa161b6',
            'azurite_sea': 'set_0df34ab314e04a479ef3538fd6c3e4e1',
            'archazia\'s_island': 'set_ceb34c63638a4ce6b80e518393964c8f',
            'archazias_island': 'set_ceb34c63638a4ce6b80e518393964c8f',
            'reign_of_jafar': 'set_e4fe64374c144642a035ee7b8451f990',
            'fabled': 'set_42a2e9232c43494dab2c72945ea6879e',
            'd23_collection': 'set_ec81a739fb204f10b31dc649c535c82e',
            'promo_set_1': 'set_c254adfcbf6d4e3482a675ecece86dcc',
            'promo_set_2': 'set_1fd69818f6e44dd79e922f403aa4f6d9',
            'challenge_promo': 'set_e0eb34fc0fbb446886f84c34381d4dce'
        }
        
        # Reverse mapping for display purposes
        self.set_id_to_friendly = {v: k for k, v in self.friendly_to_set_id.items()}
        
    def load_processing_history(self):
        """Load history of processed files to avoid reprocessing unchanged files"""
        if not self.tracking_file.exists():
            return {}
        
        try:
            with open(self.tracking_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def load_card_changes(self):
        """Load history of card changes"""
        if not self.changes_file.exists():
            return {}
        
        try:
            with open(self.changes_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def save_card_changes(self):
        """Save card changes tracking"""
        with open(self.changes_file, 'w', encoding='utf-8') as f:
            json.dump(self.card_changes, f, indent=2, ensure_ascii=False)
    
    def track_card_change(self, card_id, field, old_value, new_value, date_found):
        """Track a change to a specific card field"""
        if card_id not in self.card_changes:
            self.card_changes[card_id] = {
                'card_name': '',
                'changes': []
            }
        
        change_entry = {
            'date': date_found,
            'field': field,
            'old_value': old_value,
            'new_value': new_value,
            'timestamp': datetime.now().isoformat()
        }
        
        self.card_changes[card_id]['changes'].append(change_entry)
    
    def compare_cards(self, old_card, new_card, date_found):
        """Compare two versions of a card and track changes"""
        if not old_card:
            return new_card
        
        card_id = new_card['id']
        
        # Update card name for reference
        if card_id in self.card_changes:
            self.card_changes[card_id]['card_name'] = f"{new_card['name']} - {new_card.get('version', '')}"
        
        # Fields to monitor for changes (excluding timestamps)
        monitored_fields = [
            'name', 'version', 'cost', 'strength', 'willpower', 'lore', 
            'text', 'flavor_text', 'rarity', 'released_at', 'legalities',
            'prices', 'collector_number', 'keywords', 'classifications'
        ]
        
        for field in monitored_fields:
            old_value = old_card.get(field)
            new_value = new_card.get(field)
            
            # Compare values, handling None and different types
            if old_value != new_value:
                # Skip if both are None or empty
                if not old_value and not new_value:
                    continue
                
                self.track_card_change(card_id, field, old_value, new_value, date_found)
        
        return new_card
    
    def save_processing_history(self):
        """Save history of processed files"""
        with open(self.tracking_file, 'w', encoding='utf-8') as f:
            json.dump(self.processed_files, f, indent=2, ensure_ascii=False)
    
    def get_file_hash(self, file_path):
        """Get a simple hash/signature of a file for change detection"""
        try:
            stat = file_path.stat()
            # Use file size and modification time as a simple signature
            return f"{stat.st_size}_{stat.st_mtime}"
        except OSError:
            return None
    
    def should_process_file(self, file_path, date_str):
        """Check if a file needs processing based on change detection"""
        file_key = str(file_path.relative_to(self.input_dir))
        current_hash = self.get_file_hash(file_path)
        
        if current_hash is None:
            return False
        
        # Check if we've seen this file before
        if file_key in self.processed_files:
            stored_info = self.processed_files[file_key]
            # Skip if hash hasn't changed
            if stored_info.get('hash') == current_hash:
                return False
        
        # File is new or changed, mark it for processing
        self.processed_files[file_key] = {
            'hash': current_hash,
            'last_processed': date_str,
            'processing_date': datetime.now().isoformat()
        }
        
        return True
        
    def force_reprocess(self):
        """Clear processing history to force reprocessing of all files"""
        self.processed_files = {}
        if self.tracking_file.exists():
            self.tracking_file.unlink()
        # Note: We keep card_changes history as it's valuable historical data
        print("🔄 Processing history cleared - all files will be reprocessed")
        
    def run(self):
        """Main processing method - simple and clear"""
        print("🚀 Starting Lorcana data processing...")
        
        # Step 1: Process sets metadata
        sets_data = self.process_sets()
        
        # Step 2: Process card data
        cards_data = self.process_cards()
        
        # Step 3: Save all data
        self.save_data(sets_data, cards_data)
        
        # Step 4: Create summary report
        self.create_report(sets_data, cards_data)
        
        # Step 5: Save processing history
        self.save_processing_history()
        
        # Step 6: Save card changes tracking
        self.save_card_changes()
        
        print("✅ Processing complete!")
        
    def process_sets(self):
        """Process all sets.json files and consolidate metadata"""
        print("📚 Step 1: Processing sets metadata...")
        
        # Load existing processed sets data
        sets_data = self.load_existing_sets_data()
        
        date_dirs = sorted([d for d in self.input_dir.iterdir() if d.is_dir()])
        processed_count = 0
        skipped_count = 0
        
        for date_dir in date_dirs:
            sets_file = date_dir / 'sets.json'
            if not sets_file.exists():
                continue
            
            # Check if we need to process this file
            if not self.should_process_file(sets_file, date_dir.name):
                skipped_count += 1
                continue
                
            processed_count += 1
            with open(sets_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            print(f"  Processing {len(data)} sets from {date_dir.name}")
            
            for set_info in data:
                set_id = set_info['id']
                date_str = date_dir.name
                
                if set_id not in sets_data:
                    # First time seeing this set
                    sets_data[set_id] = {
                        **set_info,
                        'created_at': date_str,
                        'updated_at': date_str
                    }
                else:
                    # Update if data changed
                    current_data = {k: v for k, v in set_info.items()}
                    existing_data = {k: v for k, v in sets_data[set_id].items() 
                                   if k not in ['created_at', 'updated_at']}
                    
                    if current_data != existing_data:
                        sets_data[set_id].update(set_info)
                        sets_data[set_id]['updated_at'] = date_str
        
        if skipped_count > 0:
            print(f"  Skipped {skipped_count} unchanged sets files")
        if processed_count > 0:
            print(f"  Processed {processed_count} new/changed sets files")
        print(f"  Saved {len(sets_data)} sets to sets.json")
        return sets_data
        
    def load_existing_sets_data(self):
        """Load existing processed sets data to preserve previous processing"""
        sets_file = self.output_dir / 'sets.json'
        if sets_file.exists():
            try:
                with open(sets_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        return {}
        
    def load_existing_cards_data(self):
        """Load existing processed cards data to preserve previous processing"""
        cards_data = {}
        sets_dir = self.output_dir / 'sets'
        
        if not sets_dir.exists():
            return {}
            
        for card_file in sets_dir.glob('*.json'):
            set_id = card_file.stem
            try:
                with open(card_file, 'r', encoding='utf-8') as f:
                    cards = json.load(f)
                
                # Extract metadata from first card if available
                if cards:
                    first_card = cards[0]
                    cards_data[set_id] = {
                        'cards': [self.clean_card_for_processing(card) for card in cards],
                        'created_at': first_card.get('created_at', ''),
                        'updated_at': first_card.get('updated_at', '')
                    }
                else:
                    cards_data[set_id] = {
                        'cards': [],
                        'created_at': '',
                        'updated_at': ''
                    }
            except (json.JSONDecodeError, FileNotFoundError):
                continue
                
        return cards_data
        
    def clean_card_for_processing(self, card):
        """Remove timestamps from card for processing (they'll be re-added)"""
        clean_card = card.copy()
        clean_card.pop('created_at', None)
        clean_card.pop('updated_at', None)
        return clean_card
        
    def process_cards(self):
        """Process all card files and consolidate data"""
        print("🃏 Step 2: Processing card data...")
        
        # Load existing processed cards data
        cards_data = self.load_existing_cards_data()
        
        date_dirs = sorted([d for d in self.input_dir.iterdir() if d.is_dir()])
        processed_count = 0
        skipped_count = 0
        
        for date_dir in date_dirs:
            sets_dir = date_dir / 'sets'
            if not sets_dir.exists():
                continue
                
            for card_file in sets_dir.glob('*.json'):
                filename = card_file.stem
                date_str = date_dir.name
                
                # Check if we need to process this file
                if not self.should_process_file(card_file, date_str):
                    skipped_count += 1
                    continue
                
                processed_count += 1
                
                # Determine the set ID to use
                set_id = self.get_set_id_for_file(filename)
                friendly_name = self.get_friendly_name(set_id)
                
                with open(card_file, 'r', encoding='utf-8') as f:
                    cards = json.load(f)
                
                print(f"  Processing {filename} -> {set_id} ({friendly_name.replace('_', ' ').title()}): {len(cards)} cards")
                
                if set_id not in cards_data:
                    # First time seeing this set's cards
                    cards_data[set_id] = {
                        'cards': cards,
                        'created_at': date_str,
                        'updated_at': date_str
                    }
                else:
                    # Merge cards and update timestamp if changed
                    existing_cards = cards_data[set_id]['cards']
                    merged_cards = self.merge_cards(existing_cards, cards, date_str)
                    
                    if len(merged_cards) != len(existing_cards):
                        cards_data[set_id]['cards'] = merged_cards
                        cards_data[set_id]['updated_at'] = date_str
        
        if skipped_count > 0:
            print(f"  Skipped {skipped_count} unchanged card files")
        if processed_count > 0:
            print(f"  Processed {processed_count} new/changed card files")
        
        # Save individual card files
        sets_dir = self.output_dir / 'sets'
        sets_dir.mkdir(exist_ok=True)
        
        for set_id, data in cards_data.items():
            # Add timestamps to each card
            cards_with_timestamps = []
            for card in data['cards']:
                card_with_timestamps = {
                    **card,
                    'created_at': data['created_at'],
                    'updated_at': data['updated_at']
                }
                cards_with_timestamps.append(card_with_timestamps)
            
            # Save using set ID as filename
            cards_file = sets_dir / f"{set_id}.json"
            with open(cards_file, 'w', encoding='utf-8') as f:
                json.dump(cards_with_timestamps, f, indent=2, ensure_ascii=False)
            
            friendly_name = self.get_friendly_name(set_id)
            print(f"  Saved {len(cards_with_timestamps)} cards for {set_id} ({friendly_name.replace('_', ' ').title()})")
        
        total_cards = sum(len(data['cards']) for data in cards_data.values())
        print(f"  Total cards processed: {total_cards}")
        
        return cards_data
        
    def get_set_id_for_file(self, filename):
        """Convert filename to standardized set ID"""
        # If it's already a set ID, return as-is
        if filename.startswith('set_'):
            return filename
            
        # Convert friendly name to set ID
        clean_filename = filename.lower().replace("'", "").replace("'", "")
        
        if clean_filename in self.friendly_to_set_id:
            return self.friendly_to_set_id[clean_filename]
        
        # Try with apostrophe variations
        for friendly, set_id in self.friendly_to_set_id.items():
            if friendly.replace("'", "").replace("_", "") == clean_filename.replace("_", ""):
                return set_id
        
        # If no mapping found, create a set ID from the filename
        return f"set_{filename.lower()}"
        
    def get_friendly_name(self, set_id):
        """Get friendly name for a set ID"""
        if set_id in self.set_id_to_friendly:
            return self.set_id_to_friendly[set_id]
        return set_id.replace('set_', '')
        
    def merge_cards(self, existing_cards, new_cards, date_found=None):
        """Merge card lists, avoiding duplicates and tracking changes"""
        # Create a lookup of existing cards by ID
        existing_by_id = {card.get('id'): card for card in existing_cards}
        
        merged = []
        
        # Process existing cards first, checking for updates
        for card in existing_cards:
            card_id = card.get('id')
            # Find matching card in new data
            new_card = next((c for c in new_cards if c.get('id') == card_id), None)
            
            if new_card and date_found:
                # Compare and track changes
                updated_card = self.compare_cards(card, new_card, date_found)
                merged.append(updated_card)
            else:
                # No new version found, keep existing
                merged.append(card)
        
        # Add completely new cards
        existing_ids = {card.get('id') for card in existing_cards}
        for card in new_cards:
            card_id = card.get('id')
            if card_id not in existing_ids:
                merged.append(card)
                # Track new card addition
                if date_found and card_id:
                    if card_id not in self.card_changes:
                        self.card_changes[card_id] = {
                            'card_name': f"{card.get('name', '')} - {card.get('version', '')}",
                            'changes': []
                        }
                    
                    self.track_card_change(card_id, 'card_added', None, 'Card first discovered', date_found)
        
        return merged
        
    def save_data(self, sets_data, cards_data):
        """Save consolidated sets metadata"""
        sets_output = self.output_dir / 'sets.json'
        with open(sets_output, 'w', encoding='utf-8') as f:
            json.dump(sets_data, f, indent=2, ensure_ascii=False)
        
    def create_report(self, sets_data, cards_data):
        """Create summary report"""
        print("📊 Step 3: Creating summary report...")
        
        # Calculate totals
        total_cards = sum(len(data['cards']) for data in cards_data.values())
        
        # Create report data
        report = {
            'processing_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_sets': len(sets_data),
            'total_cards': total_cards,
            'sets': {},
            'card_counts': {}
        }
        
        # Add set information
        for set_id, set_info in sets_data.items():
            card_count = len(cards_data.get(set_id, {}).get('cards', []))
            report['sets'][set_id] = {
                'name': set_info['name'],
                'code': set_info['code'],
                'cards': card_count,
                'created_at': set_info['created_at'],
                'updated_at': set_info['updated_at']
            }
            report['card_counts'][set_id] = card_count
        
        # Save report
        report_file = self.output_dir / 'report.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"  Report saved: {len(sets_data)} sets, {total_cards} total cards")
        
        # Print summary
        print("📋 Summary:")
        print(f"  Total sets: {len(sets_data)}")
        print(f"  Total cards: {total_cards}")
        print("  Files created:")
        print("    - sets.json (metadata for all sets)")
        print(f"    - sets/ directory with {len(cards_data)} card files")
        print("    - report.json (processing summary)")


class LorcanaDataInspector:
    """Simple data inspector for viewing processed Lorcana data"""
    
    def __init__(self, data_dir='data/processed/lorcast'):
        self.data_dir = Path(data_dir)
        
    def show_data_summary(self):
        """Show overview of all processed data"""
        print("📊 Lorcana Data Summary")
        print("=" * 40)
        
        # Load sets data
        sets_file = self.data_dir / 'sets.json'
        if not sets_file.exists():
            print("❌ No processed data found. Run the processor first.")
            return
            
        with open(sets_file, 'r', encoding='utf-8') as f:
            sets_data = json.load(f)
        
        # Show sets summary
        print(f"📚 Sets: {len(sets_data)} total")
        print("Code | Name                 | Created    | Updated        ")
        print("-" * 55)
        
        for set_id, set_info in sets_data.items():
            code = set_info.get('code', 'N/A')[:3]
            name = set_info.get('name', 'Unknown')[:17]
            created = set_info.get('created_at', 'Unknown')
            updated = set_info.get('updated_at', 'Unknown')
            print(f"{code:>4} | {name:<17} | {created} | {updated}")
        
        # Show card files summary
        sets_dir = self.data_dir / 'sets'
        if sets_dir.exists():
            card_files = list(sets_dir.glob('*.json'))
            print(f"\n🃏 Card Files: {len(card_files)} sets")
            print("Set ID                                   | Cards")
            print("-" * 50)
            
            total_cards = 0
            for card_file in sorted(card_files):
                with open(card_file, 'r', encoding='utf-8') as f:
                    cards = json.load(f)
                card_count = len(cards)
                total_cards += card_count
                print(f"{card_file.stem:<40} | {card_count:>5}")
            
            print("-" * 50)
            print(f"{'TOTAL':<40} | {total_cards:>5}")
        
        # Show last processing info
        report_file = self.data_dir / 'report.json'
        if report_file.exists():
            with open(report_file, 'r', encoding='utf-8') as f:
                report = json.load(f)
            print(f"\n📊 Last processed: {report.get('processing_date', 'Unknown')}")
        
        print(f"📁 Data location: {self.data_dir.absolute()}")
        
    def show_set_details(self, set_id):
        """Show detailed information about a specific set"""
        sets_dir = self.data_dir / 'sets'
        card_file = sets_dir / f"{set_id}.json"
        
        if not card_file.exists():
            print(f"❌ Set {set_id} not found.")
            return
            
        with open(card_file, 'r', encoding='utf-8') as f:
            cards = json.load(f)
        
        print(f"🃏 Set Details: {set_id}")
        print("=" * 50)
        print(f"Total cards: {len(cards)}")
        
        if cards:
            first_card = cards[0]
            print(f"Created: {first_card.get('created_at', 'Unknown')}")
            print(f"Updated: {first_card.get('updated_at', 'Unknown')}")
            
            print("\nSample cards:")
            for i, card in enumerate(cards[:5]):
                name = card.get('name', 'Unknown')
                rarity = card.get('rarity', 'N/A')
                print(f"  {i+1}. {name} ({rarity})")
            
            if len(cards) > 5:
                print(f"  ... and {len(cards) - 5} more cards")
    
    def show_card_changes(self, card_name=None, limit=10):
        """Show card changes over time"""
        changes_file = self.data_dir / 'card_changes.json'
        
        if not changes_file.exists():
            print("❌ No card changes data found. Process data first to track changes.")
            return
        
        with open(changes_file, 'r', encoding='utf-8') as f:
            changes_data = json.load(f)
        
        if not changes_data:
            print("📝 No card changes recorded yet.")
            return
        
        print("🔄 Card Changes Summary")
        print("=" * 50)
        
        if card_name:
            # Search for a specific card
            found_cards = []
            for card_id, data in changes_data.items():
                if card_name.lower() in data.get('card_name', '').lower():
                    found_cards.append((card_id, data))
            
            if not found_cards:
                print(f"❌ No changes found for cards matching '{card_name}'")
                return
            
            for card_id, data in found_cards[:limit]:
                print(f"\n🃏 {data.get('card_name', 'Unknown Card')}")
                print(f"   Card ID: {card_id}")
                print(f"   Total changes: {len(data.get('changes', []))}")
                
                for change in data.get('changes', [])[-5:]:  # Show last 5 changes
                    field = change.get('field', 'unknown')
                    date = change.get('date', 'unknown')
                    old_val = str(change.get('old_value', 'N/A'))[:50]
                    new_val = str(change.get('new_value', 'N/A'))[:50]
                    print(f"   📅 {date}: {field}")
                    print(f"      Old: {old_val}{'...' if len(str(change.get('old_value', ''))) > 50 else ''}")
                    print(f"      New: {new_val}{'...' if len(str(change.get('new_value', ''))) > 50 else ''}")
        else:
            # Show overall summary
            total_cards_with_changes = len(changes_data)
            total_changes = sum(len(data.get('changes', [])) for data in changes_data.values())
            
            print(f"📊 Total cards with changes: {total_cards_with_changes}")
            print(f"📊 Total changes recorded: {total_changes}")
            
            # Show most changed cards
            print(f"\n🔥 Most Changed Cards (Top {limit}):")
            sorted_cards = sorted(changes_data.items(), 
                                key=lambda x: len(x[1].get('changes', [])), 
                                reverse=True)
            
            for i, (card_id, data) in enumerate(sorted_cards[:limit], 1):
                card_name = data.get('card_name', 'Unknown Card')
                change_count = len(data.get('changes', []))
                print(f"   {i}. {card_name} ({change_count} changes)")
            
            # Show change types summary
            change_types = {}
            for data in changes_data.values():
                for change in data.get('changes', []):
                    field = change.get('field', 'unknown')
                    change_types[field] = change_types.get(field, 0) + 1
            
            print(f"\n📊 Change Types:")
            for field, count in sorted(change_types.items(), key=lambda x: x[1], reverse=True):
                print(f"   {field}: {count} changes")


def main():
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(description='Lorcana Data Processor and Inspector')
    parser.add_argument('action', choices=['process', 'inspect', 'details', 'changes', 'force-process'], 
                       help='Action to perform')
    parser.add_argument('--set-id', help='Set ID for details view')
    parser.add_argument('--card-name', help='Card name to search for changes')
    parser.add_argument('--limit', type=int, default=10, help='Limit number of results')
    parser.add_argument('--input-dir', default='data/raw/lorcast',
                       help='Input directory (default: data/raw/lorcast)')
    parser.add_argument('--output-dir', default='data/processed/lorcast',
                       help='Output directory (default: data/processed/lorcast)')
    
    args = parser.parse_args()
    
    if args.action == 'process':
        processor = LorcanaDataProcessor(args.input_dir, args.output_dir)
        processor.run()
    elif args.action == 'force-process':
        processor = LorcanaDataProcessor(args.input_dir, args.output_dir)
        processor.force_reprocess()
        processor.run()
    elif args.action == 'inspect':
        inspector = LorcanaDataInspector(args.output_dir)
        inspector.show_data_summary()
    elif args.action == 'details':
        if not args.set_id:
            print("❌ --set-id required for details action")
            return
        inspector = LorcanaDataInspector(args.output_dir)
        inspector.show_set_details(args.set_id)
    elif args.action == 'changes':
        inspector = LorcanaDataInspector(args.output_dir)
        inspector.show_card_changes(args.card_name, args.limit)


if __name__ == "__main__":
    # If no command line arguments, run in interactive mode
    import sys
    if len(sys.argv) == 1:
        print("🎯 Lorcana Data Processor")
        print("=" * 30)
        print("1. Process data (incremental)")
        print("2. Inspect data")
        print("3. View card changes")
        print("4. Force reprocess all data")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == '1':
            processor = LorcanaDataProcessor()
            processor.run()
        elif choice == '2':
            inspector = LorcanaDataInspector()
            inspector.show_data_summary()
        elif choice == '3':
            inspector = LorcanaDataInspector()
            card_name = input("Enter card name to search (or press Enter for summary): ").strip()
            if card_name:
                inspector.show_card_changes(card_name)
            else:
                inspector.show_card_changes()
        elif choice == '4':
            processor = LorcanaDataProcessor()
            processor.force_reprocess()
            processor.run()
        elif choice == '5':
            print("👋 Goodbye!")
        else:
            print("❌ Invalid choice")
    else:
        main()
