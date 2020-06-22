#!/usr/bin/env python
# coding: utf-8
'''
@disc:   Counting the Seven Segment Display up
         Fast way over the virtual memory

@date:   22.06.2020
@device: Intel Cyclone V & Arria 10 SX
@author: Robin Sebastian
         (https://github.com/robseb)
         (git@robseb.de)
'''
import os
import time
import sys

# 
# This demo uses the python class "devmen" (https://github.com/kylemanna/pydevmem)
# be sure that this file is on the same directory 
#
import devmem

from time import sleep


# the HPS Lightweight HPS-to-FPGA bridge address offset
HPS_LW_ADRS_OFFSET = 0xFF200000 

# The offset address of the seven segment Display Controller
#                       DE10 Standard, , HAN Pilot 
SEVENSIG_ADDRES_OFFSET = [0x038,0x0,0x008]

ledValue = 0

# Selected maximum countable value for the SevenSig Display  
SEVENSIG_MAX_VALUE = [2000,0,254]
# Delay in ms between every count 
DELAY_DURATION= [0.01,0,0.050]

if __name__ == '__main__':
    print('Counting a number on the Seven Segment Display on the DE10-Standard with virtual Memory!\n')

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

    # Open the memory access to the Lightweight HPS-to-FPGA bridge
    #                  (Base address, byte len to accesses, interface)
    de = devmem.DevMem(HPS_LW_ADRS_OFFSET, SEVENSIG_ADDRES_OFFSET[devboard]+1, "/dev/mem")

    for var in range(SEVENSIG_MAX_VALUE[devboard]):
        print('Sample: '+str(var)+'/'+str(SEVENSIG_MAX_VALUE[devboard]))
        
        # Count the LED value up
        if(ledValue < SEVENSIG_MAX_VALUE[devboard]):
            ledValue +=1
        else:
            ledValue =0

        # Write the LED value to FPGA GPIO Controller
        de.write(SEVENSIG_ADDRES_OFFSET[devboard], [ledValue])

        # Wait 
        time.sleep(DELAY_DURATION[devboard])

        # Delate last console line 
        sys.stdout.write("\033[F")

    # Reset the Value
    ledValue = 0
    de.write(SEVENSIG_ADDRES_OFFSET[devboard], [ledValue])
print('End of demo...')
