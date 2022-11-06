from configparser import ConfigParser
from decimal import Decimal
from os import environ
import sys

from ccxt import exchanges

# This script loads the ini file specified and checks if all options are set and of the right type and
# makes logical sense. It also outputs a nice config class that is easier to work with

#TODO: Replace all raise with decent messages (possibly multi language capable)

class Telegram:
    def __init__(self, bottoken, chatid):
        self.bottoken = bottoken
        self.chatid = chatid

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
    def __init__(self, low, high, close, time):
        self.low = Decimal(low)
        if self.low < 0:
            raise

        self.high = Decimal(high)
        if self.high < 0:
            raise

        self.close = close

        self.time = int(time)
        if self.time < 0:
            raise


class Start:
    def __init__(self, low, high, amount, order, location, shift):
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
        if self.order not in {'buy', 'sell'}:
            raise

        self.location = location
        if self.location not in {'above', 'below'}:
            raise

        self.location_shift = Decimal(shift)
        if self.location_shift <0:
            raise

class Bounds:
    def __init__(self, high, low, step):
        self.high = Decimal(high)
        if self.high < 0:
            raise

        self.low = Decimal(low)
        if self.low < 0:
            raise

        self.step = Decimal(step)
        if self.step <= 0:
            raise


class Orders:
    def __init__(self, above, below, size):
        self.above = int(above)
        if self.above < 1:
            raise

        self.below = int(below)
        if self.below < 1:
            raise

        self.size = Decimal(size)
        if self.size <= 0:
            raise


class Type:
    def __init__(self, above, below, leverage, market, name, direction):
        self.above = above
        if self.above not in {'buy', 'sell'}:
            raise

        self.below = below
        if self.below not in {'buy', 'sell'}:
            raise

        self.leverage = int(leverage)
        if self.leverage < 1:
            raise

        self.market = market
        if market == '':
            raise

        self.name = name
        if name == '':
            raise
        
        self.direction = direction
        if self.direction not in {'short', 'long'}:
            raise


class Config:
    def __init__(
        self,
        orderAbove, orderBelow, orderSize,
        typeAbove, typeBelow, typeLeverage, typeMarket, typeName, typeDirection,
        boundsHigh, boundsLow, boundsStep,
        startLow, startHigh, startAmount, startOrder, startLocation, startLocationShift,
        stopLow, stopHigh, stopClose, stopTime,
        exchangeName, exchangeKey, exchangeSecret,
        telegramBotToken, telegramChatID,
    ):
        self.orders = Orders(orderAbove, orderBelow, orderSize)
        self.type = Type(typeAbove, typeBelow, typeLeverage, typeMarket, typeName, typeDirection)
        self.bounds = Bounds(boundsHigh, boundsLow, boundsStep)
        self.start = Start(startLow, startHigh, startAmount, startOrder, startLocation, startLocationShift)
        self.stop = Stop(stopLow, stopHigh, stopClose, stopTime)
        self.exchange = Exchange(exchangeName, exchangeKey, exchangeSecret)
        self.telegram = Telegram(telegramBotToken, telegramChatID)


if len(sys.argv) < 2:
    CONFIG = None
else:
    config = ConfigParser()
    config.read(f'strategies/{sys.argv[1]}/strategy.ini')

    CONFIG = Config(
        config['orders']['above'],
        config['orders']['below'],
        config['orders']['size'],
        config['type']['above'],
        config['type']['below'],
        config['type']['leverage'],
        config['type']['market'],
        config['type']['name'],
        config['type']['direction'],
        config['bounds']['high'],
        config['bounds']['low'],
        config['bounds']['step'],
        config['start']['low'],
        config['start']['high'],
        config['start']['amount'],
        config['start']['order'],
        config['start']['location'],
        config['start']['location_shift'],
        config['stop']['low'],
        config['stop']['high'],
        config['stop'].getboolean('close'),
        config['stop']['time'],
        config['exchange']['name'],
        # Replace these with INI settings on first release
        environ['exchange.apikey'] if 'exchange.apikey' in environ else config['exchange']['apikey'],
        environ['exchange.secret'] if 'exchange.secret' in environ else config['exchange']['secret'],
        environ['telegram.bottoken'] if 'telegram.bottoken' in environ else config['telegram']['bottoken'],
        environ['telegram.chatid'] if 'telegram.chatid' in environ else config['telegram']['chatid'],
        )

