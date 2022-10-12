from sys import argv
from create import create
from run import run
from check import check
from saidia import saidia

def main():
    if argv[1] == 'create':
        create()
        return

    if argv[1] == 'run':
        run()
        return

    if argv[1] == 'check':
        check()
        return

    if argv[1] == 'help':
        saidia()
        return

              
if __name__ == "__main__":
    main()
