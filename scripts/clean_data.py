from utils.disney_lorcana_cleanup import DisneyLorcanaCleanup
from utils.lorcast_cleanup import LorcastCleanup

if __name__ == '__main__':
    # Create an instance of the DisneyLorcanaCleanup class
    dlc = DisneyLorcanaCleanup()

    # Call the clean_sets method
    dlc.clean_sets()

    # Create an instance of the LorcastCleanup class
    lcc = LorcastCleanup()

    # Call the clean_sets and clean_cards methods
    lcc.clean_sets()
    lcc.clean_cards()