#!/usr/bin/python3
""" stub_usb.core

    Stub for usb package. Core: Core usb functions.

"""

__all__ = ['find', 'Device', 'USBError']


import array


def find(idVendor, idProduct):
    print('Mockfind')
    if idVendor == idProduct == 0:
        return None  # No device found, timeout

    stub_device = Device()
    return stub_device


class Device:
    def __init__(self):
        self.msg = "This is a mock object for testing."

    @staticmethod
    def is_kernel_driver_active(var):
        return False # kernel detachment is Pyusb-business, no testing here

    @staticmethod
    def detach_kernel_driver(var):
        pass  # kernel detachment is Pyusb-business, no testing here

    @staticmethod
    def read(address, length, timeout):
        """ Timeout is not tested, always returns usb_msg.
            Msg: Joystick all axes -90 deg.
        """
        return array.array('i', [0, 0xA6, 0xFF, 0x5A, 0x00, 0x5A, 0x00, 0x5A, 0x00, 0x5A, 0x00, 0x5A, 0x00])


class USBError(IOError):
    def __init__(self, strerror, error_code=None, errno=None):
        r"""Initialize the object.

        This initializes the USBError object. The strerror and errno are passed
        to the parent object. The error_code parameter is attributed to the
        backend_error_code member variable.
        """

        IOError.__init__(self, errno, strerror)
        self.backend_error_code = error_code