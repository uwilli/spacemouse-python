#!/usr/bin/python3
"""
Mock_Usb

This Python module is a mock module for testing purposes only, it provides a mock usb-device object
and simulates parts of the functionality of Pyusb.
It replaces the PyUsb modules util and core for testing the SpaceMouseProWireless
class without the usb device.

The classes diverge from the CamelCase naming convention to allow
for importing with the same syntax as the real PyUsb module.
"""

import array


class core:
    @staticmethod
    def find(idVendor, idProduct):
        if idVendor == idProduct == 0:
            return None # No device found, timeout

        mock_device = Device
        return mock_device


class util:
    @staticmethod
    def dispose_resources(device):
        pass


class Device:
    def __init__(self):
        self.msg = "This is a mock object for testing."

    @staticmethod
    def is_kernel_driver_active(var):
        return False # kernel detachment is Pyusb-business, no testing here

    @staticmethod
    def read(address, length, timeout):
        """ Timeout is not tested, always returns usb_msg.
            Msg: Joystick all axes -90 deg.
        """
        return array.array('i', [0, 0xA6, 0xFF, 0x5A, 0x00, 0x5A, 0x00, 0x5A, 0x00, 0x5A, 0x00, 0x5A, 0x00])

