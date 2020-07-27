import sys
import os
from stocking import Stocking


if __name__ == "__main__":
    # Set stocking/ as working directory
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    os.chdir('..')

    # Direct all output to file
    if not os.path.exists('out/'):
        os.mkdir('out/')
    sys.stdout = open('out/output.txt', 'w+')

    # Start Stocking with config
    Stocking(sys.argv[1], 'exe/settings.json').go()
