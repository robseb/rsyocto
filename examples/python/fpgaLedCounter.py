#!/usr/bin/env python
# coding: utf-8

'''
@disc:  Counting the FPGA LEDs up
        Fast way over the virtual memory
           
@date:   22.06.2020
@device: Intel Cyclone V & Intel Arria 10 SX
@author: Robin Sebastian
         (https://github.com/robseb)
         (git@robseb.de)
'''
import os
import time

# 
# This demo uses the python class "devmen" (https://github.com/kylemanna/pydevmem)
# be sure that this file is on the same directory 
#
import devmem

# 
# This demo uses the python pip package "processbar2" please install this package with the following command:
#   pip3 install  progressbar2
#

try:
    import progressbar
except ImportError:
    print('This Demo uses the Python pip package "processbar2"')
    print('Run following command to install it:')
    print('pip3 install  progressbar2')

# Used development board 
devboard =0 # 0: DE10 Standard | 1: DE10 Nano | 2: Han Pilot 


# the HPS Lightweight HPS-to-FPGA bridge base address
HPS_LW_ADRS_OFFSET = 0xFF200000 

# the offset address of the LED GPIO Controller
#                     CY5  ,CY5, A10
LEDS_ADDRES_OFFSET = [0x20,0x20,0x130]
#                   DE10ST,DE10NA, HAN
LED_MAX_COUNT_VALUE = [255,1024,4]

ledValue = 0

from time import sleep
bar = progressbar.ProgressBar(maxval=LED_MAX_COUNT_VALUE[devboard], \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])


if __name__ == '__main__':
    print("FPGA LED Bin Counter (HPS-Bridge Demo) - Faster way")

     # Read the name of the used development board 
    # The Board name for the image is located here: "/usr/rsyocto/suppBoard.txt"
    if os.path.isfile("/usr/rsyocto/suppBoard.txt"):
        supportStr = ""
        with open("/usr/rsyocto/suppBoard.txt", "r") as f:
            supportStr = f.read()
        if not supportStr.find('Terasic DE10 Nano') ==-1 :
            devboard = 1
        elif not supportStr.find('Terasic HAN Pilot') ==-1 :
            devboard = 2
        print('Your dev board: '+supportStr)

    # open the memory Access to the Lightweight HPS-to-FPGA bridge
    #                  (Base address, byte length to acceses, interface)
    de = devmem.DevMem(HPS_LW_ADRS_OFFSET, LEDS_ADDRES_OFFSET[devboard], "/dev/mem")

    # start the process bar 
    bar.start()
    
    for var in range(LED_MAX_COUNT_VALUE[devboard]):

        # count the LED value up
        if(ledValue < LED_MAX_COUNT_VALUE[devboard]):
            ledValue +=1
        else:
            ledValue =0

        # write the LED value to FPGA GPIO Controller
        de.write(LEDS_ADDRES_OFFSET[devboard], [ledValue])

        # update the bar status
        bar.update(var)

        # wait 100ms 
        time.sleep(.10)

    bar.finish()

# Turn all LEDs off
de.write(LEDS_ADDRES_OFFSET[devboard], [0])
print('End of demo...')