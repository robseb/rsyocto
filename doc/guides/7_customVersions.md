[back](6_newFPGAconf.md)
___
![GitHub](https://img.shields.io/static/v1?label=Ubuntu&message=18.04+LTS,+20.04+LTS&color=yellowgreen)
![GitHub](https://img.shields.io/static/v1?label=CentOS&message=7.0,+8.0&color=yellowgreen)
![GitHub](https://img.shields.io/static/v1?label=Intel+EDS&message=20.1&color=blue)
<br>


![Alt text](https://raw.githubusercontent.com/robseb/rsyocto/rsYocto-1.04/doc/symbols/BuildSystem.jpg?raw=true "automatic rsyocto Build system")
<br>

**The Python script *"makersyoctoSDImage.py"* allows to build with the *Intel Embedded Development Suite* (*SoC EDS*) the entire bootflow and generates a bootable image (*.img*) file with a flavor of *rsyocto***


This Python build system was designed to automate the always identical build flow for *Intel* SoC-FPGAs to reduce the possible sources of error during design.

It can use the information provided by the *Intel Quartus Prime* project to compile and configure the bootloader (u-boot) to boot up an embedded Linux and to configure the FPGA fabric with the *Quartus Prime project*. 

The Image folder contains a sub-folder for any partition of the final *SD-Card* image. Files copied into these folders will automatically be pre-installed to the depending partition on the bootable *SD-Card* image. To achieve this internally my  [*LinuxBootImageFileGenerator*](https://github.com/robseb/LinuxBootImageFileGenerator) is used to generate an image file. 

It can run on any modern Linux operating system, such as *CentOS* or *Ubuntu* Linux with the pre-installed SoC EDS. 
<br>
___

# Features
* **Automatically generate a bootable image file with configuration provided by a Quartus Prime project**
* **Cloning and compiling of the *u-boot* bootloader for Intel SoC-FPGAs**
* **Allows *menuconfig* of *u-boot***
* **Installs and uses the *Linaro* cross-platform toolchain**
* **HPS Memory- and HPS I/O- configuration based on the Quartus Prime project settings**
* **Allows to use a pre-build bootloader execuatable and default u-boot script**
* **In case of the u-boot script is configured to load a FPGA configuration the depending FPGA configuration will be generated**
* **Uses the default *rsyocto* Linux files for the boot image**
* **Allows to pre-install any files or operating systems to the SD-Card image**
* **Enables to copy board- and SoC-FPGA- specific files to the specific folders**
* **Give every board a private MAC-Address by writing it to the device tree**
* **Configures e.g. the SSH-Server and the Apache web server**s 
* **Boot image *(.img)* file generation for distributing embedded Linux Distributions**
* **Up to 4 freely configurable partitions**
* **Configurable partition size in *Byte*,*Kilobyte*,*Megabyte* or *Gigabyte***
* **File structure for each partition will be generated and user files can be added**
* **Partition file size check** 
* **Dynamic mode: Partition size = Size of the files to add to the partition**
* **An offset can be added to a dynamic size (*e.g. for user space on the running Linux*)**
* **Linux device tree (*dts*) -files inside a partition can be automatically compiled and replaced with the un-compiled file**  
* **An u-boot script with the name "*boot.script*" inside a partition can be automatically compiled and replaced with the un-compiled file**
* **Compressed files *(e.g. "tar.gz")* containing for instance the Linux *rootfs* can be unzipped and automatically added to the partition**
* **Image Sizes, Block Sizes, Start Sectors for every partition will be automatically generated for the depending configuration**
* **The final image file can be compressed to a "*zip*-archive file to reduce the image size**

* **Supported File Systems**
    * **ext2**
    * **ext3**
    * **ext4**
    * **Linux**
    * **vfat**
    * **fat**
    * **swap**
    * **RAW**
* **Supported archive file types, that can be unzipped automatically**
    * *.tar* **-Archives**
    * *.tar.gz* **-Archives**
    * *.zip* **-Archives**
* **Tested Development Environments**
    * **Ubuntu 18.04 LTS**
    * **Ubuntu 20.04 LTS**
    * **CentOS 7.7**
    * **CentOS 8.0**
* **Supported Intel Embedded Development Suite (SoC EDS) Versions**
    * **EDS 20.1 (Linux)**
* **Supported Intel SoC-FPGAs**
    * **Intel Cyclone V**
___
<br>

# Getting started with the designing of a custom rsyocto version

For generating a bootable *rsyocto* image for *Intel* SoC-FPGAs by executing a single Linux command please follow this step-by-step guide:

## Install the required development- and the build tools

* **Instal Intel Quartus Prime (18.1 or newer) for Linux**
    *    A step-by-step guide how to install *Intel Quartus Prime* on **Linux** is available [here](https://github.com/robseb/NIOSII_EclipseCompProject#i-installment-of-intel-quartus-prime-191-and-201-with-nios-ii-support) (*NIOS II support is for this project not required*)
* Install the Intel Embedded Development Suite (SoC EDS)
    * [Download](https://fpgasoftware.intel.com/soceds/20.1/?edition=standard&platform=windows&download_manager=direct) Intel SoC EDS 20.1 Standard for Linux
    * Install SoC EDS by executing the following Linux console commands
        ````shell
        chmod +x SoCEDSSetup-20.1.0.711-linux.run && ./SoCEDSSetup-20.1.0.711-linux.run
        ````
* Install the required packages
    ````shell
    sudo apt-get update -y && sudo apt-get install -y bison flex libncurses-dev \
         git device-tree-compiler  u-boot-tools
    ````
* Download the "**rsyocto_SDxx-Folder**" from the "**releases Part**" of this Github repository
* Unzip the folder and copy the internal folder **"socfpgaPlatformGenerator"** and copy it into your *Intel Quartus Prime* project
    * The project configurations will then be used to build the bootable image 
    * You can also use the default Quartus Prime project as shown in the previous [guide](6_newFPGAconf.md)
    * Note: The project compilation must be successfully done

**The Quartus Project folder should now look like this:**
![Alt text](project_folder.png?raw=true "Screenshot of the Quartus Prime Project")
<br>

* Navigate with the Linux terminal into this folder inside your Quartus Project 
    ````shell 
    cd socfpgaPlatformGenerator
* Start the Python script and follow the instructions
    ````shell
    python3 makersyoctoSDImage.py
    ````
    * Note: The execution with root (*"sudo"*) privileges is not allowed


## Understand the internal folder structure

The following table shows the internal folder structure of the in the last step downloaded "*SD-Folder*":

 | **File/Folder Name** | **Description** | **Origin** | 
 |:--|:--|:--|
 | \"Board_DE0NANOSOC\" | Contains **board specific files** for the *Terasic DE0-Nano SoC*  (*Cyclone V*) development board | *SD-Folder* |
 | \"Board_DE10NANO\" | Contains **board specific files** for the *Terasic DE10-Nano*  (*Cyclone V*) development board |*SD-Folder* |
 | \"Board_DE10STD\" | Contains **board specific files** for the *Terasic DE10-Standard (*Cyclone V*) development board |*SD-Folder* |
 | \"Board_HAN\" | Contains **board specific files** for the *Terasic HAN Pilot* (*Arria 10*) development board |*SD-Folder* |
 | \"SoCFPGA_A10\" | Contains **SoC-FPGA specific files** for the *Intel Arria 10 SX* SoC-FPGA | *SD-Folder* |
 | \"SoCFPGA_CY5\" | Contains **SoC-FPGA specific files** for the *Intel Cyclone V* SoC-FPGA |*SD-Folder* |
 | \"ubootDefaultSFP\" | Contains the default pre-compiled u-bootloader (Can be used instead to re-build one) | *[socfpgaPlatformGenerator](https://github.com/robseb/socfpgaPlatformGenerator)* |
 | \"ubootScript\" | Contains the default u-boot script | *[socfpgaPlatformGenerator](https://github.com/robseb/socfpgaPlatformGenerator)* |
 | \"LinuxBootImageFileGenerator\" | Contains the boot image file generator | *[LinuxBootImageFileGenerator](https://github.com/robseb/LinuxBootImageFileGenerator)*
 | \"makersyoctoSDImage.py\" | The Python build script |*SD-Folder* |
 | \"rootfsChange.py\"       | A Python help script to change the *rootfs* with *super user* privileges |*SD-Folder* |
 | \"rsyoctoConf.xml\"       | A XML file to configure the MAC-Address for each board and to add a description | *SD-Folder* |
 | \"SocFPGABlueprint.xml\"  | A XML file that describes the partition table for the final image |  *[socfpgaPlatformGenerator](https://github.com/robseb/socfpgaPlatformGenerator)* |
<br>

Every **Board- or SoC-FPGA specific folder** contains the following file structure:

|  **Folder name** | **Kind** | **Location on the rootfs**
|:--|:--|:--|
| "my_homepage" | **Homepages and web interfaces** | `/usr/share/apache2/default-site/htdocs`|
| "my_includes" | **C++ libraries**  | `/usr/include`|
| "my_rootdir" | **Home directory** | `/home/root`|
| "my_startUpScripts" | **Linux Shell start up scripts* ||

 | **Script name** | **Execution position** |
 |:--|:--|
 | *"my_startUpScripts/start_script.sh"* | *Before the NIC has started* | 
 | *"my_startUpScripts/run_script.sh"* | *After the network connection with SSH is established* (run level 5) | 
<br>    

  * For example the content of the pre-installed *run_script.sh* is attached here, that shows how it is possible to **interact in an easy way with the FPGA fabric**

  ```shell
    #!/bin/sh
    # Run script
    # This script will be called when the system has booted
    echo "*********************************"
    echo "rsyocto run script: started!"

    echo " Synchronization of the system time with an HTTP Server"
    htpdate -d -t -b -s www.linux.org
    echo "Time sync. done"

    # NW Up? => Turn HPS LED ON
    if grep -qF "up" /sys/class/net/eth0/operstate; then
       echo 100 > /sys/class/leds/hps_led0/brightness
       FPGA-writeBridge -lw 20 -h 01 -b
    fi
  ````
<br>

Files copied into these folders will automatically be written on the depending *rootfs* locations. Files with the same name will always overwritten by the file of the board specific folder.
These folders can also contain the *rootfs*-, Linux Device Tree, or *zImage*-file for the Linux distribution. These files must have the following syntax:

|  **File name** | **Description**  | **Final partition location** | **Final Name inside the partition** |
|:--|:--|:--|:--| 
| \"socfpga_XXX.dts\" | Linux Device Tree | Pat.1 (*vfat*)| *Complied by the build script to:* **CY5:** "*socfpga_cyclone5_socdk.dtb*" **A10:** "*socfpga_arria10_socdk_sdmmc.dtb*" |
| \"socfpga_XXX.rbf\" | Default FPGA configuration file | Pat.1 (*vfat*)| "*Name of selected inside the u-boot script*" |
| \"rootfs_XXX.tar.gz\" | Linux compressed *rootfs* | Pat.2 (*ext3*)| "*unzipped by the build system*" |
| \"zImage_XXX\" | Compressed Linux Kernel | Pat.1 (*vfat*)| "*zImage*" |
<br>

**Note: XXX represents the board specific- or SoC-FPGA specific- suffix**

Inside **board specific folders** replace "*XXX*" with following:

|  **Suffix** | **Description**  | **Example** |
|:--|:--|:--|
|*\"nano\"* | identified the *Terasic DE10-Nano*  (*Cyclone V*) development board | "*socfpga_nano.dts*"|
|*\"std\"* | identified the *Terasic DE10-Nano*  (*Cyclone V*) development board | "*socfpga_std.dts*"|
|*\"de0\"* | identified the *Terasic DE0-Nano SoC*  (*Cyclone V*) development board | "*socfpga_de0.dts*"|
|*\"han\"* | identified the *Terasic HAN Pilot*  (*Arria 10*) development board | "*socfpga_han.dts*"|

Inside **SoC-FPGA specific folders** replace "*XXX*" with following:

|  **Suffix** | **Description**  | **Example** |
|:--|:--|:--|
|*\"cy5\"* | identified the *Intel* *Cyclone V* SoC-FPGA | "*socfpga_cy5.dts*"|
|*\"a10\"* | identified the *Intel* *Arria 10 SX* SoC-FPGA | "*socfpga_a10.dts*"|
<br>

During further execution the Python build system will create new folders inside the *socfpgaPlatformGenerator* directory:
 | **File/Folder Name** | **Description** |
 |:--|:--|
 | \"toolchain\" | Contains the automatically installed *limaro* cross-platform toolchain   |
 | \"Image_partitions\" | Contains a sup folder for every disk image partition. Files copied here will be pre-installed onto the depending partition |
 <br>

The "*rsyoctoConf.xml*" XML file is used to assign the **MAC-Address** to each development board. This address will then written to the Linux Device tree. In the following paragraph the content of the  "*rsyoctoConf.xml*" file is added. Change it for your requirements!
````xml
<?xml version="1.0" encoding = "UTF-8" ?>
<!-- rsyocto Linux configuration file -->
<!-- Used by the Python script "makersyoctoSDImage.py" -->
<rsyocto>
<!-- For the assignment of the MAC Address for each board -->
<board folder_name="Board_DE10NANO"   mac_addrs="d6:7d:ae:b3:0e:ba"/> 
<board folder_name="Board_DE10STD"    mac_addrs="d6:7d:ae:b3:0e:bb"/> 
<board folder_name="Board_HAN"        mac_addrs="d6:7d:ae:b3:0e:bc"/> 
<board folder_name="Board_DE0NANOSOC" mac_addrs="d6:7d:ae:b3:0e:bd"/> 

<!-- For documentation with the Linux Kernel Version, Build date -->
<!-- and a feature description -->
<distro yocto_build="21-06-20" kernel_name ="linux-socfpga 5.5" description_txt="-- MAIN FEATURES: \n
	  python3, pip3, django 3.01, adminLTE, sqlite, openSSH Server, apache2, \n
	  php, gcc, gcc++, make, cmake, wget, curl, gdb server, gatord, time, nano, \n
	  minicom, i2c-tools, spi-tools, usbutils, ethtool, iputils, git, can-tools, \n
	  rstools, opkg, update-rc.d, crontab, devmem, iproute2, devmem, iproute2, iw \n
      -- FPGA: \n
	  Sys_ID, LEDs, Switches, ADC, Seven Segment Display, Display ... \n
      -- INCLUDE: \n
	 Intel hwlib \n
      -- WEBITERFACE: \n
	 Pinout- and Info-Page \n"/>
</rsyocto>
````
<br>


The following table summarizes the required file locations for *Intel* SoC-FPGAs:

| Partition Number | File System Type | Required Files | Note 
|:--|:--|:--|:--|
| **1** | *vfat* | Linux compressed Kernel file (*zImage*) | |
| **1** | *vfat* | Linux Device Tree File         (*.dts*) |  Will be compiled by the script |
| **1** | *vfat* | *u-boot* boot script (*.script*) | Will be compiled by the script |
| **1** | *vfat* | FPGA configuration file (*.rbf*) | Will be created with the *Intel Quartus Project* |
| **2** | *ext3* | compressed root file system (*.tar.gz*) | Will be unzipped by the script |
| **3** | *RAW* | executable of the bootloader (*.sfp*) | Will be generated by the script |
<br>

The other XML file is called "*SocFPGABlueprint.xml*". It is used by the `LinuxBootImageFileGenerator` to define the partition table of the final bootable image. Here it is enabled to change or to add new partitions to the image. However, the default configuration already allows to boot an embedded Linux on an Intel SoC-FPGA. The "\*"* is used to select the dynamic size mode. That means the script will calculate the required file size for inserting the selected files for all partitions.
 The offset value defines additional space. **Change the offset value of the partition with the type "*ext3*" (Id. 2) to increase the free avalibile diskspace on the *rootfs*.**  
     
The following lines show the XML file of a partition configuration for *Intel* *SoC-FPGAs*.
````xml
<?xml version="1.0" encoding = "UTF-8" ?>
<!-- Linux Distribution Blueprint XML file -->
<!-- Used by the Python script "LinuxDistro2Image.py" -->
<!-- to create a custom Linux boot image file -->
<!-- Description: -->
<!-- item "partition" describes a partition on the final image file-->
<!-- L "id"        => Partition number on the final image (1 is the lowest number) -->
<!-- L "type"      => Filesystem type of partition  -->
<!--   L       => ext[2-4], Linux, xfs, vfat, fat, none, raw, swap -->
<!-- L "size"      => Partition size -->
<!-- 	L	    => <no>: Byte, <no>K: Kilobyte, <no>M: Megabyte or <no>G: Gigabyte -->
<!-- 	L	    => "*" dynamic file size => Size of the files2copy + offset  -->
<!-- L "offset"    => in case a dynamic size is used the offset value is added to file size-->
<!-- L "devicetree"=> compile the Linux Device (.dts) inside the partition if available (Top folder only)-->
<!-- 	L 	    => Yes: Y or No: N -->
<!-- L "unzip"     => Unzip a compressed file if available (Top folder only) -->
<!-- 	L 	    => Yes: Y or No: N -->
<!-- L "ubootscript"  => Compile the u-boot script file ("boot.script") -->
<!-- 	L 	    => Yes, for the ARMv7A (32-bit) architecture ="arm" -->
<!-- 	L 	    => Yes, for the ARMv8A (64-bit) architecture ="arm64" -->
<!-- 	L 	    => No ="" -->
<LinuxDistroBlueprint>
<partition id="1" type="vfat" size="*" offset="1M" devicetree="Y" unzip="N" ubootscript="arm" />
<partition id="2" type="ext3" size="*" offset="500M" devicetree="N" unzip="Y" ubootscript="" />
<partition id="3" type="RAW" size="*" offset="20M"  devicetree="N" unzip="N" ubootscript="" />
</LinuxDistroBlueprint>
````
<br>

<br>

## Execution steps of the Python build script
    
The Python script will go through the following major steps that specific user inputs requires and allows.

1. **Development Board selection**
    * Choose the development board for the final image
2. **Image Version selection**
    * Give the ouput image file a name with a version number (Syntax: "*rsyocto_X_XX.img*")
    * The Version number will be written for instace to the *rootfs* location ("*/usr/rsyocto/version.txt*")
    * By pressing ENTER a date code will be used instead (e.g. "*rsYocto_20200830_1825_D10NANO.img*")
3. **Check that the Quartus Prime Project is compatible to the selection**
    * In case the required SoC-FPGA device for the board is not the same as that on the *Quartus Prime Project* a warning will appear
    * Then a generation of a new FPGA configuration and the bootloader are not possible, the default files will be used
4. **Check that the Quartus Prime Project contains no non-licend IP**
    * In case a non-licend IP, for instace for an *Intel NIOS II* Soft-Core processor, a warning message will appear
    * Then a generation of a new FPGA configuration is not possible, the default ".rbf"-file  will be used instead
5. **Selection how the bootloader should be generated**
    * The following question box will appear
        ![Alt text](bootloaderGenQuestion.png?raw=true "Bootloader Generation Question")
    * Choose the way how to build the bootloader (*It is recommented to use the default one*)
    <br>

6. **In case the entire bootloader should be generated the script will do the following tasks**
	* Download the Limaro cross-platform toolchain 
	* Generate the *Board Support Package* (*BSP*) with the *Intel Embedded Development Suite* (*SoC EDS*)
	* Clone the (*u-boot-socfpga*)https://github.com/altera-opensource/u-boot-socfpga from Github
	* Run the *Intel SoC EDS filter script*
	* Allow deeper *u-boot* configuration with **menuconfig**
	* Make the *u-boot* bootloader for the Intel SoC-FPGA device
	* The generated executable will be copied to the RAW partition folder
6. **In case the default bootloader should be used**
    * A pre-build bootloader with a default configuration will be copied to the RAW partition folder
7. **Give the script super user privileges**
    * During the unzipping of the *rootfs* the script will ask for the super user (*sudo*) admin password
8. **Change the *rootfs* or add files to the Board- or SoC-FPGA specfic folders manually**
    * At this point the script will show the following message box:
        ![Alt text](CopyFilesMes.png?raw=true "Bootloader Generation Question")
    * Now it is enabled to copy or change files inside the partition folders (*"socfpgaPlatformGenerator/Image_partitions"*) by hand 

    The script will generate for each selected partition a depending folder. At this point it is enabled to drag&drop files and folders 
    to the partition folder. This content will then be included in the final image file. 
    Linux device tree- and archive-files, copied to the partition folder, will be automatically processed by the script in case these features were enabled for the partition inside the XML file. Of cause, archive files or un-compiled device tree files will not be added to the final image. It is also possible to add the content of the Board- or SoC-FPGA specfic folders as previously shown.

    The following illustration shows the generated folder structure with the previous XML configuration file.

    ![Alt text](FolderStrucre.png?raw=true "Example of the folder structure")

    Files copied to a partition folder will then be pre-installed onto the depending partition.
    *Note: On RAW partitions are only files allowed!*
    *Note: The *u-boot* script and the Linux device tree will be compiled in the next step!* 
    <br>

    * The following manual steps are for instance now allowed:
        * Change the *u-boot* boot script (*boot.script*)
        * Change the Linux Device Tree
        * Change files inside the Linux *rootfs* or copy one to it
        * Change or add files to the other partitions
    <br>

9. **Choose if the output image should be compressed**

    The Python script allows to compress the generated bootable image files as a *".zip"* archive files. 
    This can strongly reduce the image size. Tools, like "*rufus*" can process this "*.zip*" file directly and can bring it onto a SD-Card. 

10. **Callculation of all sizes of the partition table**
    
    The script will progress the data inside the Partition folders by compiling the Linux device tree, 
    the u-boot script and will display the partition sizes for the entire image partition of the bootable image file.
    In case the *u-boot* is configured to write the FPGA configuration the script will generate 
    the depending FPGA configuration file. This is only possible if no unlicensed IP is available inside the Quartus Prime Project. 
    For instance Quartus Prime projects containing an *Intel NIOS II* Soft-Core processor can not be generated. 
    The following inlustration shows the callcuated partition table for a custom *rsyocto* build:
  
    ![Alt text](partitionTable.png?raw=true "Partition table")
    <br>

11. **Generation of the bootable image file with custom configuration**
    
    In connection the Python script will use the [*LinuxBootImageFileGenerator*](https://github.com/robseb/LinuxBootImageFileGenerator) to build the finale bootable image file. 
    The file will be located inside the "*socfpgaPlatformGenerator*" folder. 
    This image file can be distributed and flashed to a bootable SD-Card as shown in the first Guide

<br>
<br>

___
[back](6_newFPGAconf.md)
[Back to the startpage](https://github.com/robseb/rsyocto)

