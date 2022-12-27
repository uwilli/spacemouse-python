#!/usr/bin/python3
"""
This class reads the data from the 3d connexion Spacemouse Pro Wireless makes them available through member variables.
Currently only single button presses are considered. The information available would allow concurrent and nested pushes
to be recognized.
"""
import sys

from byteToIntConversion import *

import usb.core
import usb.util


######################################################################################################
# Class
######################################################################################################

class SpaceMouseProWireless:
    def __init__(self, usb_vendor_id=0x256f, usb_product_id=0xc652):
        """USB id -> change for your space mouse receiver in the default arguments
        or pass yours when initialising.
        use usbFindVendorProductID.py or $ lsusb to find yours.
        """
        # INTERFACE VARIABLES
        self.paramDict = dict(x=None,
                              y=None,
                              z=None,
                              roll=None,
                              pitch=None,
                              yaw=None,
                              b1=False,
                              b2=False,
                              b3=False,
                              b4=False,
                              escape=False,
                              shift=False,
                              control=False,
                              alt=False,
                              top=False,
                              front=False,
                              right=False,
                              rollView=False,
                              lockRotation=False,
                              menu=False,
                              fit=False)

        # DEVICE INFO
        # dict.keys is not accessible by index
        self.paramKeyList = ['x',
                             'y',
                             'z',
                             'roll',
                             'pitch',
                             'yaw',
                             'b1',
                             'b2',
                             'b3',
                             'b4',
                             'escape',
                             'shift',
                             'control',
                             'alt',
                             'top',
                             'front',
                             'right',
                             'rollView',
                             'lockRotation',
                             'menu',
                             'fit']


        self.idVendor = usb_vendor_id
        self.idProduct = usb_product_id

        # PRIVATE VARIABLES
        self._dev = None

        # CONNECT
        self._find_usb_device()


    def __del__(self):
        if self._dev is not None:
            usb.util.dispose_resources(self._dev)  # free usb device


    def get_interrupt_msg(self):
        """Spacemouse talks via receiver over Usb, using interrupt msgs.
           Timeout for waiting on interrupt, in s. (Milliseconds recommended).
        """
        usb_int = self._get_usb_msg_timeout_to_none()

        if usb_int is None:
            return 1 # No interrupt message received, stop function execution

        msg_type = usb_int[0]

        if msg_type == 1:  # Joystick
            if __class__._is_spacemouse_released(usb_int):  # joystick in 0-position
                self._write_joystick_released()
                return 0

            self._write_joystick(usb_int)

        elif msg_type == 3: # Button
            if __class__._is_spacemouse_released(usb_int):  # No button pressed
                self._write_buttons_released()
                return 0

            self._write_button(usb_int)

        elif msg_type == 22:
            # print('long press?')
            pass
        elif msg_type == 23:
            # print('inactivity?')
            pass
        else:
            raise ValueError('Unknown message type, number ' + str(msg_type) + '. Different Spacemouse?')
        return 0


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


    @staticmethod
    def _is_spacemouse_released(usb_msg):
        # if buttons released/Joystick not touched, msg is all zeros except msg type
        released = True

        for item in usb_msg[1:]:
            if item != 0:
                return False
        return True


    def _write_joystick_released(self):
        for key in self.paramKeyList[:6]:
            self.paramDict[key] = None


    def _write_buttons_released(self):
        for key in self.paramKeyList[6:]:
            self.paramDict[key] = False


    def _write_joystick(self, usb_msg):
        """Write 6 DoF of Joystick to parameter dictionary."""
        self.paramDict['x'] = to_int16(usb_msg[1], usb_msg[2])
        self.paramDict['y'] = -1 * to_int16(usb_msg[3], usb_msg[4])
        self.paramDict['z'] = -1 * to_int16(usb_msg[5], usb_msg[6])
        self.paramDict['pitch'] = -1 * to_int16(usb_msg[7], usb_msg[8])
        self.paramDict['roll'] = -1 * to_int16(usb_msg[9], usb_msg[10])
        self.paramDict['yaw'] = -1 * to_int16(usb_msg[11], usb_msg[12])


    def _write_button(self, usb_msg):
        """Button states are transmitted as a bit Register. Bytes at index 5 and 6 carry
           no information for this spacemouse.
           BitRegister Mapping (zero-indexed):
           [,, front, right,, top, fit, menu, b4, b3, b2, b1,,,, rollView, alt, escape,,,,,,,,,,,, lockRotation, control, shift]
           [,, 29,    28,   , 26,  25,  24,   23, 22, 21, 20,,,, 16,       15,  14,    ,,,,,,,,,,, 2,            1,       0    ]
        """
        bitReg = to_uint32(usb_msg[4], usb_msg[3], usb_msg[2], usb_msg[1])

        # Each individually set to false to avoid false reading of member variable with timing inbetween setting false and verifying bit register.
        if bitReg & 0x80000000 >> 2:
            self.paramDict['front'] = True
        else:
            self.paramDict['front'] = False
        if bitReg & 0x80000000 >> 3:
            self.paramDict['right'] = True
        else:
            self.paramDict['right'] = False
        if bitReg & 0x80000000 >> 5:
            self.paramDict['top'] = True
        else:
            self.paramDict['top'] = False
        if bitReg & 0x80000000 >> 6:
            self.paramDict['fit'] = True
        else:
            self.paramDict['fit'] = False
        if bitReg & 0x80000000 >> 7:
            self.paramDict['menu'] = True
        else:
            self.paramDict['menu'] = False
        if bitReg & 0x80000000 >> 8:
            self.paramDict['b4'] = True
        else:
            self.paramDict['b4'] = False
        if bitReg & 0x80000000 >> 9:
            self.paramDict['b3'] = True
        else:
            self.paramDict['b3'] = False
        if bitReg & 0x80000000 >> 10:
            self.paramDict['b2'] = True
        else:
            self.paramDict['b2'] = False
        if bitReg & 0x80000000 >> 11:
            self.paramDict['b1'] = True
        else:
            self.paramDict['b1'] = False
        if bitReg & 0x80000000 >> 15:
            self.paramDict['rollView'] = True
        else:
            self.paramDict['rollView'] = False
        if bitReg & 0x80000000 >> 16:
            self.paramDict['alt'] = True
        else:
            self.paramDict['alt'] = False
        if bitReg & 0x80000000 >> 17:
            self.paramDict['escape'] = True
        else:
            self.paramDict['escape'] = False
        if bitReg & 0x80000000 >> 29:
            self.paramDict['lockRotation'] = True
        else:
            self.paramDict['lockRotation'] = False
        if bitReg & 0x80000000 >> 30:
            self.paramDict['control'] = True
        else:
            self.paramDict['control'] = False
        if bitReg & 0x80000000 >> 31:
            self.paramDict['shift'] = True
        else:
            self.paramDict['shift'] = False


