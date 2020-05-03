import sys
sys.path.append('interfaces/')
sys.path.append('services/')
sys.path.append('forms/')
from stocking import Stocking


if __name__ == "__main__":
    Stocking('data/config.json').start()
