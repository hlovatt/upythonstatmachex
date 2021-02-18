# boot.py -- run on boot-up
# can run arbitrary Python, but best to keep it minimal

__author__ = "Howard C Lovatt"
__copyright__ = "Howard C Lovatt, 2021 onwards."
__license__ = "MIT https://opensource.org/licenses/MIT."
__repository__ = "https://github.com/hlovatt/upythonstatmechex"
__description__ = "``statmach`` traffic light example for MicroPython."
__version__ = "1.0.2"  # Version set by https://github.com/hlovatt/tag2ver

import machine
import pyb
pyb.country('AU') # ISO 3166-1 Alpha-2 code, eg US, GB, DE, AU
#pyb.main('main.py') # main script to run after this one
#pyb.usb_mode('VCP+MSC') # act as a serial and a storage device
#pyb.usb_mode('VCP+HID') # act as a serial device and a mouse
