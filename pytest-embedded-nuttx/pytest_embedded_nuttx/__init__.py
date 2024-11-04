"""Make pytest-embedded plugin work with Arduino."""

import importlib

from pytest_embedded.utils import lazy_load

from .app import NuttxApp

__getattr__ = lazy_load(
    importlib.import_module(__name__),
    {
        'NuttxApp': NuttxApp,
    },
    {
        'NuttxSerial': '.serial',
    },
)

__all__ = ['NuttxApp', 'NuttxSerial']

__version__ = '1.11.8'
