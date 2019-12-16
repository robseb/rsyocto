'''
Created on 21.03.2019
Counting a number on the Seven Sigment Display
on the Terasic DE10-Standard Board

@author: Robin Sebastian
...      (https://github.com/robseb)
'''

import os
import time
import sys

if __name__ == '__main__':
    print('Counting a number on the Seven Sigment Display on the DE10-Standard !\n')

    # check that the runing board the a DE10-Standard 
    de10StDetected = False

    if os.path.isfile("/usr/rsyocto/suppBoard.txt"):
        supportStr = ""
        with open("/usr/rsyocto/suppBoard.txt", "r") as f:
            supportStr = f.read()
        if not supportStr.find('Terasic DE10 Standard') ==-1 :
            de10StDetected = True

    if not de10StDetected :
        print("Error: This script works only with a Terasic DE10 Standard Board!")
        sys.exit()

    # Count the SevenSigment Display 
    for count in range(1024):
        os.system('FPGA-writeBridge -lw 38 -h '+ str(count) +' -b')

    # Reset the Display value
    os.system('FPGA-writeBridge -lw 38 0 -b')
    print('End...')