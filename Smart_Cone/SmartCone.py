'''
Authors: Yanning Li, Fangyu Wu
Date: Summer 2015

THIS MODULE CONSISTS OF 5 sections:
     LIABRARY: The raw data feedback from the sensor, parsed in a useful form
     VISUALIZATION: Visualization tools
     STATISTICS: Simple statistics properties of the library
     ESTIMATION: Model for vehicle detection, classification, and speed estimation
     VALIDATION: Validation tools

Essentially, this is an online emulator of the real time smart cone sensor packs.
To use the SmartCone class, do
    emulator = SmartCone(mode,buffer_size,estimator)
'''

import os
import csv
import warnings
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
import datetime
from sklearn import linear_model
from sklearn import cross_validation
from astroML.plotting import setup_text_plots
setup_text_plots(fontsize=14, usetex=True) # This will create LaTex style plotting.
from Estimators import Estimators

#Primary class
class SmartCone: 

    #LIABRARY
    def __init__(self,mode='read',bufferSize='inf',estimatorType=None):

        self.timeDiff = datetime.timedelta(hours=21,minutes=39,seconds=46,milliseconds=472.497)
        if mode == 'read':

            #Get the relative paths of data in data/.
            self.FILES = []
            for root, dirs, files in os.walk('data/'):
                for file in sorted(files):
                    if file.endswith(".csv"):
                        self.FILES.append(os.path.join(root, file))
                        #print self.FILES
            
            #Pour data from files to a list.
            self.DATASETS = []
            for file in self.FILES:
                with open(file,'r') as dataset:
                    fileReader = csv.reader(dataset)
                    for line in fileReader:
                        #print line
                        self.DATASETS.append(line)

            #Store data in buffer, which essentially acts like a queue.
            self.BUFFER = []
            if bufferSize == 'inf':
                print 'Buffer size is set to infinitive.'
                self.BUFFER = self.DATASETS

            elif isinstance(bufferSize,int) and bufferSize > 0:
                print 'Buffer size is %d.' % bufferSize
                self.BUFFER = self.DATASETS[0:buffer]
                self.currLocation = bufferSize

            else:
                sys.exit('ERROR: Buffer needs to be a positive integer.')
        
        #TODO: Read data from serial port.
        elif mode == 'listen':
            sys.exit('WARNING: Mode to be defined.')
            pass

        else:
            sys.exit('ERROR: Mode not defined.')
            
        #Instantiate an estimator class. Comment the code while testing to improve speed.
        #self.Estimator = Estimators(BUFFER=self.BUFFER,estimator=estimatorType)


    #VISUALIZATION
    def timeSeries(self,parameter='mean'):

        if parameter == 'mean':
            #plt.ion()
            print 'Plotting mean...'
            pir2Mean = [np.average([float(i) for i in line[69:133]]) for line in self.DATASETS]
            pir2Mean = np.array(pir2Mean)
            locMax = [argrelextrema(pir2Mean, np.greater)[0]]
            timeStamp = [self.timeFormat(float(line[0]))+self.timeDiff for line in self.DATASETS]
            timeStamp = np.array(timeStamp)
            #print pir2Mean[locMax]
            
            plt.figure()
            H = np.histogram(pir2Mean[locMax],bins=300)
            print len(H[1])
            h = H[0]
            plt.plot(H[1][:-1],h)
            hMax = np.argmax(h)
            norm0 = range(hMax)
            norm1 = range(hMax+1,2*hMax+1)[::-1]
            h[norm1] = h[norm1] - h[norm0]
            h[norm0] = 0
            h[hMax] = 0
            hMax1 = np.argmax(h)
            plt.plot(H[1][:-1],h)
            print (hMax1-hMax)*(H[1][1]-H[1][0])

            #plt.figure()
            #plt.hist(pir2Mean[locMax],bins=250,histtype='stepfilled',color='b',label='Peak')
            #plt.hist(pir2Mean,bins=250,histtype='stepfilled',color='r',alpha=0.5,label='Normal')
            #plt.scatter(timeStamp[locMax], pir2Mean[locMax])
            #plt.plot(timeStamp, pir2Mean)
            plt.show(block=False)
            print 'Done.'

        elif parameter == 'variance':
            print 'Plotting variance...'
            pir2Var = [np.var([float(i) for i in line[69:133]]) for line in self.DATASETS]
            timeStamp = [self.timeFormat(float(line[0]))+self.timeDiff for line in self.DATASETS]
            plt.plot(timeStamp, pir2Var)
            plt.show(block=False)
            print 'Done.'

        elif parameter == 'difference':
            print 'Plotting difference...'
            pir2Mean = [np.average([float(i) for i in line[69:133]]) for line in self.DATASETS]
            pir2Diff = [0]
            for i in range(1,len(pir2Mean)):
                pir2Diff.append(pir2Mean[i] - pir2Mean[i-1])
            timeStamp = [self.timeFormat(float(line[0]))+self.timeDiff for line in self.DATASETS]
            plt.plot(timeStamp,pir2Diff)
            plt.show(block=False)
            print 'Done.'

        elif parameter == 'ultrasonic':
            print 'Plotting ultrasonic sensor data...'
            ultrasonic = [line[134] for line in self.DATASETS]
            timeStamp = [self.timeFormat(float(line[0]))+self.timeDiff for line in self.DATASETS]
            plt.plot(timeStamp, ultrasonic)
            plt.show(block=False)
            print 'Done.'
        else:
            sys.exit('ERROR: Parameter not defined.')
        plt.show()

    def heatMap(self):
        pass

    #STATISTICS
    def stdev(self):
        pass

    def avg(self):
        pass

    #ESTIMATION
    def estimate(self):
        self.Estimator.run()
        

    #VALIDATION
    def scores(self):
        pass

    def inspect(self):
        pass


    #HLPER FUNCTIONS

    #Change time stamp format to Python datetime format
    def timeFormat(self,datenum):
        return datetime.datetime.fromtimestamp(int(datenum))

    #Update buffer
    def update(self,step=1):

        if mode == 'read': 
            for i in range(step):
                self.BUFFER.pop(0)
                self.BUFFER.append(self.DATASETS[self.curr])
            Estimator.update(self.BUFFER)

        else:  
            sys.exit('WARNING: Mode to be defined.') #Listen to serial
