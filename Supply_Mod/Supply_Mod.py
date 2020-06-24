# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 08:28:18 2020

@author: Patrick Helbingk
"""
import serial
import time


class Connection:

    def __init__(self):

        self.ser = "error"

    def initialise(self, port):

        try:

            self.ser = serial.Serial(port, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                                     stopbits=serial.STOPBITS_ONE, timeout=1)

            time.sleep(5)
            self.readempty()


        except Exception as e:
            print(e)
            print("error serial")
            return "error"

    def setvoltage(self, voltage):
        voltage = float(voltage)
        command = "VSET:" + str(voltage) + '\r'
        command = command.encode()
        print(command)
        self.ser.write(command)
        self.readempty()

    def setcurrent(self, current):
        current = float(current)
        command = "ISET:" + str(current) +'\r'
        command = command.encode()
        self.ser.write(command)
        self.readempty()

    def getvalues(self):
        self.ser.write(b'VOUT?')
        v = self.ser.readline()
        # self.ser.readline()
        self.ser.write(b'IOUT?')
        i = self.ser.readline()
        self.readempty()

        i = i.decode('utf-8')
        v = v.decode('utf-8')
        i = i[:-2]
        v = v[:-2]
        for x in i:
            print(x)

        print("end")

        if not i.endswith("A"):
            i = "N/A"

        if not v.endswith("V"):
            v = "N/A"

        return (i, v)

    def kill(self):
        if self.ser != "error":
            self.ser.close()

    def readempty(self):
        time.sleep(1)
        x = b'ava'
        while x != b'':
            x = self.ser.readline()
            print(x)
        self.ser.readline()



def main():
    ar = Connection()
    ar.initialise("COM6")
    time.sleep(2)

    # ar.setcurrent(1.0)
    # ar.setvoltage(8.13)
    ar.kill()


if __name__ == "__main__":
    main()
