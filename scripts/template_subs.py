# -*- coding: utf-8 -*-
from botscripts.action import WikiAction

import xlrd
import mwparserfromhell as mw
import time


def run_template_subs(session):
    """ Script to add or replace template parameter"""

    # Get the Filename from user
    xls_filename = input("Enter the Excel filename: ")

    #  Read the Excel File
    wb = xlrd.open_workbook( xls_filename )
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)

    # Create WikiAction Object for making action
    action = WikiAction(session)

    for i in range(sheet.nrows - 1):
        # Get the Wikipage name from the Sheet's cell
        wikipage = sheet.cell_value(i + 1, 0)

        # Get the wikitext of Wikipage
        oldtext = action.get_pagecontent(wikipage)

        if oldtext is not None:
            text = mw.parse(oldtext)

            # Get the template name, parameter and its value
            param = sheet.cell_value(i + 1, 1)
            value = sheet.cell_value(i + 1, 2)
            template_name = sheet.cell_value(i + 1, 3)

            for template in text.filter_templates():
                if template.name.matches(template_name):

                    # Add or replace template parameter value
                    template.add(param, value)

                    # Halt the execution for 1 sec
                    time.sleep(1)

                    # Check oldtext and text
                    if oldtext != text:
                        action.edit_page(wikipage, str(text))
                    else:
                        # Print message if there is no change
                        print(wikipage + ' - ' + 'No Changes!')
        else:
            continue
