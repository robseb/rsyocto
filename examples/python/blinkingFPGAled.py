#!/usr/bin/env python
# coding: utf-8

'''
@disc:   Toggling a FPGA LED with a rstools Linux
         Shell command

@date:   22.06.2020
@device: Intel Cyclone V 
@author: Robin Sebastian
         (https://github.com/robseb)
         (git@robseb.de)
'''
import os
import time
import sys

# Demo duration 
TEST_DURATIONS = 20

if __name__ == '__main__':
    print('Toggling the FPGA LED[7] with a Linux Shell command')
    # Turn all FPGA LEDs Off
    os.system("FPGA-writeBridge -lw 20 0 -b")
    for var in range(TEST_DURATIONS):
        print('Sample: '+str(var)+'/'+str(TEST_DURATIONS))

        # Turn the FPGA LED 7 ON 
        os.system("FPGA-writeBridge -lw 20 -b 7 1 -b")
        # Wait for 50ms
        time.sleep(.50)

        # Turn the FPGA LED 7 ON 
        os.system("FPGA-writeBridge -lw 20 -b 7 0 -b")
        # Wait for 50ms
        time.sleep(.50)

        # Delate last console line 
        sys.stdout.write("\033[F")
        
    # Turn all FPGA LEDs Off
    os.system("FPGA-writeBridge -lw 20 0 -b")

    print('End of demo...')