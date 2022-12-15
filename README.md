# Spacemouse-python

Python interface for 3D Connexion SpaceMouse Pro Wireless based on pyUsb.  
Other 3D-Connexion devices have not been tested.

Buttons 1-4 are single press, continuously pressing these does not generate a signal.
Slow or long presses of buttons 1-4 do not register as presses.
The rest of the buttons can be pressed continuously.

## Work in progress

Implementing tests with pytest and mock objects.
Pressing more than 2 Buttons simultaneously in some combinations causes false positives on other buttons.
I'm not sure if this is my code or the device.

## Getting started

1. Install dependencies (see Dependencies)
2. Configure access rights to USB device (see Ubuntu USB devices access rights)
3. Change product and vendor id standard arguments in spaceMouseProWireless class init function. Or pass your id's when creating the spacemouse object.
4. Run the demo.py script
   - Note : The escape key of the mouse terminates the demo program.

## Ubuntu USB devices access rights

Allowing access to specific usb device without root privileges.
1. Find vendor and product id  
   `$ lsusb`  
   Or run script "usbFindVendorProductID.py"

2. Create udev rules file for targeted device  
   `$ touch /lib/udev/rules.d/50-YourSoftwareName.rules`  
      with content:  
   `ACTION=="add", SUBSYSTEMS=="usb", ATTRS{idVendor}=="171b", ATTRS{idProduct}=="2001", MODE="660", GROUP="plugdev"`  
   Replace 171b and 2001 with your vendor and product ID.

3. Add username to plugdev group  
    `sudo adduser username plugdev`

4. Force changes  
`sudo udevadm control --reload`  
`sudo udevadm trigger`

5. Unplug and replug device

Done!

## Dependencies

### Primary dependencies (SpaceMouseProWireless class)

- Pyusb

### Secondary dependencies (demo.py)
- PyQt5
- Sys

### Development dependencies (debug, test)
- Time
- Pytest
- Sys

## Platforms

### Tested and running

- Ubuntu 22.04

### Known issues

- MacOS 12.6 (PyUSB access to device)

## Sources
I have used code and contributions from different people I'd like to thank and reference here :

- jwick1234, github.  
https://github.com/jwick1234/3d-mouse-rpi-python
- johnhw, github.
https://github.com/johnhw/pyspacenavigator/blob/master/spacenavigator.py
- Rolf of Saxony, stackoverflow.
https://stackoverflow.com/questions/3738173/why-does-pyusb-libusb-require-root-sudo-permissions-on-linux
- Martin Fitzpatrick, pythonguis.com.  
https://www.pythonguis.com/tutorials/pyqt-signals-slots-events/
