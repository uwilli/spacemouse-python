#!/usr/bin/python3
"""
Demo file for class spaceMouseProWireless. It displays the values in a pyQt window.
The escape key on the Spacemouse stops the Qt-Application.
"""

######################################################################################################
# Imports
######################################################################################################
from pyQtParamDisplay import *


######################################################################################################
# Main - Qt
######################################################################################################
if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show() # hidden by default

    app.exec()
