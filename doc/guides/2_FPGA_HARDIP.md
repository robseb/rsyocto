[back](1_Booting.md)

# Use of Hard IP, FPGA-IP and Configuration of the FPGA Fabric
This guide shows how simple it is to access any `FPGA Soft-IP`,the `I²C`-, the `UART`-, the `SPI`- or `CAN`-Bus.
Here are also commands given to change the **FPGA Fabric Configuration** by using the `FPGA Manager` of the *SoC-FPGAs*. 

## Toggling the HPS_LED of your Board
1. **Turn on the HPS_LED**
	* The HPS_LED of the *Terasic* Development boards are connected to the HPS I/O-Bank of the *SoC-FPGAs*
    * With the **Linux Device Tree** the *Altera* *I/O* driver assigns the I/O-Pin number to the Linux file "*hps_led0*"
    * Type following command to turn the LED on
        ```bash
        echo 100 > /sys/class/leds/hps_led0/brightness
        ```
1.  **Turn off the HPS_LED**
    ```bash
    echo 0 > /sys/class/leds/hps_led0/brightness
    ```
1. **To toggle the HPS_LED is a *blinkLed.py* Python script pre-installed**
    * Run run a exiting Python script that is located on the home-dir (*~*) by using
    ```bash 
    Python3 blinkLed.py
    ```
1. **With `nano`- Editor it is possible to change the script**
    ```bash 
   nano blinkLed.py
   ```
   * Later a more pleasant way will be shown... 
<br>
   
## Opening *rsyocto* Info Paper (*Platform block diagram*)
  * For every *rsyocto*-Version a information sheet is on the `Apache Webserver` pre-installed 
  * This Paper describes the Configuration of the FPGA Soft-IP and there Addresses and the used I/O Pins of the default Configuration set was written during boot to the FPGA Fabric
  * **Open it by typing the iPv4-Address of your Board into a Web browser**
  * Of cause it is possible to install any other homepage
     * Insert the homepage files to: `/usr/share/apache2/default-site/htdocs` as shown in deeper guides
     * Restart the Apache Server with following commands:
        ````bash
            /etc/init.d/apache2 stop
            /etc/init.d/apache2 start
        ````
     *  Info Papers
        * [Terasic DE10 Standard *Intel Cyclone V SoC-FPGA* development board](https://raw.githubusercontent.com/robseb/rsyocto/rsYocto-1.042/doc/symbols/DE10Std_pinout.png)
        * [Terasic DE10 Nano & DE0 Nano SoC *Intel Cyclone V SoC-FPGA* development board](https://raw.githubusercontent.com/robseb/rsyocto/rsYocto-1.042/doc/symbols/DE10Nano_pinout.png)
        * [Terasic HAN Pilot *Intel Arria 10 SX SoC-FPGA* development board](https://raw.githubusercontent.com/robseb/rsyocto/rsYocto-1.042/doc/symbols/HANPilot_pinout.png)
 
## Interacting with FPGA IP
  **In *rsyocto* all interfaces for interaction with the FPGA Fabric are activated and open during the start-up process. The following paragraph shows how easy it is to use them.**
  

  * The `rstools` contains a set of useful simple commands to interact and access all interfaces between the HPS (*Hard processor system*) and the FPGA Fabric and the `FPGA-Manager`of the SoC-FPGAs 
  * Type "*FPGA*" and press `TAB` inside your SSH-console to see all FPGA commands:

      `FPGA-gpiRead` `FPGA-gpoWrite` `FPGA-readBridge` `FPGA-readMSEL` `FPGA-resetFabric`
      `FPGA-status` `FPGA-writeBridge` `FPGA-writeConfig`
  * **The Suffix `"-h"` (*help*) after any command gives detailed information about the *rstools* command**
  * The `rstools` are part of my [`meta-intelfpga`](https://github.com/robseb/meta-intelfpga) BSP-layer for the Yocto Project  
  
  1. **Reading a AVALON-Bus FPGA Soft-IP Module connected to a ARM AXI Bridge Interface**
      * During the Boot process the FPGA-Configuration is written with a "*System ID Peripheral*"-component (*ID: 0xcafeacdc*)
      * The Module is connected via the **Lightweight HPS-to-FPGA** (*LWHPS2FPGA; lwhps2fpga*) bridge to the HPS with a address offset of *0x30*
      * Use following command to read the System ID:
        ```bash
        FPGA-readBridge -lw 30
        ```
        ![Alt text](readBridgeExample.png?raw=true "FPGA-readBridge example output")

      * The Suffix "`-lw`" selects the Lightweight HPS-to-FPGA (*LWHPS2FPGA*) bridge
      * "*30*" is the (*hex*) address offset of the *SysID* Soft-IP given by the *Intel Quartus Prime Platform Designer*
      * The Suffix "`-b`" disables an detailed output
        * Useful for  *Python-*, *C++-* or *PHP-* application
           ```bash
           FPGA-readBridge -lw 30 -b
           ```
  2. **Turn off the FPGA LEDs with a single command**
      * The FPGA LEDs are connected via a Soft-IP "*PIO (Parallel IP)*" controller to the **Lightweight HPS-to-FPGA** bus
      * For turning the LEDs off run following command
          ```bash
          FPGA-writeBridge -lw 20 0
          ```
      * The Suffix "`-lw`" selects the Lightweight HPS-to-FPGA bridge interface
      * "30" is the (*hex*) address offset of this Soft-Ip given by the *Intel Quartus Prime Platform Designer*
      
  3. **Put a Hex pattern to the FPGA LEDs**
      * With the following command any hex pattern can be written over a *AXI-Bus* to FPGA Soft-IP 
        ```bash
        FPGA-writeBridge -lw 20 -h acdc
        ```
       * The Suffix "`-h`" selects *HEX* value inputs 
  4. **Control a single FPGA LED**
      * Enabling or Disabling single Bits is also possible with the *rstools* 
      * For instance, put FPGA LED No. 7 on:  
         ```bash
         FPGA-writeBridge -lw 20 -b 7 1
         ```
      * And Off:  
         ```bash
         FPGA-writeBridge -lw 20 -b 7 0
         ```
  5. **The next Python snippet demonstrates how to interact with FPGA Soft-IP** 
        ````Python
        for count in range(1024):
            os.system('FPGA-writeBridge -lw 38 '+ str(count) +' -b')
        ````
        * This git repo contains inside `examples/Python` some Python examples with this approach  
  6. **Reading the MSEL switch**
        ```bash
        FPGA-readMSEL
        ````
      * The **MSEL** (*mode select*) switch is used to give the HPS the **right** to access the **HPS-to-FPGA Bridges** and to change the **FPGA Configuration**
      * Also with the MSEL the type and the source of the FPGA Configuration file is chosen
      * The MSEL bit-switch is reachable over the HPS `FPGA Manager` (*Hard-IP part of any Intel SoC-FPGA*)
 7. **Reading the FPGA switches for 15sec**
     * On the *LWHPS2FPGA* Bridge is with the address offset *0x00* a **PIO** (*Parallel I/O*) Soft-IP module connected 
     * It is assigned to the FPGA switches of the development baord
     * Use following command allows to read the FPGA switches of your board  
        ```bash
        FPGA-readBridge -lw 0
        ````
      * **The Suffix "`-r`" allows to update the value of the register for 15sec**
        ```bash
        FPGA-readBridge -lw 0 -r
        ````
    * For instance, updating the 4-bit switches of the *Terasic* DE10 Nano
        ![Alt text](SwitchReadingAninmation.gif?raw=true "Reading switches")
    <br>
 
8. **Using the GPI/GPO- Registers to the FPGA** 
    * *Intel SoC-FPGAs* have two 32-Bit registers to interact directly with the FPGA Fabric
    * To test this feature by connecting the FPGA LEDs with the GPO-Register
    * But now the FPGA LEDs are connected to **Lightweight HPS-to-FPGA** (*LWHPS2FPGA*) Bridge
    * The FPGA Configuration must be changed to reconnect the FPGA LED...
    * The required `.rbf` Configuration file ("*gpiConf.rbf*") is pre-installed on the home directory (*~*)
    * Execute following command to **re-configure the FPGA Fabric** with this FPGA Configuration file:
        * For the *Terasic* DE10 Standard Board 
          ```bash
          FPGA-writeConfig  -f gpiConfStd.rbf
          ```
         * For the *Terasic* DE10 Nano Board 
           ```bash
           FPGA-writeConfig -f gpiConfNano.rbf
           ```
        * For the *Terasic* DE0 Nano SoC Kit 
           ```bash
           FPGA-writeConfig -f gpiConfDe0.rbf
           ```
    * That command will check that the FPGA Configuration file is vialed for the running FPGA Fabric, then it will reset the old FPGA Configuration, **loads the new FPGA Configuration with the help of the `FPGA Manger` to FPGA-Fabric** and release the FPGA Fabric reset 
    * Now should be the LEDs connected with the direct 32-Bit GPO register
    * Enable the LEDs over this way
        ```bash
        FPGA-gpoWrite -h acdc
        ```
    * On the other direction the FPGA writes the value *0xacdcacdc* to the HPS
        ```bash
        FPGA-gpiRead
        ```
     * After this test install the original FPGA Configuration again
     * On *rsyocto* the startup FPGA Configuration is located here: `/usr/rsyocto/running_bootloader_fpgaconfig.rbf`
     * Use the Suffix "`-r`" to install the original FPGA Configuration on the FPGA Fabric(*roll back*)
        ```bash
        FPGA-writeConfig -r 
        ```
<br>

9. **Reading a AVALON-Bus FPGA Module connect to the ARM AXI HPS-to-FPGA Bridge**
      * During the Boot process the FPGA Configuration is written with a "*System ID Peripheral*" Soft-IP component (*ID: 0x23456789*)
      * The Module is connected via the **ARM AXI HPS-to-FPGA** (*HPS2FPGA; hps2fpga*) bridge to the HPS with a address offset of *0x00*
      * Use following command to read the System ID:
        ```bash
        FPGA-readBridge -hf 0
        ```
      * **The Suffix "`-hf`" selects the ARM AXI HPS-to-FPGA (*HPS2FPGA*) bridge**
<br>

10. **Reading to a HPS (MPU) Address to get the status of the HPS_KEY**
      * The `FPGA-readBridge`- and `FPGA-writeBridge`- commands allow beside to interact with both HPS-to-FPGA bridges to **access the entire memory space of the HPS** (*ARM Cortex-A9*) (**MPU** =*Microprocessor system*) 
      * **This feature can be enabled with the attribute "`-mpu`"**
      * On the *Terasic* *DE10*- and *DE0*- *Cyclone V SoC-FPGA* boards is the **HPS_KEY** connected to **GPIO1[24]** (`GPIOB`)
      * The *"gpio_ext_portb"* of `GPIO1` has the address *0xFF709050* and holds the status of the *HPS_KEY* push button (*p. 3139 of the Cyclone V SoC-FPGA HPS handbook (2018.07.17)*)
      * Use following command to read this Register:
        ```bash
        FPGA-readBridge -mpu 0xFF709050 
        ```
      * **The Suffix "`-mpu`" selects the MPU (*HPS*) memory space** (*no offset will be used*)
      * *Bit number 25* is the *HPS_KEY* value
      * **The Suffix "`-r`" allows to update the value of the register for 15sec**
      * Alternately is [`devmem2`](https://github.com/radii/devmem2) pre-installed as well
      * For this example use
      ````bash
      devmem2 0xFF709050
      ````
<br>

 ## Interacting with HPS Hard-IP (I²C, SPI, CAN, ...)
**In *rsyocto* Linux drivers for all Hard-IP components are pre-installed.** This was done within the *Linux Device Tree* and the *u-boot* secondary bootloader script.

**Inside the pre-configured FPGA Configuration are the HPS Hard-IP I/O pins routed over the `FPGA Interconnect` to FPGA I/O pins to enable the usage of `Arduino Uno shields`**. 

Typically, dedicated HPS I/O pin headers are not available on SoC-FPGA development boards. It is for this reason that I chose this route to gain access. This can be seen inside the info papers and [**here**](https://github.com/robseb/HPS2FPGAmapping). For every Hard-IP components common Linux shell tools are available.
    
1. **I²c-Devices** 
    * The *Terasic DE10 Boards* have an [*ADXL345*](https://www.analog.com/en/products/adxl345.html)-Accelerometer on `i2c0`
    * The `i2c-tools` allow to interact with this sensor
    * Scan the *i²c-Bus 0* to get the i²c-Address of this sensor 
        ```bash
       i2cdetect 0 
        ```
    * Only the i²c-address *0x53* should be found
    * With this address **read the Unique ID** (*0xE5*) of the *AXDL345*
        ```bash
            i2cget -f 0 0x53 0
        ```
    * Try to read the *X-Axis* of the accelerometer
        *   First enable the output of the sensor
            ```bash
            i2cset -f 0 0x53 0x2D 8
            ```
        *   Then start to read the X-Axis
            ```bash
            i2cget -f 0 0x53 0x32
            ```
2. **UART** (*Serial COM Port*)     
    * For UART devices are `minicom` pre-installed
    * The following command opens the *COM-Port 1* (`COM1`) with *minicom*
         ```bash
         minicom /dev/ttys1
         ```
    * **This COM-Port is routed via the FPGA Interconnect to FPGA I/O Pins on the *DE10 SoC-FPGA* Boards**
    * Pres `CMD+A`, then `Z` and then `Q` to leave `minicom` 
3. **SPI**
    * *rsyocto* can be function as `SPI-Master` or as an `SPI-Slave`  
    * The `spi-tools` are installed
    * Please follow the documentation of the [spi-tools](https://github.com/cpb-/spi-tools)
4. **CAN-Bus** (*Intel Cylone V only*)
    * **Intel Cyclone V SoC-FPGAs have two powerful Bosch `D_CAN`-Controllers embedded**
    * To interact with CAN Devices the `can-tools` with [`SocketCAN`](https://www.kernel.org/doc/html/v4.17/networking/can.html) are pre-installed
    * `SocketCAN` allows over an internal network connection to read and write CAN-Packages and monitoring there traffic 
    * To enable the `CAN0` execute this command to enable the *CAN network Port*
        ```bash
        ip link set can0 type can bitrate 125000
        ip link set up can0
         ```
        * "*125000*" is the CAN Bitrate in *Bit/s*
    * **Sniffing** the complete CAN-Bus
         ```bash
         cansniffer can0
         ```
    * Generating **Dummy Payload** 
        ```bash
        cangen can0
        ```
    * For more information please read the [can-tools](https://github.com/linux-can/can-utils) documentation
    * **A Python example show how to send a CAN-package with Python is also given in details** [here](https://github.com/robseb/rsyocto/blob/rsYocto-1.042/doc/appSpecificGuides/1_TransmittingCAN.md)
    
 
 ## Continue with the next level: [Debugging C++ applications remotely with Visual Studio](3_CPP.md)
