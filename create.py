# create.py handles everything to do with creating a new strategy folder structure, associated files
# and help text
import os
import shutil
from sys import argv
from slugify import slugify

def create():
    if argv[2] == 'help':
        print('''
        create help : Show this help.
        create mystrategy : Create new named mystrategy.
        ''')
        return

    strategyDIR = slugify(argv[2])
    os.makedirs(f'strategies/{strategyDIR}')
    shutil.copyfile('strategy.ini', f'strategies/{strategyDIR}/strategy.ini')
