#!/usr/bin/env python
# coding: utf-8

'''
@disc:   Toggling a FPGA LED with a rstools Linux
         Shell command

@date:   21.10.2019
@device: Intel Cyclone V 
@author: Robin Sebastian
         (https://github.com/robseb)
'''
import os
import time

if __name__ == '__main__':
    print('Toggling the FPGA LED[7] with a Shell command\n')
    # Turn all FPGA LEDs Off
    os.system("FPGA-writeBridge -lw 20 0 -b")
    for var in range(20):
        print("turn: ",var)
        # Turn the FPGA LED 7 ON 
        os.system("FPGA-writeBridge -lw 20 -b 7 1 -b")
        time.sleep(.50)
        # Turn the FPGA LED 7 ON 
        os.system("FPGA-writeBridge -lw 20 -b 7 0 -b")
        # Wait for 50ms
        time.sleep(.50)
    print('End of demo...')