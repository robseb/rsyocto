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
         
@date:   22.06.2020
@device: Intel Cyclone V 
@author: Robin Sebastian
         (https://github.com/robseb)
         (git@robseb.de)
'''

import os
import time
import sys

### The package "serial" must be installed with the Python pip package manager                                        
### Connect the Board to the internet and run following command inside the Linux console:          
## ->   pip3 install pyserial                                                               


try:
    import serial
except ImportError:
    print('This Demo uses the Python pip package "pyserial"')
    print('Run following command to install it:')
    print('pip3 install  pyserial')
    sys.exit()

# Demo duration  
TEST_DURATIONS = 5

# Documentation and examples with Python Serial: 
# https://pyserial.readthedocs.io/en/latest/shortintro.html

if __name__ == '__main__':
    print("Python Serial Echo Demo")

    # Read the name of the used development board 
    #-> Only the Terasic DE10 Standard and Nano Boards are allowed!
    # The Board name for the image is located here: "/usr/rsyocto/suppBoard.txt"
    if os.path.isfile("/usr/rsyocto/suppBoard.txt"):
        supportStr = ""
        with open("/usr/rsyocto/suppBoard.txt", "r") as f:
            supportStr = f.read()
        if not supportStr.find('Terasic HAN Pilot') ==-1 :
            print('The Terasic HAN Pilot Board is not supported!')
            sys.exit()

    print('This demo writes a String over COM1 and checks that the data is received again')
    print('Connect RXD and TXD with a juper wire together')
    print('Standard/Nano')
    print(' 1/D0 - TXD  ---->')
    print('                 |')
    print('                 |')
    print(' 2/D1 - RXD <----')
    tmp = input('Press enter to countinue\n')
    

    for var in range(TEST_DURATIONS):
        print('Sample: '+str(var)+'/'+str(TEST_DURATIONS))

        # Open UART1 with Baud 9600 and timeout after 1sec 
        ser = serial.Serial('/dev/ttyS1',9600, timeout=1 )

        # Write a ASIC to a String
        # b -> tells Python to insert a String as ASCII
        ser.write(b'rsYocto SoC-FPGA \n')

        # Read the transmitted string over the null modem connection back
        line = ser.readline() 

        # Print the readout to the console 
        print('RXD: '+str(line))

        # Close the COM port 
        ser.close() 

        # trigger the Task in 50ms again
        time.sleep(.050)

        if(var != TEST_DURATIONS-1):
                # Delate last two console line 
                sys.stdout.write("\033[F")
                sys.stdout.write("\033[F")
        
print('End of demo...')






