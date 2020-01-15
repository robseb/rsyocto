#!/usr/bin/env python
# coding: utf-8
'''
@disc:   Counting the Seven Segment Display up
         Fast way over the virtual memory

@date:   19.10.2019
@device: Intel Arria 10 SX
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
TEST_DURATIONS  =256


from time import sleep


# The HPS2FPGA AXI Bridge base address offset
HPS2FPGA_ADRS_OFFSET = 0xc0000000 

# The offset address of the seven segment Display Controller
SEVENSIG_ADDRES_OFFSET = 0x008

ledValue = 0

if __name__ == '__main__':
    print("FPGA LED Bin Counter for Arria 10 SX (HPS-Bridge Demo)")

    # Open the memory access to the AXI HPS2FPGA Bus
    #                  (Base address, byte len to acceses, interface)
    de = devmem.DevMem(HPS2FPGA_ADRS_OFFSET, 0x012, "/dev/mem")

    for var in range(TEST_DURATIONS):

        # Count the LED value up
        if(ledValue < 0xFF):
            ledValue +=1
        else:
            ledValue =0

        # Write the LED value to FPGA GPIO Controller
        de.write(SEVENSIG_ADDRES_OFFSET, [ledValue])

        # Wait 20ms 
        time.sleep(.020)

    # Reset the value
    ledValue = 0
    de.write(SEVENSIG_ADDRES_OFFSET, [ledValue])
print('End of demo...')
