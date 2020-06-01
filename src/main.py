import sys
sys.path.append('common/')
sys.path.append('query/')
sys.path.append('learn/')
import os
from stocking import Stocking


if __name__ == "__main__":
    # Set stocking/ as working directory
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    os.chdir('..')

    # Start Stocking with main config file and action
    Stocking(sys.argv[1]).start(int(sys.argv[2]))
