import sys
import ccxt
import datetime
from decimal import Decimal

from config import loadConfig
from utils import log


def main():
    log('Loading strategy')
    CONFIG = loadConfig(sys.argv[1])
    
    log('Connecting to exchange')
    xchange = ccxt.ftx()

    log('Fetching ticker')
    price = Decimal(xchange.fetch_ticker(CONFIG.type.market)['last'])

    # Wait for start trigger
    log('Waiting for start trigger...')
    while price > CONFIG.start.low and price < CONFIG.start.high:
        price = Decimal(xchange.fetch_ticker(CONFIG.type.market)['last'])

    # Executing initial order


if __name__ == "__main__":
    log('Script start.')
    main()
    log('Script end.')