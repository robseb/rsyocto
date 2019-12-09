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
   ![Alt text](rufusSDbuilf.png?raw=true "rufus")
  
  ## Boot *rsYocto* on your FPGA-Baord
  1. Eject the SD-Card from your Computer and insird them into the SD-slot of your FPGA Board
  2. Change the MSEL-Bit switch to following setting: 
   ![Alt text](requiredMSEL.jpg?raw=true "Required MSEL-Bit Switch Selection")
