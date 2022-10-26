#!/usr/bin/python3

"""
This script lists all found USB devices with their Vendor ID and Product ID. This information identifies each device
uniquely. This is useful for example for access rights management on Linux.

from: https://www.orangecoat.com/how-to/use-pyusb-to-find-vendor-and-product-ids-for-usb-devices
"""
import sys
import usb.core

# find USB devices
dev = usb.core.find(find_all=True)

# loop through devices, printing vendor and product ids in decimal and hex
for cfg in dev:
    sys.stdout.write('Decimal VendorID=' + str(cfg.idVendor) + ' & ProductID=' + str(cfg.idProduct) + '\n')
    sys.stdout.write('Hexadecimal VendorID=' + hex(cfg.idVendor) + ' & ProductID=' + hex(cfg.idProduct) + '\n\n')
