#!/usr/bin/env python
# coding: utf-8
'''
@disc:   Counting a number on the Seven Segment Display
         on the Terasic DE10-Standard Board with a 
         rstools shell command

@date:   18.09.2019
@device: Intel Cyclone V & Intel Arria 10 SX
@author: Robin Sebastian
         (https://github.com/robseb)
'''

import os
import time
import sys

# Selected maximum countable value for the SevenSig Display  
SEVENSIG_MAX_VALUE = [2000,0,254]

if __name__ == '__main__':
    print('Counting a number on the Seven Segment Display with a Linux shell command!\n')

    # Check that the running board is a Terasic DE10-Standard-  or Han Pilot Development Board  
    # Used development board 
    devboard = 1 # 0: DE10 Standard | 1: DE10 Nano | 2: Han Pilot 

    # The Board name for the image is located here: "/usr/rsyocto/suppBoard.txt"
    if os.path.isfile("/usr/rsyocto/suppBoard.txt"):
        supportStr = ""
        with open("/usr/rsyocto/suppBoard.txt", "r") as f:
            supportStr = f.read()
        if not supportStr.find('Terasic DE10 Standard') ==-1 :
            devboard = 0
        elif not supportStr.find('Terasic HAN Pilot') ==-1 :
            devboard = 2

    if devboard==1:
        print("Error: This script only works with a Terasic DE10 Standard- or Han Pilot Board!")
        sys.exit()

    # Count the Seven Segment Display with a rstools shell command
    for count in range(SEVENSIG_MAX_VALUE[devboard]):
        print('Sample: '+str(count)+'/'+str(SEVENSIG_MAX_VALUE[devboard]))

        if(devboard==2):
            os.system('FPGA-writeBridge -lw 8 -h '+ str(count) +' -b')
        else: # DE10 Standard Board 
            os.system('FPGA-writeBridge -lw 38 -h '+ str(count) +' -b')

        # Delate last console line 
        sys.stdout.write("\033[F")
    # Reset the Display value
    if(devboard==2):
        os.system('FPGA-writeBridge -lw 8 0 -b')
    else:# DE10 Standard Board 
        os.system('FPGA-writeBridge -lw 38 0 -b')

    print('End...')