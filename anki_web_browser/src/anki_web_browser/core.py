# -*- coding: utf-8 -*-
# This file has been modified by lovac42 for CCBC, and is not the same as the original.

# Contains center components useful across this addon
# Holds Contansts

# This files is part of anki-web-browser addon
# @author ricardo saturnino
# ------------------------------------------------


class Label:
    CARD_MENU = 'Search in &Web'
    BROWSER_ASSIGN_TO = '&Assign to field'


# --------------------------- Useful function ----------------------------

class Feedback:
    'Responsible for messages and logs'

    @staticmethod
    def log(*args, **kargs):
        pass
        # print(args, kargs)

    @staticmethod
    def showInfo(*args):
        pass

    @staticmethod
    def showWarn(*args):
        pass

    @staticmethod
    def showError(*args):
        pass