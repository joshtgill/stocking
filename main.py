import sys
sys.path.append('interfaces/')
sys.path.append('services/')
sys.path.append('objects/')
import os
from stocking import Stocking


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    Stocking(sys.argv[1]).start()
