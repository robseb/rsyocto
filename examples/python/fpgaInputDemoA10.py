#!/usr/bin/env python
# coding: utf-8

'''
@disc:   Reading the Key and Switches via the 
         Lightweight HPS-to-FPGA Bridge

@date:   03.11.2019
@device: Intel Arria 10 SX 
@author: Robin Sebastian
         (https://github.com/robseb)
'''
import os
import time
import sys

# 
# This demo uses the python class "devmen" (https://github.com/kylemanna/pydevmem)
# be sure that this file is on the same directory 
#
import devmem

# Demo duration  
TEST_DURATIONS  =50


# The Lightweight HPS-to-FPGA bridge base address offset
HPS_LW_ADRS_OFFSET = 0xFF200000 

# The offset address input devices 
HPS_LW_ADRS_OFFSET_SYSID = 0x140 # const system id with 0xCADEABCD
HPS_LW_ADRS_OFFSET_KEYS  = 0x100 # 2 key button input values 
HPS_LW_ADRS_OFFSET_SWI   = 0x110    # 2 switch button input values

ledValue = 0

HPS_FPGA_SYSID = 0xCADEABCD

if __name__ == '__main__':
    print("FPGA LED Bin Counter (HPS-Bridge Demo)")

    # Open the memory access to the Lightweight HPS-to-FPGA Bridge 
    #                  (Base address, byte len to acceses, interface)
    de = devmem.DevMem(HPS_LW_ADRS_OFFSET, HPS_LW_ADRS_OFFSET_SYSID+1, "/dev/mem")

    # Read the system ID 
    sysID  = de.read(HPS_LW_ADRS_OFFSET_SYSID,1)
    print("The system ID is")
    print(str(sysID))

    for var in range(TEST_DURATIONS):

        print('SWI: ')
        sw  = de.read(HPS_LW_ADRS_OFFSET_SWI,1)
        print(str(sw))
        print('KEY: ')
        sw  = de.read(HPS_LW_ADRS_OFFSET_KEYS,1)
        print(str(sw))

        # wait 200ms 
        time.sleep(.20)


print('End of demo...')