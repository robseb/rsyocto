# Use of Hard IP, FPGA-IP and configuration of the FPGA fabric
This guide shows how simple it is to access FPGA IP,the I²C-, the UART-Bus, the SPI-Bus or the CAN-Bus.
Also are here commands given to change the FPGA fabric configuration.

## Toggling the HPS-LED of your Board
1. Turn the HPS-LED on by typing to the console:
    ```bash
      echo 100 > /sys/class/leds/hps_led0/brightness
    ```
2.  Turn off the LED with:
    ```bash
     echo 0 > /sys/class/leds/hps_led0/brightness
    ```
3. To Toggle the LED is a *blinkLed* Python script pre-installed
    ```bash 
      python3 blinkLed.py
    ```
4. With `nano`- Editor it is possible to change the script
    ```bash 
     nano blinkLed.py
   ```
   * Later will be a pleasant way be shown (Level 4) 
   
## Opening *rsYocto* Info Paper 
  * For every *rsYocto*-Version is a Information Shied on the Apache Webserver installed
  * This Papers contains informations about the configuration of the FPGA IP and there Addresses 
  * **Open it by typing the iPv4-Address of your Board into a Web browser**
  * Of cause it is possible  to install any other homepage on *rsYocto*
     * Insert the homepage file to: `/usr/share/apache2/default-site/htdocs`
     * Restart the Apache Server with following command:
        ````bash
            /etc/init.d/apache2 stop
            /etc/init.d/apache2 start
        ````
## Interacting with FPGA IP
  * The *rstools*-layer make the interaction with any FPGA IP easy
  * Type "*FPGA* and press *TAB* inside your SSH-console to see all FPGA commands:
  `FPGA-gpiRead` `FPGA-gpoWrite` `FPGA-readBridge` `FPGA-readMSEL` `FPGA-resetFabric`
  `FPGA-status` `FPGA-writeBridge` `FPGA-writeConfig`
  * The Suffix `"-h"` after any command gives you detailed information   
  
  1. Reading a AVALON-Bus FPGA Module
      * During the Boot process is a FPGA-Configuration written with a "*System ID Peripheral*"-component (*ID: 0xcafeacdc*)
      * The Module is connected via the Lightweight-HPS-to-FPGA interface to the HPS
      * Use following command to read the System ID:
        ```bash
             FPGA-readBridge -lw 30
        ```
      * The Suffix `"-lw"` selects the Lightweight-HPS-to-FPGA interface
      * "*30*" is the (hex) address offset to read given by the Intel Qurtus Platform Designer
      * The Suffix `"-b"` disables an detailed output
        * Often used inside a *Python-*, *C++-* or *PHP-* application
           ```bash
             FPGA-readBridge -lw 30 -b
           ```
  2. Turn the FPGA LEDs with a single command off
      * The FPGA LEDs are connected via a "*PIO (Parallel IP)*"-interface to the Lightweight-HPS-to-FPGA bus
      * Run following command to turn the LEDs off
          ```bash
           FPGA-writeBridge -lw 20 0
          ```
      * The Suffix "-lw" selects the Lightweight-HPS-to-FPGA interface
      * "30" is the (hex) address offset to write given by the *Intel Quartus Prime Platform Designer*
      
  3. Put a Hex pattern to the FPGA LEDs
      * With following command can be any hex pattern written over the *AXI-Bus* 
        ```bash
         FPGA-writeBridge -lw 20 -h acdc
        ```
       * The Suffix "-h" selects HEX value inputs 
  4. Control a single FPGA LED
      * Enabling or Disabling single Bits is also possible with the *rstools* 
      * Put Led No. 8 on:  
         ```bash
           FPGA-writeBridge -lw 20 -b 8 1
         ```
  5. The next Python snippet demonstrates how to interact with FPGA-IP 
        ````python
          for count in range(1024):
            os.system('FPGA-writeBridge -lw 38 -h '+ str(count) +' -b')
        ````
  6. Reading the Status of the FPGA-fabric:
        ```bash
          FPGA-status
        ````
      * This Status Codes are transmitted by the FPGA Manager
      * The FPGA should be in the User Mode
7. Using the GPI/GPO- Registers to the FPGA 
    * Intel SoC-FPGAs have two 32-Bit register to interact directly with the FPGA 
    * To try this feature by connecting the FPGA LEDs with the GPO-Register
    * But now are the FPGA LEDs connected to Lightweight-HPS-to-FPGA Bridge
    * The FPGA configuration must be changed
    * The required `.rbf` configuration file ("*gpiConf.rbf*") is pre-installed on the home directory
    * Execute following command to configure the FPGA fabric with this file:
        ```bash
            FPGA-writeConfig  -f gpiConf.rbf
        ```
    * Now should be the LEDs connected with the direct 32-Bit register
    * Enable the LEDs over this way:
        ```bash
           FPGA-gpoWrite -h acdc
        ```
    * On the other direction writes the FPGA the value *0xacdcacdc* to the HPS
        ```bash
           FPGA-gpiRead -h acdc
        ```
     * After this test install the original FPGA configuration again
     * On *rsYocto* the startup FPGA configuration is located here `/usr/rsyocto/running_bootloader_fpgaconfig.rbf`
     * Use the Suffix `"-r"` to install the original FPGA configuration 
        ```bash
           FPGA-writeConfig -r 
        ```
 ## Interacting with Hard IP
1. **I²c-Devices** 
    * The Terasic DE10 Boards have an [*ADXL345*](https://www.analog.com/en/products/adxl345.html)-Accelerometer on i2c0
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
    * Try to read the X-Axis of the Accelerometer
        *   First enable the output of the Sensor
            ```bash
                i2cset -f 0 0x53 0x2D 8
            ```
        *   Then start to read the X-Axis
            ```bash
               i2cget -f 0 0x53 0x32
            ```
2. **UART**     
    * For Uart devices are `minicom' pre-installed
    * The following command opens the *COM-Port 1* with *minicom*
         ```bash
            mincom /dev/ttys1
         ```
    * This COM-Port is on the DE10 Boards routed to FPGA I/O Pins
    * Pres CMD+A, then Z and then Q to leave minicom 
3. **SPI**
    * *rsYocto* can be function as SPI-Master 
    * The `spi-tools` are installed
    * Please follow the documentation of the [spi-tools](https://github.com/cpb-/spi-tools)
4. **CAN-Bus** (*Intel Cylone V only*)
    * Intel Cyclone V FPGAs have two powerful Bosch `D_CAN`-Controllers embedded
    * To interact with CAN Devices are the `can-tools` pre-installed
    * They allow over internal network connection to read and write CAN-Packages and monitoring the traffic 
    * To enable the *CAN0* execute this command to enable the *CAN network Port*:
        ```bash
          ip link set can0 type can bitrate 125000
         ```
        * "*125000*" is the CAN Bitrate in *Bit/s*
    * With next shown command it is possible to transmit a CAN-Packages
        ```bash
            cansend can0 123#ADC1.ABC2
            ip link set up can0
        ```
        * This loads a CAN-Package with the Content *0xABC1* and *0xABC2* and the ID *123* to the message FIFO-Box
    * Sniffing the complete CAN-Bus
         ```bash
            cansniffer can0
         ```
    * Generating Dummy Payload 
        ```bash
           cangen can0
        ```
    * For more information please read the [can-tools](https://github.com/linux-can/can-utils) documentation
    
 
 ## Continue with the next level: [Debugging C++ applications remotely](3_CPP.md)
