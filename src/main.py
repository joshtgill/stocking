import sys
sys.path.append('shared/')
sys.path.append('query/')
sys.path.append('trade/')
import os
from stocking import Stocking


if __name__ == "__main__":
    # Set stocking/ as working directory
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    os.chdir('..')

    Stocking(sys.argv[1]).start()
