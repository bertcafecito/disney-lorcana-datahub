import os
import requests
import pandas as pd

class LorcastScraper:
    def __init__(self):
        self.base_api_url = "https://api.lorcast.com/v0"
        self.raw_dir = "data/raw/lorcast_api"

        # Create the raw directory if it does not exist
        if not os.path.exists(self.raw_dir):
            os.makedirs(self.raw_dir) 
            print(f"Directory {self.raw_dir} created.")
        else:
            print(f"Directory {self.raw_dir} already exists.")

        self.image_dir = "images/lorcast_api"

        # Create the image directory if it does not exist
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir) 
            print(f"Directory {self.image_dir} created.")
        else:
            print(f"Directory {self.image_dir} already exists.")


    def get_sets(self):
        print("Getting sets from Lorcast API...")

        # Create the API URL for the sets endpoint
        url = f"{self.base_api_url}/sets"
        print(f"API URL: {url}")

        # Make the request to the API
        print("Making request to the API...")
        try:
            response = requests.get(url)
        except Exception as e:
            print(f"Error making request to the API: {e}")
            return
        print("Request successful.")

        # Check the status code of the response
        if response.status_code != 200:
            print(f"Error: Status code {response.status_code}")
            return
        print(f"Status code: {response.status_code}")

        # Get the JSON data from the response
        data = response.json()
        print(f"Data: {data}")

        # Number of sets
        num_of_sets = len(data.get("results"))
        print(f"Number of sets: {num_of_sets}")

        # Save the data to a CSV file
        print("Saving data to CSV file...")

        # Create the file path
        file_path = f"{self.raw_dir}/sets.csv"

        # Create a DataFrame from the data
        df = pd.DataFrame(data.get("results"))

        # Save the DataFrame to a CSV file
        df.to_csv(file_path, index=False)

        print(f"Data saved to {file_path}")

        return data.get("results")
    
    def get_cards(self, set_id, set_name):
        print(f"Getting cards for set {set_name} from Lorcast API...")

        # Maka the set name file system friendly
        set_name = set_name.replace(" ", "_").lower()

        # Create the API URL for the cards endpoint
        url = f"{self.base_api_url}/sets/{set_id}/cards"
        print(f"API URL: {url}")

        # Make the request to the API
        print("Making request to the API...")
        try:
            response = requests.get(url)
        except Exception as e:
            print(f"Error making request to the API: {e}")
            return
        print("Request successful.")

        # Check the status code of the response
        if response.status_code != 200:
            print(f"Error: Status code {response.status_code}")
            return
        print(f"Status code: {response.status_code}")

        # Get the JSON data from the response
        data = response.json()
        print(f"Data: {data}")

        # Save the data to a CSV file
        print("Saving data to CSV file...")

        # Create the file path
        file_path = f"{self.raw_dir}/sets/{set_name}.csv"

        # Create the directory if it does not exist
        set_dir = f"{self.raw_dir}/sets"
        if not os.path.exists(set_dir):
            os.makedirs(set_dir)
            print(f"Directory {set_dir} created.")
        else:
            print(f"Directory {set_dir} already exists.")

        # Create a DataFrame from the data
        df = pd.DataFrame(data)

        # Save the DataFrame to a CSV file
        df.to_csv(file_path, index=False)

        print(f"Data saved to {file_path}")

        return data

    def get_images(self, card_data, set_name):
        # Maka the set name file system friendly
        set_name = set_name.replace(" ", "_").lower()

        # Create card image directory
        card_image_dir = f"{self.image_dir}/cards/{set_name}"

        # Create the directory if it does not exist
        if not os.path.exists(card_image_dir):
            os.makedirs(card_image_dir)
            print(f"Directory {card_image_dir} created.")
        else:
            print(f"Directory {card_image_dir} already exists.")

        print("Getting image for a card...")
        card_id = card_data.get('id')
        
        # Get large image URL
        large_image_uri = card_data.get('image_uris').get('digital').get('large', None)

        if large_image_uri:
            image_file_path = f"{card_image_dir}/{card_id}.avif"
            print(f"Downloading image: {large_image_uri}")
            # Download the image
            with open(image_file_path, 'wb') as image:
                image.write(requests.get(large_image_uri).content)
            print(f"Image downloaded: {image_file_path}")


    def run(self):
        sets = self.get_sets()

        # Get the cards for each set
        for set in sets:
            cards = self.get_cards(set.get("id"), set.get("name"))

            # Get the images for each card
            for card in cards:
                self.get_images(card, set.get("name"))

if __name__ == "__main__":
    scraper = LorcastScraper()
    scraper.run()

    