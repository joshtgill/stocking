import sys
sys.path.append('common/')
sys.path.append('query/')
sys.path.append('trade/')
import os
from stocking import Stocking


if __name__ == "__main__":
    # Set stocking/ as working directory
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    os.chdir('..')

    # Start Stocking with main config file
    Stocking(sys.argv[1], int(sys.argv[2])).start()
