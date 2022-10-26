#!/usr/bin/python3
"""
Demo file for class spaceMouseProWireless.
"""
######################################################################################################
# Imports
######################################################################################################
import spaceMouseProWireless as sm
import time

######################################################################################################
# Main
######################################################################################################

if __name__ == "__main__":

    controller = sm.SpaceMouseProWireless()

    # FOR LATER, in the moment only single button presses reliable
    # Remember if button pressed or released, starting with all released.
    # Order: Menu, Fit, Top, Right, Front, Roll View, B1, B2, B3, B4,  Escape, Alt, Shift, Ctrl, Lock Rotation
    # ButtonStates = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]


    # Loop, this usb device works with interrupt communication
    run = True
    sleepPeriod = 0.5

    while run:
        controller.get_interrupt_msg()
        if controller.escape:
            run = False

        for var in controller.interfaceVars:
            print(var)

        print('B1     : ', controller.b1)
        print('B2     : ', controller.b2)
        print('B3     : ', controller.b3)
        print('B4     : ', controller.b4)
        print('LockRot: ', controller.lockRotation)

        time.sleep(sleepPeriod)
    # end while
