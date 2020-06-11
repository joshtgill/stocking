import sys
sys.path.append('common/')
sys.path.append('query/')
sys.path.append('process/')
sys.stdout = open('log/output.log', 'w+')
import os
from stocking import Stocking


if __name__ == "__main__":
    # Set stocking/ as working directory
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    os.chdir('..')

    # Start Stocking with config
    stocking = Stocking(sys.argv[1])
    stocking.query()
