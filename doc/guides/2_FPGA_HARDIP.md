[back](1_Booting.md)

# Use of Hard IP, FPGA-IP and configuration of the FPGA fabric
This guide shows how simple it is to access FPGA IP,the I²C-, the UART-Bus, the SPI-Bus or the CAN-Bus.
Here are also commands given to change the FPGA fabric configuration.

## Toggling the HPS-LED of your Board
1. **Turn the HPS-LED on by typing in the console:**
    ```bash
    echo 100 > /sys/class/leds/hps_led0/brightness
    ```
2.  **Turn off the LED with:**
    ```bash
    echo 0 > /sys/class/leds/hps_led0/brightness
    ```
3. **To Toggle the LED is a *blinkLed.py* Python script pre-installed**
    ```bash 
   python3 blinkLed.py
    ```
4. **With `nano`- Editor it is possible to change the script**
    ```bash 
   nano blinkLed.py
   ```
   * Later a more pleasant way will be shown (Level 4) 
   
## Opening *rsyocto* Info Paper (*Platform block design*)
  * For every *rsYocto*-Version  a Information Shied on the Apache Webserver is installed
  * This Paper contains information's about the configuration of the FPGA IP and there Addresses and the used I/O Pins 
  * **Open it by typing the iPv4-Address of your Board into a Web browser**
  * Of cause it is possible  to install any other homepage
     * Insert the homepage files to: `/usr/share/apache2/default-site/htdocs`
     * Restart the Apache Server with following command:
        ````bash
            /etc/init.d/apache2 stop
            /etc/init.d/apache2 start
        ````
     *  Info Papers
        * [DE10 Standard](https://raw.githubusercontent.com/robseb/rsyocto/rsYocto-1.04/doc/symbols/DE10Std_pinout.png)
        * [DE10 Nano & DE0 Nano SoC](https://raw.githubusercontent.com/robseb/rsyocto/rsYocto-1.04/doc/symbols/DE10Nano_pinout.png)
        * [HAN Pilot (Arria 10)](https://raw.githubusercontent.com/robseb/rsyocto/rsYocto-1.04 /doc/symbols/HANPilot_pinout.png)
 
## Interacting with FPGA IP
  * The *rstools*-layer implifies interaction the interaction with any FPGA IP easy
  * Type "*FPGA* and press *TAB* inside your SSH-console to see all FPGA commands:
  `FPGA-gpiRead` `FPGA-gpoWrite` `FPGA-readBridge` `FPGA-readMSEL` `FPGA-resetFabric`
  `FPGA-status` `FPGA-writeBridge` `FPGA-writeConfig`
  * The Suffix `"-h"` after any command gives detailed information   
  
  1. **Reading a AVALON-Bus FPGA Module**
      * During the Boot process the FPGA-Configuration is written with a "*System ID Peripheral*"-component (*ID: 0xcafeacdc*)
      * The Module is connected via the Lightweight HPS-to-FPGA (*LWHPS2FPGA*) bridge to the HPS with a address offset of *0x30*
      * Use following command to read the System ID:
        ```bash
        FPGA-readBridge -lw 30
        ```
        ![Alt text](readBridgeExample.png?raw=true "FPGA-readBridge example output")

      * The Suffix `"-lw"` selects the Lightweight HPS-to-FPGA (*LWHPS2FPGA*) bridge
      * "*30*" is the (hex) address offset to read given by the Intel Quartus Prime Platform Designer
      * The Suffix `"-b"` disables an detailed output
        * Often used inside a *Python-*, *C++-* or *PHP-* application
           ```bash
           FPGA-readBridge -lw 30 -b
           ```
  2. **Turn off the FPGA LEDs with a single command**
      * The FPGA LEDs are connected via a "*PIO (Parallel IP)*"-interface to the Lightweight-HPS-to-FPGA bus
      * For turning the LEDs off run following command
          ```bash
           FPGA-writeBridge -lw 20 0
          ```
      * The Suffix "-lw" selects the Lightweight-HPS-to-FPGA interface
      * "30" is the (hex) address offset to write given by the *Intel Quartus Prime Platform Designer*
      
  3. **Put a Hex pattern to the FPGA LEDs**
      * With the following command any hex pattern can be written over the *AXI-Bus* 
        ```bash
        FPGA-writeBridge -lw 20 -h acdc
        ```
       * The Suffix "-h" selects HEX value inputs 
  4. **Control a single FPGA LED**
      * Enabling or Disabling single Bits is also possible with the *rstools* 
      * Put Led No. 7 on:  
         ```bash
           FPGA-writeBridge -lw 20 -b 7 1
         ```
  5. **The next Python snippet demonstrates how to interact with FPGA-IP** 
        ````python
          for count in range(1024):
            os.system('FPGA-writeBridge -lw 38 -h '+ str(count) +' -b')
        ````
  6. **Reading the Status of the FPGA-fabric:**
        ```bash
        FPGA-status
        ````
      * This Status Codes are transmitted by the FPGA Manager
      * The FPGA should be in the User Mode
 7. **Reading the FPGA switches for 15sec**
     * On the *LWHPS2FPGA* Bridge is with the address offset *0x00* a **PIO** (*Parallel I/O*) module connected
     * This is assigned to the FPGA switches 
     * Use following command to read it 
        ```bash
        FPGA-readBridge -lw 0
        ````
      * **The Suffix `"-r"` allows to update the value of the register for 15sec**
        ```bash
        FPGA-readBridge -lw 0 -r
        ````
    * Reading the 4-bit switches of the *Terasic* DE10 Nano
        ![Alt text](SwitchReadingAninmation.gif?raw=true "Reading switches")
    
 
8. **Using the GPI/GPO- Registers to the FPGA** 
    * Intel SoC-FPGAs have two 32-Bit registers to interact directly with the FPGA 
    * To test this feature by connecting the FPGA LEDs with the GPO-Register
    * But now the FPGA LEDs are connected to Lightweight-HPS-to-FPGA (*LWHPS2FPGA*) Bridge
    * The FPGA configuration must be changed
    * The required `.rbf` configuration file ("*gpiConf.rbf*") is pre-installed on the home directory
    * Execute following command to **configure the FPGA fabric** with this file:
        * For the Terasic DE10 Standard Board 
          ```bash
          FPGA-writeConfig  -f gpiConfStd.rbf
          ```
         * For the Terasic DE10 Nano Board 
           ```bash
           FPGA-writeConfig  -f gpiConfNano.rbf
           ```
    * Now should be the LEDs connected with the direct 32-Bit register
    * Enable the LEDs over this way:
        ```bash
        FPGA-gpoWrite -h acdc
        ```
    * On the other direction the FPGA writes the value *0xacdcacdc* to the HPS
        ```bash
        FPGA-gpiRead -h acdc
        ```
     * After this test install the original FPGA configuration again
     * On *rsYocto* the startup FPGA configuration is located here `/usr/rsyocto/running_bootloader_fpgaconfig.rbf`
     * Use the Suffix `"-r"` to install the original FPGA configuration 
        ```bash
       FPGA-writeConfig -r 
        ```
9. **Reading a AVALON-Bus FPGA Module connect to the HPS-to-FPGA Bridge**
      * During the Boot process the FPGA-Configuration is written with a "*System ID Peripheral*"-component (*ID: 0x23456789*)
      * The Module is connected via the HPS-to-FPGA (*HPS2FPGA*) bridge to the HPS with a address offset of *0x00*
      * Use following command to read the System ID:
        ```bash
        FPGA-readBridge -hf 0
        ```
      * The Suffix `"-hf"` selects the HPS-to-FPGA (*HPS2FPGA*) bridge
10. **Reading to a HPS (MPU) Address to get the status of the HPS_KEY**
      * The `FPGA-readBridge`- and `FPGA-writeBridge`- command allows beside to interact with both HPS-to-FPGA Bridges to read the entire memory space of the HPS 
        (*ARM Cortex-A9*) (**MPU** =*Microprocessor system*) 
      * This feature is enabled with the attribute `-mpu` 
      * On the *Terasic* DE10- and DE0- Cyclone V boards is the *HPS_KEY* connected to *GPIO1[24]* (*GPIOB*)
      * The *gpio_ext_porta* of *GPIO1* as the address *0xFF709050* and holds the status of the *HPS_KEY* push button (*.p3139 of the Cyclone V HPS handbook*)
      * Use following command to read this Register:
        ```bash
        FPGA-readBridge -mpu 0xFF709050 
        ```
      * The Suffix `"-mpu"` selects the MPU (HPS) memory space (*no offset will be used*)
      * Bit number 25 is the *HPS_KEY* value
      * **The Suffix `"-r"` allows to update the value of the register for 15sec**
      * Alternately is [`devmem2](https://github.com/radii/devmem2) pre-installed as well
      * In this example use
      ````bash
      devmem2 0xFF709050
      ````

 ## Interacting with Hard-IP
1. **I²c-Devices** 
    * The Terasic DE10 Boards contains an [*ADXL345*](https://www.analog.com/en/products/adxl345.html)-Accelerometer on i2c0
    * The `i2c-tools` allow to interact with this sensor
    * Scan the *i²c-Bus 0* to get the i²c-Address of this sensor 
        ```bash
       i2cdetect 0 
        ```
    * Only the i²c-address *0x53* should be found
    * With this address we can read the Unique ID (*0xE5*) of the *AXDL345*
        ```bash
            i2cget -f 0 0x53 0
        ```
    * Try to read the X-Axis of the accelerometer
        *   First enable the output of the Sensor
            ```bash
            i2cset -f 0 0x53 0x2D 8
            ```
        *   Then start to read the X-Axis
            ```bash
            i2cget -f 0 0x53 0x32
            ```
2. **UART**     
    * For Uart devices are `minicom` pre-installed
    * The following command opens the *COM-Port 1* with *minicom*
         ```bash
         minicom /dev/ttys1
         ```
    * This COM-Port routed to FPGA I/O Pins is on the DE10 Boards
    * Pres CMD+A, then Z and then Q to leave minicom 
3. **SPI**
    * *rsYocto* can be function as SPI-Master 
    * The `spi-tools` are installed
    * Please follow the documentation of the [spi-tools](https://github.com/cpb-/spi-tools)
4. **CAN-Bus** (*Intel Cylone V only*)
    * Intel Cyclone V FPGAs have two powerful Bosch `D_CAN`-Controllers embedded
    * To interact with CAN Devices the `can-tools` are pre-installed
    * They allow over an internal network connection to read and write CAN-Packages and monitoring the traffic 
    * To enable the *CAN0* execute this command to enable the *CAN network Port*:
        ```bash
        ip link set can0 type can bitrate 125000
        ip link set up can0
         ```
        * "*125000*" is the CAN Bitrate in *Bit/s*
    * Sniffing the complete CAN-Bus
         ```bash
         cansniffer can0
         ```
    * Generating Dummy Payload 
        ```bash
        cangen can0
        ```
    * For more information please read the [can-tools](https://github.com/linux-can/can-utils) documentation
    * A Python example show how to send a CAN-package with python is also given [here](https://github.com/robseb/rsyocto/blob/rsYocto-1.03/doc/appSpecificGuides/1_TransmittingCAN.md)
    
 
 ## Continue with the next level: [Debugging C++ applications remotely](3_CPP.md)
