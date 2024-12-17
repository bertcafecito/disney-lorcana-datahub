import logging
import os
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DisneyLorcanaCleanup:
    def __init__(self):
        self.processed_dir = 'data/processed/disney_lorcana'

    def clean_sets(self):
        # Assign the directory where the PDF files are stored
        csv_directory = f"{self.processed_dir}/sets"

        # List all the CSV files in the directory
        csv_files = [f for f in os.listdir(csv_directory) if f.endswith('.csv')]

        # Verify the PDF files were found
        logging.info(f"Found CSV files: {csv_files}")

        # Load and Process Each CSV File
        for csv_file in csv_files:
            # Create the path to the CSV file
            csv_path = os.path.join(csv_directory, csv_file)

            # Verify the PDF file path
            logging.info(f"Processing CSV file: {csv_path}")

            # Load the CSV file into a DataFrame
            df = pd.read_csv(csv_path)

            # Remove Ink Types from the Card Name
            ink_types = ['AMBER', 'AMETHYST', 'EMERALD', 'RUBY', 'SAPPHIRE', 'STEEL']
            for ink_type in ink_types:
                df['card_name'] = df['card_name'].apply(lambda x: x.replace(ink_type, '').strip())
                logging.info(f'Removed {ink_type} from the card name')

            # Remove `TOTAL` from the Card Name
            df['card_name'] = df['card_name'].apply(lambda x: x.replace('TOTAL', '').strip())
            logging.info('Removed TOTAL from the card name')

            # Save the updated DataFrame to the CSV file
            df.to_csv(csv_path, index=False)

            # Verify the CSV file was saved
            logging.info(f"Saved CSV file: {csv_path}")

if __name__ == '__main__':
    dlc = DisneyLorcanaCleanup()
    dlc.clean_sets()