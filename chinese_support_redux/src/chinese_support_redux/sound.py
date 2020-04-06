# Copyright © 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright © 2017-2019 Joseph Lorimer <joseph@lorimer.me>
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


import time, re
from aqt import mw
from re import findall, sub
from anki.hooks import runFilter

from .consts import SOUND_TAG_REGEX
from .hanzi import has_hanzi
from .main import config


def sound(hanzi, source=None):
    """Returns sound tag for a given Hanzi string."""

    from .ruby import ruby_bottom, has_ruby

    if not has_hanzi(hanzi):
        return ''

    if not source:
        source = config['speech']

    if not source:
        return ''

    if has_ruby(hanzi):
        hanzi = ruby_bottom(hanzi)

    if not hanzi:
        return ''

    if source:
        path = runFilter("AwesomeTTS.speak", hanzi, "presets", source)
        if path:
            mw.progress.timer(5000,
                lambda:mw.col.media.addFile(path), False)
            fname = re.split(r"[\\/]", path)[-1]
            return '[sound:%s]' % fname

    return ''


def extract_tags(text):
    tags = findall(SOUND_TAG_REGEX, text)
    if not tags:
        return text, ''
    return no_sound(text), ''.join(tags)


def no_sound(text):
    return sub(SOUND_TAG_REGEX, '', text)
