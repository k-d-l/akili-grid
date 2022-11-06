import ccxt
import datetime
from decimal import Decimal

from config import CONFIG
from utils import log
import time
import sys

def main():
    def get_price(exchange, market, price = -1):
        if price == -1:
            price = exchange.fetch_ticker(market)['last']
        return Decimal(exchange.price_to_precision(market,price))
    
    startTime = datetime.datetime.now()
    
    log(f'Start time {startTime.isoformat()}')
    log('Connecting to exchange')
    xchange = ccxt.ftx({
        'apiKey': CONFIG.exchange.key,
        'secret': CONFIG.exchange.secret,
    })
    xchange.headers = {
        'FTX-SUBACCOUNT': 'Sub_1',
    }
    
    pair = CONFIG.type.market;
    
#     price = get_price(xchange, pair)
#     log(f'Base price is {price}. Waiting for start price.')
#     while not(price > CONFIG.start.low and price < CONFIG.start.high):
#         price = get_price(xchange, pair)

    #loops to start grid (3 attempts by 300s (10*30) diff < 0.07 else podtyazhka) 
    for i in range(3):
        #fetch current price
        price = get_price(xchange, pair)
        log(f'Loop ({i}): Current {CONFIG.type.market} price at {price}')
        
        #starting order
        if CONFIG.type.direction == 'long':
            gridPrice = get_price(xchange, pair, price*(1-CONFIG.start.location_shift/100))
        else:
            gridPrice = get_price(xchange, pair, price*(1+CONFIG.start.location_shift/100))
        
        amount = xchange.amount_to_precision(pair, CONFIG.start.amount)
        
        log(f'Loop ({i}): Placing start {CONFIG.type.direction} order {CONFIG.start.amount}@{gridPrice}')
        
        if CONFIG.type.direction == 'long':
            order_id = xchange.createLimitBuyOrder(pair, amount, gridPrice)['id']
        if CONFIG.type.direction == 'short':
            order_id = xchange.createLimitSellOrder(pair, amount, gridPrice)['id']
     
        get_in = False
        
        delay_before_podtyazhka = 2#in loops ()
        for j in range(10):# 10 loops by 30s = 300s with one price
            price = get_price(xchange, pair)
            priceDiff = abs(100*(gridPrice - price)/price)
            status = xchange.fetch_order(order_id)['status']
            log(f'Loop ({i}): Oreder:{order_id} Diff:{priceDiff:1.5} status:{status}')  
            if status=='closed':
                log(f'Loop ({i}): Oreder:{order_id} !!!Was closed')
                get_in = True
                break
            if status=='canceled':
                log(f'Loop ({i}): Oreder:{order_id} !!!Order canceled')
                break
            if priceDiff>0.5:
                if delay_before_podtyazhka:
                    delay_before_podtyazhka -= 1
                    log(f'Loop ({i}): Oreder:{order_id} Diff:{priceDiff:1.5} !!!Delay before podtyazhka #{delay_before_podtyazhka}')   
                else:
                    log(f'Loop ({i}): Oreder:{order_id} Diff:{priceDiff:1.5} !!!Подтяжка')
                    break         
            time.sleep(30)
        log(f'Next Loop.')
        if (not get_in):
            while xchange.fetch_order(order_id)['status'] in ['open']:
                xchange.cancel_order(order_id)
                time.sleep(1)
        else:
            break
     
     
    if  (not get_in):
        log("We're out")
        sys.exit(0)
        
    else:
        log("We're in")
        sys.exit(0)
    
    
    
    #empty grid
    grid = {}
    #list of prices
    gridList = [gridPrice]
    #order is none on that price
    grid[gridPrice] = None 
    
    
    gridList += [gridPrice]
    gridPrice += CONFIG.bounds.step

    # Main loop
    price = Decimal(xchange.fetch_ticker(CONFIG.type.market)['last'])
    log('Starting main loop.')
    # I use while true and several separate exit conditions because the boolean logic
    # becomes a headache: There are too many exit conditions to concot one massive while clause        
    while True:

        # EXIT Conditions
        if price < CONFIG.stop.low or price > CONFIG.stop.high:
            break

        if (datetime.datetime.now() - startTime).total_seconds() > CONFIG.stop.time:
            break

        #TODO: This can be optimised by getting all open orders from the exchange in one call before
        # executing the loop instead of calling the exchange to check for each order. But for now, this works.

        #TODO: Also need to think of a better way to handle high frequency grids, if several orders have been filled
        # as price falls this will work, but not as it goes up
        for gridIndex in range(0, len(gridList)):
            if grid[gridList[gridIndex]] is not None:
                # Check if order is still alive
                print(grid[gridList[gridIndex]],xchange.fetch_order(grid[gridList[gridIndex]])['status'])
                if xchange.fetch_order(grid[gridList[gridIndex]])['status'] == 'closed':
                    # Order has been closed. Mark as closed
                    log(f'Order at {gridList[gridIndex]} filled.')
                    grid[gridList[gridIndex]] = None

                    # Check or place new orders below and remove any not needed
                    numOrders = 1
                    for newIndex in reversed(range(0, gridIndex)):
                        if grid[gridList[newIndex]] is None and numOrders <= CONFIG.orders.below:
                            log(f'Placing {CONFIG.type.below} order at price {gridList[newIndex]} below')
                            if CONFIG.type.below == 'buy':
                                grid[gridList[newIndex]] = xchange.createLimitBuyOrder(CONFIG.type.market, CONFIG.orders.size, gridList[newIndex])['id']
                            if CONFIG.type.below == 'sell':
                                grid[gridList[newIndex]] = xchange.createLimitSellOrder(CONFIG.type.market, CONFIG.orders.size, gridList[newIndex])['id']

                        if numOrders > CONFIG.orders.below and grid[gridList[newIndex]] is not None:
                            xchange.cancel_order(grid[gridList[newIndex]])
                            grid[gridList[newIndex]] = None

                        numOrders += 1

                    # Check or place new above and remove any not needed
                    numOrders = 1
                    for newIndex in range(gridIndex + 1, len(gridList)):
                        if grid[gridList[newIndex]] is None and numOrders <= CONFIG.orders.above:
                            log(f'Placing {CONFIG.type.above} order at price {gridList[newIndex]} above')
                            if CONFIG.type.above == 'buy':
                                grid[gridList[newIndex]] = xchange.createLimitBuyOrder(CONFIG.type.market, CONFIG.orders.size, gridList[newIndex])['id']
                            if CONFIG.type.above == 'sell':
                                grid[gridList[newIndex]] = xchange.createLimitSellOrder(CONFIG.type.market, CONFIG.orders.size, gridList[newIndex])['id']

                        if numOrders > CONFIG.orders.above and grid[gridList[newIndex]] is not None:
                            xchange.cancel_order(grid[gridList[newIndex]])
                            grid[gridList[newIndex]] = None

                        numOrders += 1

        price = Decimal(xchange.fetch_ticker(CONFIG.type.market)['last'])
    log("Exiting main loop let's find out why.")
    #TODO: Finish the app 😁


if __name__ == "__main__":
    main()
