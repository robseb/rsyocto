#!/usr/bin/env python
# coding: utf-8
'''
@disc:   Counting a number on the Seven Segment Display
         on the Terasic DE10-Standard Board with a 
         rstools shell command

@date:   18.09.2019
@device: Intel Cyclone V
@author: Robin Sebastian
         (https://github.com/robseb)
'''

import os
import time
import sys

if __name__ == '__main__':
    print('Counting a number on the Seven Segment Display on the DE10-Standard with a shell command!\n')

    # Check that the running board is a Terasic DE10-Standard  
    de10StDetected = False

    # The Board name for the image is located here: "/usr/rsyocto/suppBoard.txt"
    if os.path.isfile("/usr/rsyocto/suppBoard.txt"):
        supportStr = ""
        with open("/usr/rsyocto/suppBoard.txt", "r") as f:
            supportStr = f.read()
        if not supportStr.find('Terasic DE10 Standard') ==-1 :
            de10StDetected = True

    if not de10StDetected :
        print("Error: This script only works with a Terasic DE10 Standard Board!")
        sys.exit()

    # Count the Seven Segment Display with a rstools shell command
    for count in range(120):
        os.system('FPGA-writeBridge -lw 38 -h '+ str(count) +' -b')

    # Reset the Display value
    os.system('FPGA-writeBridge -lw 38 0 -b')
    print('End...')