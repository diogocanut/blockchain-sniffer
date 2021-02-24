import re

import requests


def get_my_ip():

    response = requests.get('http://checkip.dyndns.org').text
    ip = re.search("(?:[0-9]{1,3}\.){3}[0-9]{1,3}", response).group()

    return ip
