import pandas as pd

class DisneyLorcana:
    def the_first_chapter(self):
        """
        Clean up the data for `The First Chapter` set
        """

        print('Cleaning up the data for `The First Chapter` set')

        # Load the CSV file
        csv_file = 'data/processed/disney_lorcana/the_first_chapter.csv'
        data = pd.read_csv(csv_file)

        # Remove Ink Types from the Card Name
        ink_types = ['AMBER', 'AMETHYST', 'EMERALD', 'RUBY', 'SAPPHIRE', 'STEEL']
        for ink_type in ink_types:
            data['card_name'] = data['card_name'].apply(lambda x: x.replace(ink_type, '').strip())
            print(f'Removed {ink_type} from the card name')
        
        # Remove `TOTAL` from the Card Name
        data['card_name'] = data['card_name'].apply(lambda x: x.replace('TOTAL', '').strip())
        print('Removed TOTAL from the card name')

        # Save the cleaned data
        data.to_csv(csv_file, index=False)

        print('Cleaned up the data for `The First Chapter` set')

    def rise_of_the_floodborn(self):
        """
        Clean up the data for `Rise of The Floodborn` set
        """

        print('Cleaning up the data for `Rise of The Floodborn` set')

        # Load the CSV file
        csv_file = 'data/processed/disney_lorcana/rise_of_the_floodborn.csv'
        data = pd.read_csv(csv_file)

        # Remove Ink Types from the Card Name
        ink_types = ['AMBER', 'AMETHYST', 'EMERALD', 'RUBY', 'SAPPHIRE', 'STEEL']
        for ink_type in ink_types:
            data['card_name'] = data['card_name'].apply(lambda x: x.replace(ink_type, '').strip())
            print(f'Removed {ink_type} from the card name')
        
        # Remove `TOTAL` from the Card Name
        data['card_name'] = data['card_name'].apply(lambda x: x.replace('TOTAL', '').strip())
        print('Removed TOTAL from the card name')

        # Save the cleaned data
        data.to_csv(csv_file, index=False)

        print('Cleaned up the data for `Rise of The Floodborn` set')

    def into_the_inklands(self):
        """
        Clean up the data for `Into the Inklands` set
        """

        print('Cleaning up the data for `Into the Inklands` set')

        # Load the CSV file
        csv_file = 'data/processed/disney_lorcana/into_the_inklands.csv'
        data = pd.read_csv(csv_file)

        # Remove Ink Types from the Card Name
        ink_types = ['AMBER', 'AMETHYST', 'EMERALD', 'RUBY', 'SAPPHIRE', 'STEEL']
        for ink_type in ink_types:
            data['card_name'] = data['card_name'].apply(lambda x: x.replace(ink_type, '').strip())
            print(f'Removed {ink_type} from the card name')
        
        # Remove `TOTAL` from the Card Name
        data['card_name'] = data['card_name'].apply(lambda x: x.replace('TOTAL', '').strip())
        print('Removed TOTAL from the card name')

        # Save the cleaned data
        data.to_csv(csv_file, index=False)

        print('Cleaned up the data for `Into the Inklands` set')

    def ursulas_return(self):
        """
        Clean up the data for `Ursulas Return` set
        """

        print('Cleaning up the data for `Ursulas Return` set')

        # Load the CSV file
        csv_file = 'data/processed/disney_lorcana/ursulas_return.csv'
        data = pd.read_csv(csv_file)

        # Remove Ink Types from the Card Name
        ink_types = ['AMBER', 'AMETHYST', 'EMERALD', 'RUBY', 'SAPPHIRE', 'STEEL']
        for ink_type in ink_types:
            data['card_name'] = data['card_name'].apply(lambda x: x.replace(ink_type, '').strip())
            print(f'Removed {ink_type} from the card name')
        
        # Remove `TOTAL` from the Card Name
        data['card_name'] = data['card_name'].apply(lambda x: x.replace('TOTAL', '').strip())
        print('Removed TOTAL from the card name')

        # Save the cleaned data
        data.to_csv(csv_file, index=False)

        print('Cleaned up the data for `Ursulas Return` set')

    def shimmering_skies(self):
        """
        Clean up the data for `Shimmering Skies` set
        """

        print('Cleaning up the data for `Shimmering Skies` set')

        # Load the CSV file
        csv_file = 'data/processed/disney_lorcana/shimmering_skies.csv'
        data = pd.read_csv(csv_file)

        # Remove Ink Types from the Card Name
        ink_types = ['AMBER', 'AMETHYST', 'EMERALD', 'RUBY', 'SAPPHIRE', 'STEEL']
        for ink_type in ink_types:
            data['card_name'] = data['card_name'].apply(lambda x: x.replace(ink_type, '').strip())
            print(f'Removed {ink_type} from the card name')
        
        # Remove `TOTAL` from the Card Name
        data['card_name'] = data['card_name'].apply(lambda x: x.replace('TOTAL', '').strip())
        print('Removed TOTAL from the card name')

        # Save the cleaned data
        data.to_csv(csv_file, index=False)

        print('Cleaned up the data for `Shimmering Skies` set')

if __name__ == '__main__':

    # Create an instance of the DisneyLorcana class
    disney_lorcana = DisneyLorcana()

    # Clean up the data for `The First Chapter` set
    disney_lorcana.the_first_chapter()

    # Clean up the data for `Rise of The Floodborn` set
    disney_lorcana.rise_of_the_floodborn()

    # Clean up the data for `Into the Inklands` set
    disney_lorcana.into_the_inklands()

    # Clean up the data for `Ursula's Return` set
    disney_lorcana.ursulas_return()

    # Clean up the data for `Shimmering Skies` set
    disney_lorcana.shimmering_skies()