# -*- coding: utf-8 -*-
"""
Created on Tue May 26 10:21:51 2020

@author: Patrick
"""


import serial
import time
delay = 0.05

def decodein(x):
    
    x = x.strip(b"""\r\n""")
    x = x.decode("utf-8") 
    x = x.strip('''"''')
    return x

def initialise(com):
    
    ser = serial.Serial(com, 9600, timeout=1)
    time.sleep(delay)
    return ser

def sendcommand(ser, command):

    command = command + b"""\r\n"""
    ser.write(command)
    time.sleep(delay)
    
def getvalue(ser):
    
    sendcommand(ser, b'FETC?')
    x = ser.readline()
    x = decodein(x)
    
    try:
        
        x = float(x)
        
    except:
        x = "Error"
    time.sleep(delay)
    return x


def finddevice(ser):
    
    sendcommand(ser, b'SYST:BEEP')
    sendcommand(ser, b'SYST:BLIT 1')
    ser.readline() #Reads the OK value from Device
    time.sleep(delay)
    
def getsetup(ser):
    
    sendcommand(ser, b'CONF?')
    x = ser.readline()
    x = decodein(x)
    x = x.split(" ")
    unit = x[0]
    time.sleep(delay)
    return(unit, x)


    

