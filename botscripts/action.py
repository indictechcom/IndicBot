# -*- coding: utf-8 -*-
import config
from typing import Optional
from requests import Session, Response


class WikiAction():

    def __init__(self, session: Session) -> None:
        self.session: Session = session

    def get_crsf_token(self) -> Optional[str]:
        """ 
        Function to get the login token via `tokens` module 
        Args:
            session (Session): A requests.Session object for making authenticated requests to the Wikipedia API.
        Returns:
            Optional[str]: Returns the login token if successful, None otherwise.
        """

        response: Response = self.session.get(
            url=config.WIKI_API_ENDPOINT,
            params={
                'action': "query",
                'meta': "tokens",
                'format': "json"
            }
        )
        data: dict = response.json()
        try:
            return data['query']['tokens']['csrftoken']
        except:
           return  None

    def get_pagecontent(self, page) -> Optional[str]:
        """ 
        Function to get the wikitext of Wikipage "
        Args:
            page (str): The name of the page whose content is to be fetched.
        Returns:
            Optional[str]: Returns the wikitext of the page if successful, None otherwise.
        """

        response: Response = self.session.get(
            url=config.WIKI_API_ENDPOINT,
            params={
                "action": "parse",
                "format": "json",
                "page": page,
                "prop": "wikitext"
            }
        )
        data: dict = response.json()
        try:
            if 'parse' in data:
                return data['parse']['wikitext']['*']
            else:
                print('\n' + page + ' - ' + data['error']['info'])
                return None
        except:
            return None


    def edit_page(self, page: str, content: str, summary: str='') -> None:
        """ 
        Function to edit the Wikipage 
        Args:
            page (str): The name of the page to be edited.
            content (str): The new wikitext content of the page.
            summary (str): The edit summary.
        Returns:
            None
        """

        crsftoken: str|None = self.get_crsf_token()
        response: Response = self.session.post(
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
        data: dict = response.json()
        try:
            if data['edit']['result'] == 'Success':
                print(page + ' - ' + 'Changes Done!')
        except:
            print(page + ' - ' + 'Changes Failed!')
