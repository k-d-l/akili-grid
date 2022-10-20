# create.py handles everything to do with creating a new strategy folder structure, associated files
# and help text
import os
import shutil
from sys import argv
from slugify import slugify

def main():
    strategyDIR = slugify(argv[1])
    os.makedirs(f'strategies/{strategyDIR}')
    shutil.copyfile('strategy.ini', f'strategies/{strategyDIR}/strategy.ini')

if __name__ == "__main__":
    main()
