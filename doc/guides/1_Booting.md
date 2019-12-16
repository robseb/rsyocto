 [Back to the startpage](https://github.com/robseb/rsyocto)
 
# Booting *rsYocto* on your Board
This guide shows how to install *rsYocto* on a **SD Card** and boot it on a Terasic FPGA development Board. 

## Create a bootable SD-Card 
1. Download the newest Image of *rsYocto* for your Board
    + The final Images are located inside the **"release part"** of this Github repository 
       ![Alt text](releasepart.png?raw=true "relase part")
    
    + Suffix decoding for the Image-Names:
    
      | File Suffix | FPGA | suppored Board
      |:--|:--|:--|
      | *_DE10STD* | Intel Cyclone V | [Terasic DE10-Standard](https://www.terasic.com.tw/cgi-bin/page/archive.pl?Language=English&CategoryNo=167&No=1081)
      | *_D10NANO* | Intel Cyclone V | [Terasic DE10-Nano](https://www.terasic.com.tw/cgi-bin/page/archive.pl?Language=English&CategoryNo=167&No=1046)
      | *_HAN* | Intel Arria 10 | [Terasic HAN Pilot Platform](https://www.terasic.com.tw/cgi-bin/page/archive.pl?Language=English&CategoryNo=228&No=1133)
 2. Insert a **Micro SD Card** (1GB or greater) into your computer  
 3. Use a "**Bootable SD Card Creation Tool**" to create a bootable image on the SD card
    + For example use the tool [Rufus](https://rufus.ie/) 
    + Ignore all warning message boxes
    
    ![Alt text](rufusSDbuilf.png?raw=true "rufus")
    
  ## Prepare your Board and open the console COM-Port
  1. Eject the SD Card from your Computer and insert them into the SD slot of your FPGA Board
  2. Change the MSEL-Bit switch to following setting: 
   ![Alt text](requiredMSEL.jpg?raw=true "Required MSEL-Bit Switch Selection")
  3. Connect your FPGA-Board with a **Ethernet cable to your network**
     + Be sure that a **iPv4-DHCP** is active on this network 
  4. Connect a USB Cable between the FTDI Virtual **COM-Port** (USB CDC) and your Computer
  5. **Open the COM-Port**
     + You can use the tool [MobaXterm](https://mobaxterm.mobatek.net/) for example
     + Use following settings: `115200N8 (ASCII) with CR/LF`
    
## Boot *rsYocto* on your FPGA-Board
  1. Power Up your FPGA Board
  2. Now should boot **rsYocto** thorough following stages:
     ![Alt text](BootingStep.jpg?raw=true "Boot steps of rsYocto")
     
   <br>
   
   
   ![Alt text](rsYoctoArria10BootLog.gif?raw=true "rufus")
   ***rsYocto* is booting on a Arria 10 SX**
  
  
## Login to *rsYocto*
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
1. Open Linux or Windows Comand Promt (Windows 10) and insert this command to connect to your Board: 
    ```
      ssh root@<Boards iPv4-address>
    ```
2. Use the Passwort: `eit`
  * No other authentications are required
  * The default SSH-Port (22) is used 
3. Now should the *rsYocto* Splash screen appear

 ## Continue with the next level: [Use of Hard IP, FPGA-IP and configuration of the FPGA fabric](2_FPGA_HARDIP.md)
