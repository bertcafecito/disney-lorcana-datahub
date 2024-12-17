import logging
import os
import re
import pandas as pd
from PyPDF2 import PdfReader

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DisneyLorcanaPDF:
    def __init__(self):
        # Assign the directory where the raw data is stored
        self.processed_dir = "data/processed/disney_lorcana"
        
        # Assign the directory where the PDF files are stored
        self.pdf_directory = "data/raw/disney_lorcana/set_checklist"

        # List all the PDF files in the directory
        self.pdf_files = [f for f in os.listdir(self.pdf_directory) if f.endswith('.pdf')]

        # Verify the PDF files were found
        logging.info(f"Found PDF files: {self.pdf_files}")

    def parse_pdf(self):
        # Create an empty DataFrame to store the extracted data
        df = pd.DataFrame()

        # Load and Process Each PDF File
        for pdf_file in self.pdf_files:
            # Create the path to the PDF file
            pdf_path = os.path.join(self.pdf_directory, pdf_file)

            # Verify the PDF file path
            logging.info(f"Processing PDF file: {pdf_path}")

            # Extract the Set Name from the PDF File
            set_name = pdf_file.replace(".pdf", "")

            # Verify the Set Name
            logging.info(f"Set Name: {set_name}")

            # Open the PDF file
            reader = PdfReader(pdf_path)

            # Extract the number of pages in the PDF file
            num_pages = len(reader.pages)

            # Verify the number of pages in the PDF file
            logging.info(f"Number of pages: {num_pages}")

            # Extract the text from each page in the PDF file
            pdf_text = []
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                pdf_text.append(page.extract_text())

            # Verify the PDF text
            logging.debug(f"Extracted text: {pdf_text}")

            # Define the pattern to match 
            pattern = r"\d+\s.*"

            # Find all the match in the PDF text
            matches = re.findall(pattern, pdf_text[0])

            # Verify the matches
            logging.debug(f"Matches: {matches}")

            # Define the pattern to split the matches
            pattern = r"\s"

            # Split the matches using the pattern and limit to 1 split
            split_matches = [re.split(pattern, match, 1) for match in matches]

            # Verify the split matches
            logging.debug(f"Split matches: {split_matches}")

            # Load the split matches into a DataFrame
            df = pd.DataFrame(split_matches, columns=["card_number", "card_name"])

            # Add the Set Name to the DataFrame
            df["set_name"] = set_name

            # Verify the DataFrame by counting the number of rows
            logging.info(f"DataFrame row count: {len(df)}")

            # Create the path to save the extracted data
            csv_file = f"{self.processed_dir}/sets/{set_name}.csv"

            # Verify the CSV file path
            logging.info(f"Saving CSV file: {csv_file}")

            # Create CSV directory if it does not exist
            os.makedirs(os.path.dirname(csv_file), exist_ok=True)

            # Verify the CSV directory was created
            logging.info(f"Created CSV directory: {os.path.dirname(csv_file)}")
            
            # Save the extracted data to a CSV file
            df.to_csv(csv_file, index=False)

            # Verify the CSV file was saved
            logging.info(f"Saved CSV file: {csv_file}")

if __name__ == '__main__':
    # Create an instance of the DisneyLorcanaPDF class
    disney_lorcana_pdf = DisneyLorcanaPDF()

    # Parse the PDF files
    disney_lorcana_pdf.parse_pdf()