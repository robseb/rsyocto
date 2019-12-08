![Alt text](doc/symbols/rsYoctoLogo.jpg?raw=true "rsYocto Logo")

rsYocto is an open source embedded Linux System designed with the Yocto Project for Intel SoC-FPGAs (Intel Cyclone V and Intel Arria 10).  The full compatibility with the Yocto Project allows the best customization for the strong requirements of embedded applications. rsYocto implements a modern Linux Kernel and brings a set of today fundamentally needed components to Intel SoC-FPGAs and help to simplify the complex process of development for FPGA-, Industrial 4.0-, Internet of Things- or deep learning applications.
To allow that is for example Python3 with the Python Package manager PiP and the Apache Webserver with PHP included. Thereby it is really easy to install Python applications from the Raspberry Pi on a powerful Intel SoC-FPGA. rsYocto is for is best optimization complete console based, but the Apache Webserver can bring any GUI to Computers, Smartphones or Tablets, by hosting for example a monitor web interface. 
During development, a major concern was placed on the integration of powerful and simple to install development environments that do not require a JTAG-connection or any cross-building environment. rsyocto application can build, deployed and even debugged over the network. With the implementation of Microsoft Visual Studio and Visual Studio Code is a simply installment and quick jumpstart in the development process possible, because all required compilers run direct on rsyocto. 

The “rsyoctoMakingSD”- script allow developer to customize the rsyocto image with the installment of their own software files or FPGA configuration file, that will be configured on the FPGA fabric before the Linux boots. 

rsyocto is with the drivers for all Hard-IP Interfaces (e.g. I²C, CAN,…) and simple Linux test commands (e.g. i2c-tools) ready for development of industrial connected solutions. With a single command is rsyocto capable to load a new FPGA configuration or to read and write the AXI-Bridge Interface to the FPGA. 

The final rsyocto image can be installed on a SD-Card with any commen used Image creating tools. Versions are available for the Terasic DE10 Standard- (Cyclone V), Terasic DE10 Nano- (Cyclone V) or Terasic Han Pilot (Arria 10).  
Try it out!

  
# Features of rsYocto

![Alt text](doc/symbols/rsYoctoLayers.jpg?raw=true "rsYocto Layers")

 
