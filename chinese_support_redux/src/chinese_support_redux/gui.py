# Copyright © 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright © 2017-2020 Joseph Lorimer <joseph@lorimer.me>
#
# This file is part of Chinese Support Redux.
#
# Chinese Support Redux is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# Chinese Support Redux is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# Chinese Support Redux.  If not, see <https://www.gnu.org/licenses/>.




#
# The files in this addon may have been modified for CCBC, and may not be the same as the original.
# The files in this addon may have been modified for CCBC, and may not be the same as the original.
# The files in this addon may have been modified for CCBC, and may not be the same as the original.
#


from functools import partial

from PyQt4.QtGui import QKeySequence, QAction, QActionGroup, QMenu
from anki.lang import _
from aqt import mw
from aqt.utils import openLink

from .about import CSR_GITHUB_URL, showAbout
from .fill import (
    bulk_fill_all,
    bulk_fill_classifiers,
    bulk_fill_defs,
    bulk_fill_hanzi,
    bulk_fill_silhouette,
    bulk_fill_sound,
    bulk_fill_transcript,
)
from .main import config


SPEECH_ENGINES = {
    'Baidu Translate': 'baidu|zh',
    'Google Mandarin (PRC)': 'google|zh-cn',
    'Google Mandarin (Taiwan)': 'google|zh-tw',
    'Amazon Polly' : 'aws|Zhiyu',
    'Disabled': None,
}

PHONETIC_TARGETS = {
    'Pinyin': 'pinyin',
    'Pinyin (Taiwan)': 'pinyin_tw',
    'Bopomofo': 'bopomofo',
    'Jyutping': 'jyutping',
}


def load_menu():
    for k, v in PHONETIC_TARGETS.items():
        add_menu_item(
            'Chinese Support Redux (CCBC)::Phonetics',
            k,
            partial(config.update, {'target': v}),
            checkable=True,
            checked=bool(config['target'] == v),
        )

    for k, v in SPEECH_ENGINES.items():
        add_menu_item(
            'Chinese Support Redux (CCBC)::Speech Engine',
            k,
            partial(config.update, {'speech': v}),
            checkable=True,
            checked=bool(config['speech'] == v),
        )

    add_menu('Chinese Support Redux (CCBC)::Bulk Fill')
    add_menu_item('Chinese Support Redux (CCBC)::Bulk Fill', _('Hanzi'), bulk_fill_hanzi)
    add_menu_item(
        'Chinese Support Redux (CCBC)::Bulk Fill', _('Transcription'), bulk_fill_transcript
    )
    add_menu_item('Chinese Support Redux (CCBC)::Bulk Fill', _('Definitions'), bulk_fill_defs)
    add_menu_item('Chinese Support Redux (CCBC)::Bulk Fill', _('Classifiers'), bulk_fill_classifiers)
    add_menu_item('Chinese Support Redux (CCBC)::Bulk Fill', _('Sound'), bulk_fill_sound)
    add_menu_item('Chinese Support Redux (CCBC)::Bulk Fill', _('Silhouette'), bulk_fill_silhouette)
    add_menu_item('Chinese Support Redux (CCBC)::Bulk Fill', _('All'), bulk_fill_all)

    # add_menu('Chinese Support Redux (CCBC)::Help')
    # add_menu_item(
        # 'Chinese Support Redux (CCBC)::Help',
        # _('Report a bug or make a feature request'),
        # lambda: openLink(CSR_GITHUB_URL + '/issues'),
    # )
    add_menu_item('Chinese Support Redux (CCBC)', _('About...'), showAbout)


def unload_menu():
    for menu in mw.custom_menus.values():
        mw.form.menuAddon.removeAction(menu.menuAction())

    mw.custom_menus.clear()


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
