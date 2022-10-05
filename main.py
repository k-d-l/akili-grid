import sys
import ccxt
from decimal import Decimal

from config import loadConfig
from utils import log


def main():
    log('Loading strategy')
    CONFIG = loadConfig(sys.argv[1])

    log('Connecting to exchange')
    xchange = ccxt.ftx({
        'apiKey': CONFIG.exchange.key,
        'secret': CONFIG.exchange.secret,
    })

    log('Fetching ticker')
    price = Decimal(xchange.fetch_ticker(CONFIG.type.market)['last'])

    # Wait for start trigger
    log(f'Base price is {price}. Waiting for start trigger...')
    while price > CONFIG.start.low and price < CONFIG.start.high:
        price = Decimal(xchange.fetch_ticker(CONFIG.type.market)['last'])

    log(f'Trigger hit. Price is {price}')

    log('Placing startup order')
    # Executing initial order

    log('Creating initial orders')
    # Place initial grid orders
    grid = CONFIG.bounds.low
    orders = 0
    while grid <= CONFIG.bounds.high and orders < CONFIG.orders.above:
        if grid > price:
            if CONFIG.type.above == 'sell':
                log(f'Creating sell order at {grid} above start price')
                xchange.createLimitSellOrder(CONFIG.type.market, CONFIG.orders.size, grid)
                orders += 1
            if CONFIG.type.above == 'buy':
                log(f'Creating buy order at {grid} above start price')
                xchange.createLimitBuyOrder(CONFIG.type.market, CONFIG.orders.size, grid)
                orders += 1
        grid += CONFIG.bounds.step

    grid = CONFIG.bounds.high
    orders = 0
    while grid >= CONFIG.bounds.low and orders < CONFIG.orders.below:
        if grid < price:
            if CONFIG.type.below == 'sell':
                log(f'Creating sell order at {grid} below start price')
                xchange.createLimitSellOrder(CONFIG.type.market, CONFIG.orders.size, grid)
                orders += 1
            if CONFIG.type.below == 'buy':
                log(f'Creating buy order at {grid} below start price')
                xchange.createLimitBuyOrder(CONFIG.type.market, CONFIG.orders.size, grid)
                orders += 1
        grid -= CONFIG.bounds.step


if __name__ == "__main__":
    log('Script start.')
    main()
    log('Script end.')
