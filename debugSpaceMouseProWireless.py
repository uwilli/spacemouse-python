#!/usr/bin/python3
"""
This support class contains debug functions for development of the parent class.
"""

from spaceMouseProWireless import SpaceMouseProWireless

import time


######################################################################################################
# Class
######################################################################################################

class DebugSpaceMouseProWireless(SpaceMouseProWireless):
    def __init__(self):
        super().__init__()

    def print_raw_usb_msg(self, timeout=10):
        """Blocking until interrupt message received or timeout (in seconds)"""
        int_msg = None
        timeoutAfter = time.time() + timeout

        print('Waiting on interrupt message...')

        # Loop until timeout or interrupt message received.
        while int_msg is None:
            if timeoutAfter < time.time():
                print('Timeout without interrupt message arriving.')
                return

            int_msg = super()._get_usb_msg_timeout_to_none()

        print('Message : ')
        print(int_msg)

    def print_button_msg(self, timeout=10, binary=True):
        """Blocking until interrupt message of type Button received or timeout (in seconds)"""
        int_msg = None
        timeoutAfter = time.time() + timeout

        print('Waiting on Button message...')

        # Loop until timeout or interrupt message received.
        while timeoutAfter > time.time():
            int_msg = super()._get_usb_msg_timeout_to_none()

            if int_msg is None:
                continue
            if int_msg[0] == 3:
                break

        if int_msg is None:
            print('Timeout without button message arriving.')

        print('Button message : ')
        if binary:
            print('Index    | Value binary')
            print('1         ', format(int_msg[1], '08b'))
            print('2         ', format(int_msg[2], '08b'))
            print('3         ', format(int_msg[3], '08b'))
            print('4         ', format(int_msg[4], '08b'))
            print('5         ', format(int_msg[5], '08b'))
            print('6         ', format(int_msg[6], '08b'))
        else:
            print(int_msg)


    def print_device_connected(self):
        if self._dev is None:
            print('No Usb device is connected.')
        else:
            print(self._dev)

    def print_button_press(self):
        """Not a very efficient method, but works for debugging"""
        sleepPeriod = 0.1

        while not self.paramDict['escape']:
            super().get_interrupt_msg()

            for key in self.paramKeyList[6:]:
                if self.paramDict[key]:
                    print(key + ' is pressed.')
            time.sleep(sleepPeriod)