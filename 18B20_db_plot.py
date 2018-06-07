#!/usr/bin/python
# -*- coding: utf-8 -*-


from PyQt4 import QtCore, QtGui
import pyqtgraph as pg
import random
import sys
import time
from datetime import datetime
from time import strftime
import csv
import threading
import MySQLdb
from w1thermsensor import W1ThermSensor


filename = strftime('%d-%b-%Y %H-%M')
temp1 = []


    
def get_readings():
    sensor = W1ThermSensor()

    with open('./data/'+filename+'.csv', 'a') as data_log:
        header = csv.writer(data_log)
        header.writerow(['Date', 'Time', 'Temperature'])
    
    while True:
        temp = sensor.get_temperature()
        print('Temperature={0}{1}'.format(round(temp, 1), '°C'))
        temp1.append(temp)

        with open('./data/'+filename+'.csv', 'a') as data_log:
            data_log.write(strftime('%d/%m/%y,%H:%M:%S'))
            data_log.write(','+str(round(temp, 1)))
            data_log.write(strftime('\n'))

        time.sleep(3)
        return str(round(temp, 1))
        
def db_insert():
    db = MySQLdb.connect(host="vixman", user="insert_db",passwd="up", db="meteo")
    cur = db.cursor()
    
    while True:
        temp = get_readings()
        
        try:
            sql = ("""INSERT INTO temperature (temp) VALUES (%s)""",(temp))
            print "Writing to database..."
            cur.execute(*sql)
            db.commit()
            print "Write Complete"
        except:
            db.rollback()
            print 'Failed writing to database'
     
    cur.close()
    db.close()
                


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
    db = threading.Thread(target=db_insert)
    db.start()
    app = QtGui.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()


