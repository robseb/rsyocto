#!/usr/bin/env python
# coding: utf-8

'''
@disc:  ADC readout Sensor Test (Analog Devices LTC2308)
        Fast way over the virtual memory
           
@date:   21.01.2020
@device: Intel Cyclone V 
@author: Robin Sebastian
         (https://github.com/robseb)
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

# Demo duration  
TEST_DURATIONS  =30

# the Lightweight HPS-to-FPGA Bus base address offset
HPS_LW_ADRS_OFFSET = 0xFF200000 

# LTC2308 Address offset
ADC_ADDRES_OFFSET = 0x40

# Register set of the LTC2308
ADC_CMD_REG_OFFSET  = 0x0
ADC_DATA_REG_OFFSET = 0x4

#### Used ADC Channel 
# Select here the ADC Channel for this Demo 
ADC_CH = 1
##

### FIFO Convention Data Size for average calculation
FIFO_SIZE = 255 # MAX=1024 

VALUE_OR_VOLTAGE_OUTPUT = 0 # 1: Raw Value output | 0: Volage

if __name__ == '__main__':
    print("ADC readout Demo for LTC2308 ADC with Channel "+str(ADC_CH))

    # The ADC is only supported with rsYocto Version 1.031 or later
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
            print("Warning: Failed to read rsYocto Version")

    if not versionNo > 1.031:
        print("Error: The ADC is only supported with rsYocto Version 1.031 or later ")
        print(" This Version is: "+versionStr)
        sys.exit()

    # open the memory Access to the Lightweight HPS-to-FPGA bridge
    #                  (Base address, byte length to acceses, interface)
    de = devmem.DevMem(HPS_LW_ADRS_OFFSET, ADC_ADDRES_OFFSET+0x8, "/dev/mem")
    
    # Enter test loop
    for var in range(TEST_DURATIONS):

        # Set meassure number for ADC convert
        de.write(ADC_ADDRES_OFFSET+ADC_DATA_REG_OFFSET,[FIFO_SIZE])
        # Enable the convention with CH0 
        de.write(ADC_ADDRES_OFFSET+ADC_CMD_REG_OFFSET, [(ADC_CH <<1) | 0x00])
        de.write(ADC_ADDRES_OFFSET+ADC_CMD_REG_OFFSET, [(ADC_CH <<1) | 0x01])
        de.write(ADC_ADDRES_OFFSET+ADC_CMD_REG_OFFSET, [(ADC_CH <<1) | 0x00])
        
        timeout = 300 #ms
        # Wait untis convention is done or timeout
        while (not(timeout == 0)):
            
            if(de.read(ADC_ADDRES_OFFSET+ADC_CMD_REG_OFFSET,1)[0] & (1<<0)): 
                break

            timeout = timeout -1
            time.sleep(.001) # delay 1ms 

        # Avarage FIFO values
        rawValue = 0
        for i in range(FIFO_SIZE): 
            rawValue = rawValue+ (de.read(ADC_ADDRES_OFFSET+ADC_DATA_REG_OFFSET,1))[0]
        
        value = rawValue / FIFO_SIZE

        if VALUE_OR_VOLTAGE_OUTPUT:
            value = round(value,2)
            print("ADC AVG: "+str(value))
        else: 
            # Convert ADC Value to Volage
            volage = round(value/1000,2)
            print("U AVG: "+str(volage)+"V")

        time.sleep(.2) # 200ms delay

print('End of demo...')