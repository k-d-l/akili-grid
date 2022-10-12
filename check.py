# check.py handles everything to do with checking if the strategy.ini is valid
# eventually should also do a logical check in addition to a syntax check
import os
import shutil
from sys import argv
from slugify import slugify
from config import CONFIG

def check():
    if argv[2] == 'help':
        print('''
        check help : Show this help.
        check mystrategy : Checks if the strategy settings are valid.
        ''')
        return

    # Check stuff here
    print(CONFIG)