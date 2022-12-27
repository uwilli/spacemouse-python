#!/usr/bin/python3
"""
Collection of pyQt classes for demo.py. Displays the parameters of the spacemouse in
a window.
"""

######################################################################################################
# Imports
######################################################################################################
import spaceMouseProWireless as sm
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import sys


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
        self.table1 = QTableWidget()
        self.table2 = QTableWidget()

        self.thread = QThread()
        self.worker = SpaceMouseLoop()

        # SETUP
        self.windowSetup()
        self.runSpaceMouse()


    def windowSetup(self):
        self.setWindowTitle('Spacemouse Pro Wireless')

        self.table1.setRowCount(10)
        self.table1.setColumnCount(2)
        self.table1.horizontalHeader().hide()
        self.table1.verticalHeader().hide()

        self.table2.setRowCount(11)
        self.table2.setColumnCount(2)
        self.table2.horizontalHeader().hide()
        self.table2.verticalHeader().hide()

        for row, entry in enumerate(self.worker.ct.paramKeyList[:10]):
            newItem = QTableWidgetItem(entry)
            self.table1.setItem(row, 0, newItem)
            row += 1

        for row, entry in enumerate(self.worker.ct.paramKeyList[10:]):
            newItem = QTableWidgetItem(entry)
            self.table2.setItem(row, 0, newItem)
            row += 1

        columns = QHBoxLayout()
        columns.addWidget(self.table1)
        columns.addWidget(self.table2)

        container = QWidget()
        container.setLayout(columns)

        self.setMinimumSize(430, 350)
        self.setCentralWidget(container)


    def runSpaceMouse(self):
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(QApplication.quit)
        self.worker.progress.connect(self.displayParams)
        self.thread.start()


    def displayParams(self):
        for row, entry in enumerate(self.worker.ct.paramKeyList[:10]):
            newItem = QTableWidgetItem(str(self.worker.ct.paramDict[entry]))
            self.table1.setItem(row, 1, newItem)
            row += 1

        for row, entry in enumerate(self.worker.ct.paramKeyList[10:]):
            newItem = QTableWidgetItem(str(self.worker.ct.paramDict[entry]))
            self.table2.setItem(row, 1, newItem)
            row += 1
