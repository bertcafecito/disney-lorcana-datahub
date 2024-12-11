import json
import logging
import os
import pandas as pd
from pandas import json_normalize

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LorcastCleanup:
    def __init__(self):
        self.raw_dir = 'data/raw/lorcast_api'
        self.processed_dir = 'data/processed/lorcast_api'

        # Create the Processed Directory if it does not exist
        try:
            if not os.path.exists(self.processed_dir):
                os.makedirs(self.processed_dir)
                logging.info(f"Directory {self.processed_dir} created.")
            else:
                logging.info(f"Directory {self.processed_dir} already exists.")
        except Exception as e:
            logging.error(f"Error creating directory {self.processed_dir}: {e}")
            return
        
    def clean_sets(self):
        """
        Clean up the sets JSON files and save the cleaned data to a new CSV file.
        """
        logging.info("Cleaning up sets JSON files...")

        # Load the sets JSON files
        logging.info("Loading sets JSON files...")
        json_file = f"{self.raw_dir}/sets.json"

        try:
            if os.path.exists(json_file):
                logging.info(f"File {json_file} exists.")

            with open(json_file, 'r') as file:
                sets = json.load(file)

            logging.info(f"File {json_file} loaded.")
        except Exception as e:
            logging.error(f"Error loading file {json_file}: {e}")
            return

        logging.info("Currently there is no cleanup to perform.")

        # Save the cleaned data to a new CSV file
        logging.info("Saving cleaned data to CSV file...")
        csv_file = f"{self.processed_dir}/sets.csv"
        logging.info(f"CSV File: {csv_file}.")

        try:
            df = pd.DataFrame(sets)
            df.to_csv(csv_file, index=False)
            logging.info(f"Data saved to {csv_file}.")
        except Exception as e:
            logging.error(f"Error saving data to {csv_file}: {e}")
            return
        
    def clean_cards(self):
        """
        Clean up the cards JSON files and save the cleaned data to a new CSV file.
        """
        # Assign the directory where the PDF files are stored
        json_directory = f"{self.raw_dir}/sets"
        logging.info(f"JSON Directory: {json_directory}.")

        # List all the CSV files in the directory
        json_files = [f for f in os.listdir(json_directory) if f.endswith('.json')]
        logging.info(f"JSON Files: {json_files}.")

        cards_list = []

        # Load and Process Each JSON File
        for json_file in json_files:
            logging.info(f"Loading and processing {json_file}...")

            try:
                with open(f"{json_directory}/{json_file}", 'r') as file:
                    cards = json.load(file)

                logging.info(f"File {json_file} loaded.")
            except Exception as e:
                logging.error(f"Error loading file {json_file}: {e}")
                return

            # Append the cards to the list
            cards_list.extend(cards)

        # Create a data from the cards_list
        df = pd.DataFrame(cards_list)        

        # Flatten the cards_types into separate rows
        card_type_df = df[['id', 'type']]
        # Drop rows with empty lists
        card_type_df = card_type_df[card_type_df.astype(str)['type'] != '[]']
        card_type_df = card_type_df.explode('type')

        # Flatten the cards_keywords into separate rows
        card_keywords_df = df[['id', 'keywords']]
        # Drop rows with empty lists
        card_keywords_df = card_keywords_df[card_keywords_df.astype(str)['keywords'] != '[]']
        card_keywords_df = card_keywords_df.explode('keywords')
            
        # Flatten the cards_classifications into separate rows
        card_classifications_df = df[['id', 'classifications']]
        # Drop rows with empty lists
        card_classifications_df = card_classifications_df[card_classifications_df.astype(str)['classifications'] != '[]']
        card_classifications_df = card_classifications_df.explode('classifications')

        # Flatten the cards_illustrators into separate rows
        card_illustrators_df = df[['id', 'illustrators']]
        # Drop rows with empty lists
        card_illustrators_df = card_illustrators_df[card_illustrators_df.astype(str)['illustrators'] != '[]']
        card_illustrators_df = card_illustrators_df.explode('illustrators')
        
        # Flatten 'set' semi-structured JSON data into a DataFrame
        card_set_df = df[['id', 'set']]
        set_df = json_normalize(card_set_df['set'])
        card_set_df = card_set_df.drop(columns=['set']).join(set_df, lsuffix='_card', rsuffix='_set')

        # Flatten 'prices' semi-structured JSON data into a DataFrame
        card_legalities_df = df[['id', 'legalities']]
        legalities_df = json_normalize(card_legalities_df['legalities'])
        card_legalities_df = card_legalities_df.drop(columns=['legalities']).join(legalities_df, lsuffix='_card', rsuffix='_legalities')

        # Flatten 'prices' semi-structured JSON data into a DataFrame
        card_prices_df = df[['id', 'prices']]
        prices_df = json_normalize(card_prices_df['prices'])
        card_prices_df = card_prices_df.drop(columns=['prices']).join(prices_df, lsuffix='_card', rsuffix='_prices')

        # Drop the columns that have been flattened
        df = df.drop(columns=['type', 'keywords', 'classifications', 'illustrators', 'set', 'legalities', 'prices', 'image_uris'])

        # Save the cleaned data to a new CSV file
        logging.info("Saving cleaned data to CSV file...")
        csv_file = f"{self.processed_dir}/cards.csv"
        logging.info(f"CSV File: {csv_file}.")
        try:
            df.to_csv(csv_file, index=False)
            logging.info(f"Data saved to {csv_file}.")
        except Exception as e:
            logging.error(f"Error saving data to {csv_file}: {e}")
            return
        
        # Save the flattened data to new CSV files
        logging.info("Saving flattened data to CSV files...")
        card_type_csv_file = f"{self.processed_dir}/cards_type.csv"
        card_keywords_csv_file = f"{self.processed_dir}/cards_keywords.csv"
        card_classifications_csv_file = f"{self.processed_dir}/cards_classifications.csv"
        card_illustrators_csv_file = f"{self.processed_dir}/cards_illustrators.csv"
        card_set_csv_file = f"{self.processed_dir}/cards_set.csv"
        card_legalities_csv_file = f"{self.processed_dir}/cards_legalities.csv"
        card_prices_csv_file = f"{self.processed_dir}/cards_prices.csv"

        try:
            card_type_df.to_csv(card_type_csv_file, index=False)
            card_keywords_df.to_csv(card_keywords_csv_file, index=False)
            card_classifications_df.to_csv(card_classifications_csv_file, index=False)
            card_illustrators_df.to_csv(card_illustrators_csv_file, index=False)
            card_set_df.to_csv(card_set_csv_file, index=False)
            card_legalities_df.to_csv(card_legalities_csv_file, index=False)
            card_prices_df.to_csv(card_prices_csv_file, index=False)
            logging.info(f"Data saved to {card_type_csv_file}, {card_keywords_csv_file}, {card_classifications_csv_file}, {card_illustrators_csv_file}, {card_set_csv_file}, {card_legalities_csv_file}, {card_prices_csv_file}.")
        except Exception as e:
            logging.error(f"Error saving data to {card_type_csv_file}, {card_keywords_csv_file}, {card_classifications_csv_file}, {card_illustrators_csv_file}, {card_set_csv_file}, {card_legalities_csv_file}, {card_prices_csv_file}: {e}")
            return

        
if __name__ == '__main__':
    cleanup = LorcastCleanup()
    cleanup.clean_sets()
    cleanup.clean_cards()