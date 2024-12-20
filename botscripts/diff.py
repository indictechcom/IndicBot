# -*- coding: utf-8 -*-

import difflib


def diff(oldtext: str, newtext: str) -> None:
    """ 
    Diff the text 
    Args:
        oldtext (str): The old text
        newtext (str): The new text
    Returns:
        None
    """

    oldtext_lines: list  = oldtext.splitlines()
    newtext_lines: list = newtext.splitlines()

    for line in difflib.unified_diff(oldtext_lines, newtext_lines,
                                     fromfile='Before', tofile='After',
                                     n=0, lineterm=''):
        print(line)
