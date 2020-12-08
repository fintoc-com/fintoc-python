"""
__init__.py
===========

Let's initialize this machine.
"""

__version__ = "0.3.0"

import locale

from fintoc.client import Client

try:
    locale.setlocale(locale.LC_ALL, "")
except locale.Error:
    pass
