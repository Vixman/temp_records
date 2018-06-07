#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time
import Adafruit_DHT
from datetime import datetime
from time import strftime
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.animation as animation
import threading


filename = strftime('%d-%b-%Y %H-%M')
temp1 = []
    

def get_readings():
    
    sensor = Adafruit_DHT.DHT11
    PIN = 4
    #temp1 = []
    
    while True:
 
        humidity, temperature = Adafruit_DHT.read_retry(sensor, PIN)
        if humidity is not None and temperature is not None:
            print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
            print strftime('%d-%b-%Y %H:%M:%S')
            data = temperature, humidity
            temp1.append(str(data[0]))
            temp = str(data[0])
            hum = str(data[1])
            
        else:
            print('Failed to get reading. Try again!')
            sys.exit(1)

        with open('./data/'+filename+'.csv', 'a') as data_log:
            header = csv.writer(data_log)
            header.writerow(['Date', 'Time', 'Temperature', 'Humidity'])
            data_log.write(strftime('%d/%m/%y,%H:%M:%S'))
            data_log.write(','+temp+','+hum)
            data_log.write(strftime('\n'))
    time.sleep(6)
    return temp1
        
        

def plotting():
    
    fig = plt.figure()
    rect = fig.patch
    rect.set_facecolor('#65d939')
    
    def animate(i):
        time.sleep(3)
        ftemp = './data/'+filename+'.csv'
        
        with open(ftemp) as fh:
            incsv = csv.reader(fh)
            next(fh)
            temp = []
            timeC = []
        
            for line in fh:
                lines = line.split(',')
                degree = lines[2]
                timeB=  lines[1]
                timeA= timeB[:8]
                time_string = datetime.strptime(timeA,'%H:%M:%S')
                try:
                    temp.append(float(degree))
                    timeC.append(time_string)
                except:
                    print "dont know"

            ax1 = fig.add_subplot(1,1,1,axisbg='black')
            ax1.clear()
            ax1.plot(timeC,temp, 'c', linewidth = 3.3)
            plt.title('Temperature')
            plt.xlabel('Time')
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
            ax1.xaxis.set_major_locator(mdates.MinuteLocator(interval = 8))
            _ = plt.xticks(rotation = 30)
            
    ani = animation.FuncAnimation(fig, animate, interval = 6000)
    plt.show()

    
if __name__ == '__main__':
    readings = threading.Thread(name='reading',target=get_readings)
    plotting = threading.Thread(name='plot',target=plotting)
    readings.start()
    plotting.start()





