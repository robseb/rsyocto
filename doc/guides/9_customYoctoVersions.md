[back](7_customVersions.md)
___
![GitHub](https://img.shields.io/static/v1?label=Ubuntu&message=18.04+LTS,+20.04+LTS&color=yellowgreen)
![GitHub](https://img.shields.io/static/v1?label=CentOS&message=7.0,+8.0&color=yellowgreen)
![GitHub](https://img.shields.io/static/v1?label=Intel+EDS&message=20.1&color=blue)
![GitHub](https://img.shields.io/static/v1?label=Supported+SocFPGA&message=Intel+Arria10,+Cyclone+V&color=red")
<br>

**This is a more advanced guide of my  [ 	Designing of custom rsyoto versions](7_customVersions.md) to show to use the build system with custom Yocto Project Linux distributions to automate the entire bootflow for Intel Cyclone V- and Intel Arria 10 SX SoC-FPGA.** The Python scripts work with any Intel Cyclone V and Intel Arria 10 SoC-FPGA board with booting via SD-Card.  

![Alt text](BuildSystemHead.png?raw=true "Symbol of the build system")
**Use your *Intel Quartus Prime* FPGA project to create your own *rsyocto* with your FPGA Configuration**
___
<br>


![Alt text](https://raw.githubusercontent.com/robseb/rsyocto/master/doc/symbols/BuildSystem.jpg?raw=true "automatic rsyocto Build system")
**Block diagram of the fully automated build system to design new releases**
<br>

**This is a more advanced guide of my  [Designing of custom rsyoto versions](7_customVersions.md) to show to use of the build system with custom OpenEmbbeded Yocto Project Linux distributions to automate the entire bootflow for Intel Cyclone V- and Intel Arria 10 SX SoC-FPGA.**
___
<br>

## Designing of custom Yocto-Project based Linux Distributions with the *rsyocto* build system 

1. Install all required tools, like Intel SoC-EDS on a Linux Computer
    * For installing and setting up of your build computer please follow the instructions of the [Designing of custom rsyoto versions](7_customVersions.md) guide

2. Download and unzip the SD-Card folder 
    * Download the "**rsyocto_SDxx-Folder**" from the "**releases Part**" of this Github repository 
    
    <p align="center">
    <a href="https://github.com/robseb/rsyocto/releases">
        <img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/robseb/rsyocto">
    </a>	 
    </p>

    * Unzip the folder
4. **Copy this folder into your *Intel Quartus Prime* FPGA project folder**
5. Change the files of the SD-Card folder for your requirements
    * To allow to generate special Linux Distributions chnage the SD-Card folder as described in the [Designing of custom rsyoto versions](7_customVersions.md) guide
6. Run the *rsyocto* build script with your Yocto-Project Linux files 
    * The "*makersyoctoSDImage.py*" Python script allow some specific attributes:
    ````shell
    vm@yoctoBuntoX:~/Desktop/DE10NANOrsyocto/socfpgaPlatformGenerator$ python3 makersyoctoSDImage.py -h
    ##############################################################################
    #                                                                            #
    #    ########   ######     ##    ##  #######   ######  ########  #######     #
    #    ##     ## ##    ##     ##  ##  ##     ## ##    ##    ##    ##     ##    #
    #    ##     ## ##            ####   ##     ## ##          ##    ##     ##    #
    #    ########   ######        ##    ##     ## ##          ##    ##     ##    #
    #    ##   ##         ##       ##    ##     ## ##          ##    ##     ##    #
    #    ##    ##  ##    ##       ##    ##     ## ##    ##    ##    ##     ##    #
    #    ##     ##  ######        ##     #######   ######     ##     #######     #
    #                                                                            #
    #       AUTOMATIC SCRIPT FOR BRINGING A CUSTOM RSYOCTO LINUX FLAVOR          #
    #                         TO BOOTABLE IMAGE FILE                             #
    #                                                                            #
    #               by Robin Sebastian (https://github.com/robseb)               #
    #                          Contact: git@robseb.de                            #
    #                            Vers.: 3.11                                     #
    #                                                                            #
    ##############################################################################
    
    usage: makersyoctoSDImage.py [-h] [-y YOCTO_LINUX] [-g DEVICETREE_GEN]
    
    optional arguments:
      -h, --help            show this help message and exit
      -y YOCTO_LINUX, --yocto_linux YOCTO_LINUX
                            Use the Yocto Project zImage,rootfs files ["-y 1"]
      -g DEVICETREE_GEN, --devicetree_gen DEVICETREE_GEN
                            Use SoC EDS DeviceTree Generator ["-g 1 --> no GUI | 2
                            --> GUI"]
    ````
    * Posibile arguments of the script:
        * **"`-y`"** or **"`--yocto_linux`"** enables to **use the output files of the Yocto Project** (*zImage, rootfs and Linux Device Tree*) for the build
            * The script copies these file form the Yocto Project output folder to the SD-Card partitions, instate of the Linux files located inside the SD-Card folder
        * **"`-g`"** or **"`--devicetree_gen`"** uses the  **Intel Device Tree generated to automatically generate a Linux Device Tree** based on *Intel Quartus Prime* FPGA Project settings  
            * The Device Tree file will be located inside the SD-Card partition folder and can only be seen as reference because the Intel Device Tree generator is not recommenced by Intel any more
    * **Start the build script to generate a Linux Distribution with your Yocto-Project files**
    ````shell
    python3 makersyoctoSDImage.py -y 1
    ````
7. Follow the instruction of the Python build script 
    * The procdure will be identical as shown in the [Designing of custom rsyoto versions](7_customVersions.md) guide
    * Only following message box will appear to show the available Yocto Project output Linux Distribution files
    ````shell
    ##########################################################################################
    #                  COMPATIBLE YOCTO PROJECT LINUX DISTRIBUTION WAS FOUND                 #
    #                           Use this distribution for the build?                         #
    #                                                                                        #
    #----------------------------------------------------------------------------------------#
    #   No.    |             Specs of the found Yocto Project Linux Distribution             #
    #----------------------------------------------------------------------------------------#
    #     1    | Directory: "/home/vm/poky/build/tmp/deploy/images/cyclone5/"                #
    #     2    | Modification Date: Tue Apr  6 16:28:01 2021                                 #
    #     3    | rootfs: "core-image-minimal-cyclone5-20210406142211.rootfs.tar.gz           #
    #     4    | zImage: "zImage--5.10+gitAUTOINC+f7700e50b1-r0-cyclone5-20210407093253.bin" #
    #     5    | Devicetree: "-"                                                             #
    #----------------------------------------------------------------------------------------#
    #                                                                                        #
    ##########################################################################################
    
     
    #######################################################################
    #                 Use this distribution for the build?                #
    #                                                                     #
    #---------------------------------------------------------------------#
    #   No.    |                           Task                           #
    #---------------------------------------------------------------------#
    #     1    | Yes, use these files for this build                      #
    #     2    | No, copy file manually instead                           #
    #     3    | Use the existing Linux files inside the Partition folder #
    #---------------------------------------------------------------------#
    #   Select a item by typing a number (1-3) [q=Abort]                  #
    #  Please input a number: $    
    ````
    * Type `1` to let the script use this files for the build

8. Select the Linux Device Tree for the build
    * My [**meta-intelfpga](https://github.com/robseb/meta-intelfpga) BSP layer for the OpenEmbedded Yocto Project did not build the Linux *device tree*
    * Instate, the build script will ask the user to **copy a Linux *device tree file* with a specific name to the Image Partition folder** as shown:
    ````shell
    #################################################################################################################
    #                  Inside the Yocto Project Repo. folder no Linux Devicetree (.dts) was found!                  #
    #                      Use the existing Linux devicetree file inside the partition folder OR                     #
    #                          Copy a Linux devicetree file (.dts) to the partition folder                          #
    #                                                                                                               #
    #---------------------------------------------------------------------------------------------------------------#
    #   No.    |                          Name and Location of the required file to copy                           #
    #---------------------------------------------------------------------------------------------------------------#
    #     1    | Directory: "/home/vm/Desktop/DE10NANOrsyocto/socfpgaPlatformGenerator/Image_partitions/Pat_1_vfat" #
    #     2    | Requiered Name: "socfpga_cyclone5_socdk.dts"                                                       #
    #---------------------------------------------------------------------------------------------------------------#
    #                                                                                                               #
    #################################################################################################################
    ````
    * For reference the Intel Device tree generator can also be used. To doe this run this script
        ````shell
        python3 makersyoctoSDImage.py -g 1
        ````
        * The Python script will place this Linux device tree file with the name "*_reference.dts*" to the *Board folder*
    * Copy the file with shown name to the shown location and continue the script 
    * The script will generate a bootable Linux Distribution image for the *Intel Quartus Prime FPGA* project 
      
9. Flash the image to a SD-Card and boot your *Intel SoC-FPGA* board up
    * done 
    
<br>
<br>

___
[back](6_newFPGAconf.md)
[Back to the startpage](https://github.com/robseb/rsyocto)

