from utils.lorcast_scraper import LorcastScraper

if __name__ == "__main__":
    # Get the Lorcast API Data
    scraper = LorcastScraper()
    scraper.run()