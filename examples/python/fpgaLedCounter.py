#!/usr/bin/env python
# coding: utf-8

'''
@disc:  Counting the FPGA LEDs up
        Fast way over the virtual memory
           
@date:   16.09.2019
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
TEST_DURATIONS  =300

# 
# This demo uses the python pip package "processbar2" please install this package with the following command:
#   pip install  progressbar2
#

import progressbar
from time import sleep
bar = progressbar.ProgressBar(maxval=TEST_DURATIONS, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])

# the HPS Lightweight HPS-to-FPGA bridge base address
HPS_LW_ADRS_OFFSET = 0xFF200000 

# the offset address of the LED GPIO Controller
LEDS_ADDRES_OFFSET = 0x20

ledValue = 0

if __name__ == '__main__':
    print("FPGA LED Bin Counter (HPS-Bridge Demo) - Faster way")

    # open the memory Access to the Lightweight HPS-to-FPGA bridge
    #                  (Base address, byte length to acceses, interface)
    de = devmem.DevMem(HPS_LW_ADRS_OFFSET, 0x21, "/dev/mem")

    # start the process bar 
    bar.start()
    
    for var in range(TEST_DURATIONS):

        # count the LED value up
        if(ledValue < 255):
            ledValue +=1
        else:
            ledValue =0

        # write the LED value to FPGA GPIO Controller
        de.write(LEDS_ADDRES_OFFSET, [ledValue])

        # update the bar status
        bar.update(var)

        # wait 200ms 
        time.sleep(.020)

    bar.finish()

print('End of demo...')