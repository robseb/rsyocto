[Back to the startpage](https://github.com/robseb/rsyocto)

# Using the Intel NIOS II Soft-Core processor running *FreeRTOS* to interact with Hard Processor System (HPS) IP 

![Alt text](NIOS2HPSconecpt.png?raw=true "Concept")
<br>

The following step-by-step guide demonstrate how to access Hard-IP, such as UART, of the *ARM Cortex-A9* system with the *Intel NIOS II* processor running as Soft-IP inside the FPGA Fabric. The microcontroller (*MCU*) executes the real-time operating system ***FreeRTOS***. A task running on *FreeRTOS* can than be used to communicate with HPS Hard-IP. This Demo is written for an *Intel Cyclone V* SoC-FPGA on a *Terasic DE10-Nano*, *DE10-Standard* and *DE0-Nano SoC*. 
<br>

*Intel SoC-FPGAs*, such as the Cyclone V, have a *ARM AXI Interface* between the HPS- and FPGA-part of the SoC to allow the FPGA to access almost the entire memory space of the *ARM Cortex-A9* application processor system. This interface is called **FPGA-to-HPS Bridge**. 

This includes for instance all Hard-IP modules, such as *UART*-,*I²C*- or *CAN*-Bus and the on-chip memory used by the bootloader during boot. It is enabled to export the interrupt lines of the Hard-IP module to the FPGA Fabric as well.  This skill can bring the capability to the *Intel NIOS II* processor to react for example to *CAN*-Packages via a *CAN RX* interrupt.

An additional microcontroller inside the SoC, running a real-time operating system, such as *FreeRTOS*, can rapidly extend the real-time related performance of an embedded Linux Distribution. Such a two processor solution can combine the benefits of a Linux- and real-time OS and it can be assumed that the real-time performance is significantly higher as a single processor solution with a real-time optimized Linux Kernel.

For my embedded Linux *rsyocto* I already wrote examples and guides that demonstrate the interaction between FPGA Soft-IP devices and embedded Linux. That can be assumed for the *Intel NIOS II* to Linux communication as well.
<br>

This guide shows the second path of this two Processor solution: The design of a *Intel NIOS II* Soft-Core processor that can use the HPS Hard-IP. The configuration of the *Intel NIOS II* and the Bridge interface to the HPS is with *Intel's Quartus Prime Platform Designer* really straight forwards.

The most complicated part is the designing of all components beside. For example it is necessary to give after each boot the FPGA the privilege to access the address space of the HPS. Only the HPS can give these rights. That means a special optimized embedded Linux with an entire boot flow is necessary to achieve that.  

**Requirements of the final demo application**

* Configuration of the FPGA Fabric with an *Intel NIOS II* Soft-Core Processor
* Installment of *FreeRTOS* on the *Intel NIOS II* Core
* Configuration of the *FPGA2HPS* Bridge to allow the Hard-IP interaction with the *Intel NIOS II*
* Toggling the *HPS_LED* via a *FreeRTOS* Task
* Reading the *HPS_KEY* via a external (*EXTI*) Interrupt with the *Intel NIOS II*
* Sending a UART ASCI String with the *Intel NIOS II* core over the Hard-IP UART interface

**Required steps to achieve this demo**
  
* **On FPGA hardware side**
    * HPS configuration with enabling of the **FPGA-to-HPS**-Bridge and assignment of **Interrupt lines to the FPGA Fabric**
    * *Intel NIOS II* Soft-Core processor configuration with system memory
    * Connecting of the*Intel NIOS II* AVALON Bus via an **Address Expander** to the **FPGA-to-HPS**-Bridge
    * Connecting of the *Intel NIOS II* Interrupt controller to the **IRQ Bridge** to the exported HPS Interrupt lines
    * Connecting of a Soft-IP timer to *Intel NIOS II* Avalon bus to give the *FreeRTOS* a system schedule *systick* timer interrupt
    * Connecting some FPGA-LEDs and FPGA-Switches to the *Intel NIOS II*
* **On HPS software side**
    * Using the *u-boot* boot script to enable to give the FPGA the privileges to access the Hard-IP
    * It can alternatively be done via the usage of a Linux Shell start up script
    * Changing the **Linux Device Tree* to disable the loading of the Linux driver for the  *Intel NIOS II* used modules
* **On NIOS II software side**
    * Creating of an Eclipse for *Intel NIOS II* project with *FreeRTOS* support
    * Writing some *FreeRTOS* tasks to communicate with the Hard-IP 

The most complicated and time consuming part of this project is not the FPGA design, that is completely automated by *Intel's Quartus Prime Platform Designer*. 
Instead it is to design a bootflow for an embedded Linux to give the FPGA the privileges to access the HPS-Memory space and to install the latest *FreeRTOS* version on the *Intel NIOS II* processor.

To automate these two build steps I designed two Python scripts. To accomplish that I wrote a small library, called [socfpgaHAL](https://github.com/robseb/socfpgaHAL) as a *Hardware Abstraction layer* (**HAL**) as a *Intel NIOS II* driver for the Hard-IP modules. 
<br>

# Installment of the required development tools

Follow the [following instructions](https://github.com/robseb/rsyocto/blob/rsYocto-1.04/doc/guides/7_customVersions.md) to install the required development tools:
* *Intel Quartus Prime* Lite for Windows and Linux 
    * with *Eclipse for NIOS II* support
* *Intel Embedded Development Suite* (*SoC EDS*) 20.1 for Linux


# Design of the required SoC-FPGA Platform 

**Finished Quartus Prime projects are available inside this Github repository.**

The *Intel NIOS II* Soft-Core processor can be designed as usually and will for that reason not mentioned in detail. Only the necessary application specific points will be shown here:  
* **Necessary points to run the real-time OS **FreeRTOS** on a *Intel NIOS II* Core**
    * **Interval Timer Intel FPGA** as *systick* source for *FreeRTOS*
        * **Name:** `sys_clk`
        * **Period:** `1ms`
        * **Counter Size:** `32`
        * **No Start/Stop control bit:** `YES`
        * **Interrupt line with the lowest priority (*priority level 0*) to the *Intel NIOS II* Interrupt Controller** 
    * **Required system memory space:** `~250K Byte`
* **Necessary points to connect the *Intel NIOS II* Core with the HPS**
    * **Enable the FPGA-to-HPS interface**
    * **FPGA-to-HPS width:** `32-bit`
    * **Enable the HPS-to-FPGA Interrupt line for the modules**
    * **Use an Address Span Expander to allow the *Intel NIOS II* with its memory to interact with the 32-bit address size of the HPS**
        * Due to the fact that the *Intel NIOS II* requires some system memory the available address bus is too small  
        * By using a sub-window offset of *0xfc000000* it is for the *Intel NIOS II* Core enabled to access the entire memory space of the HPS components
        * That means a *Intel NIOS II* Core can for example access the base address of *CAN0* (*HPS base Address: 0xFFC00000*) by using the address *0x3C00000* (*=0xFFC00000-0xFFC00000*)
        * **Use the following settings for the Address Span Expander**
            <br>

            ![Alt text](addressExpander.png?raw=true "Address Span Expander")
            <br>

    * **Connect the *Intel NIOS II* AVALON Bus to the Window Slave Port of the Address Span Expander**
    * **Connect the FPGA-to-HPS Bridge of the HPS module to the expander master port of the Address Span Expander**
* **Necessary points to connect HPS Interrupt lines to the *Intel NIOS II* Core**
    * **Use an Interrupt Bridge module**
        * To allow to use different clock domains between the *Intel NIOS II* core and the HPS
        * **Connect exported HPS-to-FPGA Interrupt lines with the Interrupt Receiver port of the Interrupt Bridge module**
<br>
The following table illustrates the for the *Intel NIOS II* accessible memory space with this configuration:
<br>

![Alt text](MemorySpace.png?raw=true "Accessible memory space")
<br>


# Using an u-boot boot script or a Linux Shell script to give the *Intel NIOS II* Core the privilege to access HPS memory space

Every module of the HPS has its own privilege bit. Only in the case this bit is set, it is for the FPGA Fabric possible to access the depending peripheral components. 
The documentation of these registers are available inside the **Intel Cyclone V Hard Processor System Technical Reference Manual** ([Link](https://www.intel.com/content/dam/www/programmable/us/en/pdfs/literature/hb/cyclone-v/cv_5v4.pdf)).

For instance to enable the **UART1** component it is necessary to set the bit number 7 of the register `l4sp` (*HPS Address 0xFF80000C*).
![Alt text](exampleBitFiled.png?raw=true "Example documentation of l4sp")

As mentioned it is only for the HPS possible to change these registers and it must be done after every power up of the SoC-FPGA.
To achieve that two suitable solutions are possible
1. **Setting the registers inside an *u-boot* script during boot**
2. **Using a Linux Shell boot script**
  
The first solutions have the advantage to give the privilege instantly after the board is powered on. A major disadvantage is that a complex bootload design is necessary for adding an single *u-boot* command. It will burn the most time for this project. However, with the **build system** of *rsyocto* based on the [*socfpgaPlatformGenerator*](https://github.com/robseb/socfpgaPlatformGenerator) this can be done in a few minutes. 

For *rsyocto*-based Linux Distributions follow the [customization guide](https://github.com/robseb/rsyocto/blob/rsYocto-1.04/doc/guides/7_customVersions.md) and for general *Intel* SoC-FPGAs can [this guide](https://github.com/robseb/socfpgaPlatformGenerator) and [this guide](https://github.com/robseb/rsyocto/blob/rsYocto-1.042/doc/guides/9_customYoctoVersions.md) be considered. 

For example to give the *Intel NIOS II* core the privilege to access the entire peripheral components add the following to the *u-boot* script (*socfpgaPlatformGenerator/ubootScript/uboot_cyclone5.script*): 

````script
echo --- enable HPS-to-FPGA, FPGA-to-HPS, LWHPS-to-FPGA bridges ---
bridge enable;

echo --- enable FPGA2HPS peripherals access --

echo     for I2C,CAN,UART,TIM
mw.w 0xFF80000C 0x7FF
  
echo     for GPIO
mw.w 0xFF800010 0x3FC

echo     for OSC
mw.b 0xFF800014 0x60  

echo     for SPI
mw.b 0xFF800018 0x03

echo     for on-chip RAM
mw.b 0xFF800098 0x01

echo     Reset Bridges 
mw.b 0xFFD0501C 0x0  
````
<br>

**Be sure that these commands are added after the FPGA configuration is written and the FPGA Fabric was released from Reset.**
The `mw.w` *u-boot* command allows to write a word (*32-bit*) and the `mw.b` can write a byte (*8-bit*) to an address. **After any change of the privilege settings it is necessary to release the Bridges from Reset.** This must be done via the `brgmodrst` register (*Address: 0xFFD0501C*) by writing an "*0*".
<br>

Alternatively it is also possible to change the registers with a Linux Shell script or just a single console command.
For giving the *Intel NIOS II* core the privilege to access the memory space of the *I²C-,CAN-,UART-* and *Timer*, run the following command on the running Embedded Linux:

````shell  
devmem2 0xFF80000C w 0x7FF
devmem2 0xFFD0501C w 0
````
<br>

These two commands can also be inserted to a Linux Shell start up script as shown in the next example (*e.g. for the DE10-Nano:   socfpgaPlatformGenerator/Board_DE0NANOSOC/my_startUpScripts/startup_script.sh*):

`````shell
#!/bin/sh
# Startup script
# This script will be executed before the system starts the NIC
echo "rsyocto Startup script: started!"

echo "--- enable FPGA2HPS peripherals access --"
echo "   for I2C,CAN,UART,TIM"
devmem2 0xFF80000C w 0x7FF
echo "    Reset Bridges" 
devmem2 0xFFD0501C w 0

# Map RNG to the driver
RNGD_OPTS="-r /dev/random"
echo "Startup script: end!"
`````
<br>

# Change the *Linux Device Tree* to disable the loading of a used component by *Intel NIOS II* Soft-Core processor 

To prevent the Linux Distribution to interact at the same time as the *Intel NIOS II* to an identical Hard-IP component disable it from the *Linux Device Tree*. Then this address space will not be used by the Linux Kernel and *Kernel Mode drivers*. For instance in case **UART1** is used by the *Intel NIOS II* Soft-Core processor disable the device for the embedded Linux.
The following code shows the *Linux Device Tree* description for loading the driver for **UART1** (**serial1**):
`````shell
		serial1@ffc03000 {
			compatible = "snps,dw-apb-uart-16.1", "snps,dw-apb-uart";
			reg = <0xffc03000 0x1000>;
			interrupts = <0x0 0xa3 0x4>;
			reg-shift = <0x2>;
			reg-io-width = <0x4>;
			clocks = <0x29>;
			dmas = <0x34 0x1e 0x34 0x1f>;
			dma-names = "tx", "rx";
			phandle = <0x63>;
			status = "okay";
		};
`````
<br>

A change of the `status` from *"okay"* to *"disabled"* will disable the loading of the driver for this device. 
Change for with *Intel NIOS II* used peripheral component the `status` attributes to  *"disabled"*.
````shell
status = "disabled";
````

# Booting the new designed Linux Distribution and configuring the FPGA Fabric with the *Intel NIOS II* Core

**Use the build script as usual to generate a bootable image file with the changed bootflow.** 
**The Intel *Intel NIOS II* Soft-Core processor is typically only in a demo mode (*un-licensed*) available.** *Intel* Quartus Prime will reject to generate a binary FPGA Configuration file with a *Intel NIOS II* core. However, the **build system** will use for FPGA configuration a default file. That can be later overwritten.
<br>

Flash the output image file (*.img*) to a SD-Card and boot your development board with it, as shown in the [first guide](https://github.com/robseb/rsyocto/blob/rsYocto-1.04/doc/guides/1_Booting.md).
<br>

After the complete boot of the embedded Linux is done connect the onboard *ALTERA JTAG Blaster* via an USB cable to your development computer. 
Write the FPGA configuration of your Quartus Prime project with the integrated debugger to the FPGA Fabric of your development board. 


# Generating a *NIOS II for Eclipse* demo project with *FreeRTOS* and the HPS HAL lib

Another time consuming part of this project is usually to implement a real-time operating system (*e.g. *FreeRTOS**) into an *Eclipse* project. I designed a Python script (*"NIOSII_EclipseCompProject*") to automate these steps, as well. It can clone the latest *FreeRTOS* version from Github and install an optimized port of it for the *Intel NIOS II* processor. I wrote a small HAL library for accessing HPS IP with the *Intel NIOS II* core. It can be pre-installed with custom user libraries, as well. The Python script will generate an **Eclipse example project**. That can be used as a reference for a further development. 

**Concept of the *"NIOSII_EclipseCompProject"* Python script:**

![Alt text](EclipseGenConcept.png?raw=true "Concept of NIOSII_EclipseCompProject")
<br>

Follow the [step-by-step guide of the script](https://github.com/robseb/NIOSII_EclipseCompProject) to generate the required project for this purpose. 

Be sure, that you select inside the Python script the implementation of the [socfpgaHAL](https://github.com/robseb/socfpgaHAL) as shown in the following screenshot: 
![Alt text](AddSoCHalMes.png?raw=true "Generation with socfpgaHAL") 
<br>

Finish the generation of the **Eclipse example project** and then start *Eclipse* as described inside the documentation of the *"[NIOSII_EclipseCompProject](https://github.com/robseb/NIOSII_EclipseCompProject)"*. 


# Starting a new *NIOS II for Eclipse* debug session and running the example code

The starting of a new debug session is also shown inside the documentation of "*NIOSII_EclipseCompProject*" [Github repository](https://github.com/robseb/NIOSII_EclipseCompProject). Create a new *Eclipse* project that based on the *Intel NIOS II* Software example **"*FreeRTOS*+socfpgaHAL-robseb"**.
<br>

The project contains *FreeRTOS* implementation that accesses multiple Hard-IP components. 
<br>

# Understanding the *socfpgaHAL* Library 

The "*socfpgaHAL*" is a small library that can be used as an HAL for interaction with HPS Hard-IP with a *Intel NIOS II* processor. 

**The Structure of the "*socfpgaHAL*"**: 

 | **File Name** | **Description** | 
 |:--|:--|
 | *"socfpgaHAL.h"* | Main HAL file should only be used to include the HAL |
 | *"socfpgaHAL_config.h"* | The configuration file of the HAL | 
<br>

Use the configuration file to enable the access of components. For instance the GPIO support can be enabled by adding to the configuration file (*socfpgaHAL/socfpgaHAL_config.h*):
````c
#define SOCFPGAHAL_ENABLE_GPIO 			(1)
```` 
<br>

**Currently the support for the following Hard-IP components is available:**


| **Peripheral Name** | **Module Name** | **Description**
|:--|:--|:--|
| **GPIO** | *GPIO0*, *GPIO1*, *GPIO2* | *General-purpose I/O* |
| **Timer** | *SPTIMER0*, *SPTIMER1*, *OSCTIMER0*, *OSCTIMER1* | *Timer* |
| **UART** | *UART0*, *UART1*, *UART Soft-IP* | 16550 based *Synopsys DesignWare APB Universal Asynchronous Receiver/Transmitter* |

<br>

___
 [Back to the startpage](https://github.com/robseb/rsyocto)
 
