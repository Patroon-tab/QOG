from tkinter import *
from DMM_UT61B.DMM import Connection
import serial
import serial.tools.list_ports


class MyGui:

    def __init__(self):

        self.window = Tk()
        self.window.title("UT61B Gui V0.9")
        self.window.iconbitmap("icon2.ico")
        self.dropdowncom()

        lab = Label(self.window, text="Choose Com -->")
        lab.grid(column=0, row=0, sticky="w")

        self.dmmval = Label(self.window, text="DMM Value", width=16)
        self.dmmval.grid(column=0, row=2, columnspan=2, rowspan=3)
        self.dmmval.config(font=("Courier", 15))

        button = Button(self.window, text="Get Value", width=14, command=self.getvalues)
        button.grid(column=1, row=1)

    def dropdowncom(self):

        find_com = serial.tools.list_ports
        COM = find_com.comports()
        COM_LIST = []

        if COM == []:
            COM_LIST.append("COM0")
        else:

            for x in COM:
                COM_LIST.append(x[0])

        self.dmmcom = StringVar(self.window)
        self.dmmcom.set(COM_LIST[0])
        self.DMM = OptionMenu(self.window, self.dmmcom, *COM_LIST)
        self.DMM.grid(column=1, row=0, sticky="w")
        self.DMM.config(width=11)

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
            self.DMM['menu'].add_command(label=choice, command=lambda v=self.dmmcom, l=choice: v.set(l))

        self.dmmcom.set(self.COM_LIST[0])
        #self.window.after(1000, self.updatecoms)

    def getvalues(self):

        dmm = Connection()
        dmm.initialize(self.dmmcom.get())

        x = dmm.getvalue()
        value = x[0]
        unit = x[2]

        if value != "Error":

            self.dmmval.config(text=("%.5f %s" % (value, unit)))

        else:
            self.dmmval.config(text="Error")

        dmm.kill()

    def start(self):
        self.updatecoms()
        self.window.mainloop()


def main():
    window = MyGui()
    window.start()


if __name__ == '__main__':
    main()
