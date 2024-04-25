import pytz
import requests
from datetime import datetime


def get_current_gmt_time():

    try:
        response = requests.get(
            'http://worldtimeapi.org/api/timezone/Etc/GMT').json()

        return response['datetime']

    except Exception:

        return datetime.now(pytz.timezone('GMT'))
