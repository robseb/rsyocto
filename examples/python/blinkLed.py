'''
Created on 21.03.2019
Blinking HPS LED Demo 

@author: Robin Sebastian
...      (https://github.com/robseb)
'''
import os
import time

if __name__ == '__main__':
    print('Hello from a Python Application runing o a SoC-FPGA !\n')
    print('Blinky LED Example')
    for var in range(20):
        print("turn: ",var)
        # Trun the HPS LED 0 ON 
        os.system("echo 100 > /sys/class/leds/hps_led0/brightness")
        time.sleep(.200)
        # Trun the HPS LED 0 OFF
        os.system("echo 0 > /sys/class/leds/hps_led0/brightness")
        time.sleep(.500)
    print('End...')