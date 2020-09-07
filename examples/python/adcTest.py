#!/usr/bin/env python
# coding: utf-8

'''
@disc:  ADC readout Sensor Test (Analog Devices LTC2308)
        Fast way over the virtual memory
           
@date:   04.09.2020
@device: Intel Cyclone V 
@author: Robin Sebastian
         (https://github.com/robseb)
         (git@robseb.de)
'''
import os
import time
import math
import sys
# 
# This demo uses the python class "devmen" (https://github.com/kylemanna/pydevmem)
# be sure that this file is on the same directory 
#
import devmem

#### Used ADC Channel 
# Select here the ADC Channel for this Demo 
ADC_CH = 0

# Demo duration  
TEST_DURATIONS  =100

# The Lightweight HPS-to-FPGA Bus base address offset
HPS_LW_ADRS_OFFSET = 0xFF200000 

# LTC2308 Address offset
ADC_ADDRES_OFFSET = 0x40

#
##### Register Set of the Intel University program Analog Devices LTC2308 Soft-IP
#

# ADC data register no for channel (read only)
ADC_REG_OFF_DATACH  = ADC_CH*4

# ADC Control register no (write only)
ADC_REG_OFF_UPDATE      =  0 # Update the converted values
ADC_REG_OFF_AUTO_UPDATE =  4 # Enables or disables auto-updating

# The number of available number 
ADC_REG_RANGE=           28

if __name__ == '__main__':
    print("ADC readout Demo for LTC2308 ADC with Channel "+str(ADC_CH))

    # Read the name of the used development board 
    #-> Only the Terasic DE10 Standard and Nano Boards are allowed!
    # The Board name for the image is located here: "/usr/rsyocto/suppBoard.txt"
    if os.path.isfile("/usr/rsyocto/suppBoard.txt"):
        supportStr = ""
        with open("/usr/rsyocto/suppBoard.txt", "r") as f:
            supportStr = f.read()
        if not supportStr.find('Terasic HAN Pilot') ==-1 :
            print('The Terasic HAN Pilot Board has no LTC2308 and is not supported!')
            sys.exit()

    # The ADC is only supported with rsyocto Version 1.04 or later
    versionNo = 0
    # The rsYocto Version Number is located here: "/usr/rsyocto/version.txt"
    if os.path.isfile("/usr/rsyocto/version.txt"):
        versionStr = ""
        with open("/usr/rsyocto/version.txt", "r") as f:
            versionStr = f.read()
        # Convert String to int
        try: 
            versionNo = float(versionStr)
        except ValueError:
            print("Warning: Failed to read rsyocto Version")

    if not versionNo >= 1.04:
        print("Error: The ADC is only supported with rsyocto Version 1.04 or later ")
        print(" This Version is: "+versionStr)
        sys.exit()

    # open the memory Access to the Lightweight HPS-to-FPGA bridge
    #                  (Base address, byte length to acceses, interface)
    de = devmem.DevMem(HPS_LW_ADRS_OFFSET, ADC_ADDRES_OFFSET+ADC_REG_RANGE, "/dev/mem")
    
    # Enable the auto conversion update mode 
    de.write(ADC_ADDRES_OFFSET+ADC_REG_OFF_UPDATE,[1])

    print('Reading the current ADC value ...')

    # Enter test loop
    for var in range(TEST_DURATIONS):

        print('Sample: '+str(var)+'/'+str(TEST_DURATIONS))

        # Read the ADC Value from the selected Channel
        raw_value = (de.read(ADC_ADDRES_OFFSET+ADC_REG_OFF_DATACH,1))[0]
        # Remove Bit 12-31 (Bit 15 is always high)
        raw_value = (raw_value & 0x00000FFF)
        print("-> ADC CH"+str(ADC_CH)+': ' +str(raw_value))

        # Convert ADC Value to Volage
        u_value = round((raw_value*5)/4095,4)
        print("-> U   AVG: "+str(u_value)+"V")

        time.sleep(.2) # 200ms delay

        if var != TEST_DURATIONS-1:
            # Delate last 3 console line 
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[F")

    # Disable the ADC again
    de.write(ADC_ADDRES_OFFSET+ADC_REG_OFF_UPDATE,[0])

print('End of demo...')
