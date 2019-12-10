![Alt text](doc/symbols/rsYoctoLogo.jpg?raw=true "rsYocto Logo")

### *rsYocto* is an open-source embedded Linux System designed with the Yocto Project and optimized for Intel SoC-FPGAs (Intel Cyclone V and Intel Arria 10) to allow the best customization for the strong requirements of modern embedded applications.
<br>

*rsYocto* implements a **modern Linux Kernel** and brings a set of today fundamentally needed components to Intel SoC-FPGAs and help to **simplify the complex process of development** for FPGA-, Industrial 4.0-, Internet of Things- or deep learning applications.

To realise that **Python3** with the Python Package manager **PiP** and the **Apache Webserver** with **PHP** are all ready included. Thereby it is really easy to install Python applications from the *Raspberry Pi* on a powerful Intel SoC-FPGA. *rsYocto* is for is best optimization complete console based, but the Apache Webserver can bring any GUI to Computers, Smartphones or Tablets, by hosting for example a monitor web interface.

During development, a major concern was placed on the integration of **powerful and simple to install development IDEs** that do not require a JTAG-connection or any cross-building environment. *rsYocto* application can **build, deployed and even debugged over the network**. With the implementation of *Microsoft Visual Studio* and *Visual Studio Code* is a simple installment and quick jumpstart in the development process possible, because all required compilers run directly on *rsYocto*.

It is with the implementation of drivers for **all Hard-IP Interfaces** (e.g. **I²C, CAN,…**) and simple Linux test commands (e.g. **i2c-tools** or **can-utils**) ready for development of industrial connected solutions. With a single command is *rsYocto* capable to **load a new FPGA configuration** or to **read and write the AXI-Bridge Interface to the FPGA**.

The “*rsyoctoMakingSD*”- script allow developer to **customize the *rsYocto*-image** with the installment of their own software files or **FPGA configuration file, that will be configured on the FPGA fabric before the Linux boots**.

The final *rsYocto*-Image can be **installed** on a **SD-Card** with any commonly **used Boot-Image creating tools**. Versions are available for the **Terasic DE10 Standard-** (Cyclone V), **Terasic DE10 Nano-** (Cyclone V) and **Terasic Han Pilot** (Arria 10).

On the Terasic DE10 Nano board can be the  **Arduino Uno header** used to connect clients to a Hard-IP Bus, because the HPS interfaces with the pre installed configuration are routed to FPGA I/O-Pins. 
<br>

# Features of *rsYocto*

![Alt text](doc/symbols/rsYoctoLayers.jpg?raw=true "System Overview")
**System Overview of rsYocto**
___
**Main pre-installed Linux commands**

`arch` `arm-poky-linux-gnueabi-gcc-nm` `automake` `addgroup` `arm-poky-linux-gnueabi-ar` 
`adduser` `arm-poky-linux-gnueabi-cpp` `asc2log` `autoupdate` `agetty` `ash` `apachectl` 
`arm-poky-linux-gnueabi-g++` `autoconf` `ar` `arm-poky-linux-gnueabi-gcc` `autoheader`
`b2sum` `bg` `bzegrep` `bash` `blkdiscard` `bunzip2` `bzcat` `bzfgrep` `bzless` `basename` 
`bcmserver``busybox` `bzcmp` `bzip2``c++` `cangen` `ccache` `chpasswd` `csplit` `cangw` `chgpasswd`
`compgen` `csplit.coreutils` `canlogserver` `cfdisk` `chgrp` `chroot` `cal` `canplayer`  `chgrp.coreutils` `chroot.coreutils` `cmp.diffutils` `compopt` `ctrlaltdel` `cal.util-linux` `cansend` `chattr` `chmem` `chrt` `caller` `cansniffer` `chcon`
`chrt.util-linux` `colcrt` `coproc` `cut.coreutils` `can-calc-bit-timing` `chcon.coreutils` `chmod.coreutils` `chsh` `colrm`
`cvtsudoers` `canbusload` `cat` `chcpu` `choom` `cp.coreutils` `candump` `chvt` `comm` `cpio` `canfdtest` `cc` `chfn` 
`chown.coreutils` `cksum` `comm.coreutils` `cpp`
`date` `fdisk` `FPGA-gpiRead` `FPGA-gpoWrite` `FPGA-readBridge` `FPGA-readMSEL` `FPGA-resetFabric` `FPGA-status` `FPGA-writeBridge` `FPGA-writeConfig`
`g++` `gdb` `gunzip` `gcc` `gdbserver` `gzip` `hostname` `httpd`  `hexdump` `i2cdetect` `i2ctransfer` `i2cdump` `i2cget` `i2cset` `lscpu` `lsipc`
`microcom` `minicom` `mount` `mkdir` `php` `pip3` `phpdbg` `pydoc3` `python3` `python3.7` `rsync` `route`
`tee`  `tftp` `top` `tac.coreutils` `tcf-agent` `tail` `tcf-client` `telinit` `time` `ttytclsh` `telnet` `tar`              
___

**Build, deployed and debugged your applications over the network**

![Alt text](doc/symbols/rsYoctoInterfaces.jpg?raw=true "poerfull remote developemed IDEs")
**Poerfull remote developemed IDEs and Web server to install your web interface**
<br>
<br>

# Tutorials
The entries guide in the usege and the development of rsyocto applications is parted in following levels: 

| Level | Objective | Guide
|:--|:--|:--|
| 1 | **Booting rsyocto on your Board** | [**Getting started Guide**](doc/guides/1_Booting.md)
| 2 | **Using SSH to controll and reconfige the FPGA** |[Guide](doc/guides/2_SSH_FPGA.md)
| 3 | **Debugging C++ applications remotely** | [Guide](doc/guides/3_CPP.md)
| 4 | **Debugging Python applications remotely** | [Guide](doc/guides/4_Python.md)
| 6 | **Analyze your applications with ARM Streamline** | [Guide](doc/guides/5_Streamline.md)
| 7 | **Developing a new FPGA configuration**| [Guide](doc/guides/6_newFPGAconf.md)
<br>

# Built With
* [Intel SoC FPGA Embedded Development Suite (EDS) 18.1.0.625](https://www.intel.com/content/www/us/en/software/programmable/soc-eds/overview.html) - Linux
* [Intel Quartus Prime 18.1.0 Lite Edition](https://www.intel.com/content/www/us/en/software/programmable/quartus-prime/download.html) - Cyclone V
* [Intel Quartus Prime 18.1.0 Standard Edition](https://www.intel.com/content/www/us/en/software/programmable/quartus-prime/download.html) - Arria 10
* [The Yocto Project](https://www.yoctoproject.org/) 
* [meta-altera](https://github.com/kraj/meta-altera) 
* [meta-openembedded](https://github.com/openembedded/meta-openembedded)
  * [meta-python](https://github.com/openembedded/meta-openembedded/tree/master/meta-python) 
  * [meta-webserver](https://github.com/openembedded/meta-openembedded/tree/master/meta-webserver)
  * [meta-networking](https://github.com/openembedded/meta-openembedded/tree/master/meta-networking) 
* [meta-linaro](https://git.linaro.org/openembedded/meta-linaro.git)
* [meta-rstools](https://github.com/robseb/meta-rstools)
<br>

# Development process of *rsYocto*

![Alt text](doc/symbols/rsYoctoRequieredBuildingSteps.jpg?raw=true "rsYocto requiered building steps")
**Applied Build Flow to create *rsYocto***

# Author

* **Robin Sebastian**

*rsYocto* was developed a year ago as an student project and fruther for my master thesis optimized.
No companys were involved in this project. I‘m looking for an interesting job offer up to summer 2020 witch possibly connects my mentioned workfields.
