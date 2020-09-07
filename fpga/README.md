 [Back to the startpage](https://github.com/robseb/rsyocto)

# Intel Quartus Prime demo FPGA project 
<br>

| **File Name** | **FPGA** | **supported Board name** | **Description** | **Documentation** |
|:--|:--|:--|:--|:--|
|"*D10STDNANO_DDR3.qprs*" | *Cyclone V* | *every Cyclone V* Board | System DDR3 memory configuration script | - |
|"*DE0NANOrsyocto.qar*" | *Cyclone V* | *Terasic DE10-Nano* | Quartus prime archive file of the default FPGA configuration | [Info Papers](https://raw.githubusercontent.com/robseb/rsyocto/rsYocto-1.04/doc/symbols/DE10Nano_pinout.png) |
|"*DE0NANOrsyocto.v*" | *Cyclone V* | *Terasic DE10-Nano* | The top-level Verilog file | [Info Papers](https://raw.githubusercontent.com/robseb/rsyocto/rsYocto-1.04/doc/symbols/DE10Nano_pinout.png) |
|"*DE10STDrsyocto.qar*" | *Cyclone V* | *Terasic DE10-Standard* | Quartus prime archive file of the default FPGA configuration | [Info Papers](https://raw.githubusercontent.com/robseb/rsyocto/rsYocto-1.04/doc/symbols/symbols/DE10Std_pinout.png) |
|"*DE10STDrsyocto.v*" | *Cyclone V* | *Terasic DE10-Nano* | The top-level Verilog file | [Info Papers](https://raw.githubusercontent.com/robseb/rsyocto/rsYocto-1.04/doc/symbols/symbols/DE10Std_pinout.png) |
|"*DE0NANOrsyocto.qar*" | *Cyclone V* | *Terasic DE0-Nano SoC* | Quartus prime archive file of the default FPGA configuration | [Info Papers](https://raw.githubusercontent.com/robseb/rsyocto/rsYocto-1.04/doc/symbols/symbols/DE10Std_pinout.png) |
|"*DE0NANOrsyocto.v*" | *Cyclone V* | *Terasic DE0-Nano SoC* | The top-level Verilog file | [Info Papers](https://raw.githubusercontent.com/robseb/rsyocto/rsYocto-1.04/doc/symbols/symbols/DE10Std_pinout.png) |
|"*DE10NANO_NIOS.qar*" | *Cyclone V* | *Terasic DE10-Nano* | Quartus prime archive file with a *NIOS II processor* accessing HPS Hard-IP| [Guide](https://github.com/robseb/rsyocto/blob/rsYocto-1.04/doc/appSpecificGuides/4_NIOS2HPS.md) |
|"*DE10STD_NIOS.qar*" | *Cyclone V* | *Terasic DE10-Standard* | Quartus prime archive file with a *NIOS II processor* accessing HPS Hard-IP| [Guide](https://github.com/robseb/rsyocto/blob/rsYocto-1.04/doc/appSpecificGuides/4_NIOS2HPS.md) |
|"*DE0NANO_NIOS.qar*" | *Cyclone V* | *Terasic DE10-Nano SoC* | Quartus prime archive file with a *NIOS II processor* accessing HPS Hard-IP| [Guide](https://github.com/robseb/rsyocto/blob/rsYocto-1.04/doc/appSpecificGuides/4_NIOS2HPS.md) |
<br>
<br>

# For the Terasic DE10 Standard Board
* Unzip the project with *Intel* Quartus Prime
* Copy the folder **"ip"** (sub folder: *fpga/DE10STD_IP/* ) into the main Quartus Prime Project directory (Folder: *DE10STDrsyocto*)
* Build the project (the IP should now be found)


___
[Back to the startpage](https://github.com/robseb/rsyocto)
