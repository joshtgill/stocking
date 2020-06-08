import sys
sys.path.append('common/')
sys.path.append('query/')
sys.path.append('process/')
import os
from stocking import Stocking


if __name__ == "__main__":
    # Set stocking/ as working directory
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    os.chdir('..')

    # Start Stocking based on role with config if necessary
    stocking = Stocking()
    role = sys.argv[1].lower()
    if role == 'query':
        stocking.query(sys.argv[2])
    elif role == 'process':
        stocking.analyze()
