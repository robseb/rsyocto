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

![Alt text](doc/symbols/rsYoctoInterfaces.jpg?raw=true "poerfull remote developemed IDEs")
*poerfull remote developemed IDEs**
<br>
# Mondivation

![Alt text](doc/symbols/rsYoctoRequieredBuildingSteps.jpg?raw=true "rsYocto Layers")
*required building steps for rsYocto**
<br>
# Built With
* [Intel SoC FPGA Embedded Development Suite (EDS) 18.1.0.625](https://www.intel.com/content/www/us/en/software/programmable/soc-eds/overview.html) 
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
# Author
+ **Robin Sebastian**
*rsYocto* was developed by Robin Sebastian a year ago as an student project and for his master thesis further optimized.
No companys were involved in this project.
