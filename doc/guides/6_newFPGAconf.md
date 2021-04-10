[back](5_Streamline.md)

#  	Developing a new FPGA Configuration with Intel Quartus Prime 

**This guide describes how to design a new FPGA Configuration with a custom *Intel Quartus Prime* project. That FPGA Configuration can be written during boot or during runtime by Linux.** 

For each board the used default FPGA Configuration and a version with an *Intel NIOS II Soft-Core processor* inside this repository are available. The *Intel Quartus Prime* Project with the *Intel NIOS II Soft-Core processor* is connected via the *FPGA-to-HPS*-Bridge to the Hard-IP of the HPS. This allows to use Hard-IP components, such as CAN with the *NIOS II* processor. 

## Getting started with Intel Quartus Prime

  * Instal *Intel Quartus Prime* (*18.1 or later*)
  * A s*tep-by-step* guide how to install *Intel Quartus Prime* on Linux is [available here](https://github.com/robseb/NIOSII_EclipseCompProject#i-installment-of-intel-quartus-prime-191-and-201-with-nios-ii-support) (*Of cause NIOS II support is only for a NIOS II Project required*)
  
  * **Use a demo project** 
      * Clone the *Intel Quartus Prime* archive file (*.qar*) from this repository for your project
      * Start *Intel Quartus Prime* and choose "**`Project/Archive Project`**" to select the archive file
      * Start the **compilation** of the *Quartus Prime* project 
  * **Design your own FPGA Configuration file**
      * I wrote a [guide](https://github.com/robseb/HPS2FPGAmapping) to show in steps how to design a custom *Intel Quartus Prime* project and how to use FPGA I/O with the HPS and Linux
 


*rsyocto* allows with its BSP (*board support package*) layer `meta-intelfpga` to change the FPGA Configuration with a single Linux command as shown in chapter two:
  ````bash
      FPGA-writeConfig  -f gpiConf.rbf
  ````   
  
 ## Steps to generate the FPGA Configuration files with an Intel Quartus Prime FPGA Project
  **Note: The new build system can do these steps automatically!**

   1. **For the Arria 10 SX SoC-FPGA:**
      * Be sure that "**`Enables the HPS early release of HPS IO`**" is enabled in the **Intel Quartus Prime**- and HPS- Settings 
           * To **split the FPGA Configuration in a peripheral- and core- FPGA Configuration** 
           * This allows to hold for example the **memory configuration of the HPS** during FPGA Configuration changes  (*EMIF= external memory interface controller of the Intel Arria 10 SX is part of the FPGA Fabric and need a connection over the FPGA Interconnect before the secondary bootloader (u-boot) can use the SDRAM*) 
           * For more information please visit the [Intel Arria 10 documentation](https://www.intel.com/content/www/us/en/programmable/documentation/mzh1527115949958.html) page
              ![Alt text](Arria10Conf.jpg?raw=true "Quartus config for Arria 10")
      * Execute the following *Intel SoC-EDS-Shell* command:
        ````bash
          quartus_cpf -c --hps -o bitstream_compression=on rsHAN.sof socfpga.rbf
        ````
        * **SOF here:** "`rsHAN.sof`" 
        * **RBF here:** "`socfpga.rbf`"
      * With this command two FPGA Configuration files for the **HPS-** and **Memory-System** (*e.g. HPS PLL, HPS I/O, HPS Core voltage,...*) and for everything else are generated
        * **Output:** `socfpga.periph.rbf`" and "`socfpga.core.rbf`"
        
  2. **For the Cyclone V SoC-FPGA:**
      * For **FPGA Configuration of the FPGA with Linux** use these export settings: 
        * **Type:** "`Raw Binary File (.rbf)`" 
        * **Mode:** "**`Passive Parallel x16`**"  
        * **Name:** "`socfpga_nano_linux.rbf`", "`socfpga_std_linux.rbf`" or "`socfpga_de0_linux.rbf`"
       
            ![Alt text](fpgaConfSettings1.png?raw=true "FPGA Configuration settings 1")
            
      * For **FPGA Configuration of the FPGA during the boot** use these export settings: 
        * **Type:** "`Raw Binary File (.rbf)`" 
        * **Mode:** "**`Passive Parallel x8`**"  
        * **Name:** "`socfpga_nano.rbf`" or "`socfpga_std_linux.rbf`" or "`socfpga_de0_linux.rbf`"
            ![Alt text](fpgaConfSettings2.png?raw=true "FPGA Configuration settings 2")
        
___

 ## Continue with the next level: [Designing of a custom rsyocto Version](7_customVersions.md)
 [Back to the startpage](https://github.com/robseb/rsyocto)
 
