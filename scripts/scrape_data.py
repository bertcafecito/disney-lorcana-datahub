from utils.disney_lorcana_pdf import DisneyLorcanaPDF
from utils.lorcast_scraper import LorcastScraper

if __name__ == "__main__":
    # Get the Disney Lorcana PDF Data
    disney_lorcana_pdf = DisneyLorcanaPDF()
    disney_lorcana_pdf.parse_pdf()

    # Get the Lorcast API Data
    scraper = LorcastScraper()
    scraper.run()