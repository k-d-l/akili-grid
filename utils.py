import datetime
from requests import get
from urllib import parse
from config import CONFIG


def log(msg):
    msg = CONFIG.type.name + ':' + msg
    print(datetime.datetime.now().isoformat(), msg)

    #TODO: Calling telegram API slows things down considerably. This should be an async call so it doesn't slow down
    # the script, especially when running a high frequency grid
    if CONFIG.telegram.bottoken == '' or CONFIG.telegram.chatid == '':
        return

    params = {
        'chat_id': CONFIG.telegram.chatid,
        'text': msg
    }
    payload_str = parse.urlencode(params, safe='@')
    get('https://api.telegram.org/bot' + CONFIG.telegram.bottoken + '/sendMessage', params=payload_str)
    

