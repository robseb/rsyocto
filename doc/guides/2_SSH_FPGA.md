# Using SSH to controll and reconfige the FPGA
This guide shows how to connect via SSH remotly to *rsYocto* and how simple it is to read FPGA IP and changing the FPGA configuration. 

## Connecting to *rsYocto* with SSH
1. Open Linux or Windows Comand Promt (Windows 10) and insiert this command to connect to your Board:
    ```
      ssh root@<Boards iPv4-address>
    ```
2. Use the Passwort: `eit`
  * no other autentifications are requiered
  * The default SSH-Port (22) is here used 
3. Now should the *rsYocto* Slapsrean apper

## Toogeling the HPS-LED of your Board
1. Following turns the HPS Led on
    ```bash
      echo 100 > /sys/class/leds/hps_led0/brightness
    ```
2.  Turn of the LED with:
    ```bash
     echo 0 > /sys/class/leds/hps_led0/brightness
    ```
3. To toogle the LED is a *BlinkLED* Python scipt pre-installed
    ```bash 
      python3 blinkLed.py
    ```
4. With `nano`- Editor it is posible to change the script
    ```bash 
     nano blinkLed.py
   ```
   * later will be a pleasant way be shown (Level 4) 
   
## Opening *rsYocto* Info Paper 
  * For every *rsYocto*-Version is a Information Shied on the Appace Webserver installed
  * this Papers contains informations about the configuration of the FPGA IP and there Addresses 
  * Open it by typing the iPv4-Address of your Board into a Web brauser
  
## Interact with FPGA IP
  * My *rstools*-layer make the interaction with any FPGA IP really simply
  * Type "*FPGA* and press *TAB* inside your SSH-console to see all FPGA comands:
  `FPGA-gpiRead` `FPGA-gpoWrite` `FPGA-readBridge` `FPGA-readMSEL` `FPGA-resetFabric`
  `FPGA-status` `FPGA-writeBridge` `FPGA-writeConfig`
  * The Suffix "-h" after any comand gives you detailed informations  
  1. Try to read a AVALON-Bus Module
    * during the Boot process is a FPGA-Configuration written with Configuration 
      with a "System ID Peripheral" written with ID (0xcafeacdc)
    * The Module is connected via the Lightweight-HPS-to-FPGA interface to the HPS
    * Use following command to read the System ID:
           ```bash
             FPGA-readBridge -lw 30
           ```
      * The Suffix "-lw" selects the Lightweight-HPS-to-FPGA interface
      * "30" is the (hex) address offset to read given by the Intel Qurtus Plattorm Designer
      * The Suffix "-b" allows to use this command into a Python-,C++ or PHP application
           ```bash
             FPGA-readBridge -lw 30 -b
           ```
  2. Turn the FPGA Leds with a single comand on
      * The FPGA Leds are connected via a "PIO (Parallel IP)" to the Lightweight Bus
      * run following command to turn the LEDs off
          ```bash
           FPGA-writeBridge -lw 20 0
          ```
      * The Suffix "-lw" selects the Lightweight-HPS-to-FPGA interface
      * "30" is the (hex) address offset to write given by the Intel Qurtus Plattorm Designer
      
  3. Put a Hex Puttern to the FPGA LEDs
      * With following comand can you write any hex pattern over the AXI-Bus 
        ```bash
         PGA-writeBridge -lw 20 -h acdc
        ```
       * The Suffix "-h" selects HEX value inputs 
  4. Control a single FPGA LED
      * Enabling or Disabling single Bits is also posible with the *rstools* 
      * Put Led No. 8 on:  
         ```bash
           FPGA-writeBridge -lw 20 -b 8 1
         ```
      * The Suffix "-h" selects HEX value inputs 
  5. H!!! ier Python script zum Stuern der LEDs einfügen !!!!    
      
  6. read the Status of the FPGA-fabric with follwoing command:
        ```bash
          FPGA-status
        ````
      * This Status Codes are transmited by the FPGA Manager
      * The FPGA should be in the User Mode
7. Intel SoC-FPGAs have two 32-Bit register to interect with the FPGA directly
    * To try this feature we can connect the FPGA LEDs with *rsYocto* 
    * But now are the FPGA LEDs connected to LightWight Brige interface
    * We need to change the FPGA Configuation
    * The requiered *.rbf* configuration file ("gpiConf.rbf") is pre-installed on the home directery
    * we can run following command to configre the FPGA with this file:
        ```bash
            FPGA-writeConfig  -f gpiConf.rbf
        ```
    * Now should the be the LEDs connected with the direct 32-Bit register
    * Enable the LEDs over this way with following command:
        ```bash
           FPGA-gpoWrite -h acdc
        ```
    * On other direction writes the FPGA the value 0xacdcacdc to the HPS
        ```bash
           FPGA-gpiRead -h acdc
        ```
     * After this test we can write the orginal FPGA configurartion
     * On *rsYocto* the startup FPGA configuration is located here `/usr/rsyocto/running_bootloader_fpgaconfig.rbf`
     * Use the Suffix "-r" to install the orginal FPGA configuration 
        ```bash
         FPGA-writeConfig -r 
        ```
