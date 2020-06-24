# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 08:35:14 2020

@author: Patrick
"""

from tkinter import *
import tkinter
import serial.tools.list_ports
from Supply_Mod import Connection
import serial
import time


class MyGui:

    def __init__(self):

        self.bg = "dark slate gray"
        self.window = Tk()
        self.window.title("Supplymod RC 0.9")
        self.window.iconbitmap("icon2.ico")
        self.window.configure(bg=self.bg)
        self.padx = 5
        self.pady = 2
        self.connectionstat = False
        self.window.geometry("510x250")

        # Frame 1
        self.frame1 = Frame(self.window, bg=self.bg)
        self.frame1.pack_propagate(False)
        self.frame1.grid(column=1, row=0, pady=5, padx=5, sticky="w")

        self.isv = Label(self.frame1, width=9, text="20 V", font="Calibri 20")
        self.isv.grid(column=0, row=0, sticky="w", padx=self.padx, pady=self.pady)

        self.isi = Label(self.frame1, width=9, text="0.5 A", font="Calibri 20")
        self.isi.grid(column=0, row=1, sticky="w", padx=self.padx, pady=self.pady)

        self.inpv = Entry(self.frame1, width=9, font="Calibri 20", justify='center')
        self.inpv.grid(column=1, row=0, sticky="w", padx=self.padx, pady=self.pady)
        self.inpv.insert(0, "20")

        self.inpc = Entry(self.frame1, width=9, font="Calibri 20", justify='center')
        self.inpc.grid(column=1, row=1, sticky="w", padx=self.padx, pady=self.pady)
        self.inpc.insert(0, "0.5")
        # Frame 1 End 

        # Frame 2
        self.frame2 = Frame(self.window, bg=self.bg)
        self.frame2.grid(row=1, column=1, pady=5, padx=5, sticky="w")

        but = Button(self.frame2, text="READ", width=11, height=1, command=self.read, font="Calibri 14")
        but.grid(row=0, column=0, padx=self.padx, sticky="w", ipadx=6)

        but = Button(self.frame2, text="WRITE", width=11, height=1, command=self.setvals, font="Calibri 14")
        but.grid(row=0, column=1, padx=self.padx, sticky="w", ipadx=6)
        # Frame 2 End

        # Frame 3
        self.frame3 = Frame(self.window, bg=self.bg)
        self.frame3.grid(row=2, column=1, pady=5, padx=5, sticky="w")

        self.conbut = Button(self.frame3, text="CONNECT", width=11, height=1, command=self.connect, font="Calibri 14")
        self.conbut.grid(row=0, column=0, sticky="w", padx=self.padx, ipadx=6)

        self.dropdowncom(self.frame3)
        # Frame 3 End

        # Frame 4
        self.frame4 = Frame(self.window, bg=self.bg)
        self.frame4.grid(row=3, column=0, columnspan=2, pady=5, padx=5, sticky="w")
        self.errorbox = Label(self.frame4, text="No error", width=31, height=1, font="Calibri 20")
        self.errorbox.grid(row=0, column=0, padx=self.padx, ipadx=5)
        but = Button(self.frame4, text="R", width=3, height=1, command=self.updatecoms,font="Calibri 14")
        but.grid(row=0, column=2)
        # Frame 4 End

        # Frame 5
        self.frame5 = Frame(self.window, bg=self.bg)
        self.frame5.grid(row=0, column=0, rowspan=3)
        canvas = Canvas(self.frame5, width=208, height=156, bd=0, highlightthickness=0, relief='ridge')
        canvas.grid(row=0, column=0, padx=(10, 0))
        self.img = PhotoImage(file="pic.png")
        canvas.create_image(0, 0, anchor=NW, image=self.img)
        # Frame 5 End


    def start(self):

        self.connection = Connection()
        self.window.mainloop()
        self.connection.kill()

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
        self.DMM.grid(column=2, row=0, sticky="w", padx=self.padx, ipadx=1, ipady=2)
        self.DMM.config(width=9, height=1, highlightthickness=0, font="Calibri 14")

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

    def connect(self):

        if self.connectionstat == False:

            self.connection.initialise(self.dmmcom.get())

            if self.connection.ser != "error":

                self.conbut.config(text="DISCONNECT")
                self.connectionstat = True
                self.errorbox["text"] = ""

            elif self.connection.ser == "error":
                self.errorbox[
                    "text"] = "Problem connecting to Port"

        elif self.connectionstat == True:

            self.connection.kill()
            self.conbut.config(text="CONNECT")
            self.connectionstat = False

    def read(self):

        if self.connectionstat == False:

            self.errorbox["text"] = "Device is not Connected"

        else:

            self.errorbox["text"] = ""

            vals = self.connection.getvalues()

            if vals[0] == "N/A" or vals[1] == "N/A":

                self.errorbox["text"] = "NO DATA RECEIVED"

            else:

                self.isv["text"] = vals[0]
                self.isi["text"] = vals[1]

    def setvals(self):

        if self.connectionstat == False:
            self.errorbox["text"] = "Device is not Connected"

        else:
            self.errorbox["text"] = ""
            voltage = float(self.inpv.get())
            self.connection.setvoltage(voltage)
            # current = float(self.inpc.get())
            # self.connection.setcurrent(current)


def main():
    gui = MyGui()
    gui.start()


if __name__ == '__main__':
    main()
