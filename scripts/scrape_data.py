import csv
import os
import re
from PyPDF2 import PdfReader

class PDFScraper:
    
    def v1(self, datasource_name, lorcana_set_name, pdf_path):
        """ 
        This is the first version of the method that scrapes data from the PDF file.

        Currently, this method only supports the following raw data sources sets:

        - Disney Lorcana
            - The First Chapter
            - Rise of The Floodborn
            - Into the Inklands
            - Ursula's Return
            - Shimmering Skies
        """
        print(f"Scraping data for the {datasource_name} data source")
        print(f"Scraping data for the {lorcana_set_name} set")
        print(f"Scraping data from the PDF path: {pdf_path}")

        # Open the PDF file
        reader = PdfReader(pdf_path)

        # Get the number of pages
        number_of_pages = len(reader.pages)
        print(f"Number of pages: {number_of_pages}")

        # Only extract text from the first page
        page = reader.pages[0]
        text = page.extract_text()
        # Uncomment the following line to see the extracted text for debugging purposes
        # print(text)

        # Extract text that matches a specific pattern
        # The pattern is a number followed by a space and then any character
        pattern = r'\d+\s.*'
        matches = re.findall(pattern, text)
        # Uncomment the following line to see the matches for debugging purposes
        # print(matches)

        # Split each value in the list by the first space only
        text_list = [re.split(r'\s', x, 1) for x in matches]
        # Uncomment the following line to see the text list for debugging purposes
        
        # Create data directory if it does not exist
        data_dir = f"data/processed/{datasource_name.lower().replace(' ', '_')}"
        print(f"Data directory: {data_dir}")

        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            print("Data directory created")
        else:
            print("Data directory already exists")

        # Create a CSV file
        csv_file = f"{data_dir}/{lorcana_set_name.lower().replace(' ', '_')}.csv"
        print(f"CSV file: {csv_file}")

        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["card_number", "card_name"])

            for item in text_list:
                writer.writerow(item)

        print("Data extraction complete")


if __name__ == '__main__':

    # Create an instance of the PDFScraper class
    pdf_scraper = PDFScraper()

    # Extract data for `The First Chapter` set from the `Disney Lorcana` data source
    pdf_scraper.v1(
        datasource_name='Disney Lorcana',
        lorcana_set_name='The First Chapter',
        pdf_path='data/raw/disney_lorcana/the-first-chapter-set-checklist.pdf'
    )

    # Extract data for `Rise of The Floodborn` set from the `Disney Lorcana` data source
    pdf_scraper.v1(
        datasource_name='Disney Lorcana',
        lorcana_set_name='Rise of The Floodborn',
        pdf_path='data/raw/disney_lorcana/rise-of-the-floodborn-set-checklist.pdf'
    )

    # Extract data for `Into the Inklands` set from the `Disney Lorcana` data source
    pdf_scraper.v1(
        datasource_name='Disney Lorcana',
        lorcana_set_name='Into the Inklands',
        pdf_path='data/raw/disney_lorcana/into-the-inklands-set-checklist.pdf'
    )

    # Extract data for `Ursula's Return` set from the `Disney Lorcana` data source
    pdf_scraper.v1(
        datasource_name='Disney Lorcana',
        lorcana_set_name="Ursulas Return",
        pdf_path='data/raw/disney_lorcana/ursulas-return-set-checklist.pdf'
    )

    # Extract data for `Shimmering Skies` set from the `Disney Lorcana` data source
    pdf_scraper.v1(
        datasource_name='Disney Lorcana',
        lorcana_set_name='Shimmering Skies',
        pdf_path='data/raw/disney_lorcana/shimmering-skies-set-checklist.pdf'
    )
