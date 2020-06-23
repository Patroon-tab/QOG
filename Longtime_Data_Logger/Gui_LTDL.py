# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 10:14:08 2020

@author: Patrick
"""
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
from tkinter import messagebox


class MyGui:

    def __init__(self):

        self.window = Tk()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)


        """
        but = Button(self.window, text = "Start", font = "Calibri 20", width = 6, height = 1)
        but.grid(row = 3, column = 3)
        """
        # Frame1
        self.frame1 = Frame(self.window)
        self.frame1.grid(row=0, column=0)
        lab = Label(self.frame1, text="File Header:", font="calibri 20", width=10, height=1)
        lab.grid(row=0, column=0)

        self.headerentry = ScrolledText(self.frame1, height=3, width=20)
        self.headerentry.grid(row=0, column=1)
        #Frame1 End

        # Frame2
        self.frame2 = Frame(self.window)
        self.frame2.grid(row=1, column=0)
        lab = Label(self.frame2, text="Path:", font="calibri 20")
        lab.grid(row=0, column=0)
        buttonpath = Button(self.frame2, text="Browse", command=self.browse_button, font="calibri 20", width=7,
                            height=1)
        buttonpath.grid(row=0, column=1)
        #Frame2 End

        #Frame3
        widthtime = 3
        self.frame3 = Frame(self.window)
        self.frame3.grid(row=2, column = 0)
        self.dayE = Entry(self.frame3, width=widthtime)
        self.dayE.grid(row = 0, column = 1)
        lab = Label(self.frame3, text = "Days:")
        lab.grid(row = 0, column = 0)
        self.hourE = Entry(self.frame3,width=widthtime)
        self.hourE.grid(row=0, column=3)
        lab = Label(self.frame3, text="Hours:")
        lab.grid(row=0, column=2)
        self.minutesE = Entry(self.frame3,width=widthtime)
        self.minutesE.grid(row=0, column=5)
        lab = Label(self.frame3, text="Minutes:")
        lab.grid(row=0, column=4)
        #Fram3 End
    def start(self):
        self.window.mainloop()

    def browse_button(self):
        self.filename = filedialog.askdirectory()
        print(self.filename)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?\n some meassurement will be lost\n and the programm will stop meassuring"):
            self.window.destroy()

def main():
    la = MyGui()
    la.start()

if __name__ == '__main__':
    main()
