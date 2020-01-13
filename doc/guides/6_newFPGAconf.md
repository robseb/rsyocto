[back](5_Streamline.md)

#  	Developing a new FPGA configuration

*rsYocto* allows with the layer `meta-rstools` to change the FPGA configuration with a single Linux command. That was shown in chapter 2 with:
  ````bash
      FPGA-writeConfig  -f gpiConf.rbf
  ````   
  
   **The required steps to generate right configuration files with a Quartus Prime Project are:**
   1. **for the Arria 10:**
      * Be sure that "**Enables the HPS early release of HPS IO**"  in the Quartus Prime- and HPS- Settings is enabled
           * Parts the configuration in a peripheral- and the core- configuration 
           * This allows to hold for example the memory configuration of the HPS during FPGA configuration changes 
           * For more information please visit the [Intel Arria 10 documentation](https://www.intel.com/content/www/us/en/programmable/documentation/mzh1527115949958.html) page
              ![Alt text](Arria10Conf.jpg?raw=true "Quartus connfig for Arria 10")
      * Execute following EDS-Shell command:
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
        * Mode: `Passive Paralle x16`  
       
            ![Alt text](fpgaConfSettings1.png?raw=true "FPGA Configuration settings 1")
            
      * For **configuration of the FPGA  during the boot** use these export settings: 
        * Type: `Raw Binary File (.rbf)` 
        * Mode: `Passive Paralle x8`  
       
            ![Alt text](fpgaConfSettings2.png?raw=true "FPGA Configuration settings 2")
        
___
## Including the FPGA-Configuration files and other files to the SD-Image or changing the Device Tree
   With the *rsYocto*-"`makersYoctoSDImage.py`" script a simple way of changing the Image automatically is available. 
   This script uses internally the ALTERA Script `"make_sdimage.py"`, that only works with CentOS.
   
   The following step-by-step guide shows how to setup a **CentOS VM**:
   
1. Download the [CentOS 6.5 64-Bit ISO Image](http://vault.centos.org/6.5/isos/x86_64/)
2.  Install a Virtual Machine Hypervisor, like *VMware Workstation Player* or *Virtual Box* 
3. Create a new CentOS VM 
4.	After CentOS is installed as a Live-DVD burn it to the HDD
    *	Start the Application “Install to Hard Drive” from the Desktop
    *	Follow the Installer wizard of this Application with default Settings 
    *  At the end choose: “*write changes to the Disk*” and later on restart the VM manually  
5. On CentOS install the device Tree compiler Tool `dtc`
6. Dowload the "**rsyocto_SDxx-Folder**" from the "**releases Part**" of this Github repository to CentOS
      
    
| File Name | Platform / Board | Origin | Description | Internal name (inside the script)
|:--|:--|:--|:--|:--|
|\"makersYoctoSDImage.py\"| *all*| by hand | the automatic *rsYocto* buliding script | *executed* | 
|\"make_sdimage.py\"|*all*| wget | Altera SD image making script | *executed* | 
|\"infoRSyocto.txt\"|*all*| by hand | rsYocto splech screen Infos | *integreted* | 
|\"network_interfaces.txt\"|*all*| by hand | the Linux Network Interface configuration file (*/etc/network/interfaces*) | *interfaces* | 
| \"rootfs_a10 .tar.gz\"|*all*| Yocto Project |compresed rootFs file for Arria 10 | *unziping* |
| \"rootfs_cy5.tar.gz\"|*all*| Yocto Project |compresed rootFs file for Cyclone V | *unziping* |       
|\"preloader_cy5.bin\"|*CY5*| EDS | prestage bootloader | *preloader-mkpimage.bin* | 
|\"preloader_a10.bin\"|*A10*| EDS | prestage bootloader | *uboot_w_dtb-mkpimage.bin* | 
|\"uboot_cy5.img\"|*CY5*| EDS | Uboot bootloader | *u-boot.img* | 
|\"uboot_a10.img\"|*A10*| EDS | Uboot bootloader | *u-boot.img* | 
|\"uboot_cy5.scr\"|*CY5*| by hand | Uboot bootloader script | *u-boot.scr* |   
|\"uboot_a10.scr\"|*A10*| by hand | Uboot bootloader script | *u-boot.scr* |
|\"zImage_cy5\"|*CY5*| Yocto Project | Linux Kernel | *zImage* |   
|\"zImage_a10\"|*A10*| Yocto Project | Linux Kernel | *zImage* |
|\"socfpga_cy5.dts\"|*CY5*| by hand | Linux Device Tree | *socfpga.dtb* |
|\"socfpga_a10.dts\"|*A10*| by hand | Linux Device Tree | *socfpga_arria10_socdk_sdmmc.dtb* |
|\"socfpga_nano.rbf\"|*DE10 Nano*| Quartus Prime | FPGA Config  | *socfpga.rbf* |
|\"socfpga_std.rbf\"|*DE10 Standart*| Quartus Prime | FPGA Config  | *socfpga.rbf* |
|\"socfpga_han_periph.rbf\"|*HAN Pilot*| EDS | FPGA Periph Config (Memory, ...)  | *socfpga.periph.rbf* |
|\"socfpga_han_core.rbf\"|*HAN Pilot*| EDS | FPGA Core Config (user)  | *ghrd_10as066n2.core.rbf* |
|\"socfpga_nano_linux.rbf\"|*DE10 Nano*| Quartus Prime | FPGA Config for written by Linux  | *running_bootloader_fpgaconfig.rbf* |          
|\"socfpga_std_linux.rbf\"|*DE10 Standart*| Quartus Prime | FPGA Config for written by Linux |*running_bootloader_fpgaconfig.rbf* |

**The Content  of the "rsyocto_SDxx-Folder"** 

 7. With the Text-File \"infoRSyocto.txt\" it is possible to add some notes to the final image
  * The **MAC address** can also be changed here:
     ````
     -- MAC: d6:7d:ae:b3:0e:ba
     ````
8. Change if necessary the network configurations by adding the *network_interfaces.text*. This file will be used as Linux */etc/network/interfaces* file
  * For using a **static iPv4-Address** instead of a dynamic one:
    * Remove following line from the *network_interfaces.txt*-file:
      ````txt 
      iface eth0 inet dhcp
      ````
    * Insert instead of (here with the iPv4-Address *192.168.0.150* and the gateway *192.168.0.100*):
      ````txt
      iface eth0 inet static
        address 192.168.0.150
        netmask 255.255.255.0
        network 192.168.0.0
        gateway 192.168.0.100
      ````
9. **Replacing the pre-installed *rsYocto* files with your files**
  * It is also allowed to **delete files for unused platforms and devices** or to **replace other self developed files**
    * For example for changing the `Device Tree`
      * Open the `dts-File` with an editor 
  * An example is available [here](https://github.com/robseb/HPS2FPGAmapping)  
10. **Open the Linux console and navigate into the SD-folder**
11. For allocating more **user memory space** edit the following line inside the *makersYoctoSDImage.py* script
    ````python
    #
    # #################### CHANGE HERE THE ADDITIONAL ROOTFS SPACE FOR USER SPACE ####################
    #
    # Size of the available User Space in Mega Byte (MB) 
    #
    USER_SPACE_SIZE_MB =600 # 600MB 
    #
    ###################################################################################################
    #
    #
  
    ````
12. **Start the building script with:**
    ````bash  
    sudo python makersYoctoSDImage.py   
    ````
13. The script will ask for a **version Number** and will wait for user changes
14. Now it is possible to **pre-install files to the image** by adding the files to:
  
  |  **Folder name** | **Kind** | **Location on the rootfs**
  |:--|:--|:--|
  | "my_homepage" | **Homepages and web interfaces** | `/usr/share/apache2/default-site/htdocs`|
  | "my_includes" | **C++ libraries**  | `/usr/include`|
  | "my_rootdir" | **Home directory** | `/home/root`|
  
15. At this point it is also possible to **change Linux startup scripts** 
  * If necessary edit following script files
  
    | **Script name** | **Execution position** |
    |:--|:--|
    | *"my_startUpScripts/start_script.sh"* | *Before the NIC has started* | 
    | *"my_startUpScripts/run_script.sh"* | *After the network connection with SSH is established* | 
    
  * **Note:** For more information about the execution position look at the table on chapter 1
  
  * For example the content of the pre-installed *run_script.sh* is attached here, that shows how it is possible to **interact in a easy way with the FPGA fabric**

  ```console
    #!/bin/sh
    # Run script
    # This script will be called when the system has booted
    echo "*********************************"
    echo "rsYocto run script: started!"

    echo " Synchronization of the system time with a HTTP Server"
    htpdate -d -t -b -s www.linux.org
    echo "Time sync. done"

    # NW Up? => Turn HPS LED ON
    if grep -qF "up" /sys/class/net/eth0/operstate; then
       echo 100 > /sys/class/leds/hps_led0/brightness
       FPGA-writeBridge -lw 20 -h 01 -b
    fi
  ````

13. Press ENTER to generate the new *rsYocto"-Image 
14. The final image can be deployed to any SD-Card as shown in chapter 1



 [Back to the startpage](https://github.com/robseb/rsyocto)
 
