#!/usr/bin/env python
# coding: utf-8

'''
@disc:   Reading the Key and Switches via the 
         LightWight HPS2FPGA Bridge

@date:   22.06.2020
@device: Intel Cyclone V 
@author: Robin Sebastian
         (https://github.com/robseb)
         (git@robseb.de)
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
#                           CY5 , A10
HPS_LW_ADRS_OFFSET_SYSID = [0x30,0x140] # const system id with 0xCADEACDC
HPS_LW_ADRS_OFFSET_KEYS  = [0x10,0x100] # 2 key button input values 
HPS_LW_ADRS_OFFSET_SWI   = [0x00,0x110] # 4 switches input values
HPS_FPGA_SYSID           = [0xCAFEACDC,0xCAFEACDC]     # ID of the SysID IP
ledValue = 0

 # The FPGA family used for this demo
Fpgafamily =0 # 0 : Cyclone V | 1: Arria 10 SX

# Demo duration 
TEST_DURATIONS = 100

if __name__ == '__main__':
    print("FPGA LED Bin Counter (HPS-Bridge Demo)")
    
    # Read the name of the used development board 
    # The Board name for the image is located here: "/usr/rsyocto/suppBoard.txt"
    if os.path.isfile("/usr/rsyocto/suppBoard.txt"):
        supportStr = ""
        with open("/usr/rsyocto/suppBoard.txt", "r") as f:
            supportStr = f.read()
        if not supportStr.find('Terasic HAN Pilot') ==-1 :
            Fpgafamily = 1
        print('Your dev board: '+supportStr)

    # Open the memory access to the Lightweight HPS-to-FPGA Bridge
    #                  (Base address, byte length to acceses, interface)
    de = devmem.DevMem(HPS_LW_ADRS_OFFSET, HPS_LW_ADRS_OFFSET_SYSID[Fpgafamily]+1, "/dev/mem")

    # Read the system ID 
    sysIDraw  = de.read(HPS_LW_ADRS_OFFSET_SYSID[Fpgafamily],1)
    sysID  = sysIDraw.data[0]

    print("The system ID is: "+hex(sysID))
    # Check that the ID os vailed
    if sysID == HPS_FPGA_SYSID[Fpgafamily]:
        print('The system ID is vailed!')
    else:
        print('The system ID is not vailed!')

    print('Reading the FPGA Buttons and Swiches')
    for var in range(TEST_DURATIONS):
        print('Sample: '+str(var)+'/'+str(TEST_DURATIONS))

        # Read the Key Buttons
        pb  = de.read(HPS_LW_ADRS_OFFSET_KEYS[Fpgafamily],1)
        print('Push Buttons: '+str(pb)+' 0b'+bin(pb.data[0]))

        # Read the switches 
        sw  = de.read(HPS_LW_ADRS_OFFSET_SWI[Fpgafamily],1)
        print('Swicthes:  '+str(sw)+' 0b'+bin(sw.data[0]))

        # Wait for 100ms
        time.sleep(.100)

        if var != TEST_DURATIONS-1:
            # Delate last 3 console line 
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[F")


print('End of demo...')