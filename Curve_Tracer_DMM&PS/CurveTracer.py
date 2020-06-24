1  # -*- coding: utf-8 -*-
"""
Created on Sat May 16 19:29:40 2020

@author: Patrick
"""
import serial
import time
import numpy as np
from DMM_UT61B.DMM import Connection as ConnectionDMM
from RND_320_KD3005P.Controll_PS import Connection as ConnectionPS
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import serial.tools.list_ports
from tkinter import *
from tkinter.ttk import *


class MyGui:

    def __init__(self, root):

        self.root = root

        self.root.withdraw()

        self.window = Toplevel(root)
        self.window.protocol("WM_DELETE_WINDOW", self.root.destroy)

        self.window.title("Diode Curve Tracer  DCT V19.1")

        Sourcelist = ["DMM1", "DMM2", "Supply"]

        canvas = Canvas(self.window, width=150, height=65)
        canvas.place(relx=0.874, rely=0.55, anchor=CENTER)
        self.img = PhotoImage(file="pll.png")
        canvas.create_image(20, 20, anchor=NW, image=self.img)

        self.start = Label(self.window, text="Start[V]:")
        self.start.grid(column=0, row=0, sticky="e")
        self.start = Entry(self.window, width=12)
        self.start.grid(column=1, row=0)

        self.stop = Label(self.window, text="Stop[V]:")
        self.stop.grid(column=0, row=1, sticky="e")
        self.stop = Entry(self.window, width=12)
        self.stop.grid(column=1, row=1)

        self.schrit = Label(self.window, text="Step[V]:")
        self.schrit.grid(column=0, row=2, sticky="e")
        self.schrit = Entry(self.window, width=12)
        self.schrit.grid(column=1, row=2)

        lab = Label(self.window, text="TITLE:")
        lab.grid(column=2, row=0, sticky="e")

        lab = Label(self.window, text="X-AXIS:")
        lab.grid(column=2, row=1, sticky="e")

        lab = Label(self.window, text="Y-AXIS:")
        lab.grid(column=2, row=2, sticky="e")

        self.title = Entry(self.window, width=20)
        self.title.grid(column=3, row=0)
        self.title.insert(0, "Grüne_LED")

        self.xa = Entry(self.window, width=20)
        self.xa.grid(column=3, row=1)
        self.xa.insert(0, "Spannung [V]")

        self.ya = Entry(self.window, width=20)
        self.ya.grid(column=3, row=2)
        self.ya.insert(0, "Strom [mA]")

        lab = Label(self.window, text="X-Values: ")
        lab.grid(column=0, row=3, sticky="e")

        lab = Label(self.window, text="Created 05/2020 by Patrick Helbingk")
        lab.grid(column=3, row=4, columnspan=3, sticky="e")

        self.sourcevariablex = StringVar(self.window)
        xaxiss = OptionMenu(self.window, self.sourcevariablex, Sourcelist[0], *Sourcelist)
        xaxiss.config(width=8)
        xaxiss.grid(row=3, column=1)

        lab = Label(self.window, text="Y-Values: ")
        lab.grid(column=0, row=4, sticky="e")

        self.sourcevariabley = StringVar(self.window)
        yaxiss = OptionMenu(self.window, self.sourcevariabley, Sourcelist[0], *Sourcelist)
        yaxiss.config(width=8)
        yaxiss.grid(row=4, column=1)

        self.progressbar = Progressbar(self.window, orient=HORIZONTAL, length=169, mode='determinate')
        self.progressbar.grid(row=3, column=2, columnspan=2, sticky="w")

        startmeassure = Button(self.window, text="Start Messung", width=17, command=lambda: self.measure())
        startmeassure.grid(column=4, row=1, sticky="e")

        startmeassure = Button(self.window, text="Setup", width=17, command=lambda: self.testcon())
        startmeassure.grid(column=4, row=0, sticky="e")

    def testcon(self):

        self.testwindow = Tk()
        self.testwindow.title("Diode Curve Traces : Setup")

        self.dmm1 = Label(self.testwindow, text="DMM1:")
        self.dmm1.grid(column=0, row=3, sticky="e")

        self.dmm2 = Label(self.testwindow, text="DMM2:")
        self.dmm2.grid(column=0, row=4, sticky="e")

        ps = Label(self.testwindow, text="PS:")
        ps.grid(column=0, row=5, sticky="e")
        dmm1show = Label(self.testwindow, text="DMM1", width=15, anchor="center")
        dmm1show.grid(column=3, row=3)
        dmm1show.config(font=("Courier", 15))

        dmm2show = Label(self.testwindow, text="DMM2", width=15, anchor="center")
        dmm2show.grid(column=3, row=4)
        dmm2show.config(font=("Courier", 15))

        self.psshow = Label(self.testwindow, text="PS", width=15, anchor="center")
        self.psshow.grid(column=3, row=5)
        self.psshow.config(font=("Courier", 15))

        button = Button(self.testwindow, text="Ping DMM1", width=14,
                        command=lambda: self.getdmm(self.dmm1com.get(), dmm1show))
        button.grid(column=2, row=3, sticky="e")

        button = Button(self.testwindow, text="Ping DMM2", width=14,
                        command=lambda: self.getdmm(self.dmm2com.get(), dmm2show))
        button.grid(column=2, row=4)

        button = Button(self.testwindow, text="Ping PS", width=14, command=lambda: self.getps(self.pscom.get()))
        button.grid(column=2, row=5, sticky="e")

        self.dropdowncom()

        self.testwindow.mainloop()

    def dropdowncom(self):
        find_com = serial.tools.list_ports
        COM = find_com.comports()
        COM_LIST = []
        for x in COM:
            COM_LIST.append(x[0])
            print(COM_LIST)

        self.dmm1com = StringVar(self.testwindow)
        self.DMM1 = OptionMenu(self.testwindow, self.dmm1com, COM_LIST[0], *COM_LIST)
        self.DMM1.grid(column=1, row=3)
        self.DMM1.config(width=7)

        self.dmm2com = StringVar(self.testwindow)
        DMM2 = OptionMenu(self.testwindow, self.dmm2com, COM_LIST[0], *COM_LIST)
        DMM2.grid(column=1, row=4)
        DMM2.config(width=7)

        self.pscom = StringVar(self.testwindow)
        PS = OptionMenu(self.testwindow, self.pscom, COM_LIST[0], *COM_LIST)
        PS.grid(column=1, row=5)
        PS.config(width=7)

    def getps(self, com):

        ps = ConnectionPS()
        ps.initialize(com)
        i, v = ps.getvaluees()
        ps.kill()

        if i == "N/A" or v == "N/A":
            self.psshow.config(text="PS N/A")
        else:
            self.psshow.config(text="%sV:%sA" % (v, i))

    def getdmm(self, com, dmm):

        dmmo = ConnectionDMM()
        dmmo.initialize(com)
        time.sleep(1)
        a = dmmo.getvalue()
        dmmo.kill()

        if a[5] == 1:
            dmm.config(text="DMM n/a")
        else:
            dmm.config(text=("%.3f%s%s" % (a[1] / 10 ** a[4], a[3], a[2])))

    def measure(self):

        startv = self.start.get()
        stopv = self.stop.get()
        stepv = self.schrit.get()
        print(startv, stopv, stepv)
        voltages = np.arange(float(startv), float(stopv) + float(stepv), float(stepv))
        xdevice = self.sourcevariablex.get()
        ydevice = self.sourcevariabley.get()
        xvalues = []
        yvalues = []
        progress = 0

        ps = ConnectionPS()
        ps.setvoltage(0)
        time.sleep(2)

        if xdevice == "DMM1" or ydevice == "DMM1":
            dmm1 = ConnectionDMM()
            dmm1.initialize(self.dmm1com.get())
        if xdevice == "DMM2" or ydevice == "DMM2":
            dmm2 = ConnectionDMM()
            dmm2.initialize(self.dmm2com.get())

        for x in voltages:
            ps.setvoltage(x)
            time.sleep(2)
            if xdevice == "DMM1":
                a = dmm1.getvalue()
                xvalues.append(a[0])
            elif ydevice == "DMM1":
                a = dmm1.getvalue()
                yvalues.append(a[0])

            if xdevice == "DMM2":
                a = dmm2.getvalue()
                xvalues.append(a[0])
            elif ydevice == "DMM2":
                a = dmm2.getvalue()
                yvalues.append(a[0])

            progress = progress + 1
            self.progressbar['value'] = int((progress / len(voltages)) * 100)
            self.window.update()
        self.progressbar['value'] = 0
        ps.setvoltage(0)

        if xdevice == "DMM1" or ydevice == "DMM1":
            serdmm1.kill()
        if xdevice == "DMM2" or ydevice == "DMM2":
            serdmm2.kill()
        ps.kill()

        if xdevice == "Supply":
            xvalues = voltages
        if ydevice == "Supply":
            yvalues = voltages

        self.showplot(xvalues, yvalues)

    def showplot(self, x, y):

        window2 = Tk()
        window2.geometry('720x480')
        window2.title("Diode Curve Traces : Graph")

        fig = Figure(figsize=(3, 2), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(x, y)

        ax.set_xlabel(self.xa.get())
        ax.set_ylabel(self.ya.get())
        ax.set_title(self.title.get())
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=window2)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, window2)
        toolbar.update()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        window2.mainloop()

        #TODO


def main():
    root = Tk()
    MyGui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
