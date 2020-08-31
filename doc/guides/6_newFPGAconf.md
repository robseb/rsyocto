[back](5_Streamline.md)

#  	Developing a new FPGA configuration with Intel Quartus Prime 

This guide describes how to design a new FPGA configuration with a custom *Intel Quartus Prime* project. That configuration can be written during boot or on runtime by Linux. For each board the used default configuration and a version with a *Intel NIOS II Soft-Core processor* inside this repository are available. The Quartus Prime Project with the *Intel NIOS II Soft-Core processor* is connected via the *FPGA2HPS*-Bridge to the Hard-IP of the HPS. This allows to use Hard-IP components, such as CAN with the *NIOS II*. 

## Getting started with Intel Quartus Prime

  * Instal *Intel Quartus Prime* (18.1 or newer)
  * A step-by-step guide how to install Intel Quartus Prime on Linux is [available here](https://github.com/robseb/NIOSII_EclipseCompProject#i-installment-of-intel-quartus-prime-191-and-201-with-nios-ii-support) (Of cause NIOS II support is only for a NIOS II Project required)
  
  * **Use a demo project** 
      * Clone the *Intel Quartus Prime* archive file (*.qar*) from this repository for your project
      * Start *Intel Quartus Prime* and choose `Project/Archive Project` to select the archive file
      * Start the Compilation of the *Quartus Prime* project 
  * **Design your own FPGA configuration file**
      * I wrote a [guide](https://github.com/robseb/HPS2FPGAmapping) to show in steps how to design a custom *Quartus Prime* project and how to use FPGA I/O with the HPS and Linux
 


*rsYocto* allows with the layer `meta-rstools` to change the FPGA configuration with a single Linux command. That was shown in chapter 2 with:
  ````bash
      FPGA-writeConfig  -f gpiConf.rbf
  ````   
  
 ## Steps to generate the FPGA configuration files with a Quartus Prime Project
  **Note: The new build system can do these steps automatically!**

   1. **for the Arria 10:**
      * Be sure that "**Enables the HPS early release of HPS IO**" is enabled in the Quartus Prime- and HPS- Settings 
           * To split the configuration in a peripheral- and core- configuration 
           * This allows to hold for example the memory configuration of the HPS during FPGA configuration changes 
           * For more information please visit the [Intel Arria 10 documentation](https://www.intel.com/content/www/us/en/programmable/documentation/mzh1527115949958.html) page
              ![Alt text](Arria10Conf.jpg?raw=true "Quartus config for Arria 10")
      * Execute the following EDS-Shell command:
        ````bash
          quartus_cpf -c --hps -o bitstream_compression=on rsHAN.sof socfpga.rbf
        ````
        * SOF here: `rsHAN.sof` 
        * RBF here: `socfpga.rbf`
      * With this command two configuration files for the HPS- and Memory-System and for everything else are generated
        * Output: `socfpga.periph.rbf`and `socfpga.core.rbf`
        
  2. **for the Cyclone V:**
      * For **configuration of the FPGA with *Linux*** use these export settings: 
        * Type: `Raw Binary File (.rbf)` 
        * Mode: `Passive Parallel x16`  
        * Name:     `socfpga_nano_linux.rbf` or `socfpga_std_linux.rbf`
       
            ![Alt text](fpgaConfSettings1.png?raw=true "FPGA Configuration settings 1")
            
      * For **configuration of the FPGA during the boot** use these export settings: 
        * Type: `Raw Binary File (.rbf)` 
        * Mode: `Passive Parallel x8`  
        * Name: `socfpga_nano.rbf` or `socfpga_std.rbf`
            ![Alt text](fpgaConfSettings2.png?raw=true "FPGA Configuration settings 2")
        
___

 ## Continue with the next level: [Designing of a custom rsyocto Version](7_customVersions.md)
 [Back to the startpage](https://github.com/robseb/rsyocto)
 
