#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import pyqtgraph as pg
import random
import sys
import time
import Adafruit_DHT
from datetime import datetime
from time import strftime
import csv
import threading
import numpy as np

temp1 = []
    
def get_readings():    
    sensor = Adafruit_DHT.DHT11
    PIN = 4
        
    while True:     
        humidity, temperature = Adafruit_DHT.read_retry(sensor, PIN)
        if humidity is not None and temperature is not None:
            print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
            print strftime('%d-%b-%Y %H:%M:%S')
            data = temperature, humidity
            temp1.append(data[0])
            temp = str(data[0])
            hum = str(data[1])
            #print temp1
                
        else:
            print('Failed to get reading. Try again!')
            sys.exit(1)

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.central_widget = QtGui.QStackedWidget()
        self.setWindowTitle('Temperature Plot')
        self.setCentralWidget(self.central_widget)
        self.login_widget = LoginWidget(self)
        self.login_widget.button.clicked.connect(self.plotter)
        #self.login_widget.button.clicked.connect(self.get_readings)
        self.login_widget.button1.clicked.connect(self.stoplot)
        self.central_widget.addWidget(self.login_widget)
        
        

    def plotter(self):
        self.data =[]
        self.curve = self.login_widget.plot.getPlotItem().plot()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updater)
        self.timer.start(500)

    def stoplot(self):
        self.timer.stop()
    
    def updater(self):
        self.data.append(temp1) 
        self.curve.setData(temp1)

class LoginWidget(QtGui.QWidget):
    
    def __init__(self, parent=None):
        super(LoginWidget, self).__init__(parent)
        
        self.button1 = QtGui.QPushButton('Stop Plotting')
        self.button = QtGui.QPushButton('Start Plotting')
        
        layout1 = QtGui.QHBoxLayout()
        self.plot = pg.PlotWidget()
        layout1.addWidget(self.plot)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.button1)

        layout.addLayout(layout1)
        self.setLayout(layout)
        
        

if __name__ == '__main__':
    readings = threading.Thread(target=get_readings)
    readings.start()
    app = QtGui.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()


