# -*- coding: utf-8 -*-
import requests
import config
import getpass
from typing import Optional

Ses: requests.Session = requests.Session()


def fetch_login_token() -> str:
    """ 
    Fetch login token via `tokens` module 
    Args:
        None
    Returns:
        str: Returns the login token
    """

    response: requests.Response = Ses.get(
        url=config.WIKI_API_ENDPOINT,
        params= {
            'action': "query",
            'meta': "tokens",
            'type': "login",
            'format': "json"
        }
    )
    data: dict = response.json()
    return data['query']['tokens']['logintoken']


def login() -> Optional[requests.Session]:
    """ 
    Send a post request along with login token 
    Args:
        None
    Returns:
        Optional[requests.Session]: Returns the session object if successful, None otherwise.
    """

    login_token: str  = fetch_login_token()

    # Get the password from user
    password: str = getpass.getpass()

    response: requests.Response = Ses.post(
        config.WIKI_API_ENDPOINT,
        data ={
            'action': "clientlogin",
            'username': config.USERNAME,
            'password': password,
            'loginreturnurl': 'http://127.0.0.1/',
            'logintoken': login_token,
            'format': "json"
        }
    )

    data: dict = response.json()

    if data['clientlogin']['status'] == 'PASS':
        print('Login success! Welcome, ' + data['clientlogin']['username'] + '!')
        return Ses
    else:
        print('Oops! Something went wrong -- ' + data['clientlogin']['messagecode'])
        return None
