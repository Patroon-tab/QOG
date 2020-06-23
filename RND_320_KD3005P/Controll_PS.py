# -*- coding: utf-8 -*-
"""
Created on Tue May 12 17:24:10 2020

@author: Patrick
"""
import serial


class Connection:

    def __init__(self):
        pass

    def initialize(self, port):
        self.ser = serial.Serial()
        self.port = port
        self.ser = serial.Serial(self.port, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE, timeout=1)

    def setvoltage(self, voltage):
        command = "VSET1:" + str(voltage)
        command = command.encode()
        self.ser.write(command)

    def setcurrent(self, current):
        command = "ISET1:" + str(current)
        command = command.encode()
        self.ser.write(command)

    def getvaluees(self):
        self.ser.write(b'VOUT1?')
        v = self.ser.readline()
        self.ser.write(b'IOUT1?')
        i = self.ser.readline()
        if i == b'' or v == b'':
            i = b'N/A'
            v = b'N/A'
        i = i.decode('utf-8')
        v = v.decode('utf-8')
        return (i, v)

    def kill(self):
        self.ser.close()
