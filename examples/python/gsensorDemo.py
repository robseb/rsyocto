#!/usr/bin/env python
# coding: utf-8

'''
@disc:   Reading the ADXL345 Accelerometer 
         over the i2c-Bus
         
@date:   22.06.2020
@device: Intel Cyclone V 
@author: Robin Sebastian
         (https://github.com/robseb)
         (git@robseb.de)
'''

import sys 
import os
import fcntl
import time

# The i²c Address of the ADXL345
addr = 0x53

### ADXL345 Registers - Address - map  ###

ADXL345_DEVID = 0x00                   # Static unique device ID (0xE5 = 229)
ADXL345_DEVID_ID    = 0xE5

ADXL345_POWER_CTL = 0x2D               #  Power-saving features control
ADXL345_POWER_CTL_START  = (1<< 3)     #  Starts the Measure 

ADXL345_DATA_FORMAT = 0x31             # Data format register                                                 
ADXL345_DATA_FORMAT_RANGE_4G  = (1<< 0)             # Data range: 4g
ADXL345_DATA_FORMAT_RANGE_8G  = (1<< 1)             # Data range: 8g
ADXL345_DATA_FORMAT_RANGE_16G = (1<< 0) | (1<< 1)   # Data range: 16g
                                                    # (default) : 2g
ADXL345_DATA_FORMAT_FULL_RES  = (1<<3 ) # Sets the 10 bit full resolution mode
ADXL345_DATA_FORMAT_JUSTIFY = (1<<2)    #  selects left-justified (MSB) mode

ADXL345_DATAX0 = 0x32                   # x Axis low value register
ADXL345_DATAX1 = 0x33                   # x Axis high value register
ADXL345_DATAY0 = 0x34                   # y Axis low value register
ADXL345_DATAY1 = 0x35                   # y Axis high value register
ADXL345_DATAZ0 = 0x36                   # z Axis low value register
ADXL345_DATAZ1 = 0x37                   # z Axis high value register

# Demo duration 
TEST_DURATIONS = 100

if __name__ == '__main__':
    print("I2C ADXL345 G-Sensor Demo")
    
    # Read the name of the used development board 
    #-> Only the Terasic DE10 Standard and Nano Boards are allowed!
    # The Board name for the image is located here: "/usr/rsyocto/suppBoard.txt"
    if os.path.isfile("/usr/rsyocto/suppBoard.txt"):
        supportStr = ""
        with open("/usr/rsyocto/suppBoard.txt", "r") as f:
            supportStr = f.read()
        if not supportStr.find('Terasic HAN Pilot') ==-1 :
            print('The Terasic HAN Pilot Board has no ADXL345 and is not supported!')
            sys.exit()


    ### Open the onboard I²C-Bus 0 
    dev = os.open("/dev/i2c-0", os.O_RDWR)

    ### Check if the device is reachable
    if (fcntl.ioctl(dev, 0x0703, addr) < 0) :
        print("EROR:something went wrong!")
        print("Failed to acquire the ADXL345.\n")
        sys.exit()

    ### Read the static unique ID
    rList =[ADXL345_DEVID]
    arr = bytearray(rList)
    # Write the address to read to the slave
    os.write(dev,arr)
    # Read the date of the address 
    id =os.read(dev,1)
    
    # Check the device ID of the ADXL345
    # id[0] contains the actual value and removes suffix "\x"
    if ADXL345_DEVID_ID is not id[0]:
        print("ERROR: The Device ID is wrong!")
        sys.exit()

    ## Enabling the 10bit high resolution mode with a range of 4g

    # Register (address), 8bit data
    rList =[ADXL345_DATA_FORMAT,ADXL345_DATA_FORMAT_RANGE_4G |
    ADXL345_DATA_FORMAT_FULL_RES ]
    arr = bytearray(rList)
    # write the data to the i²c-device
    os.write(dev,arr)

    ## Enable the measurement mode 
    #  Register (address), 8bit data
    rList =[ADXL345_POWER_CTL,ADXL345_POWER_CTL_START]
    arr = bytearray(rList)
    # Write the data to the i²c-device
    os.write(dev,arr)

    ledOn =0
    row_val_x =[0,0]
    row_val_y =[0,0]
    row_val_z =[0,0]

    for var in range(TEST_DURATIONS):
        print('Sample: '+str(var)+'/'+str(TEST_DURATIONS))
        ### Read the x-axis values
        rList =[ADXL345_DATAX0]
        arr = bytearray(rList)
        os.write(dev,arr)
        row_val_x[0]=os.read(dev,1)

        rList =[ADXL345_DATAX1]
        arr = bytearray(rList)
        os.write(dev,arr)
        row_val_x[1] =os.read(dev,1)
        row = row_val_x[1][0]  & 3 # remove bit 2-7 

        # Add the 8-bit values together to a 10bit value 
        x = (row <<8) | row_val_x[0][0]

        ### Read the y-axis values
        rList =[ADXL345_DATAY0]
        arr = bytearray(rList)
        os.write(dev,arr)
        row_val_y[0]=os.read(dev,1)

        rList =[ADXL345_DATAY1]
        arr = bytearray(rList)
        os.write(dev,arr)
        row_val_y[1] =os.read(dev,1)
        row = row_val_y[1][0]  & 3 # remove bit 2-7 

        # Add the 8-bit values together to a 10bit value 
        y = (row<<8) | row_val_y[0][0]

        ### Read the z-axis values
        rList =[ADXL345_DATAZ0]
        arr = bytearray(rList)
        os.write(dev,arr)
        row_val_z[0]=os.read(dev,1)

        rList =[ADXL345_DATAZ1]
        arr = bytearray(rList)
        os.write(dev,arr)
        row_val_z[1] =os.read(dev,1)
        row = row_val_z[1][0]  & 3 # remove bit 2-7 

        # Add the 8-bit values together to a 10bit value 
        z = (row<<8) | row_val_z[0][0]

        # print the values 
        print("X: %10d,  Y: %10d,  Z: %10d" % (x,y,z))


        # tootle the HPS LED during readout
        ledOn = not ledOn
        os.system('echo '+str(100 if ledOn else 0)+' > /sys/class/leds/hps_led0/brightness')

        # Wait 300ms
        time.sleep(.300)

        if(var != TEST_DURATIONS-1):
            # Delate last two console line 
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[F")
        

    ## Disable the measurement mode 
    #       Register (address), 8bit data
    rList =[ADXL345_POWER_CTL,0]
    arr = bytearray(rList)
    # write the data to the i²c-device
    os.write(dev,arr)

    # close the i2c channel 
    time.sleep(.100)

    os.close(dev)
    os.system('echo 0 > /sys/class/leds/hps_led0/brightness')
    print('End of demo...')
