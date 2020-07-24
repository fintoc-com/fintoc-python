"""
__init__.py
===========

Let's initialize this machine.
"""

__version__ = "0.2.0"

import locale
from fintoc.client import Client

locale.setlocale(locale.LC_ALL, "")
