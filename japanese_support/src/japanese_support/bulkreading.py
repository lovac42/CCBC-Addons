# -*- coding: utf-8 -*-
# Copyright: Ankitects Pty Ltd and contributors
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# Bulk update of readings.
#

from aqt.qt import *
from anki.hooks import addHook
from .reading import mecab
from .notetypes import isJapaneseNoteType
from aqt import mw

from .main import conf


# Bulk updates
##########################################################################

def regenerateReadings(nids):
    global mecab
    mw.checkpoint("Bulk-add Readings")
    mw.progress.start()
    for nid in nids:
        note = mw.col.getNote(nid)
        # Amend notetypes.py to add your note types
        _noteName = note.model()['name'].lower()
        if not isJapaneseNoteType(_noteName):
            continue

        src = None
        srcFields = conf.get('srcFields')
        for field in srcFields:
            if field in note:
                src = field
                break
        if not src:
            # no src field
            continue
        # dst is the destination field for the Readings
        dst = None
        dstFields = conf.get('dstFields')
        for field in dstFields:
            if field in note:
                dst = field
                break
        if not dst:
            # no dst field
            continue
        if note[dst]:
            # already contains data, skip
            continue
        srcTxt = mw.col.media.strip(note[src])
        if not srcTxt.strip():
            continue
        try:
            note[dst] = mecab.reading(srcTxt)
        except Exception as e:
            mecab = None
            raise
        note.flush()
    mw.progress.finish()
    mw.reset()

def setupMenu(browser):
    a = QAction("Japanese Support: Bulk-add Readings", browser)
    a.triggered.connect(lambda: onRegenerate(browser))
    browser.form.menuTool.addSeparator()
    browser.form.menuTool.addAction(a)

def onRegenerate(browser):
    regenerateReadings(browser.selectedNotes())

addHook("browser.setupMenus", setupMenu)
