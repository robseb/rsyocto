
# Developing a new FPGA configuration

*rsYocto* allows to chnage the FPGA configuration with an single Linux comand. That was shown in chaper 2 with:
  ````bash
      FPGA-writeConfig  -f gpiConf.rbf
  ````    
   The requiered steps to generate with Qurtus Project the right configuration file:
   1. On Arria 10: 
      * Be shure that "**Enables the HPS early relase of HPS IO**" is in the Qurtus Prime- and HPS- Settings enabeled
      * Execute following EDS-Shel command:
        ````bash
          quartus_cpf -c --hps -o bitstream_compression=on rsHAN.sof socfpga.rbf
        ````
      * With this command are to configuration file for the HPS- and Menory-System and for the reset greatedet
  2. Cyclone V: 
      * For **configuring the FPGA with *rsYocto*** use these export settings: 
        * Type: `Raw Binary File (.rbf)` 
        * Mode: `Passive Paralle x16`  
       
            ![Alt text](fpgaConfSettings1.png?raw=true "FPGA Configuration settings 1")
            
      * For **configuring during the boot** use these export settings: 
        * Type: `Raw Binary File (.rbf)` 
        * Mode: `Passive Paralle x8`  
       
            ![Alt text](fpgaConfSettings2.png?raw=true "FPGA Configuration settings 2")
        
## Include the FPGA-Configuration file to the SD-Image  
   With the *rsYocto*- "*makeAutoSDImage.py*" is an esay way avelibil to chnage build automaticly given. 
   This script uses internaly the ALTERA Script `"make_sdimage.py"`, that only works on CentOS. 
   The following step-by-step guide shows how to setup a CentOS VM for the generation of the *rsYocto*-Image:
   
1. Download the  [CentOS 6.5 64-Bit ISO Image](http://vault.centos.org/6.5/isos/x86_64/)
2.  Install a Virtual Machine Hypervisor, like VMware Workstation Player or Virtual Box 
3. Create a new CentOS VM 
    *	Use the “New Virtual Machine Wizard” (see Step 3 on) again 
    *	32GB system storage should be enough for our task
4.	After CentOS is installed as a Live-DVD burn it to the HDD
    *	Start the Application “Install to Hard Drive” from the Desktop
    *	Follow the Installer Wizard of this Application with the default Settings 
    *  At the end choose: “write changes to the Disk” and later on restart the VM manually  
5. On CentOS install the device Tree compiler Tool `dtc`
6. Dowload the "**rsyocto_SDxx-Folder**" from the "**relases Part**" of this Github repositorie to CentOS
      
      
| File Name | Platform / Board | Origin | Discription | internal remaing name 
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

**The Contet of the "rsyocto_SDxx-Folder"** 

7. Relace the `.rbf-File` with a new FPGA configuration file
8. It is also allowed to delate files for unsued plattforms or devices
9. At this point it is also posible to change the `Device Tree`of *rsYocto*
  * Open the `dts-File` with a editor 
9. Open the Linux console and navigate into the SD-folder
10. Start the building script with: 
    ````bash  
      sudo python makersYoctoSDImage.py   
    ````
11. The script will be ask for a Verison No and will wait for user chnages

12. Now it is posible to pre-insataled files to the Image by adding the files to:
  
  |  Folder name | Kind | location on the rootfs
  |:--|:--|:--|
  | "my_homepage" | homepages and webinterfaces | `/usr/share/apache2/default-site/htdocs`|
  | "my_includes" | C++ libaries  | `/usr/include`|
  | "my_rootdir" | home directory | `/home/root`|
13. Press ENTER to generate your *rsYocto"-Image 
14. The final script can be deploded to a SD-Card


