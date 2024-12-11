import json
import os
import pandas as pd
import ast

class LorcastCleanup:
    def __init__(self):
        self.raw_data_dir = 'data/raw/lorcast_api'
        self.processed_data_dir = 'data/processed/lorcast_api'

        # Create the cleaned data directory if it doesn't exist
        if not os.path.exists(self.processed_data_dir):
            os.makedirs(self.processed_data_dir)
            print("Created directory: ", self.processed_data_dir)
        else:
            print("Directory already exists: ", self.processed_data_dir)

    def sets_data(self):
        # Create raw path for the sets CSV file
        sets_file_path = f'{self.raw_data_dir}/sets.csv'

        print("No cleanup needed for sets data")

        # Read the raw data from the CSV file
        df = pd.read_csv(sets_file_path)

        # Save the cleaned data to the processed data directory
        df.to_csv(f'{self.processed_data_dir}/sets.csv', index=False)

    def cards_data(self, set_file_path):
        print(f"Cleaning up data for set: {set_file_path}")

        # Read the raw data from the CSV file
        df = pd.read_csv(set_file_path)

        # Drop the columns that are not needed
        df.drop(columns=['image_uris'], inplace=True)

        # Explode 'type' column
        df['type'] = df['type'].apply(ast.literal_eval)
        df = df.explode('type').reset_index(drop=True)
        # Select id and type columns
        a = df[['id', 'type']]
        print(a.head())

        # Repalce raw for processed in the file path
        set_file_path = set_file_path.replace('raw', 'processed')

        # Create the processed data directory if it doesn't exist
        if not os.path.exists(os.path.dirname(set_file_path)):
            os.makedirs(os.path.dirname(set_file_path))
            print("Created directory: ", os.path.dirname(set_file_path))
        else:
            print("Directory already exists: ", os.path.dirname(set_file_path))

        # Save the cleaned data to the processed data directory
        df.to_csv(set_file_path, index=False)

if __name__ == "__main__":
    # Get the Lorcast API Data
    cleanup = LorcastCleanup()
    cleanup.sets_data()

    # Get all the set file paths from the raw data directory under the sets directory
    set_files = os.listdir(cleanup.raw_data_dir + '/sets')
    for set_file in set_files:
        set_file_path = f'{cleanup.raw_data_dir}/sets/{set_file}'
        cleanup.cards_data(set_file_path)