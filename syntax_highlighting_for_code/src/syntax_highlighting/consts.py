# -*- coding: utf-8 -*-
# This file has been modified by lovac42 for CCBC, and is not the same as the original.

"""
This file is part of the Syntax Highlighting add-on for Anki.

Global variables

Copyright: (c) 2018 Glutanimate <https://glutanimate.com/>
License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>
"""

import sys
import os
from anki import version

anki21 = version.startswith("2.1.")
addon_path = os.path.dirname(__file__)
