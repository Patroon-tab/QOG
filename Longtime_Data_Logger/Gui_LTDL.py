# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 10:14:08 2020

@author: Patrick
"""
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog


class MyGui:

    def __init__(self):
        self.window = Tk()

        """
        but = Button(self.window, text = "Start", font = "Calibri 20", width = 6, height = 1)
        but.grid(row = 3, column = 3)
        """
        # Frame1
        self.frame1 = Frame(self.window)
        self.frame1.grid(row=0, column=0)
        lab = Label(self.frame1, text="File Header", font="calibri 20", width=10, height=1)
        lab.grid(row=0, column=0)

        self.headerentry = ScrolledText(self.frame1, height=3, width=20)
        self.headerentry.grid(row=0, column=1)

        # Frame2
        self.frame2 = Frame(self.window)
        self.frame2.grid(row=1, column=0)
        lab = Label(self.frame2, text="Path:", font="calibri 20")
        lab.grid(row=0, column=0)
        buttonpath = Button(self.frame2, text="Browse", command=self.browse_button, font="calibri 20", width=7,
                            height=1)
        buttonpath.grid(row=0, column=1)

    def start(self):
        self.window.mainloop()

    def browse_button(self):
        self.filename = filedialog.askdirectory()
        print(self.filename)


la = MyGui()
la.start()