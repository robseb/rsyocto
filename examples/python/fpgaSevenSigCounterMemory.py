#!/usr/bin/env python
# coding: utf-8
'''
@disc:   Counting the Seven Segment Display up
         Fast way over the virtual memory

@date:   19.10.2019
@device: Intel Cyclone V 
@author: Robin Sebastian
         (https://github.com/robseb)
'''
import os
import time

# 
# This demo uses the python class "devmen" (https://github.com/kylemanna/pydevmem)
# be sure that this file is on the same directory 
#
import devmem

# Demo duration  
TEST_DURATIONS  =4096


from time import sleep


# the HPS Lightweight HPS-to-FPGA bridge address offset
HPS_LW_ADRS_OFFSET = 0xFF200000 

# The offset address of the seven segment Display Controller
SEVENSIG_ADDRES_OFFSET = 0x038

ledValue = 0

if __name__ == '__main__':
    print('Counting a number on the Seven Segment Display on the DE10-Standard with virtual Memory!\n')

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
        print("Error: This script works only with a Terasic DE10 Standard Board!")
        sys.exit()

    # Open the memory access to the Lightweight HPS-to-FPGA bridge
    #                  (Base address, byte len to accesses, interface)
    de = devmem.DevMem(HPS_LW_ADRS_OFFSET, 0x042, "/dev/mem")

    for var in range(TEST_DURATIONS):

        # Count the LED value up
        if(ledValue < 0xFF):
            ledValue +=1
        else:
            ledValue =0

        # Write the LED value to FPGA GPIO Controller
        de.write(SEVENSIG_ADDRES_OFFSET, [ledValue])

        # Wait 10ms 
        time.sleep(.010)

    # Reset the Value
    ledValue = 0
    de.write(SEVENSIG_ADDRES_OFFSET, [ledValue])
print('End of demo...')
