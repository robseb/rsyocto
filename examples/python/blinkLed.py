#!/usr/bin/env python
# coding: utf-8

'''
@disc: Toggling the HPS LED Demo 

@device: Intel Cyclone V & Intel Arria 10 SX
@date:   22.06.2020
@author: Robin Sebastian
        (https://github.com/robseb)
        (git@robseb.de)
'''
import os
import time
import sys

# Demo duration 
TEST_DURATIONS = 20
 

PATH_OF_HPS_LED_DRIVER = '/sys/class/leds/hps_led0/brightness'

if __name__ == '__main__':
    print('Hello from a Python Application running on a SoC-FPGA !\n')
    print('Toggling HPS LED Example')

    # Read the name of the used development board 
    # The Board name for the image is located here: "/usr/rsyocto/suppBoard.txt"
    if os.path.isfile("/usr/rsyocto/suppBoard.txt"):
        supportStr = ""
        with open("/usr/rsyocto/suppBoard.txt", "r") as f:
            supportStr = f.read()
        print('Your dev board: '+supportStr)
 
    for var in range(TEST_DURATIONS):
        print('Sample: '+str(var)+'/'+str(TEST_DURATIONS))

        # Turn the HPS LED 0 ON 
        os.system("echo 100 > "+PATH_OF_HPS_LED_DRIVER)
        time.sleep(.200)

        # Turn the HPS LED 0 OFF
        os.system("echo 0 > "+PATH_OF_HPS_LED_DRIVER)
        time.sleep(.500)

        # Delate last console line 
        sys.stdout.write("\033[F")

    # Turn the HPS LED 0 OFF
    os.system("echo 0 > /sys/class/leds/hps_led0/brightness")
    print('End of demo...')