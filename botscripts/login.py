# -*- coding: utf-8 -*-

import requests
import config
import getpass

Ses = requests.Session()


def fetch_login_token():
    """ Fetch login token via `tokens` module """

    response = Ses.get(
        url=config.WIKI_API_ENDPOINT,
        params= {
            'action': "query",
            'meta': "tokens",
            'type': "login",
            'format': "json"
        }
    )
    data = response.json()
    return data['query']['tokens']['logintoken']


def login():
    """ Send a post request along with login token """

    login_token = fetch_login_token()

    # Get the password from user
    password = getpass.getpass()

    response = Ses.post(
        config.WIKI_API_ENDPOINT,
        data={
            'action': "clientlogin",
            'username': config.USERNAME,
            'password': password,
            'loginreturnurl': 'http://127.0.0.1/',
            'logintoken': login_token,
            'format': "json"
        }
    )

    data = response.json()

    if data['clientlogin']['status'] == 'PASS':
        print('Login success! Welcome, ' + data['clientlogin']['username'] + '!')
        return Ses
    else:
        print('Oops! Something went wrong -- ' + data['clientlogin']['messagecode'])
        return None
