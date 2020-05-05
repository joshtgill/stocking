import sys
sys.path.append('interfaces/')
sys.path.append('services/')
sys.path.append('objects/')
from stocking import Stocking


if __name__ == "__main__":
    Stocking(sys.argv[1]).start()
