# Booting rsyocto on your Board
This guide shows how to install rsyocto on SD and boot them on Terasic DE10 FPGA Board. 

## Creating a bootebil SD-Card 
1. Download the newest Image of *rsYocto* for your Board
  + The final Images are located inside the **"relase part"** of this Github repositorie
  + Suffix decoding for the Images 
  
  | File Suffix | FPGA | suppored Board
  |:--|:--|:--|
  | *_DE10STD* | Intel Cyclone V | [Terrasic DE10-Standard](https://www.terasic.com.tw/cgi-bin/page/archive.pl?Language=English&CategoryNo=167&No=1081)
  | *_D10NANO* | Intel Cyclone V | [Terrasic DE10-Nano](https://www.terasic.com.tw/cgi-bin/page/archive.pl?Language=English&CategoryNo=167&No=1046)
  | *_HAN* | Intel Arria 10 | [Terrasic HAN Pilot Platform](https://www.terasic.com.tw/cgi-bin/page/archive.pl?Language=English&CategoryNo=228&No=1133)
 2. Instert a Micro SD-Card (1GB or greater) into your coumputer  
