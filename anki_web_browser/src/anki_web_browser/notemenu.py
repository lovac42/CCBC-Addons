# -*- coding: utf-8 -*-
# This file has been modified by lovac42 for CCBC, and is not the same as the original.

# Plugin: anki-web-browser - Context menu for notes
# Responsible for adding options in the context menu on Anki notes
# Shows registered providers (websites) to search for the selected sentence
# --------------------------------------------

from .core import Label, Feedback
from PyQt4.QtGui import QMenu, QAction

class NoteMenuHandler:    
    _providers = []
    _controller = None
    _note = None
    _searchString = '{}'

    def __init__(self, note, query):
        self._note = note
        if query:
            self._searchString = query

    @classmethod
    def setOptions(clz, newValue):
        if newValue:
            clz._providers = newValue

    @classmethod
    def setController(clz, reference):
        if not reference:
            raise AttributeError('Controller must have a value')
        clz._controller = reference

    @staticmethod
    def onReviewerMenu(webView, menu, note):
        'Handles context menu event on Reviwer'

        if not webView.hasSelection():
            return

        _query = webView.selectedText()

        if not _query:
            return

        _instance = NoteMenuHandler(note, _query)
        _instance.showCustomMenu(menu)

    @staticmethod
    def onEditorMenu(webView, menu):
        """ Handles context menu event on Editor """

        if not webView.hasSelection():
            return

        _query = webView.selectedText()

        _note = webView.editor.note
        _instance = NoteMenuHandler(_note, _query)
        _instance.showCustomMenu(menu)

    def showCustomMenu(self, parentMenu):
        """ Builds the addon entry in the context menu, adding options according to the providers """

        submenu = QMenu(Label.CARD_MENU, parentMenu)

        for index, prov in enumerate(NoteMenuHandler._providers):
            act = QAction('(&' + str(index + 1) + ') ' + prov.name, submenu, 
                triggered=self._makeMenuAction(prov.url))
            submenu.addAction(act)

        parentMenu.addMenu(submenu)

    def _makeMenuAction(self, value):
        """
            Creates correct action for the context menu selection.
            Otherwise, it would repeat only the last element
        """

        return lambda: self.showInBrowser(value)

    def showInBrowser(self, website):
        if not self._controller:
            tooltip(_("Error! No Web Browser were found"), period=5000)

        self._controller.openInBrowser(website, self._searchString, self._note)

# -----------------------------------------------------------------------------