#!/usr/bin/env python
# coding: utf-8
'''
@disc:   Counting the FPGA LEDs up
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
# be sure that this file is same directory 
#
import devmem

# demo duration  
TEST_DURATIONS  =16


from time import sleep


# The Lightweight HPS-to-FPGA base address offset
HPS_LW_ADRS_OFFSET = 0xFF200000 

# The offset address of the LED GPIO Controller
LEDS_ADDRES_OFFSET = 0x130

ledValue = 0

if __name__ == '__main__':
    print("FPGA LED Bin Counter for Arria 10 SX (HPS-Bridge Demo)")

    # open the memory access to the Lightweight HPS-to-FPGA bridge
    #                  (Base address, byte len to acceses, interface)
    de = devmem.DevMem(HPS_LW_ADRS_OFFSET, 0x121, "/dev/mem")

    for var in range(TEST_DURATIONS):

        # count the LED value up
        if(ledValue < 2):
            ledValue +=1
        else:
            ledValue =0

        # write the LED value to FPGA GPIO Controller
        de.write(LEDS_ADDRES_OFFSET, [ledValue])

        # wait 200ms 
        time.sleep(.080)

print('End of demo...')
