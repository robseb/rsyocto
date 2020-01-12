 [Back to the startpage](https://github.com/robseb/rsyocto)
 
# Booting *rsYocto* on your Board
This guide shows how to install *rsYocto* on a **SD Card** and boot it on a Terasic FPGA development Board. 

## Create a bootable SD-Card 
1. **Download the newest Image for your Board**
    + The final Images are located inside the **"release part"** of this Github repository 
       ![Alt text](releasepart2.png?raw=true "relase part")
    
    + Suffix decoding for the Image-Names:
    
      | File Suffix | FPGA | suppored Board
      |:--|:--|:--|
      | *_DE10STD* | Intel Cyclone V | [Terasic DE10-Standard](https://www.terasic.com.tw/cgi-bin/page/archive.pl?Language=English&CategoryNo=167&No=1081)
      | *_D10NANO* | Intel Cyclone V | [Terasic DE10-Nano](https://www.terasic.com.tw/cgi-bin/page/archive.pl?Language=English&CategoryNo=167&No=1046)
      | *_HAN* | Intel Arria 10 | [Terasic HAN Pilot Platform](https://www.terasic.com.tw/cgi-bin/page/archive.pl?Language=English&CategoryNo=228&No=1133)
      
      **Note:** *rsyocto_SD ...* is the associated SD-Card folder for the relase (see Part 5) 
 2. Insert a **Micro SD Card** (1GB or greater) into your computer  
 3. Use a "**Bootable SD Card Creation Tool**" to create a bootable image on the SD card
    + For example use the tool [Rufus](https://rufus.ie/) 
    + Rufus can also use the ZIP-archive directly (that is even faster)
    + Ignore all warning message boxes

      
    ![Alt text](rufusSDbuilf2.png?raw=true "rufus")
    
  ## Prepare your Board and open the console COM-Port
  1. Eject the SD Card from your Computer and insert it into the SD -Reader of your FPGA Board
  2. Change the MSEL-Bit switch to following setting: 
   ![Alt text](requiredMSEL.jpg?raw=true "Required MSEL-Bit Switch Selection")
  3. Connect your FPGA-Board with a **Ethernet cable to your network**
     + Be sure that a **iPv4-DHCP** is active on this network 
  4. Connect a USB Cable between the FTDI Virtual **COM-Port** (USB CDC) and your Computer
  5. **Open the COM-Port**
     + You can use the tool [MobaXterm](https://mobaxterm.mobatek.net/) for example
     + Use following settings: `115200N8 (ASCII) with CR/LF`
    
## Boot *rsYocto* on your FPGA-Board
  1. Power up your FPGA Board
  2. Now **rsYocto** boots through following stages:
  
   | No | Stage | Description | Taks 
   |:--|:--|:--|:--|
   | 1 | **Primary Bootloader** | Pre-configuration of the **FPGA configuration** (*Arria 10 SX only*) | Connecting HPS to FPGA SDRAM-Controller 
   | 2 | **Primary Bootloader** | Booting of primary bootloader | Hardware check and startup (SDRAM,...)
   | 3 | **Secoundary Bootloader** | Booting of *u-boot* | Loading and execution of the bootloader script
   | 4 | **Bootloader script** | Secoundary bootloader script execution | Writing the **FPGA configuration** and loading of the Linux Kernel
   | 5 | **Secoundary Bootloader** | Booting of *u-boot* | Loading and execution of the bootloader script
   | 6 | **Linux Kernel** | Booting of the Linux Kernel starts |  
   | 7 | **Linux Kernel** | Reading the Device Tree | The Kernel reads the device tree and loads the drivers 
   | 8 | **Linux Kernel** | Execution of the startup scripts from the rootFs starts | 
   | 9 | **startup-script** | **Excecution of by the user configurable startup script** |
   | 10 | **Network Interface** | Activation of the Network interface | Waiting for an DHCP reception with an iPv4-Address
   | 11 | **YYYYYYXXXXXXXXXXX **| RNG, .... | 
   | 12 | **OpenSSH** | *OpenSSH* SSH Server  | Starting
   | 13 | **Apache** | *Apache* Web Server  | Starting
   | 14 | **run-script** | **Excecution of by the user configurable startup script** | Time Syncronisation via HTTP
   | 15 | **BusyBox** | *BusyBox* Linux console interface | 
   | 16 | **User Commmand input after password authentication** |
   <br>
 
  ### **The Linux requests an iPv4-Address by a DHCP-server**
  ### **After the system has booted properly and a network connection is established -> HPS LED turns ON**
  <br>
  
   ![Alt text](rsYoctoArria10BootLog.gif?raw=true "rufus")
   ***rsYocto* is booting on an Arria 10 SX**
  
  
## Login
* Default device name: `cyclone5` or `arria10` 
* Login: `root`
* Passwort:  `eit`
* Default MAC: `d6:7d:ae:b3:0e:ba`
 <br>
 
 ## Find the iPv4 Address of your Board
 * Use following Linux Command to get the iPv4 Address of your Board
     ````shell
      ifconfig
     ```` 
 * the IP Address is also shown during the boot
 <br> 
 
## Connect to *rsYocto* with SSH
1. Open Linux or *Windows Command Prompt* (Windows 10) and insert this command to connect to your Board: 
    ```
    ssh root@<Boards iPv4-address>
    ```
2. Use following the Passwort: `eit`
  * No other authentications are required
  * The default SSH-Port (22) is used 
3. Now *rsYocto* Splash screen appears

 ## Continue with the next level: [Use of Hard IP, FPGA-IP and configuration of the FPGA fabric](2_FPGA_HARDIP.md)
