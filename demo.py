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

    ct = sm.SpaceMouseProWireless() # controller

    # Loop, this usb device works with interrupt communication
    run = True
    sleepPeriod = 0.5

    while run:
        ct.get_interrupt_msg()
        if ct.paramDict['escape']:
            run = False

        for key in ct.paramKeyList:
            print(key, ' : ', ct.paramDict[key])

        time.sleep(sleepPeriod)
    # end while
