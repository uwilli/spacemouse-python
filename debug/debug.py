#!/usr/bin/python3
"""
Debug file for class spaceMouseProWireless.
"""
######################################################################################################
# Imports
######################################################################################################
import debugSpaceMouseProWireless as dsm

######################################################################################################
# Main
######################################################################################################

if __name__ == "__main__":
    ct = dsm.DebugSpaceMouseProWireless()

    #ct.print_device_connected()
    #ct.print_raw_usb_msg()
    #ct.print_button_msg()
    #ct.get_interrupt_msg()
    #ct.print_button_press()
    ct.print_joystick_active()
