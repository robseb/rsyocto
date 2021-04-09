
<p align="center">
	<img margin-right="100%" src="doc/symbols/rsYoctoLogo.jpg">
</p>

### *rsyocto* is an open source embedded Linux Distribution designed with the Yocto Project and with a custom build flow to be optimized for Intel SoC-FPGAs (*Intel Cyclone V* and *Intel Arria 10* with a *ARM CORTEX-A9*) to achieve the best customization for the strong requirements of modern embedded SoC-FPGA applications.

<p align="center">
	 <img src="https://img.shields.io/static/v1?label=Status&message=active&color=orange">
	 <a href="https://github.com/robseb/rsyocto/releases">
	 	<img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/robseb/rsyocto">
		<img alt="GitHub Releases" src="https://img.shields.io/github/downloads/robseb/rsyocto/latest/total"> 
		<img alt="GitHub Releases" src="https://img.shields.io/github/downloads/robseb/rsyocto/total">
	 </a>	 
	 <img src="https://img.shields.io/static/v1?label=Supported+SocFPGA&message=Intel+Arria10,+Cyclone+V&color=blue">
	 <a href="https://github.com/robseb/rsyocto/issues">
		<img alt="GitHub issues" src="https://img.shields.io/github/issues/robseb/rsyocto">
	 </a>
	 <img src="https://img.shields.io/badge/License-MIT%20-yellow.svg" alt="license">
</p>

___


`I'm working on the new rsyocto release! This branch is work under process! Please use the MASTER branch!`


*rsyocto* implements a **modern Linux Kernel (linux-socfpga 5.10)** and brings a set of today fundamentally needed components to **Intel SoC-FPGAs** to helps to **simplify the complex process of development** for FPGA-, Industrial 4.0-, Internet of things- (IoT), automotive- and deep learning (AI) accelerator- applications.

To realize that **Python3** with the Python Package manager **pip (PyPI)** and the **Apache Webserver** with **PHP** are already included. Thereby it is really easy to install Python applications from the *Raspberry Pi* on a powerful Intel SoC-FPGA. *rsyocto* is for its best optimization complete console based, but the Apache Webserver can bring any modern GUI to Computers, Smartphones or Tablets, by hosting for example a monitor web interface. For that the Python Web framework **Django 3.0** is pre-installed.

During development, a major concern was placed on the integration of **powerful and simple to install development IDEs** that do not require a JTAG-connection or any cross-building environment. All kinds of *rsyocto* applications and parts can be **build, deployed and even debugged over the network** (fully rootable over the Internet). With the implementation of *Microsoft Visual Studio* and *Visual Studio Code* a simple installment and quick jump start in the development process is possible, because all required compilers run directly on *rsyocto*. The custom developed build system goes even a step further. 

*rsyocto* was designed with an automatically Python based `build system`. That generates an highly optimized **customize *rsyocto*-image** with the installment of users **private** **applications**, **boot configurations**, **scripts**, **FPGA configuration files, that will be configured on the FPGA Fabric before the Linux boots** and a lot more with a only Intel Quartus Prime FPGA project. This feature enables users, without the requirement of deep Linux knowledge, to design own *rsyocto* flavors with its own FPGA projects for complex Intel SoC-FPGAs. The `build system` generates the 3-stage bootloader, finds the right embedded Linux Distribution files, configures the partitions of the final image in the right way, configures the`OpenSSH Server` and automates a lot more with a one shell single command.    

*rsyocto* is with the implementation of drivers for **all Hard-IP Interfaces** (e.g. **I²C-, CAN-BUS,…**), **all Interfaces between hard processor system (HPS) and the FPGA Fabric**  and simple Linux test commands (e.g. **i2c-tools** or **can-utils**) ready for the development of industrial connected solutions. For instance, with a single command *rsyocto* is capable to **load a new FPGA configuration** (`FPGA Manager`) or to **read and write the ARM AXI-Bridge Interface to the FPGA Fabric**. The Linux test commands allow in a simple fashion to communicate with the FPGA Fabric via all available interfaces, such as **Lightweight HPS-to-FPGA-** (`lwhps2fpga`) , **HPS-to-FPGA-Bridge**  (`hps2fpga`) , **shared-memory** (`hps2sdram`) or **general purpose signals** (`gpi` and `gpo`). Python- and C++- demo applications show a powerful way with a high throughput to interact with FPGA Soft-IP. 


The final *rsyocto*-Image can be **installed** on a **SD-Card** with any commonly **used Boot-Image creating tools**. Versions are available for the **Terasic DE10 Standard-** (Cyclone V SoC-FPGA), **Terasic DE10 Nano-** (Cyclone V SoC-FPGA), **Terasic Han Pilot** (Arria 10 SX SoC-FPGA) and **Terasic DE0-Nano SoC** (Cyclone V SoC-FPGA).

On the Terasic DE10 Nano board the **Arduino Uno header** can be used to connect external devices to a Hard-IP Bus, because the HPS interfaces with the pre-installed configuration are routed to FPGA I/O-Pins. An example shows how to use *rsyocto*, the **FPGA-to-HPS-Bridge** to access Hard-IP of the HPS with a **NIOS II Soft-Core Processor** running **FreeRTOS**. **NIOS II Eclipse platforms** can also be generated automatically.

<br>

I noticed that right now only desktop Linux systems, like *Ubuntu*, are available for *free*. In my opinion they are not designed for embedded SoC-FPGAs and therefore, they cannot be considered for long-term embedded systems.

That was for me the starting point to try to develop my own fully optimized Linux distribution. Shortly after, I announced that the *Intel* development tools and documentations for HPS development are not nearly as good as those for the FPGA part. At the beginning it was really complicated to get anything running. 
After a hard time, I'm able to present this first working project. To get there, **I had to develop my own approach that I think is the best for embedded use-case by designing my own build flow with my own Python scripts**.

I think nearly everybody will have the same problems that I had during the development. For that reason, **I try to give everybody a solution for their rapid prototyping**.
Within this repository I have also integrated a step by step guide to show my solution with the openEmbedded Yocto project and the *Intel SoC EDS*.

**With my first versions I got only positive feedback from the community. However,...**

**This project is by far not finished and issue free. I will continue my work and upload newer versions. I invite everybody to submit issues, comments and ideas and to support me in other ways...**

<br>


# System Overview of rsyocto

![Alt text](https://raw.githubusercontent.com/robseb/rsyocto/rsYocto-1.042/doc/symbols/rsYoctoLayers.jpg?raw=true "System Overview")
___

**Build, debug and deploy your applications over the network**

![Alt text](https://raw.githubusercontent.com/robseb/rsyocto/rsYocto-1.042/doc/symbols/rsYoctoInterfaces.jpg?raw=true "powerfully remote development IDEs")
**Ready for powerful remote development IDEs and fitted with a Web server to host modern web applications**
<br>
<br>

# Key Advantages
* **Embedded Linux specially developed for Intel SoC-FPGAs**
    * **Linux Kernel 5.11** ([*Source*](https://github.com/altera-opensource/linux-socfpga/tree/socfpga-5.11))
* Full **usage of the Dual-Core ARM (*ARMv7-A*) Cortex-A9** with
	* The **ARM** (*SIMD*) **NEON-Engine**
	* The **Vector Floating Point Unit (*VFP*)** 
	* The **ARM *Thumb-2* Instruction Set**
    * The **ARM *PL390* Generic Interrupt Controller (GIC)** 
    * The of the **ARM TrustZone** for ARMv7-A and **Arteris  *FlexNoC*** Network-on-Chip Interconnect for the *Intel Arria 10 SX*
    * The **ARM CoreSight Debug and Trace Engine** with *ARM Development Studio (DS-5)* support
    * The **external memory interface controller** (*EMIF*) (*SDRAM DDR3/DDR4 controller*) of the *Intel Arria 10 SX* with **Early I/O enabled** 
    
* For the best performance completely custom optimized 
* **Console based** (**GUI less**) with `Busybox`
* **Watchdog** timer is enabled    
<br>

* **FPGA Fabric configuration during the boot (*u-boot script*) and with a single Linux command**
* **All Bridge Interfaces between the HPS and FPGA are tested, enabled and ready for use!**
* **Tools to interact with the FPGA Fabric via the ARM AXI HPS-to-FPGA bridges**
* **Access the FPGA Fabric with Shell scripts, C++-, Python-Applications or PHP or Django web applications**
* **HPS Hard IP components (I²C-,SPI-, CAN-BUS or UART) are routed to FPGA I/O**
	* Ready for connecting different devices 
		* e.g. **Arduino Uno shields**
* **Accelerometer** and **ADC** can be accessed via Python or C++ (*Demos available*) (*only for the Cyclone V boards*)
* `socketCAN` pre-installed and pre-configured (*examples available!*) (*Only for Cyclone V SoC-FPGAs*)
* Console based Bus test tools (e.g. `can-utils`)
* Console memory dump tools (e.g. `devmem2`) 
<br>

* Full `Linux Network stack` with **dynamic and static iPv4** is supported
* `OpenSSH-Server` starts automatically during boot and is configured for user authentications 
*  UTC Time is synced during bootup with `htpdate` and a HTTP Time server
*  A virtual software random number generator (**RNG**) is used (*This SoC-FPGAs have no build in TRNG.*)
* `resolvconf` the  Linux DNS network tool is pre-installed 
* **Pre-installed development tools and DevOps**
    * `gcc`compiler *9.3.0*
    * `glibc` and `glib-2.0`(*The GNU C Library*)
    * `cmake` *3.16.5* 
    * `Python 3.8`
    *  `Python3-dev` and `Python-dev`
    * `git` *2.31*, `wget` *1.20.3*, `curl` *7.69.1* 
    
* **Support for remote based development IDEs pre-installed**
	* *Visual Studio Code* for **remote Python debugging**
    * *Visual Studio Code* for **remote Interface development**
	* *Visual Studio* for **remote C++ debugging**
    * *Visual Studio Code* for **remote C++ debugging** with `cmake` 
    * *ARM Development Studio (DS-5)* for **remote- (Ethernet) and JTAG- C++ debugging**  
• `gcc-compiler` and `gdb-server`
* **ARM Development Studio (DS-5) Streamline** is pre-installed and immediately is after start ready for **trace analysis**
* The ["NIOSII_EclipseCompProject](https://github.com/robseb/NIOSII_EclipseCompProject)" can generate custom **Eclipse for NIOS II** projects with for instance the real-time operating system (*RTOS*) **FreeRTOS**
<br>

* **`Python`**,**`Python3`**
* `Apache` webserver with `PHP` and `SQLite`
* `git`,`curl` and `wget` **download manager**
* **Latest `Django` version is pre-installed for Python-based web framework development**
* `udate-rc.d` and `crontab` for startup- and time-triggered shell script scheduling
* **Full integrated Python `pip3` (*Python-pip*) package manager**
* `opkg` **package manager** *0.4.2* enables to add some packages from different Linux Distributions.

<br>

* **Custom designed `Build System` to generate the entire bootflow for Intel SoC-FPGAs automatically**
    * **Allows to design highly optimized *rsyocto* flavors for your specific requirements**
    * Overview of the main feature of the "*[socfpgaPlatformGenerator](https://github.com/robseb/socfpgaPlatformGenerator)*" Build System: 
        * Automatically generate a bootable image file with configuration provided by a *Quartus Prime* FPGA project
        * Cloning and compiling of the *u-boot* bootloader for *Intel SoC-FPGAs*
        * **Allows a highly optimization of the u-boot (*e.g. via Linux `menuconfig`*)**
        * In case of the u-boot script is configured to load a FPGA configuration the depending FPGA configuration will be generated
        * Allows to pre-install any files or operating systems to a SD-Card image
        * **Boot image (.img) file generation** for distributing embedded Linux Distributions
        * Dynamic mode: *Partition size = Size of the files to add to the partition*
        * Linux Device Tree (*.dts*) -files inside a partition can be automatically compiled and replaced with the un-compiled file
        * Compressed files (*e.g. "tar.gz"*) containing for instance the Linux *rootfs* can be unzipped and automatically added to the partition
	* **To add the following to a deployable and shareable image file**
		* Custom bootloader configuration
		* FPGA configuration files 
		* *u-boot* boot script
		* Files/Applications
		* Software Libraries 
		* Web sites 
		* Linux Shell Startup scripts 
		* Network Interface settings 
<br>

* **Full supported boards**
	* **Terasic DE10-Standard** (Intel Cyclone V SoC-FPGA)
	* **Terasic DE10-Nano** (Intel Cyclone V SoC-FPGA)
    * **Terasic DE0-Nano SoC Kit *(Atlas-SoC Kit)*** (Intel Cyclone V SoC-FPGA)
	* **Terasic HAN-Pilot** (Intel Arria 10 SX SoC-FPGA)

<br>

# Tutorials 

### Getting Started Guides

| Level | Objective | Guide
|:--|:--|:--|
| 1 | **Booting *rsyocto* on your Board** | [**Getting started Guide**](doc/guides/1_Booting.md) |
| 2 | **Use of Hard-IP, FPGA-IP and FPGA Configuration of the FPGA Fabric** |[Step by step guide 1](doc/guides/2_FPGA_HARDIP.md) |
| 3a | **Debugging C++ applications remotely** with *Microsoft Visual Studio* | [Step by step guide 2a](doc/guides/3_CPP.md) |
| 3b | **Debugging C++ applications remotely** with **CMAKE** and *Microsoft Visual Studio Code* | [Step by step guide 2b](doc/guides/3_CPP_CMAKE.md) |
| 4 | **Debugging Python applications remotely** | [Step by step guide 3](doc/guides/4_Python.md) |
| 5 | **Analyzation of applications with ARM DS-5 Streamline** | [Step by step guide 4](doc/guides/5_Streamline.md) |
| 6 | **Developing a custom FPGA Configuration with Intel Quartus Prime**| [Step by step guide 5](https://github.com/robseb/rsyocto/blob/rsYocto-1.042/doc/guides/6_newFPGAconf.md) |
<br>

### Customization Guides 

| No. | Objective | Guide
|:--|:--|:--|
| 1 | **Designing of custom *rsyoto* versions** with your content and FPGA project | [Guide](https://github.com/robseb/rsyocto/blob/rsYocto-1.042/doc/guides/7_customVersions.md)  |
| 2 | **Install addional Packages** with `opkg`- and `pip3` package manager  | [Guide](https://github.com/robseb/rsyocto/blob/rsYocto-1.042/doc/guides/7_customVersions.md)  |
| 2 | **Build your own custom Linux Distro for Intel SoC-FPGAs** with the Yocto Project | [Guide](https://github.com/robseb/rsyocto/blob/rsYocto-1.042/doc/guides/7_customVersions.md)  |
<br>

### Application-specific Guides

| No. | Objective | Guide
|:--|:--|:--|
| 1 | **Transmitting CAN-Bus packages with Python** | [Guide](doc/appSpecificGuides/1_TransmittingCAN.md) |
| 2 | **Developing a Django web application for interacting with the FPGA Fabric** | [Guide](doc/appSpecificGuides/2_DjangoWebApps.md) |
| 3 | **Writing a Linux Startup script** | [Guide](doc/appSpecificGuides/3_LinuxStartUpScript.md) |
| 4 | **Examples of using *Microsoft Visual Studio*  for C++ development** | [Guide](https://github.com/robseb/LinuxVSCppFPGA) |
| 5 | **Using the *Intel NIOS II* Soft-Core Processor, running *FreeRTOS*, to interact with HPS Hard-IP** | [Guide](https://github.com/robseb/rsyocto/blob/rsYocto-1.042/doc/appSpecificGuides/4_NIOS2HPS.md) |
<br>


# Folder Structure 
| Folder | Content
|:--|:--|
| `doc`    | Documentation  |
| `fpga`    | Quartus Prime projects |
|  `examples/python` | *rsyocto* Python examples |
|  `build_system` | *rsyocto* build scripts |

The **C++-Demo Project** for *Microsoft Visual Studio* are available [here](https://github.com/robseb/LinuxVSCppFPGA).

The final *rsyocto* boot images (*img*) are available inside the **packages-Part of this repository**!



# Built With / Credits & Contribution
* [Intel SoC FPGA Embedded Development Suite (EDS) 20.1](https://www.intel.com/content/www/us/en/software/programmable/soc-eds/overview.html) - Linux
* [Intel Quartus Prime 20.1 Lite Edition](https://www.intel.com/content/www/us/en/software/programmable/quartus-prime/download.html) - Cyclone V
* [Intel Quartus Prime 18.1.0 Standard Edition](https://www.intel.com/content/www/us/en/software/programmable/quartus-prime/download.html) - Arria 10
* [LinuxBootImageFileGenerator](https://github.com/robseb/LinuxBootImageFileGenerator)
* [socfpgaPlatformGenerator](https://github.com/robseb/socfpgaPlatformGenerator)
* [pydevmem](https://github.com/kylemanna/pydevmem)
* [PiP2Bitbake](https://github.com/robseb/PiP2Bitbake)
* [The Yocto Project](https://www.yoctoproject.org/) 
* [meta-intelfpga](https://github.com/robseb/meta-intelfpga) 
* [meta-openembedded](https://github.com/openembedded/meta-openembedded)
  * [meta-Python](https://github.com/openembedded/meta-openembedded/tree/master/meta-Python) 
  * [meta-webserver](https://github.com/openembedded/meta-openembedded/tree/master/meta-webserver)
  * [meta-networking](https://github.com/openembedded/meta-openembedded/tree/master/meta-networking) 
<br>

# Development Process

The first version of *rsyocto* (*release december of 2019*) was developed with the *Intel Embedded Development Suite* (*SoC EDS*) version 18.1 and a custom Yocto Project meta-layer. 

By default the specifications of these two development tools are not compatible to each other. To handle this issue **I designed a custom build flow to progress the output Linux files of the Yocto project and to create all necessary boot stages**. 

This build system consists of an Ubuntu Linux and a *CentOS* Linux part. On *CentOS* was an *Altera* script used to generate the boot images. 
With re-design of the bootflow of *Intel* SoC-FPGAs with the SoC EDS Version 19.1 it was essential for me to design an new build system that can run on a single development computer (Ubuntu Linux or *CentOS*) and generate all required bootloaders fully automatically. **My implementation has the big benefit, that it enables the generation of complete custom Linux versions with own FPGA Projects by just running a Python script. A deep Linux knowledge is for this process not required.**  
<br>

**My first approach to design this Linux Distribution** 
![Alt text](https://raw.githubusercontent.com/robseb/rsyocto/rsYocto-1.042/doc/symbols/rsYoctoRequieredBuildingSteps.jpg?raw=true "rsyocto required building steps")
**Build Flow to create the first rsyocto version**
<br>
<br>

# Build system for generation of custom rsyocto flavors

![Alt text](https://raw.githubusercontent.com/robseb/rsyocto/rsYocto-1.042/doc/symbols/BuildSystem.jpg?raw=true "automatic rsyocto Build system")
**Block diagram of the fully automated build system to design new releases**
<br>
<br>

This illustration shows my new development procedure and the required complexity to create *rsyocto*. **I entirely automated the required complex bootflow** to generate with a *Intel Quartus Prime* FPGA project and Linux Distribution files (*e.g. zImage,rootfs,...*) a bootable image file (*.img*). 
The script uses the **Intel Embedded Development Suite (SoC EDS)** in version **20.1** (*2020*) to design the necessary bootloaders based on the project settings for an Intel Cyclone V- and Intel Arria 10 SX SoC-FPGA.
**It was designed to allow a high optimization of all components**, such as the *u-boot* boot script or the Linux Device Tree. With this project I want to give other developers a full-functional system to reduce their development effort. 

For designing custom *rsyocto* Versions it is only necessary to copy the `"socfpgaPlatformGenerator"`- Folder (available inside Repository's Releases part) into a Quartus Prime FPGA project folder. The included Python script can then generate the entire platform and can output a shareable and a bootable image file ("*.img").Be the way, it is also possible to use this script with your own Linux Distribution files as I show later.

My build flow consists of three stages to enable the support for other embedded Linux platforms or with different embedded Linux Distributions.
In the following table these three stages are visible. The stage one is on the lowest level and its classes will be used by the next stage.
<br>


| Stage | Python Script Name | Description | Output 
|:--|:--|:--|:--|
| 1 | [LinuxBootImageFileGenerator](https://github.com/robseb/LinuxBootImageFileGenerator) |  Class to automatically generate a bootable Image file with a specifiable partition table | Image file for enabling booting for almost all embedded Linux distributions |
| 2 | [socfpgaPlatformGenerator](https://github.com/robseb/socfpgaPlatformGenerator) |  Class to generate all necessary components for booting an embedded Linux on Intel (ALTERA) SoC-FPGAs to build the bootloader (u-boot) and bring all components to a bootable image | Image for booting any *Intel* SoC-FPGA |
| 3 |[makersyoctoSDImage.py](https://github.com/robseb/rsyocto/tree/rsYocto-1.042/build_system) | Python script to generate a custom *rsyocto* version with for instance *rootfs* changes (*SSH configuration*) | Image with a custom *rsyocto* flavor |

<br>


# Embedded native remote development environment

As described, I attach great importance to easy-to-use and powerful Integrated development environments (**IDE**) for the Linux application development, due to the fact that the requirement and complexity of embedded applications grows exponentially year after year and the only way to counter act this trend are simple to install and use IDEs. 

On the Linux generation site, I could simplify the complex multi-stage bootloader and Linux generation process with my Python scripts and pre-installed Bus-tools and the ARM Development (DS-5) Studio integration can help with hardware-level development and trace debugging. 
For the Linux Desktop application development, I used following approach for my project:


![Alt text](https://raw.githubusercontent.com/robseb/rsyocto/rsYocto-1.042/doc/symbols/EmbeddedNativDevApproch.jpg)
**My pre-configured and preferred Linux application development approach for C++,Python and Web**


This replaces the complex *Eclipse*- and *Visual Studio* IDEs and annoys all essential components on the embedded Linux itself.
In this concept the development projects are located for the best code tracking inside a *git*- (*GitHub* or *GitLab*) repository. This repo can be directly cloned to the *rootfs* of the embedded Linux via a secure shell (**SSH**) interface over the network. A developer can use a other SSH connection to its development machine.

The development machine can be any computer that runs the compact code editor *Microsoft Visual Studio Code Insider*. The *Microsoft Visual Studio Code Insider* version allows the remote connection to an embedded ARMv7-A and ARMv8-A Linux distributions, such as *rsyocto*. Via SSH established *VS Code* a connection to the `Linux Shell` of embedded Linux and via **SFTP** it is enabled to access the `root file system` (*rootfs*). The code editor uses the existing development tools on the target platform, such as the `native gcc-compiler` or `Python` for the application engineering and debugging (e.g. `gdb-server`). 

A difficult to install and configure cross-compiler or Python framework is on the development machine not required, because everything runs directly natively on the development board. This makes the complex design and usage of a `Linux Framework` for this Linux Distribution unnecessary, due to the fact that the source code runs directly on the right location and can access all interfaces, files and libraries natively. This brings a high optimization in terms of feature usage of *rsyocto* and it can help to reduce the code size. 

*VS Code* and *rsyocto* enables in this way to develop *Python*, *PHP*, *HTML*,*CSS*,*C++* with `cmake` and a lot more. I wrote for these use cases examples. The ARMv7-A CPU of the *Intel Cyclone V-* and *Intel Arria 10 SX-* SoC-FPGA-devices are more than powerful enough to notice no major difference between cross-compilation- and native compilation-time. For cloning a *git* repo is only some user space on the *rootfs* required.


<br>

# Q&A


### How to get started with the Yocto Project for Intel SoC-FPGAs?
Inside my [`meta-intelfpga` BSP layer](https://github.com/robseb/meta-intelfpga) I described in details how to get started with the Yocto project for *Intel SoC-FPGAs*.
Also I published inside this layer the source code and documentation to bring **tools to update the FPGA configuration with the running Linux and to interact with simple commands with the FPGA Fabric** to the Yocto Project.

### How to import Python pip (*Python-pip*) packages to Yocto Project 
I designed a simple Python script to pre-install Python pip (PyPI)- Packages within a final Yocto Project Linux Image (see [here](https://github.com/robseb/PiP2Bitbake).

### How to automatically generate an Intel NIOS II Eclipse project with for instance FreeRTOS

I wrote [Python Script](https://github.com/robseb/NIOSII_EclipseCompProject) to automatically generate an Intel NIOS II Eclipse Project with custom software components (e.g. FreeRTOS). 

<br>

# Continuation

**I will continue my work and upload newer versions. I invite everybody to submit issues, comments and ideas.**

Currently I am working on a Windows 10 .net Desktop application to manage FPGA configurations and to allow to record data via the network. To release that I will design a server task, running on *rsyocto*, that can send Python- or C++-values with TCP to the desktop. The following screenshot shows the development state of this project.

![Alt text](https://raw.githubusercontent.com/robseb/rsyocto/rsYocto-1.042/doc/symbols/destopSoftwareAlphaState.jpg?raw=true "rsyocto required building steps")

<br>


# Author
* **Robin Sebastian [(LinkedIn)](https://www.linkedin.com/in/robin-sebastian-a5080220a)**

rsyocto are projects, that I have fully developed on my own. No companies are involved in my projects. 
I’m recently graduated as a master in electrical engineering with the major embedded systems (M. Sc.).

**[Github sponsoring is welcome.](https://github.com/sponsors/robseb)**

[![Gitter](https://badges.gitter.im/rsyocto/community.svg)](https://gitter.im/rsyocto/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
[![Email me!](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)](mailto:git@robseb.de)

[![GitHub stars](https://img.shields.io/github/stars/robseb/rsyocto?style=social)](https://GitHub.com/robseb/rsyocto/stargazers/)
[![GitHub watchers](https://img.shields.io/github/watchers/robseb/rsyocto?style=social)](https://github.com/robseb/rsyocto/watchers)
[![GitHub followers](https://img.shields.io/github/followers/robseb?style=social)](https://github.com/robseb)
