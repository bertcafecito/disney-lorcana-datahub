import os
import json
import shutil
from datetime import datetime

RAW_DIR = "data/raw/lorcast"
PROCESSED_DIR = "data/processed/lorcast"
LOG_FILE = f"{PROCESSED_DIR}/processed_folders.log"

def load_processed_folders():
    """Load the list of processed folders from the log file."""
    if not os.path.exists(LOG_FILE):
        return set()
    with open(LOG_FILE, "r") as f:
        return set(line.strip() for line in f)

def save_processed_folder(folder):
    with open(LOG_FILE, "a") as f:
        f.write(folder + "\n")

def consolidate_sets():
    output_path = f"{PROCESSED_DIR}/sets.json"
    sets_by_id = {}

    # Load existing master sets.json if it exists
    if os.path.isfile(output_path):
        with open(output_path, "r", encoding="utf-8") as f:
            try:
                existing_sets = json.load(f)
                for s in existing_sets:
                    sets_by_id[s["id"]] = s
            except Exception as e:
                print(f"Error reading existing {output_path}: {e}")

    # Load processed folders
    processed_folders = load_processed_folders()

    # Process only new folders
    new_folders = []
    added_count = 0
    for folder in os.listdir(RAW_DIR):
        folder_path = os.path.join(RAW_DIR, folder)
        sets_file = os.path.join(folder_path, "sets.json")
        if (
            os.path.isdir(folder_path)
            and os.path.isfile(sets_file)
            and folder not in processed_folders
        ):
            new_folders.append(folder)
            with open(sets_file, "r", encoding="utf-8") as f:
                try:
                    sets = json.load(f)
                    for s in sets:
                        if s["id"] not in sets_by_id:
                            added_count += 1
                        sets_by_id[s["id"]] = s
                except Exception as e:
                    print(f"Error reading {sets_file}: {e}")

    # Add processed_at date to each set
    processed_date = datetime.now().strftime("%Y-%m-%d")
    for s in sets_by_id.values():
        s["processed_at"] = processed_date

    # Sort by released_at then name for consistency
    all_sets = sorted(sets_by_id.values(), key=lambda s: (s.get("released_at", ""), s.get("name", "")))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as out:
        json.dump(all_sets, out, indent=4, ensure_ascii=False)

    # Save processed folders
    for folder in new_folders:
        save_processed_folder(folder)

    print(f"Added {added_count} new sets from {len(new_folders)} new folders.")
        
def process_folder(folder_path, output_path):
    # Example: copy all files from folder_path to output_path
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    for filename in os.listdir(folder_path):
        src = os.path.join(folder_path, filename)
        dst = os.path.join(output_path, filename)
        if os.path.isfile(src):
            shutil.copy2(src, dst)

def main():
    consolidate_sets()

if __name__ == "__main__":
    main()