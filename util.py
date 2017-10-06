import os
import getpass
import sys

import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://forum-raspberrypi.de/'


def check_directory(directory):
    if not os.path.isdir(directory):
        os.mkdir(directory)
        return False
    return True


def get_token(line):
    return line.strip().replace('var SECURITY_TOKEN = ', '').replace(';', '').replace("'", '')


def login(username, password):
    session = requests.Session()
    soup = BeautifulSoup(session.get(BASE_URL).text, 'html5lib')
    java_script = str(soup.find('script'))
    token = [get_token(line) for line in java_script.split('\n') if 'var SECURITY_TOKEN' in line]
    data = {
        'username': username,
        'password': password,
        'useCookies': 1,
        't': token
    }
    session.post(BASE_URL + 'login', data=data)
    return session


def get_input(prompt, default=None, hidden=False):
    if default is not None:
        prompt += ' [{0}]'.format(default)
    prompt += ': '

    try:
        if hidden:
            value = getpass.getpass(prompt)
        else:
            try:
                # Python 2
                value = raw_input(prompt)
            except NameError:
                # Python 3
                value = input(prompt)
    except KeyboardInterrupt:
        print('\nInterrupted!')
        sys.exit()

    if default is not None and not value:
        return default
    else:
        return value
