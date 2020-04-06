# -*- coding: utf-8 -*-
# Copyright Lovac42
# Copyright Ankitects Pty Ltd and contributors
# Used/unused kanji list code originally by 'LaC'
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from .lib.com.lovac42.anki.version import CCBC
if CCBC:
    from . import stats
