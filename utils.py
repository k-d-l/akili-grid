import datetime
from requests import get
from urllib import parse


def log(msg):
    print(datetime.datetime.now().isoformat(), msg)
    params = {
        'chat_id': 117223531,
        'text': msg
    }

    payload_str = parse.urlencode(params, safe='@')
