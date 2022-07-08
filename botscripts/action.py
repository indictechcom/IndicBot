# -*- coding: utf-8 -*-
import config


class WikiAction():

    def __init__(self, session):
        self.session = session

    def get_crsf_token(self):
        """ Function to get the login token via `tokens` module """

        response = self.session.get(
            url=config.WIKI_API_ENDPOINT,
            params={
                'action': "query",
                'meta': "tokens",
                'format': "json"
            }
        )
        data = response.json()
        try:
            return data['query']['tokens']['csrftoken']
        except:
           return  None

    def get_pagecontent(self, page):
        """ Function to get the wikitext of Wikipage """

        response = self.session.get(
            url=config.WIKI_API_ENDPOINT,
            params={
                "action": "parse",
                "format": "json",
                "page": page,
                "prop": "wikitext"
            }
        )
        data = response.json()
        try:
            if 'parse' in data:
                return data['parse']['wikitext']['*']
            else:
                print('\n' + page + ' - ' + data['error']['info'])
                return None
        except:
            return None


    def edit_page(self, page, content, summary=''):
        """ Function to edit the Wikipage """

        crsftoken = self.get_crsf_token()
        response = self.session.post(
            url=config.WIKI_API_ENDPOINT,
            data={
                "action": "edit",
                "title": page,
                "text": content,
                "summary": summary,
                "nocreate": True,
                "token": crsftoken,
                "format": "json"
            }
        )
        data = response.json()
        try:
            if data['edit']['result'] == 'Success':
                print(page + ' - ' + 'Changes Done!')
        except:
            print(page + ' - ' + 'Changes Failed!')

