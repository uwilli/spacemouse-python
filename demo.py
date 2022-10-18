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

    controller = sm.Spacemouse()

    # FOR LATER, in the moment only single button presses reliable
    # Remember if button pressed or released, starting with all released.
    # Order: Menu, Fit, Top, Right, Front, Roll View, B1, B2, B3, B4,  Escape, Alt, Shift, Ctrl, Lock Rotation
    # ButtonStates = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]


    # Loop, this usb device works with interrupt communication
    run = True
    sleepPeriod = 0.01

    while run:
        controller.get_interrupt_msg()
        if controller.escape:
            run = False

        # Should print none with no movement
        print('x     : ', controller.x)
        print('y     : ', controller.y)
        print('z     : ', controller.z)
        print('roll  : ', controller.roll)
        print('pitch : ', controller.pitch)
        print('yaw   : ', controller.yaw)

        print('B1     : ', controller.b1)
        print('B2     : ', controller.b2)
        print('B3     : ', controller.b3)
        print('B4     : ', controller.b4)
        print('LockRot: ', controller.lockRotation)

        time.sleep(sleepPeriod)
    # end while
