# Using SSH to controll and reconfige the FPGA
This guide shows how to connect via SSH remotly to *rsYocto* and how simple it is to read FPGA IP and changing the FPGA configuration. 

## Connecting to *rsYocto* with SSH
1. Open Linux or Windows Comand Promt (Windows 10) and insiert this command to connect to your Board:
    ```bash
      ssh root@<Boards iPv4-address>
    ```
2. Use the Passwort `eit`
  * no other autentifications are requiered
  * The default SSH-Port (22) is here used 
3. Now should the *rsYocto* Slapsrean apper

## Toogeling the HPS-LED of your Board
1. Following turns the HPS Led on
    ```bash
    echo 100 > /sys/class/leds/hps_led0/brightness
    ```
2. To turn of the LED with:
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
    * "30" is the address offset to read given by the Intel Qurtus Plattorm Designer
  * The Suffix "-b" allows to use this command into a Python-,C++ or PHP application
       ```bash
       FPGA-readBridge -lw 30 -b
      ```
  
  2. read the Status of the FPGA-fabric with follwoing command:
       ```bash
       FPGA-status
       ```
