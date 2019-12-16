'''
Created on 10.08.2019

Python UART Comunication on the 
Adruino  Shild

The best Test Build for this demo is to connect 
RX and TX together with a cable (null modem)

D1 - RXD <----
             |
D0 - TXD <---

@author: Robin Sebastian
...      (https://github.com/robseb)
'''
import os
import time

### The packge "serial" must be Installed with the Python PIP package manger                                        #
### Connect the Board to a internet connection and run following comand inside the Linux console:                   #
## ->   python3 -m pip install --upgrade pyserial --trusted-host pypi.org --trusted-host files.pythonhosted.org  <- #
# (PIP3 package manager to install serial)                                                                          #

import serial

TEST_DURATIONS = 10

# Documation and examples to Python Serial: 
# https://pyserial.readthedocs.io/en/latest/shortintro.html

if __name__ == '__main__':
    print("Python Serial Demo")

    for var in range(TEST_DURATIONS):
        # Open UART1 with Baud 9600
        ser = serial.Serial('/dev/ttyS1',9600)
        # Write a ASIC to a String
        # b -> tells Python to insiert a String as ASCI
        ser.write(b'rsYocto SoC-FPGA \n')

        # read the transmit over the null modem connection back
        line = ser.readline() 

        # Print the readout back to the console
        print(line)

        # Close the COM port 
        ser.close() 
        # triger the Task in 50ms again and repead 
        time.sleep(.050)
        
print('End...')






