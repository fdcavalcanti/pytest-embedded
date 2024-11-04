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
        'NuttxSerial': '.serial',  # requires 'esp'
        'NuttxDut': '.dut',  # requires 'esp'
    },
)

__all__ = ['NuttxApp', 'NuttxSerial', 'NuttxDut']

__version__ = '1.11.8'
