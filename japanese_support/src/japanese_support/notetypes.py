"""
-*- coding: utf-8 -*-
Author: RawToast
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

Configure settings for the note types and source fields for the Japanese
Support plugin here

"""

from aqt import mw

from .main import conf


def isJapaneseNoteType(noteName):
    noteName = noteName.lower()
    for allowedString in conf.get("noteTypes"):
        if allowedString.lower() in noteName:
            return True

    return False
