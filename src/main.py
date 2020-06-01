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

    # Start Stocking with config based on action
    stocking = Stocking()
    action = sys.argv[1].lower()
    if action == 'query':  # Query
        stocking.query(sys.argv[2])
    elif action == 'learn':  # Learn
        stocking.learn()
