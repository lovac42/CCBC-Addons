
from aqt import mw
from aqt.qt import *
from anki.hooks import runHook, addHook

from .lib.com.lovac42.anki.gui import toolbar
from .main import conf


awesome_config = None
def getAwesomeConfig(c):
    global awesome_config
    awesome_config = c


js_menu = None
atts_menu = None
def load_menu():
    global atts_menu, js_menu

    runHook('AwesomeTTS.config', getAwesomeConfig)

    menu = mw.form.menuAddon
    js_menu = toolbar.getSubMenu(menu, "Japanese Support (CCBC)")
    atts_menu = toolbar.getSubMenu(js_menu, "AwesomeTTS Presets")

    sel = conf.get('speech')

    if awesome_config:
        for k,v in awesome_config["presets"].items():
            atts_menu.addAction(getAction(sel,k,k))
        atts_menu.addAction(getAction(sel))
        atts_menu.addAction(refreshPresets(sel))
    else:
        atts_menu.addAction(getAction(sel))
        atts_menu.addAction(refreshPresets(sel))



def getAction(sel, voice=None, label="Disabled"):
    a = QAction(mw)
    a.setText(label)
    a.setCheckable(True)
    a.setChecked(sel == voice)
    a.triggered.connect(lambda:updateVoice(voice))
    return a

def refreshPresets(sel):
    a = QAction(mw)
    a.setText("  (Refresh Preset List)")
    a.triggered.connect(refresh_menu)
    return a


def updateVoice(v):
    conf.set('speech',v)
    conf.save()
    refresh_menu()


def refresh_menu():
    js_menu.removeAction(atts_menu.menuAction())
    load_menu()


addHook("profileLoaded", load_menu)
