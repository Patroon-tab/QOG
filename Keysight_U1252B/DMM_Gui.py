# -*- coding: utf-8 -*-
"""
Created on Tue May 26 16:04:29 2020

@author: Patrick
"""

from tkinter import *
from Serial_Communication import initialise
from Serial_Communication import getsetup
from Serial_Communication import getvalue
from Serial_Communication import finddevice
import serial
import serial.tools.list_ports


class MyGui:

    def __init__(self, window):

        self.window = window
        self.dropdowncom()

        lab = Label(self.window, text="Choose Com -->")
        lab.grid(column=0, row=0, sticky="w")

        self.dmmval = Label(self.window, text="DMM Value", width=16)
        self.dmmval.grid(column=0, row=2, columnspan=2, rowspan=3)
        self.dmmval.config(font=("Courier", 15))

        button = Button(self.window, text="Ping", width=14, command=self.pingdmm)
        button.grid(column=0, row=1)

        button = Button(self.window, text="Get Value", width=14, command=self.getvalues)
        button.grid(column=1, row=1)

    def dropdowncom(self):

        find_com = serial.tools.list_ports
        COM = find_com.comports()
        COM_LIST = []
        for x in COM:
            COM_LIST.append(x[0])

        self.dmmcom = StringVar(self.window)
        self.dmmcom.set(COM_LIST[0])
        self.DMM = OptionMenu(self.window, self.dmmcom, *COM_LIST)
        self.DMM.grid(column=1, row=0, sticky="w")
        self.DMM.config(width=11)

    def pingdmm(self):

        ser = initialise(self.dmmcom.get())
        finddevice(ser)
        ser.close()

    def getvalues(self):

        ser = initialise(self.dmmcom.get())
        unit = getsetup(ser)[0]
        value = getvalue(ser)

        if value != "Error":

            self.dmmval.config(text=("%.5f %s" % (value, unit)))

        else:
            self.dmmval.config(text="Error")


window = Tk()
MyGui(window)
window.mainloop()
