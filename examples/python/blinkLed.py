#!/usr/bin/env python
# coding: utf-8

'''
@disc: Toggling the HPS LED Demo 

@device: Intel Cyclone V 
@date:   23.09.2019
@author: Robin Sebastian
        (https://github.com/robseb)
'''
import os
import time

if __name__ == '__main__':
    print('Hello from a Python Application running on a SoC-FPGA !\n')
    print('Toggling HPS LED Example')
    # Repeat 20 times  
    for var in range(20):
        print("turn: ",var)
        # Turn the HPS LED 0 ON 
        os.system("echo 100 > /sys/class/leds/hps_led0/brightness")
        time.sleep(.200)
        # Turn the HPS LED 0 OFF
        os.system("echo 0 > /sys/class/leds/hps_led0/brightness")
        time.sleep(.500)
    print('End of demo...')