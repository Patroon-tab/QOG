import serial
import time

"""
Author: Patrick Helbingk
"""


class Connection:

    def __init__(self):

        self.ser = "error"

    def initialize(self, port):
        self.port = port

        try:
            self.ser = serial.Serial()
            self.ser = serial.Serial(self.port, baudrate=2400, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                                     stopbits=serial.STOPBITS_ONE, timeout=0.1, rtscts=False, dsrdtr=True)
            self.ser.setRTS(0)
            self.ser.setDTR(1)
            self.ser.setDTR(0)
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
            self.ser.setDTR(1)




        except:
            print("Port is already Open please close Port and restart programm")

    def getvalue(self):

        self.ser.setRTS(0)
        self.ser.setDTR(1)
        self.ser.setDTR(0)
        time.sleep(0.1)
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        time.sleep(0.1)
        self.ser.setDTR(1)
        tries = 0
        error = 0
        time.sleep(0.1)
        z = 0

        while True:

            x = self.ser.read(1)
            error = 0
            z = z + 1
            if z == 30:
                rawvalue = 0
                value = 0
                unit = "Error"
                prefix = "Error"
                precision = 0
                error = 1
                break

            if x == b'+' or x == b'-':
                vorzeichen = x
                value = self.ser.read(4)
                self.ser.read(1)
                precision = self.ser.read(1)
                self.ser.read(1)
                self.ser.read(1)
                prefix = self.ser.read(1)
                unit = self.ser.read(1)
                self.ser.read(2)
                rawvalue = 0
                factor = 0
                if self.ser.read(1) != b'\n':
                    print("There is an error on the DMM side, data is not send correctly")
                    error = 1

                if value == b'?0:?':
                    print("Out of range")
                    value = "!range"
                elif vorzeichen == b'+':
                    value = float(value)
                elif vorzeichen == b'-':
                    value = float(value) * -1

                if unit == b' ':
                    unit = "Ohm"
                elif unit == b'@':
                    unit = "A"
                elif unit == b'\x80':
                    unit = "V"
                elif unit == b'\x08':
                    unit = "Hz"
                elif unit == b'\x02':
                    unit = "Celsius"
                elif unit == b'\x01':
                    unit = "Fahrenheit"
                    print("Common dont use the imperial System")
                else:
                    unit = "not supported"
                    print("You are using an non supported Meassurement Unit for example Farrad")

                if prefix == b'@':
                    prefix = "m"
                    factor = 1000
                elif prefix == b'\x00':
                    prefix = ""
                    factor = 1
                elif prefix == b'\x80':
                    prefix = "u"
                    factor = 1000000
                elif prefix == b' ':
                    prefix = "k"
                    factor = 0.001
                elif prefix == b'\x10':
                    prefix = "M"
                    factor = 0.000001

                if precision == b'0':
                    precision = 0
                elif precision == b'1':  # corrct
                    precision = 3
                elif precision == b'2':
                    precision = 2
                elif precision == b'4':  # correct
                    precision = 1
                else:
                    print("There is an error")
                    error = 1

                try:

                    if value != "!range":
                        rawvalue = (value / factor) / 10 ** precision
                    else:
                        rawvalue = "!range"

                except:
                    pass

                if error != 1:

                    break

                else:
                    self.ser.readline()

                    tries = tries + 1

                if tries == 5:
                    rawvalue = 0
                    value = 0
                    unit = "Error"
                    prefix = "Error"
                    precision = 0
                    break

        return (rawvalue, value, unit, prefix, precision, error)

    def kill(self):
        self.ser.close()
