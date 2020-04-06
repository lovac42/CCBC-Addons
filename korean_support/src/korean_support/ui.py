# -*- coding: utf-8 -*-
# Copyright 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright 2017 Luo Li-Yan <joseph.lorimer13@gmail.com>
# Copyright © 2018 Scott Gigante <scottgigante@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html




#
# The files in this addon may have been modified for CCBC, and may not be the same as the original.
# The files in this addon may have been modified for CCBC, and may not be the same as the original.
# The files in this addon may have been modified for CCBC, and may not be the same as the original.
#



from aqt import mw
from aqt.qt import QAction
from aqt.utils import showInfo, openLink, askUser

from PyQt4.QtGui import QKeySequence, QAction, QActionGroup, QMenu
from anki.lang import _
from anki.hooks import runHook
from functools import partial

from .about import CSR_GITHUB_URL, showAbout
from .config import korean_support_config as config
from .fill_missing import fill_silhouette, fill_sounds, fill_translation


dictionaries = [
    ("None", _("None")),
    ("local_en", _("English")),
]


awesome_config = None
def getAwesomeConfig(c):
    global awesome_config
    awesome_config = c


def loadMenu():

    add_menu('Korean Support (CCBC)::Use local dictionary')
    for d, d_names in dictionaries:
        add_menu_item(
            'Korean Support (CCBC)::Use local dictionary',
            d_names,
            partial(config.update, {'dictionary': d_names}),
            checkable=True,
            checked=bool(config['dictionary'] == d_names),
        )

    runHook('AwesomeTTS.config', getAwesomeConfig)
    if awesome_config:
        for k,v in awesome_config["presets"].items():
            add_menu_item(
                'Korean Support (CCBC)::AwesomeTTS Presets',
                k,
                partial(config.update, {'speech': k}),
                checkable=True,
                checked=bool(config['speech'] == k),
            )

        add_menu_item(
            "Korean Support (CCBC)::AwesomeTTS Presets",
            "Disabled",
            partial(config.update, {'speech': None}),
            checkable=True,
            checked=bool(config['speech'] == None),
        )
        add_menu_item(
            "Korean Support (CCBC)::AwesomeTTS Presets",
            _('  (Refresh Preset List)'), refresh_menu)
    else:
        add_menu_item(
            "Korean Support (CCBC)::AwesomeTTS Presets",
            "Disabled",
            partial(config.update, {'speech': None}),
            checkable=True,
            checked=True,
        )
        add_menu_item(
            "Korean Support (CCBC)::AwesomeTTS Presets",
            _('  (Refresh Preset List)'), refresh_menu)


    add_menu('Korean Support (CCBC)::Bulk Fill')
    add_menu_item('Korean Support (CCBC)::Bulk Fill', _('Fill missing sounds'), fill_sounds)
    add_menu_item('Korean Support (CCBC)::Bulk Fill', _('Fill translation'), fill_translation)
    add_menu_item('Korean Support (CCBC)::Bulk Fill', _('Fill silhouette'), fill_silhouette)

    add_menu_item('Korean Support (CCBC)', _('About...'), showAbout)



def unload_menu():
    for menu in mw.custom_menus.values():
        mw.form.menuAddon.removeAction(menu.menuAction())
    mw.custom_menus.clear()


def refresh_menu():
    unload_menu()
    loadMenu()


def add_menu(path):
    if not hasattr(mw, 'custom_menus'):
        mw.custom_menus = {}

    if len(path.split('::')) == 2:
        parent_path, child_path = path.split('::')
        has_child = True
    else:
        parent_path = path
        has_child = False

    if parent_path not in mw.custom_menus:
        parent = QMenu('&' + parent_path, mw)
        mw.custom_menus[parent_path] = parent
        mw.form.menuAddon.insertMenu(mw.form.menuTools.menuAction(), parent)

    if has_child and (path not in mw.custom_menus):
        child = QMenu('&' + child_path, mw)
        mw.custom_menus[path] = child
        mw.custom_menus[parent_path].addMenu(child)



def add_menu_item(path, text, func, keys=None, checkable=False, checked=False):
    action = QAction(text, mw)

    if keys:
        action.setShortcut(QKeySequence(keys))

    if checkable:
        action.setCheckable(checkable)
        action.toggled.connect(func)
        if not hasattr(mw, 'action_groups'):
            mw.action_groups = {}
        if path not in mw.action_groups:
            mw.action_groups[path] = QActionGroup(None)
        mw.action_groups[path].addAction(action)
        action.setChecked(checked)
    else:
        action.triggered.connect(func)

    add_menu(path)
    mw.custom_menus[path].addAction(action)


