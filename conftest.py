""" conftest.py

Configuration file for pytest. Replace module imports with stub_usb
without explicitly changing imports in class definition of spaceMouseProWireless.
When imported in class definition, they are regarded as already loaded.
"""

import sys

sys.modules['usb.core'] = __import__('stub_usb.core')
sys.modules['usb.util'] = __import__('stub_usb.util')
sys.modules['usb'] = __import__('stub_usb') # Needed because usb.py imports backend, legacy, etc (which are not part of the stub).

