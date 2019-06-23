# -*- coding: utf-8 -*-

import difflib


def diff(oldtext, newtext):
    """ Diff the text """

    oldtext_lines = oldtext.splitlines()
    newtext_lines = newtext.splitlines()

    for line in difflib.unified_diff(oldtext_lines, newtext_lines,
                                     fromfile='Before', tofile='After',
                                     n=0, lineterm=''):
        print(line)
