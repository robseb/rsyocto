#!/usr/bin/env python
# coding: utf-8

'''
@disc:   Reading the Key and Switches via the 
         LightWight HPS2FPGA Bridge

@date:   19.10.2019
@device: Intel Cyclone V 
@author: Robin Sebastian
         (https://github.com/robseb)
'''
import os
import time
import sys

# 
# This demo uses the python class "devmen" (https://github.com/kylemanna/pydevmem)
# be sure that this file is in the same directory 
#
import devmem


# the Lightweight HPS-to-FPGA Bus base address offset
HPS_LW_ADRS_OFFSET = 0xFF200000 

# the offset addresses of the input devices 
HPS_LW_ADRS_OFFSET_SYSID = 0x30 # const system id with 0xCADEACDC
HPS_LW_ADRS_OFFSET_KEYS  = 0x10 # 2 key button input values 
HPS_LW_ADRS_OFFSET_SWI   = 0    # 4 switches input values

ledValue = 0

HPS_FPGA_SYSID = 0xCADEACDC

if __name__ == '__main__':
    print("FPGA LED Bin Counter (HPS-Bridge Demo)")

    # Open the memory access to the Lightweight HPS-to- FPGA Bus
    #                  (Base address, byte length to acceses, interface)
    de = devmem.DevMem(HPS_LW_ADRS_OFFSET, HPS_LW_ADRS_OFFSET_SYSID+1, "/dev/mem")

    # Read the system ID 
    sysID  = de.read(HPS_LW_ADRS_OFFSET_SYSID,1)
    print("The system ID is:"+str(sysID.data))

    # Read the Key Buttons
    pb  = de.read(HPS_LW_ADRS_OFFSET_KEYS,1)
    print('The value of the push buttons: ')
    print(str(pb))

    # Read the switches 
    sw  = de.read(HPS_LW_ADRS_OFFSET_SWI,1)
    print('The value of the switches: ')
    print(str(sw))


print('End of demo...')