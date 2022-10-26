#!/usr/bin/python3
"""
This class reads the data from the 3d connexion Spacemouse Pro Wireless makes them available through member variables.
Currently only single button presses are considered. The information available would allow concurrent and nested pushes
to be recognized.
"""

import usb.core
import usb.util


######################################################################################################
# Class
######################################################################################################

class SpaceMouseProWireless:
    def __init__(self):
        # INTERFACE VARIABLES
        self.x = None
        self.y = None
        self.z = None
        self.roll = None
        self.pitch = None
        self.yaw = None

        self.b1 = False
        self.b2 = False
        self.b3 = False
        self.b4 = False

        self.escape = False
        self.shift = False
        self.control = False
        self.alt = False

        self.top = False
        self.front = False
        self.right = False
        self.rollView = False
        self.lockRotation = False

        self.menu = False
        self.fit = False

        # DEVICE INFO
        # I consider changing the individual member variables to a list.
        # self.interfaceVars = [self.x, self.y, self.z, self.roll, self.pitch, self.yaw, self.lockRotation]

        # USB id -> change for your space mouse receiver
        self.idVendor = 0x256f  # use usbFindVendorProductID.py
        self.idProduct = 0xc652

        # PRIVATE VARIABLES
        self._dev = None

        # CONNECT
        self._find_usb_device()


    def __del__(self):
        usb.util.dispose_resources(self._dev)  # free usb device

    def _find_usb_device(self):
        """Look for Spacemouse and connect if found."""
        self._dev = usb.core.find(idVendor=self.idVendor, idProduct=self.idProduct)

        if self._dev is None:
            raise ValueError('Spacemouse not found')

        # dev.set_configuration() # Apparently automatically chosen config, as this throws an error.

        # Deal with Error resource-busy
        if self._dev.is_kernel_driver_active(0):
            try:
                self._dev.detach_kernel_driver(0)
            except usb.core.USBError:
                raise RuntimeError("Could not detach kernel driver from interface 0")

    def _get_usb_msg_timeout_to_none(self):
        try:
            # args: endpoint address, msg length (wMaxPacketSize), timeout (optional, device default if not set)
            usb_msg = self._dev.read(0x81, 0x20, 10)
        except usb.core.USBError as er:
            if er.errno == 110:  # Timeout
                return None
            raise
        return usb_msg

    def _is_spacemouse_released(self, usb_msg):
        # if buttons released/Joystick not touched, msg is all zeros except msg type
        released = True

        for item in usb_msg[1:]:
            if item != 0:
                return False
        return True

    def __buttons_to_false(self):
        self.b1 = False
        self.b2 = False
        self.b3 = False
        self.b4 = False

        self.escape = False
        self.shift = False
        self.control = False
        self.alt = False

        self.top = False
        self.front = False
        self.right = False
        self.rollView = False
        self.lockRotation = False

        self.menu = False
        self.fit = False

    def _write_released(self):
        self.x = None
        self.y = None
        self.z = None
        self.roll = None
        self.pitch = None
        self.yaw = None

        self.__buttons_to_false()

    def _write_joystick(self, usb_msg):
        """Write 6 DoF of Joystick to member variables."""
        self.x = self.__to_int16(usb_msg[1], usb_msg[2])
        self.y = -1 * self.__to_int16(usb_msg[3], usb_msg[4])
        self.z = -1 * self.__to_int16(usb_msg[5], usb_msg[6])
        self.pitch = -1 * self.__to_int16(usb_msg[7], usb_msg[8])
        self.roll = -1 * self.__to_int16(usb_msg[9], usb_msg[10])
        self.yaw = -1 * self.__to_int16(usb_msg[11], usb_msg[12])

    def _write_button(self, usb_msg):
        """Button states are transmitted as a bit Register. Bytes at index 5 and 6 carry
           no information for this spacemouse.
           BitRegister Mapping (zero-indexed):
           [,, front, right,, top, fit, menu, b4, b3, b2, b1,,,, rollView, alt, escape,,,,,,,,,,,, lockRotation, control, shift]
           [,, 2,     3,    , 5,   6,   7,    8,  9,  10, 11,,,, 15,       16,  17,    ,,,,,,,,,,, 29,           30,      31   ]
        """
        bitReg = self.__to_uint32(usb_msg[4], usb_msg[3], usb_msg[2], usb_msg[1])

        # Each individually set to false to avoid false reading of member variable with timing inbetween setting false and verifying bit register.
        if bitReg & 0x80000000 >> 2:
            self.front = True
        else:
            self.front = False
        if bitReg & 0x80000000 >> 3:
            self.right = True
        else:
            self.right = False
        if bitReg & 0x80000000 >> 5:
            self.top = True
        else:
            self.top = False
        if bitReg & 0x80000000 >> 6:
            self.fit = True
        else:
            self.fit = False
        if bitReg & 0x80000000 >> 7:
            self.menu = True
        else:
            self.menu = False
        if bitReg & 0x80000000 >> 8:
            self.b4 = True
        else:
            self.b4 = False
        if bitReg & 0x80000000 >> 9:
            self.b3 = True
        else:
            self.b3 = False
        if bitReg & 0x80000000 >> 10:
            self.b2 = True
        else:
            self.b2 = False
        if bitReg & 0x80000000 >> 11:
            self.b1 = True
        else:
            self.b1 = False
        if bitReg & 0x80000000 >> 15:
            self.rollView = True
        else:
            self.rollView = False
        if bitReg & 0x80000000 >> 16:
            self.alt = True
        else:
            self.alt = False
        if bitReg & 0x80000000 >> 17:
            self.escape = True
        else:
            self.escape = False
        if bitReg & 0x80000000 >> 29:
            self.lockRotation = True
        else:
            self.lockRotation = False
        if bitReg & 0x80000000 >> 30:
            self.control = True
        else:
            self.control = False
        if bitReg & 0x80000000 >> 31:
            self.shift = True
        else:
            self.shift = False


    def get_interrupt_msg(self):
        """Spacemouse talks via receiver over Usb, using interrupt msgs.
           Timeout for waiting on interrupt, in s. (Milliseconds recommended).
        """
        usb_int = self._get_usb_msg_timeout_to_none()

        if usb_int is None:
            return # No interrupt message received, stop function execution

        if self._is_spacemouse_released(usb_int): # No button pressed, joystick in 0-position
            self._write_released()
            return

        msg_type = usb_int[0]

        if msg_type == 1:  # Joystick
            self._write_joystick(usb_int)

        elif msg_type == 3: # Button
            self._write_button(usb_int)

        elif msg_type == 22:
            # print('long press?')
            pass
        elif msg_type == 23:
            # print('inactivity?')
            pass
        else:
            print(msg_type)
            raise ValueError('Unknown message type. Different Spacemouse?')


    def __to_int16(self, y1, y2):
        """y1 is LSB
           convert two 8 bit bytes to a signed 16-bit integer
        """
        x = y1 | (y2 << 8)
        if x >= 32768:
            x = -(65536 - x)
        return x

    def __to_uint32(self, y1, y2, y3, y4):
        """y1 is LSB"""
        x = y1 | (y2 << 8) | (y3 << 16) | (y4 << 24)
        return x