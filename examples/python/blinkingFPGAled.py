'''
Created on 21.03.2019
Blinking FPGA LED 

@author: Robin Sebastian
...      (https://github.com/robseb)
'''
import os
import time

if __name__ == '__main__':
    print('Toogling the FPGA LED[7] !\n')
    # Turn all FPGA LEDs Off
    os.system("FPGA-writeBridge -lw 20 0 -b")
    for var in range(20):
        print("turn: ",var)
        # Trun the FPGA LED 8 ON 
        os.system("FPGA-writeBridge -lw 20 -b 8 1 -b")
        time.sleep(.50)
        # Trun the FPGA LED 8 OFF
        os.system("FPGA-writeBridge -lw 20 -b 8 0 -b")
        time.sleep(.50)
    print('End...')
