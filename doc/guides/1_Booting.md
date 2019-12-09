# Booting rsyocto on your Board
This guide shows how to install rsyocto on SD and boot them on Terasic DE10 FPGA Board. 

## Creating a bootebil SD-Card 
1. Download the newest Image of *rsYocto* for your Board
  + The final Images are located inside the **"relase part"** of this Github repositorie
  + Suffix decoding for the Images 
  
  | File Suffix | FPGA | suppored Board
  |:--|:--|:--|
  | *_DE10STD* | Intel Cyclone V | [Terasic DE10-Standard](https://www.terasic.com.tw/cgi-bin/page/archive.pl?Language=English&CategoryNo=167&No=1081)
  | *_D10NANO* | Intel Cyclone V | [Terasic DE10-Nano](https://www.terasic.com.tw/cgi-bin/page/archive.pl?Language=English&CategoryNo=167&No=1046)
  | *_HAN* | Intel Arria 10 | [Terasic HAN Pilot Platform](https://www.terasic.com.tw/cgi-bin/page/archive.pl?Language=English&CategoryNo=228&No=1133)
 2. Instert a Micro SD-Card (1GB or greater) into your coumputer  
 3. Use a Bootimage creating tool to create a bootebil image on the SD card
  + For example use the tool [Rufus](https://rufus.ie/) 
  + Ingonre all warning message boxes
  
  ## Prepare your Board and open the console COM-Port
  1. Eject the SD-Card from your Computer and insird them into the SD-slot of your FPGA Board
  2. Change the MSEL-Bit switch to following setting: 
   ![Alt text](requiredMSEL.jpg?raw=true "Required MSEL-Bit Switch Selection")
  3. Connect your FPGA-Board with a **Ethernet cabel to your network**
    + Be sure that a **iPv4-DHCP** is activ on this network 
  4. Connect a USB Kabel to the FTDI Virtual **COM-Port** (USB CDC) and to your Computer
  5. Open the COM-Port
    + you can use for example the tool [MobaXterm](https://mobaxterm.mobatek.net/)
    + Use following settings: **`115200N8 (ASCII) with CR/LF` **
    
## Boot *rsYocto* on your FPGA-Baord
  1. Power Up your FPGA Board
  2. Now should boot **rsYocto** thorough following stages:
     ![Alt text](BootingStep.jpg?raw=true "Boot steps of rsYocto")
  
## Login to *rsYocto*
* User Name: `admin`
* Passwort:  `eit`
  
