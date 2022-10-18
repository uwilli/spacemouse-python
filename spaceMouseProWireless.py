#!/usr/bin/python3
"""
This class reads the data from the 3d connexion Spacemouse Pro Wireless makes them available through member variables.
Currently only single button presses are considered. The information available would allow concurrent and nested pushes
to be recognized.

Sources used:
From jwick1234, github.
Link: https://github.com/uwilli/3d-mouse-rpi-python/blob/develop/HelloSpaceNavigator.py
From johnhw, github.
Space Mouse Wireless Windows: https://github.com/johnhw/pyspacenavigator/blob/master/spacenavigator.py

Changed and blended and marinated by Urban Willi
"""

import usb.core
import usb.util


######################################################################################################
# Class
######################################################################################################

class Spacemouse:
    def __init__(self):
        # Interface variables
        self.x = None
        self.y = None
        self.z = None
        self.roll = None
        self.pitch = None
        self.yaw = None

        self.escape = None
        self.b1 = None
        self.b2 = None
        self.b3 = None
        self.b4 = None
        self.lockRotation = None

        # USB id -> change for your space mouse receiver
        self.idVendor = 0x256f  # use usbFindVendorProductID.py
        self.idProduct = 0xc652

        # Private variables
        self._dev = None

        ## Init
        # Look for Space Mouse
        self._dev = usb.core.find(idVendor=self.idVendor, idProduct=self.idProduct)
        if self._dev is None:
            raise ValueError('Spacemouse not found')
        else:
            print('Spacemouse Pro Wireless found')

        # dev.set_configuration() # Apparently automatically chosen config, as this throws an error.

        # Deal with Error resource-busy
        if self._dev.is_kernel_driver_active(0):
            try:
                self._dev.detach_kernel_driver(0)
            except usb.core.USBError:
                raise RuntimeError("Could not detach kernel driver from interface 0")


    def __del__(self):
        usb.util.dispose_resources(self._dev)  # free usb device


    # Spacemouse talks via receiver over Usb, using interrupt msgs.
    # Timeout for waiting on interrupt, in s. (Milliseconds recommended).
    # Single button presses and following release recognized. Simultaneous several buttons not yet supported.
    def get_interrupt_msg(self):
        try:
            # args: endpoint address, msg length (wMaxPacketSize), timeout (optional, device default if not set)
            usb_int = self._dev.read(0x81, 0x20, 10)
        except usb.core.USBError as er:
            if er.errno == 110:  # Timeout
                return
            raise

        msg_type = usb_int[0]

        released = True  # if buttons released/Joystick not touched, msg is all zeros except msg type
        for item in usb_int[1:]:
            if item != 0:
                released = False
                break

        if msg_type == 1:  # Joystick
            if released:
                self.x = None
                self.y = None
                self.z = None
                self.roll = None
                self.pitch = None
                self.yaw = None
                print('Joystick released')
                return

            print('Joystick')

            self.x = self.__to_int16(self.__try_index_abs_val(usb_int, 1), self.__try_index_abs_val(usb_int, 2))
            self.y = -1 * self.__to_int16(self.__try_index_abs_val(usb_int, 3), self.__try_index_abs_val(usb_int, 4))
            self.z = -1 * self.__to_int16(self.__try_index_abs_val(usb_int, 5), self.__try_index_abs_val(usb_int, 6))
            self.pitch = -1 * self.__to_int16(self.__try_index_abs_val(usb_int, 7), self.__try_index_abs_val(usb_int, 8))
            self.roll = -1 * self.__to_int16(self.__try_index_abs_val(usb_int, 9), self.__try_index_abs_val(usb_int, 10))
            self.yaw = -1 * self.__to_int16(self.__try_index_abs_val(usb_int, 11), self.__try_index_abs_val(usb_int, 12))

            # print('x     : ', self.x)
            # print('y     : ', self.y)
            # print('z     : ', self.z)
            # print('pitch  : ', self.pitch)
            # print('roll : ', self.roll)
            # print('yaw   : ', self.yaw)

        elif msg_type == 3:
            if released:
                self.escape = None
                self.b1 = None
                self.b2 = None
                self.b3 = None
                self.b4 = None
                self.lockRotation = None
                print('Button released')
                return
            # print('Button')

            # Position 1
            val = self.__try_index_abs_val(usb_int, 1)
            if val == 1:
                print('Menu')
            elif val == 2:
                print('Fit')
            elif val == 4:
                print('Top')
            elif val == 16:
                print('Right')
            elif val == 32:
                print('Front')

            # Position 2
            val = self.__try_index_abs_val(usb_int, 2)
            if val == 1:
                print('Roll View')
            elif val == 16:
                self.b1 = True
                # print('B1')
            elif val == 32:
                self.b2 = True
                # print('B2')
            elif val == 64:
                self.b3 = True
                # print('B3')
            elif val == 128:
                self.b4 = True
                # print('B4')

            # Position 3
            val = self.__try_index_abs_val(usb_int, 3)
            if val == -1:  # out of range
                return

            if val == 64:
                # print('Escape')
                self.escape = True
            elif val == 128:
                print('Alt')

            # Position 4
            val = self.__try_index_abs_val(usb_int, 4)
            if val == -1:  # out of range
                return

            if val == 1:
                print('Shift')
            elif val == 2:
                print('Ctrl')
            elif val == 4:
                self.lockRotation = True
                # print('Lock Rotation')

        elif msg_type == 23:
            # print('inactivity?')
            pass
        else:
            print('unknown')

        # enumerate
        # for i, item in enumerate(usb_int):
        #     print(item)

    # returns -1 if index out of range
    def __try_index_abs_val(self, list, index):
        try:
            ret = list[index]
        except ValueError:
            return -1
        return ret

    # convert two 8 bit bytes to a signed 16 bit integer
    # from johnhw
    def __to_int16(self, y1, y2):
        x = y1 | (y2 << 8)
        if x >= 32768:
            x = -(65536 - x)
        return x
