import sys
sys.path.append('services/')
sys.path.append('structures/')
from stocking import Stocking


if __name__ == "__main__":
    Stocking('config.json').start()
