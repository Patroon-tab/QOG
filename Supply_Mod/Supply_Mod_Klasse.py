# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 08:28:18 2020

@author: Patrick Helbingk
"""

class Connection:
    
    def __init__(self):
        
        self.ser = "error"
        

        
    def initialise(self, port):
        
        try:
            
            self.ser = serial.Serial()           
            self.ser = serial.Serial(port, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1)
            time.sleep(1)
            
            for x in range(7):
                self.ser.readline()
            
        except:
            
            return "error"
        
    def setvoltage(self, voltage):
           
        command = "VSET:" + str(voltage)
        command = command.encode()
        self.ser.write(command)
        self.ser.readline()
        
    def setcurrent(self, current):
        
        command = "ISET:" + str(current)
        command = command.encode()
        ser.write(command)
        ser.readline()
        
    def getvalues(self):
        
        self.ser.write(b'VOUT?')
        v = self.ser.readline()
        self.ser.readline()
        self.ser.write(b'IOUT?')
        i = self.ser.readline()
        self.ser.readline()
        
            
        i = i.decode('utf-8')
        v = v.decode('utf-8')
        
        if not i.endswith("A"):
            i = "N/A"
            
        if not v.endswith("V"):
            v = "N/A"
        
        return (i, v)
    
    def kill(self):
        
        if self.ser != "error":
            
            self.ser.close()
        
        
