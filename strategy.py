# This file contains the various settings for the grid strategy.
# All prices are on the quote currency (e.g. BTC)

# Each setting is preceded by a comment explaining what it does. All settings must be defined in this file 
# so do not comment out any.

# Total number of active buy orders at any given time
TOTAL_BUY_ORDERS = 1

# Total number of active sell orders at any given time
TOTAL_SELL_ORDERS = 1

# Lowe grid price
LOW_PRICE = 18000

# High grid price
HIGH_PRICE = 20000

# Number of grids between low and high price (including low and high price)
GRID_COUNT = 3

# Grid gets updated when price goes below TRIGGER_PRICE
TRIGGER_PRICE = None

# Grid gets disable when price goes above TAKE_PROFIT_PRICE
TAKE_PROFIT_PRICE = None

# Grid gets disable when price goes below STOP_LOSS_PRICE
STOP_LOSS_PRICE = None
