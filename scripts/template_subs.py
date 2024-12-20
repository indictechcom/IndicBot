# -*- coding: utf-8 -*-
from botscripts.action import WikiAction
from botscripts.diff import diff

import xlrd
import mwparserfromhell as mw
import time
from requests import Session
from typing import Any

def run_template_subs(session: Session) -> None:
    """ 
    Script to add or replace template parameter
    Args:
        session (Session): A requests.Session object for making authenticated requests to the Wikipedia API.
    Returns:
        None
    """

    # Get the Filename from user
    xls_filename: str = input("Enter the Excel filename: ")

    #  Read the Excel File
    wb: Any = xlrd.open_workbook(xls_filename)
    sheet: Any = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)

    # Create WikiAction Object for making action
    action: WikiAction = WikiAction(session)

    # Variable to check user all response
    apply_all: bool = False

    for i in range(sheet.nrows - 1):
        # Get the Wikipage name from the Sheet's cell
        wikipage: Any = sheet.cell_value(i + 1, 0)

        # Get the wikitext of Wikipage
        oldtext: str|None = action.get_pagecontent(wikipage)

        if oldtext is not None:
            text: Any = mw.parse(oldtext)

            # Get the template name, parameter and its value
            param: Any = sheet.cell_value(i + 1, 1)
            value: Any = sheet.cell_value(i + 1, 2)
            template_name: Any = sheet.cell_value(i + 1, 3)

            for template in text.filter_templates():
                if template.name.matches(template_name):

                    # Add or replace template parameter value
                    template.add(param, value)

                    # Halt the execution for 1 sec
                    time.sleep(1)

                    # Check oldtext and text
                    if oldtext != text:

                        # Make and print the diff
                        print('\nDiff of Wikipage - ' + wikipage)
                        diff(oldtext, text)

                        if apply_all is False:
                            # User prompt
                            res: str = input("Do you want the chagnes (Yes - y, No - n, All - a, Quit- q)? ").lower()

                            # Edit the page on y or yes response
                            if (res == 'y') or (res == 'yes'):
                                # Edit the page
                                action.edit_page(wikipage, str(text))

                            # Skip the page on n or no response
                            elif (res == 'n') or (res == 'no'):
                                continue

                            elif (res == 'a') or (res == 'all'):
                                apply_all = True

                                # Edit the page
                                action.edit_page(wikipage, str(text))

                            elif (res == 'q') or (res == 'quit'):
                                return

                            else:
                                print(" Wrong input :(")
                                return

                        else:
                            # Edit the page
                            action.edit_page(wikipage, str(text))

                    else:
                        # Print message if there is no change
                        print(wikipage + ' - ' + 'No Changes!')
        else:
            continue
