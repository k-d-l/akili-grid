from configparser import ConfigParser
from decimal import Decimal
from ccxt import exchanges

# This script loads the ini file specified and checks if all options are set and of the right type and
# makes logical sense. It also outputs a nice config class that is easier to work with

class Exchange:
    def __init__(self, name, key, secret):
        self.name = name
        if self.name not in exchanges:
            raise
        
        self.key = key
        if self.key == '':
            raise

        self.secret = secret
        if self.secret == '':
            raise

class Stop:
    def __init__(self, low, high, close):
        self.low = Decimal(low)
        if self.low < 0:
            raise

        self.high = Decimal(high)
        if self.high < 0:
            raise

        self.close = close

class Start:
    def __init__(self, low, high, amount, order):
        self.low = Decimal(low)
        if self.low < 0:
            raise

        self.high = Decimal(high)
        if self.high < 0:
            raise

        if self.high < self.low:
            raise

        self.amount = Decimal(amount)
        if self.amount < 0:
            raise

        self.order = order
        if self.order not in {'buy','sell'}:
            raise


class Bounds:
    def __init__(self, high, low, step):
        self.high = Decimal(high)
        if self.high < 0:
            raise
        
        self.low = Decimal(low)
        if self.low < 0:
            raise

        self.step = Decimal(low)
        if self.step <= 0:
            raise

class Orders:
    def __init__(self, above , below):
        self.above = int(above)
        if self.above < 1:
            raise

        self.below = int(below)
        if self.below < 1:
            raise

class Type:
    def __init__(self, above, below, leverage, market):
        self.above = above
        if self.above not in {'buy','sell'}:
            raise

        self.below = below
        if self.below not in {'buy','sell'}:
            raise

        self.leverage = int(leverage)
        if self.leverage < 1:
            raise
        
        self.market = market

class Config:
     def __init__(
        self, 
        orderAbove ,orderBelow, 
        typeAbove, typeBelow, typeLeverage, typeMarket, 
        boundsHigh, boundsLow, boundsStep,
        startLow, startHigh, startAmount, startOrder,
        stopLow, stopHigh, stopClose,
        exchangeName, exchangeKey, exchangeSecret,
        ):
        self.orders = Orders(orderAbove ,orderBelow)
        self.type = Type(typeAbove, typeBelow, typeLeverage, typeMarket)
        self.bounds = Bounds(boundsHigh, boundsLow, boundsStep)
        self.start = Start(startLow, startHigh, startAmount, startOrder)
        self.stop = Stop(stopLow, stopHigh, stopClose)
        self.exchange = Exchange(exchangeName, exchangeKey, exchangeSecret)


def loadConfig(configFile):
    config = ConfigParser()
    config.read(configFile)

    return Config(
        config['orders']['above'],
        config['orders']['below'],
        config['type']['above'],
        config['type']['below'],
        config['type']['leverage'],
        config['type']['market'],
        config['bounds']['high'],
        config['bounds']['low'],
        config['bounds']['step'],
        config['start']['low'],
        config['start']['high'],
        config['start']['amount'],
        config['start']['order'],
        config['stop']['low'],
        config['stop']['high'],
        config['stop'].getboolean('close'),
        config['exchange']['name'],
        config['exchange']['key'],
        config['exchange']['secret'],    
    )