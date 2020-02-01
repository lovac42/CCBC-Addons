# -*- coding: utf-8 -*-
# Unknown author, taken from https://ankiweb.net/shared/info/1600138415

''' adds inline javascript to gif that restarts them when there are clicked '''

import re
from anki.hooks import addHook, wrap
from aqt import mw
from aqt.reviewer import Reviewer
from aqt.utils import showInfo

def gif_filter(qa_html, qa_type, fields, model, data, col):
    
    gifRegEx = "<img src=\"(.*?).gif\""
    
    def add_javascript(t):
        r = "%s onclick=\"this.src = (this.src + \'?x=\' + Math.random())\" style=\"cursor: pointer;\" %s" % (t.group(0)[0:5], t.group(0)[5:])
        return r
    
    return re.sub(gifRegEx, add_javascript, qa_html)

addHook("mungeQA", gif_filter)