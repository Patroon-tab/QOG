# -*- coding: utf-8 -*-
"""
Created on Tue May 26 10:21:51 2020

@author: Patrick
"""

import serial
import time

delay = 0.05


class Connection:

    def __init__(self):
        pass

    def initialize(self, port):
        try:

            self.port = port
            self.ser = serial.Serial(self.port, 9600, timeout=1)
            time.sleep(delay)

        except:
            pass


    def decodein(self, x):
        x = x.strip(b"""\r\n""")
        x = x.decode("utf-8")
        x = x.strip('''"''')
        return x

    def sendcommand(self, command):
        command = command + b"""\r\n"""
        self.ser.write(command)
        time.sleep(delay)

    def getValue(self):

        self.sendcommand(b'FETC?')
        x = self.ser.readline()
        x = self.decodein(x)

        try:

            x = float(x)

        except:
            x = "Error"
        time.sleep(delay)

        return x

    def finddevice(self):

        self.sendcommand(b'SYST:BEEP')
        self.sendcommand(b'SYST:BLIT 1')
        self.ser.readline()  # Reads the OK value from Device
        time.sleep(delay)

    def getsetup(self):

        self.sendcommand(b'CONF?')
        x = self.ser.readline()
        x = self.decodein(x)
        x = x.split(" ")
        unit = x[0]
        time.sleep(delay)
        return (unit, x)

    def getbattery(self):

        self.sendcommand(b'SYST:BATT?')
        x = self.ser.readline()
        x = self.decodein(x)
        x = float(x)
        return x
        

    def kill(self):
        self.ser.close()

def main():
    dmm = Connection()
    dmm.initialize("COM5")
    print(dmm.getValue())
    print(dmm.getbattery())
    dmm.kill()


if __name__ == '__main__':
    main()
