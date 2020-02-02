# -*- coding: utf-8 -*-
# This file has been modified by lovac42 for CCBC, and is not the same as the original.

"""
This file is part of the Syntax Highlighting add-on for Anki.

Configuration shim between Anki 2.0 and Anki 2.1

Copyright: (c) 2018 Glutanimate <https://glutanimate.com/>
License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>
"""

import os
import io

from aqt import mw
from anki.utils import json
from anki.hooks import addHook

from .consts import *

###############################################################
###
# Configurable preferences
###
###############################################################

# Defaults conf
# - we create a new item in mw.col.conf. This syncs the
# options across machines (but not on mobile)
default_conf = {'linenos': True,  # show numbers by default
                'centerfragments': True,  # Use <center> when generating code fragments
                'cssclasses': False,  # Use css classes instead of colors directly in html
                'defaultlangperdeck': True,  # Default to last used language per deck
                'deckdefaultlang': {},  # Map to store the default language per deck
                'lang': 'Python'}  # default language is Python

###############################################################


# Synced conf

def sync_keys(tosync, ref):
    for key in [x for x in list(tosync.keys()) if x not in ref]:
        del(tosync[key])

    for key in [x for x in list(ref.keys()) if x not in tosync]:
        tosync[key] = ref[key]

def sync_config_with_default(col):
    if not 'syntax_highlighting_conf' in col.conf:
        col.conf['syntax_highlighting_conf'] = default_conf
    else:
        sync_keys(col.conf['syntax_highlighting_conf'], default_conf)

    # Mark collection state as modified, else config changes get lost unless
    # some unrelated action triggers the flush of collection data to db
    col.setMod()
    # col.flush()

# If config options have changed, sync with default config first
addHook("profileLoaded", lambda:sync_config_with_default(mw.col))




# added code to share dicts across modules.
class SharedConfig:
    local_conf={}

    def __init__(self):
        addHook("profileLoaded", self.profileLoaded)

    def profileLoaded(self):
        self.local_conf=mw.addonManager.getConfig(__name__)
        mw.addonManager.setConfigUpdatedAction(__name__, self.updateConfig)

    def updateConfig(self, conf):
        self.local_conf=conf

    def get(self, k):
        return self.local_conf.get(k)
