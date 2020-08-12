# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 10:14:08 2020

@author: Patrick
"""

"""
IMPORTANT NOTE: To make this guy look better there is still some work to do. Software works it just doesn't look that nice yet
"""
import time
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
from tkinter import messagebox
import serial.tools.list_ports
from matplotlib import style
style.use('ggplot')
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

from matplotlib.figure import Figure
from Keysight_U1252B.Communication import Connection

import numpy as np


class MyGui:

    def __init__(self):
        self.window = Tk()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.xvals = []
        self.yvals = []

        """
        but = Button(self.window, text = "Start", font = "Calibri 20", width = 6, height = 1)
        but.grid(row = 3, column = 3)
        """
        # Frame1
        self.frame1 = Frame(self.window)
        self.frame1.grid(row=0, column=0)

        lab = Label(self.frame1, text="File Header:", font="calibri 20", width=10, height=1, anchor="e")
        lab.grid(row=0, column=0, sticky="E", pady=15)

        self.headerentry = ScrolledText(self.frame1, height=3, width=20)
        self.headerentry.grid(row=0, column=1, sticky="E")

        lab = Label(self.frame1, text="File Path:", font="calibri 20", width=10, height=1, anchor="e")
        lab.grid(row=1, column=0)
        buttonpath = Button(self.frame1, text="Browse", command=self.browse_button, font="calibri 20", width=11,
                            height=1, anchor="center")
        buttonpath.grid(row=1, column=1, sticky="w", pady=(0, 5))
        # Frame1 End

        # Frame3
        widthtime = 3
        self.frame3 = Frame(self.window)
        self.frame3.grid(row=1, column=0)
        lab = Label(self.frame3, text="Duration:", font="calibri 20", width=8, height=1)
        lab.grid(row=1, column=0, sticky="e", padx=(0, 20))
        self.dayE = Entry(self.frame3, width=widthtime)
        self.dayE.grid(row=0, column=2, padx=(5, 18))
        lab = Label(self.frame3, text="Days:", font="calibri 15")
        lab.grid(row=0, column=1, sticky="e")
        self.hourE = Entry(self.frame3, width=widthtime)
        self.hourE.grid(row=1, column=2, padx=(5, 18))
        lab = Label(self.frame3, text="Hours:", font="calibri 15")
        lab.grid(row=1, column=1, sticky="e")
        self.minutesE = Entry(self.frame3, width=widthtime)
        self.minutesE.grid(row=2, column=2, padx=(5, 18))
        lab = Label(self.frame3, text="Minutes:", font="calibri 15")
        lab.grid(row=2, column=1, sticky="e")
        lab = Label(self.frame3, text="Interval:", font="calibri 20")
        lab.grid(row=3, column=0, padx=(0, 20))
        lab = Label(self.frame3, text="Seconds:", font="calibri 15")
        lab.grid(row=3, column=1, sticky="e")
        self.entryT = Entry(self.frame3, width=widthtime)
        self.entryT.grid(row=3, column=2, padx=(5, 18))

        # Frame3 End

        # Frame5 Start
        self.frame5 = Frame(self.window)
        self.frame5.grid(row=3, column=0)
        lab = Label(self.frame5, text="DMM:", font="calibri 20")
        lab.grid(row=0, column=0, sticky="e", padx=10)
        but = Button(self.frame5, text="Ping", command=self.ping, font="calibri 12", pady=2)
        but.grid(row=0, column=3, padx=10)
        but = Button(self.frame5, text="R", command=self.ping, font="calibri 12", pady=2)
        but.grid(row=0, column=4, padx=10)
        self.dropdowncom(self.frame5)

        # self.batterystat = Progressbar(self.frame5, orient=HORIZONTAL, length=100, mode="determinate")
        # self.batterystat.grid(row=1, column=0, columnspan=2)
        # Frame5 End

        # Frame7

        self.frame7 = Frame(self.window)
        self.frame7.grid(column=1, row=3)
        self.batlabel = Label(self.frame7, text="Battery: n/a %", font="calibri 15")
        self.batlabel.grid(row=0, column=1, padx=20)
        but = Button(self.frame7, text="Start", command=self.startmeas, font="calibri 15")
        but.grid(row=0, column=2, padx=(10, 0))
        self.percentlab = Label(self.frame7, text="Progress: 0%", font="calibri 15")
        self.percentlab.grid(row=0, column=0, padx=(0, 10))

        # Frame Graph

        self.frame8 = Frame(self.window)
        self.frame8.grid(row=0, column=1, rowspan=2)

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.suba = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame8)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)


        # Frame Graph End

    def dropdowncom(self, frame):

        find_com = serial.tools.list_ports
        COM = find_com.comports()
        self.COM_LIST = []
        for x in COM:
            self.COM_LIST.append(x[0])

        if self.COM_LIST == []:
            self.COM_LIST.append("COM0")

        self.dmmcom = StringVar(self.window)
        self.dmmcom.set(self.COM_LIST[0])
        self.DMM = OptionMenu(frame, self.dmmcom, *self.COM_LIST)
        self.DMM.grid(column=1, row=0, sticky="e")
        self.DMM.config(width=5, height=1, highlightthickness=0, font="Calibri 14")

    def updatecoms(self):
        print("update")
        find_com = serial.tools.list_ports
        COM = find_com.comports()
        self.COM_LIST = []
        for x in COM:
            self.COM_LIST.append(x[0])

        if self.COM_LIST == []:
            self.COM_LIST.append("COM0")

        self.dmmcom.set('')
        self.DMM['menu'].delete(0, 'end')

        new_choices = self.COM_LIST

        for choice in new_choices:
            self.DMM['menu'].add_command(label=choice, command=tkinter._setit(self.dmmcom, choice))

        self.dmmcom.set(self.COM_LIST[0])

    def updatecoms(self):
        print("update")
        find_com = serial.tools.list_ports
        COM = find_com.comports()
        self.COM_LIST = []
        for x in COM:
            self.COM_LIST.append(x[0])

        if self.COM_LIST == []:
            self.COM_LIST.append("COM0")

        self.dmmcom.set('')
        self.DMM['menu'].delete(0, 'end')

        new_choices = self.COM_LIST

        for choice in new_choices:
            self.DMM['menu'].add_command(label=choice, command=tkinter._setit(self.dmmcom, choice))

        self.dmmcom.set(self.COM_LIST[0])

    def start(self):
        self.window.mainloop()

    def browse_button(self):
        print("Browse")
        self.filename = filedialog.askdirectory()
        print(self.filename)

    def ping(self):

        self.dmm = Connection()
        self.dmm.initialize(self.dmmcom.get())
        self.dmm.finddevice()
        self.batlabel["text"] = "Battery: " + str(self.dmm.getbattery()) + "%"
        self.dmm.kill()

    def gettime(self):

        try:
            d = int(self.dayE.get())
        except:
            d = 0
        try:
            h = int(self.hourE.get())
        except:
            h = 0
        try:
            m = float(self.minutesE.get())
        except:
            m = 0
        try:
            timeb = float(self.entryT.get())
        except:
            timeb = 3

        self.time = d * 24 * 60 * 60 + h * 60 * 60 + m * 60
        self.timebet = timeb

    def startmeas(self):
        self.suba.clear()

        print("clear")
        self.gettime()
        numberofmeas = self.time / self.timebet
        numberofmeas = int(numberofmeas)
        print(numberofmeas)
        time = 0
        path = self.filename + "/measurement.txt"
        file = open(path, "w")
        file.write(self.headerentry.get('1.0', END) + "\n")
        file.write("Meassurement[n]; Time[s]; Value; Unit \n")
        file.close()
        com = self.dmmcom.get()
        self.dmm.initialize(com)
        unitdmm = self.dmm.getsetup()[0]
        self.xvals = []
        self.yvals = []


        for x in range(numberofmeas):
            self.dmm.initialize(com)
            value = self.dmm.getValue()
            self.dmm.kill()
            file = open(path, "a")
            print(x, time)
            linewr = ("%d;%.3f;%.6f;%s \n" % (x, time, value, unitdmm))
            self.xvals.append(time)
            self.yvals.append(value)
            print(linewr)
            file.write(linewr)
            file.close()
            self.suba.plot(self.xvals, self.yvals, color="blue")
            self.canvas.draw()
            percent = (x / numberofmeas) * 100
            self.percentlab["text"] = ("Progress: %.2f" % percent)  # Showing percentage in Gui
            self.sleep(self.timebet)
            time = time + self.timebet



        file.close()

    def rgraph(self):

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.suba = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame8)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    def sleep(self, x):

        duration = 0
        start = time.perf_counter()
        print("sleep")
        while duration <= x:
            time.sleep(0.005)
            self.window.update()
            duration = time.perf_counter() - start

    def on_closing(self):
        if messagebox.askokcancel("Quit",

                                  "Do you want to quit?\n some meassurement will be lost\n and the programm will stop meassuring"):
            self.window.destroy()


def main():
    la = MyGui()
    la.start()


if __name__ == '__main__':
    main()
