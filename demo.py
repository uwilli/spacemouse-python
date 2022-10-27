#!/usr/bin/python3
"""
Demo file for class spaceMouseProWireless. It displays the values in a pyQt window.
"""
import sys

######################################################################################################
# Imports
######################################################################################################
import spaceMouseProWireless as sm
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QObject, QThread, pyqtSignal


######################################################################################################
# Window and worker class - Qt
######################################################################################################
class SpaceMouseLoop(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ct = sm.SpaceMouseProWireless()  # controller


    def run(self):
        while not self.ct.paramDict['escape']:
            ret = self.ct.get_interrupt_msg()
            if ret == 0:
                self.progress.emit()
        self.finished.emit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # MEMBER VARIABLES
        self.x = QLabel()
        self.y = QLabel()
        self.z = QLabel()
        self.roll = QLabel()
        self.pitch = QLabel()
        self.yaw = QLabel()
        self.b1 = QLabel()
        self.b2 = QLabel()
        self.b3 = QLabel()
        self.b4 = QLabel()
        self.escape = QLabel()
        self.shift = QLabel()
        self.control = QLabel()
        self.alt = QLabel()
        self.top = QLabel()
        self.front = QLabel()
        self.right = QLabel()
        self.rollView = QLabel()
        self.lockRotation = QLabel()
        self.menu = QLabel()
        self.fit = QLabel()

        self.thread = QThread()
        self.worker = SpaceMouseLoop()

        # SETUP
        self.windowSetup()
        self.runSpaceMouse()


    def windowSetup(self):
        self.setWindowTitle('Spacemouse Pro Wireless')

        col1 = QVBoxLayout()
        col1Name = QVBoxLayout()
        col2 = QVBoxLayout()
        row = QHBoxLayout()

        divider = QLabel()
        divider.setText(':')

        col1.addWidget(self.x)
        col1.addWidget(self.y)
        col1.addWidget(self.z)
        col1.addWidget(self.roll)
        col1.addWidget(self.pitch)
        col1.addWidget(self.yaw)
        col1.addWidget(self.b1)
        col1.addWidget(self.b2)
        col1.addWidget(self.b3)
        col1.addWidget(self.b4)
        col2.addWidget(self.shift)
        col2.addWidget(self.control)
        col2.addWidget(self.alt)
        col2.addWidget(self.top)
        col2.addWidget(self.front)
        col2.addWidget(self.right)
        col2.addWidget(self.rollView)
        col2.addWidget(self.lockRotation)
        col2.addWidget(self.menu)
        col2.addWidget(self.fit)

        row.addLayout(col1)
        row.addLayout(col2)


        container = QWidget()
        container.setLayout(row)

        self.setCentralWidget(container)


    def runSpaceMouse(self):
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(sys.exit)
        self.worker.progress.connect(self.displayParams)
        self.thread.start()


    def displayParams(self):
        self.x.setText('x                :    ' + str(self.worker.ct.paramDict['x']))
        self.y.setText('y                :    ' + str(self.worker.ct.paramDict['y']))
        self.z.setText('z                :    ' + str(self.worker.ct.paramDict['z']))
        self.roll.setText('roll           :    ' + str(self.worker.ct.paramDict['roll']))
        self.pitch.setText('pitch        :    ' + str(self.worker.ct.paramDict['pitch']))
        self.yaw.setText('yaw          :    ' + str(self.worker.ct.paramDict['yaw']))
        self.b1.setText('Button 1 :    ' + str(self.worker.ct.paramDict['b1']))
        self.b2.setText('Button 2 :    ' + str(self.worker.ct.paramDict['b2']))
        self.b3.setText('Button 3 :    ' + str(self.worker.ct.paramDict['b3']))
        self.b4.setText('Button 4 :    ' + str(self.worker.ct.paramDict['b4']))



######################################################################################################
# Main - Qt
######################################################################################################
if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show() # hidden by default

    app.exec()
