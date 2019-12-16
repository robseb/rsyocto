'''
Created on 19.08.2019
Reading the ADXL345 Accelerometer

@author: Robin Sebastian
...      (https://github.com/robseb)
'''

import sys 
import os
import fcntl
import time

# the i²c Adress of the ADXL345
addr = 0x53

### ADXL345 Registers - Address - map  ###

ADXL345_DEVID = 0x00                   # static unique device ID (0xE5 = 229)
ADXL345_DEVID_ID    = 0xE5

ADXL345_POWER_CTL = 0x2D               #  Power-saving features control
ADXL345_POWER_CTL_START  = (1<< 3)     #  starts the Measure 

ADXL345_DATA_FORMAT = 0x31             # Data format register                                                 
ADXL345_DATA_FORMAT_RANGE_4G  = (1<< 0)             # data range: 4g
ADXL345_DATA_FORMAT_RANGE_8G  = (1<< 1)             # data range: 8g
ADXL345_DATA_FORMAT_RANGE_16G = (1<< 0) | (1<< 1)   # data range: 16g
                                                    # (default) : 2g
ADXL345_DATA_FORMAT_FULL_RES  = (1<<3 ) # sets the 10 bit full resulution mode
ADXL345_DATA_FORMAT_JUSTIFY = (1<<2)    #  selects left-justified (MSB) mode

ADXL345_DATAX0 = 0x32                   # x axsis low value register
ADXL345_DATAX1 = 0x33                   # x axsis high value register
ADXL345_DATAY0 = 0x34                   # y axsis low value register
ADXL345_DATAY1 = 0x35                   # y axsis high value register
ADXL345_DATAZ0 = 0x36                   # z axsis low value register
ADXL345_DATAZ1 = 0x37                   # z axsis high value register

if __name__ == '__main__':
    print("I2C ADXL345 G-Sensor Demo")
    
    ### open the onboard I²C-Bus 0 
    dev = os.open("/dev/i2c-0", os.O_RDWR)

    ### check if device is reachable
    if (fcntl.ioctl(dev, 0x0703, addr) < 0) :
        print("EROR:something went wrong!")
        print("Failed to acquire the ADXL345.\n")
        sys.exit()

    ### read the static unique ID
    rList =[ADXL345_DEVID]
    arr = bytearray(rList)
    # write the address to read to the slave
    os.write(dev,arr)
    # read the date of the address 
    id =os.read(dev,1)
    
    # Check the deive ID 
    # id[0] contains the actual value and removes suffix "\x"
    if ADXL345_DEVID_ID is not id[0]:
        print("EROR:the Device ID is wrong!")
        sys.exit()

    ## Enabling the 10bit high resulution mode with a range of 4g

    #     Register (address), 8bit data
    rList =[ADXL345_DATA_FORMAT,ADXL345_DATA_FORMAT_RANGE_4G |
    ADXL345_DATA_FORMAT_FULL_RES ]
    arr = bytearray(rList)
    # write the data to the i²c-device
    os.write(dev,arr)

    ## Enanble the measurement mode 
    #       Register (address), 8bit data
    rList =[ADXL345_POWER_CTL,ADXL345_POWER_CTL_START]
    arr = bytearray(rList)
    # write the data to the i²c-device
    os.write(dev,arr)

    ledOn =0
    row_val_x =[0,0]
    row_val_y =[0,0]
    row_val_z =[0,0]

    for var in range(50):

        ### read the x-axis values
        rList =[ADXL345_DATAX0]
        arr = bytearray(rList)
        os.write(dev,arr)
        row_val_x[0]=os.read(dev,1)

        rList =[ADXL345_DATAX1]
        arr = bytearray(rList)
        os.write(dev,arr)
        row_val_x[1] =os.read(dev,1)
        row = row_val_x[1][0]  & 3 # remove bit 2-7 

        # add the 8-bit values togther to a 10bit value 
        x = (row <<8) | row_val_x[0][0]

        ### read the y-axis values
        rList =[ADXL345_DATAY0]
        arr = bytearray(rList)
        os.write(dev,arr)
        row_val_y[0]=os.read(dev,1)

        rList =[ADXL345_DATAY1]
        arr = bytearray(rList)
        os.write(dev,arr)
        row_val_y[1] =os.read(dev,1)
        row = row_val_y[1][0]  & 3 # remove bit 2-7 

        # add the 8-bit values togther to a 10bit value 
        y = (row<<8) | row_val_y[0][0]

        ### read the z-axis values
        rList =[ADXL345_DATAZ0]
        arr = bytearray(rList)
        os.write(dev,arr)
        row_val_z[0]=os.read(dev,1)

        rList =[ADXL345_DATAZ1]
        arr = bytearray(rList)
        os.write(dev,arr)
        row_val_z[1] =os.read(dev,1)
        row = row_val_z[1][0]  & 3 # remove bit 2-7 

        # add the 8-bit values togther to a 10bit value 
        z = (row<<8) | row_val_z[0][0]

        # print the values 
       # print("x : "+str(x)+" y: "+str(y)+" z: "+str(z)) 
        print("X: %10d,  Y: %10d,  Z: %10d" % (x,y,z))


        # toogle the HPS LED
        ledOn = not ledOn
        os.system('echo '+str(100 if ledOn else 0)+' > /sys/class/leds/hps_led0/brightness')

        # wait 300ms
        time.sleep(.300)

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
    print('Ende...')
