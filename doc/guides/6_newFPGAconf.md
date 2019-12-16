
#  	Developing a new FPGA configuration

*rsYocto* allows to change the FPGA configuration with an single Linux command. That was shown in chapter 2 with:
  ````bash
      FPGA-writeConfig  -f gpiConf.rbf
  ````   
   The required steps to generate with a Quartus Prine Project the right configuration file are:
   1. **for the Arria 10:**
      * Be sure that "**Enables the HPS early release of HPS IO**" is in the Quartus Prime- and HPS- Settings enabled
          ![Alt text](Arria10Conf.jpg?raw=true "Quartus connfig for Arria 10")
      * Execute following EDS-Shell command:
        ````bash
          quartus_cpf -c --hps -o bitstream_compression=on rsHAN.sof socfpga.rbf
        ````
        * SOF here: `rsHAN.sof` 
        * RBF here: `socfpga.rbf`
      * With this command are two configuration files for the HPS- and Menory-System and for everything else generated
        * Output: `socfpga.periph.rbf`and `socfpga.core.rbf`
        
  2. **for the Cyclone V:**
      * For **configuration of the FPGA with *rsYocto*** use these export settings: 
        * Type: `Raw Binary File (.rbf)` 
        * Mode: `Passive Paralle x16`  
       
            ![Alt text](fpgaConfSettings1.png?raw=true "FPGA Configuration settings 1")
            
      * For **configuration of the FPGA  during the boot** use these export settings: 
        * Type: `Raw Binary File (.rbf)` 
        * Mode: `Passive Paralle x8`  
       
            ![Alt text](fpgaConfSettings2.png?raw=true "FPGA Configuration settings 2")
        
___
## Including the FPGA-Configuration files and other files or to the SD-Image or chnaging the Device Tree
   With the *rsYocto*-"`makersYoctoSDImage.py`" script is a simple way avelibil to change Image automatically given. 
   This script uses internaly the ALTERA Script `"make_sdimage.py"`, that only works with CentOS.
   
   The following step-by-step guide shows how to setup a **CentOS VM**:
   
1. Download the [CentOS 6.5 64-Bit ISO Image](http://vault.centos.org/6.5/isos/x86_64/)
2.  Install a Virtual Machine Hypervisor, like VMware Workstation Player or Virtual Box 
3. Create a new CentOS VM 
4.	After CentOS is installed as a Live-DVD burn it to the HDD
    *	Start the Application “Install to Hard Drive” from the Desktop
    *	Follow the Installer Wizard of this Application with the default Settings 
    *  At the end choose: “write changes to the Disk” and later on restart the VM manually  
5. On CentOS install the device Tree compiler Tool `dtc`
6. Dowload the "**rsyocto_SDxx-Folder**" from the "**relases Part**" of this Github repository to CentOS
      
    
| File Name | Platform / Board | Origin | Description | Internal name (inside the script)
|:--|:--|:--|:--|:--|
|\"makersYoctoSDImage.py\"| *all*| by hand | the automatic *rsYocto* script | *executed* | 
|\"make_sdimage.py\"|*all*| wget | Altera SD image making script | *executed* | 
|\"infoRSyocto.txt\"|*all*| by hand | rsYocto splech screen Infos | *integreted* | 
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
7. With the Text-File \"infoRSyocto.txt\" it is posible to add some notes to the final image
  * The MAC address can also be changed here:
     ````
     -- MAC: d6:7d:ae:b3:0e:ba
     ````

7. Replace the `.rbf-File` with a new FPGA configuration file
8. It is also allowed to delete files for unused platforms and devices
9. At this point it is also possible to change the `Device Tree`of *rsYocto*
  * Open the `dts-File` with a editor 
9. Open the Linux console and navigate into the SD folder
10. Start the building script with: 
    ````bash  
    sudo python makersYoctoSDImage.py   
    ````
11. The script will be ask for a version Number and will wait for user changes
12. Now it is possible to pre-installed files to the Image by adding the files to:
  
  |  Folder name | Kind | Location on the rootfs
  |:--|:--|:--|
  | "my_homepage" | **Homepages and web interfaces** | `/usr/share/apache2/default-site/htdocs`|
  | "my_includes" | **C++ libraries**  | `/usr/include`|
  | "my_rootdir" | **Home directory** | `/home/root`|
  
13. Press ENTER to generate the new *rsYocto"-Image 
14. The final script can be deploded to any SD Card


