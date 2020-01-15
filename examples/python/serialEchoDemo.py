#!/usr/bin/env python
# coding: utf-8

'''
@disc:  Python UART Communication on the 
        Arduino  Shied
        
        The best Test Build for this demo is to connect 
        RX and TX together with a cable (null modem)

        D1 - RXD <----
                     |
        D0 - TXD <---
         
@date:   10.09.2019
@device: Intel Cyclone V 
@author: Robin Sebastian
         (https://github.com/robseb)
'''

import os
import time

### The package "serial" must be installed with the Python pip package manager                                        
### Connect the Board to the internet and run following command inside the Linux console:          
## ->   pip install pyserial                                                               

import serial

# Demo duration  
TEST_DURATIONS = 10

# Documentation and examples with Python Serial: 
# https://pyserial.readthedocs.io/en/latest/shortintro.html

if __name__ == '__main__':
    print("Python Serial Echo Demo")

    for var in range(TEST_DURATIONS):

        # Open UART1 with Baud 9600 and timeout after 1sec 
        ser = serial.Serial('/dev/ttyS1',9600, timeout=1 )

        # Write a ASIC to a String
        # b -> tells Python to insert a String as ASCII
        ser.write(b'rsYocto SoC-FPGA \n')

        # Read the transmitted string over the null modem connection back
        line = ser.readline() 

        # Print the readout to the console 
        print(line)

        # Close the COM port 
        ser.close() 

        # trigger the Task in 50ms again
        time.sleep(.050)
        
print('End of demo...')






