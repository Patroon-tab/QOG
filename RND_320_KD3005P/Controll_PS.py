# -*- coding: utf-8 -*-
"""
Created on Tue May 12 17:24:10 2020

@author: Patrick
"""
import serial
import time

def initialise(com):
    
    global ser   
    ser = serial.Serial()           
    ser = serial.Serial(com, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1)
    return ser
  
def setvoltage(ser, voltage):

     command = "VSET1:" + str(voltage)
     command = command.encode()
     ser.write(command)

def setcurrent(ser, current):
     
     command = "ISET1:" + str(current)
     command = command.encode()
     ser.write(command)

def getvalues(ser):
    ser.write(b'VOUT1?')
    v = ser.readline()
    ser.write(b'IOUT1?')
    i = ser.readline()
    if i == b'' or v == b'':
        i = b'N/A'
        v = b'N/A'
    i = i.decode('utf-8')
    v = v.decode('utf-8')
    return (i, v)


    
     
     
     
