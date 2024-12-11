import json
import logging
import os
import requests
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LorcastScraper:
    def __init__(self):
        self.base_api_url = "https://api.lorcast.com/v0"
        self.raw_dir = "data/raw/lorcast_api"
        
        # Create the Raw Directory if it does not exist
        try:
            if not os.path.exists(self.raw_dir):
                os.makedirs(self.raw_dir)
                logging.info(f"Directory {self.raw_dir} created.")
            else:
                logging.info(f"Directory {self.raw_dir} already exists.")
        except Exception as e:
            logging.error(f"Error creating directory {self.raw_dir}: {e}")
            return

        self.image_dir = "images/lorcast_api"

        # Create the Image Directory if it does not exist
        try:
            if not os.path.exists(self.image_dir):
                os.makedirs(self.image_dir)
                logging.info(f"Directory {self.image_dir} created.")
            else:
                logging.info(f"Directory {self.image_dir} already exists.")
        except Exception as e:
            logging.error(f"Error creating directory {self.image_dir}: {e}")
            return
        
        self.sets_dir = f"{self.raw_dir}/sets"

        # Create the Sets Directory if it does not exist
        try:
            if not os.path.exists(self.sets_dir):
                os.makedirs(self.sets_dir)
                logging.info(f"Directory {self.sets_dir} created.")
            else:
                logging.info(f"Directory {self.sets_dir} already exists.")
        except Exception as e:
            logging.error(f"Error creating directory {self.sets_dir}: {e}")
            return

    def get_sets(self):
        """
        Get the sets from the Lorcast API and save the data to a JSON file.

        Returns:
            list: A list of sets.
        """
        logging.info("Getting sets from Lorcast API...")

        # Create the API URL for the endpoint that procides a comprehensive list of all card sets 
        # available in the Lorcana Trading Card Game
        url = f"{self.base_api_url}/sets"
        logging.info(f"API URL: {url}")

        # Make the request to the API
        try:
            logging.info("Making request to the API...")
            response = requests.get(url)
        except Exception as e:
            logging.error(f"Error making request to the API: {e}")
            return
        
        # Check the status code of the response
        if response.status_code != 200:
            logging.error(f"Error: Status code {response.status_code}")
            return
        
        logging.info(f"Status code: {response.status_code}")

        # Get the JSON data from the response
        try:
            data = response.json()
            logging.debug(f"Data: {data}")
        except Exception as e:
            logging.error(f"Error getting JSON data from response: {e}")
            return

        # Get the sets from the data
        try:
            sets = data.get("results")
            logging.debug(f"Sets: {sets}")
        except Exception as e:
            logging.error(f"Error getting sets from data: {e}")
            return

        # Save the data to a JSON file
        logging.info("Saving data to JSON file...")
        file_path = f"{self.raw_dir}/sets.json"

        # Save the sets to a JSON file
        try:
            with open(file_path, "w") as file:
                json.dump(sets, file)
            logging.info(f"Data saved to {file_path}")
        except Exception as e:
            logging.error(f"Error saving data to {file_path}: {e}")
            return
        
        logging.info("Finished getting sets from Lorcast API.")
        
        # Return the sets data
        return sets
    
    def get_cards(self, set_id, set_name):
        """
        Get the cards for a set from the Lorcast API and save the data to a JSON file.

        Parameters:
            set_id (str): The ID of the set.
            set_name (str): The name of the set.
        """
        logging.info(f"Getting cards for set {set_name} from Lorcast API...")

        # Create the API URL for the endpoint that returns all of the cards in a given set
        url = f"{self.base_api_url}/sets/{set_id}/cards"
        logging.info(f"API URL: {url}")

        # Make the request to the API
        try:
            logging.info("Making request to the API...")
            response = requests.get(url)
        except Exception as e:
            logging.error(f"Error making request to the API: {e}")
            return
        
        # Check the status code of the response
        if response.status_code != 200:
            logging.error(f"Error: Status code {response.status_code}")
            return
        
        logging.info(f"Status code: {response.status_code}")

        # Get the JSON data from the response
        try:
            cards = response.json()
            logging.debug(f"Cards: {cards}")
        except Exception as e:
            logging.error(f"Error getting JSON data from response: {e}")
            return
        
        # Save the data to a JSON file
        logging.info("Saving data to JSON file...")

        # Make the set name file system friendly
        set_name = set_name.replace(" ", "_").lower()
        file_path = f"{self.sets_dir}/{set_name}.json"

        # Save the cards to a JSON file
        try:
            with open(file_path, "w") as file:
                json.dump(cards, file)
            logging.info(f"Data saved to {file_path}")
        except Exception as e:
            logging.error(f"Error saving data to {file_path}: {e}")
            return

        logging.info(f"Finished getting cards for set {set_name} from Lorcast API.")

        # Return the cards data
        return cards
        
    def get_images(self, cards_json, set_name):
        """
        Get the images for the cards in a set and save them to a directory.

        Parameters:
            card_json (list): A list of card data in JSON format.
            set_name (str): The name of the set.
        """
        logging.info(f"Getting images for cards in set {set_name}...")

        # Create the Image directory for each set name if it does not exist
        # Make the set name file system friendly
        set_name = set_name.replace(" ", "_").lower()
        set_image_dir = f"{self.image_dir}/cards/{set_name}"

        try:
            if not os.path.exists(self.sets_dir):
                os.makedirs(self.sets_dir)
                logging.info(f"Directory {self.sets_dir} created.")
            else:
                logging.info(f"Directory {self.sets_dir} already exists.")
        except Exception as e:
            logging.error(f"Error creating directory {self.sets_dir}: {e}")
            return
    
        # Get image_uri for each card
        for card_data in cards_json:
            # Get the image URI for the card
            image_uri = card_data.get("image_uris").get("digital").get("large")
            logging.info(f"Image URI: {image_uri}")

            if image_uri:
                # Create file path for the image
                file_path = f"{set_image_dir}/{card_data.get('id')}.avif"
                logging.info(f"File path: {file_path}")

                # Download the image
                try:
                    # Wait 20 milliseconds
                    logging.info("Waiting 20 milliseconds...")
                    time.sleep(0.02)

                    logging.info("Downloading image...")
                    response = requests.get(image_uri)
                    with open(file_path, "wb") as file:
                        file.write(response.content)
                    logging.info(f"Image downloaded: {file_path}")
                except Exception as e:
                    logging.error(f"Error downloading image: {e}")
                    return

    def run(self):
        logging.info("Starting Lorcast API scraper...")

        # Set the start time
        start_time = time.time()

        # Get Disney Lorcana Sets from the API
        sets = self.get_sets()

        # Wait 20 milliseconds
        logging.info("Waiting 20 milliseconds...")
        time.sleep(0.02)

        # Get the cards for each set
        for set in sets:
            set_id = set.get("id")
            set_name = set.get("name")

            # Wait 20 milliseconds
            logging.info("Waiting 20 milliseconds...")
            time.sleep(0.02)

            # Get the cards for the set
            cards = self.get_cards(set_id, set_name)

            # Get the images for provided cards
            self.get_images(cards, set_name)

        # Set the end time
        end_time = time.time()

        # Calculate the duration of the scraper
        duration = end_time - start_time
        logging.info(f"Lorcast API scraper duration: {duration} seconds.")

        logging.info("Lorcast API scraper finished.")

if __name__ == "__main__":
    scraper = LorcastScraper()
    scraper.run()

    