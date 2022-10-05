import sys
from config import loadConfig
import pprint

def main():
    CONFIG = loadConfig(sys.argv[1])

if __name__ == "__main__":
    main()