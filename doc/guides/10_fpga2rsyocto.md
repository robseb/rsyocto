[Back to the startpage](https://github.com/robseb/rsyocto)


## Writing the FPGA-Configuration over the network with your *Intel Quartus Prime* FPGA Project


![Alt text](flashFPGASymbol.jpg?raw=true "Symbol Python script")
<br>


For FPGA developers, a **Python script** has been developed that allows the **FPGA-Configuration to be written over the network** (*SSH/SFTP*) by simply running it in an *Intel Quartus Prime* FPGA project folder. The script can compile the FPGA project and change the FPGA-Configuration of the bootloader (*u-boot*) to start the FPGA-Configuration after a restart. This has the same effect as a classic *FPGA-Configuration device*. 

### Features

* **Python script to write the FPGA-Configuration over the Network**
    * **Just executed inside the *Intel Quartus Prime* FPGA project folder**
    * Communicates with the SoC-FPGA board over the network
    * **Compiling** the *Intel Quartus Prime* FPGA project 
    * **Changing the running FPGA-Configuration** of the FPGA-Fabric
    * **Changing the bootloader (*u-boot*) FPGA-Configuration**
        * **After a restart, *u-boot* writes the new FPGA-Configuration into the FPGA-Fabric** 
        * Behavior like a *classical FPGA configuration device*
* **Network Interface**
    * Script uses a the *Secure Shell Protocol* (**SSH**) and the *SSH File Transfer Protocol* (**SFTP**) for the communication with the *rsyocto*
    * Any other connection, like JTAG or USB, to the board is not required
    * Uses SSH with user authentication to make attaching to the card as easy as possible 
        * It is only necessary to insert the IPv4-Address of the SoC-FPGA board

* **Supported Development Environments**
    * **Windows 10**
    * **Ubuntu** *18.04 LTS*
    * **Ubuntu** *20.04 LTS*
    * **CentOS** *7.7*
    * **CentOS** *8.0*
* **Supported Intel Embedded Development Suite (*SoC-EDS*) Versions**
    * SoC-EDS *16.1* or later for Windows or Linux
* **Supported Intel Quartus Prime Versions**
    * *Intel Quartus Prime* **Lite** 16.1 or later for Windows or Linux
    * *Intel Quartus Prime* **Standard** 16.1 or later for Windows or Linux    
    * *Intel Quartus Prime* **Pro** 16.1 or later for Windows or Linux 
* **Supported Intel SoC-FPGAs running *rsyocto***
    * **Intel Cyclone V**

### Getting Started 

To chnage the running- and boot FPGA-Configuration by compiling the Intel Quartus Prime FPGA project only the following line must be executed inside the FPGA project: 
````shell
python3 flashFPGA2rsyocto.py
````

However, to enable this features  the Python build script uses the `Intel SoC-EDS Command Shell` and the `Intel Quartus Prime Shell`. 
These are part of *Intel Embedded Development Suite (*SoC-EDS*)* and of *Intel Quartus Prime*. This guide shows how to install this tools properly.
*Intel Quartus Prime* must be only installed in case the script should compile and build the FPGA project. 
<br>

#### Install development tools
<br>

**1. Install the *Intel Embedded Development Suite 20.1* (*SoC-EDS*)**

* [Download](https://fpgasoftware.intel.com/soceds/20.1/?edition=standard&platform=windows&download_manager=direct) *Intel SoC EDS 20.1 Standard for Windows or Linux*
* **For Windows**
    * Follow the instructions of the installer 
* **For Linux**
    * **Install** SoC EDS by executing the following Linux console commands
        ````shell
        chmod +x SoCEDSSetup-20.1.0.711-linux.run && ./SoCEDSSetup-20.1.0.711-linux.run
        ````

**2. Instal Intel Quartus Prime (18.1 or later) for Windows or Linux**

* **Note:** *Intel Quartus Pirme* is only required for compiling the FPGA project. FPGA-Configuration files are generated with SoC-EDS 
*   A step-by-step guide how to install *Intel Quartus Prime* on **Linux** or **Windows** is available [here](https://github.com/robseb/NIOSII_EclipseCompProject#i-installment-of-intel-quartus-prime-191-and-201-with-nios-ii-support) (*NIOS II support is for this project not required*)

**3. Instal Python and Python pip (*PyPip*)**

*  A step-by-step guide how to install *Python* on **Linux** or **Windows** is available [here](https://github.com/robseb/NIOSII_EclipseCompProject#i-installment-of-intel-quartus-prime-191-and-201-with-nios-ii-support)


**4. Install the required Python pip (*PyPip*) packages `paramiko`**

* Execute the following command on Linux or Windows to install `paramiko` (*a API for SSH/SFTP for Python*)
````shell
pip3 install paramiko
````
<br>

#### Run the script inside a Quartus Prime FPGA project
<br>

**1. Copy the Python script into your *Intel Quartus Prime* FPGA project folder**

* **Clone this GitHub repository**
````shell
git clone https://github.com/robseb/rsyocto.git
````

* **Copy the Python script `flashFPGA2rsyocto.py` into your *Intel Quartus Prime* FPGA project folder**
    * Location Source: `build_system/flashFPGA2rsyocto.py`
    * Location Destination: *Intel Quartus Prime* FPGA Top Folder

    ![Alt text](flashFPGAQuartus.jpg?raw=true "Symbol Python script")
    
    **Just copy the Python script into the top-folder of the *Intel Quartus Prime* FPGA project**


**2. Run the Python build script to generate a new FPGA-Configuration and flash it to the FPGA-Fabric**

* **Set the IPv4-Address of your board**
    * Before you can start the Python script to chnage the FPGA-Configuration it is only essential to set the IP-Address
    * Use following command to set the IPv4-Address of your board
    ````shell
    python3 flashFPGA2rsyocto.py -ip 192.168.0.109 
    ````
    * **Note:** On Windows use `python` instate of `python3`
    * The argument `-ip` will write the IP-Address to the XML file `confFlashFPGA2rsyocto.xml`
        <details>
            <summary><strong>Content of the XML File</strong></summary>
            <a name="Pos0"></a>

        ````xml
        <?xml version="1.0" encoding = "UTF-8" ?>
        <!-- Used by the Python script "flashFPGA2rsyocto.py" -->
        <!-- to store the settings of the used development board -->
        <!-- Description: -->
        <!-- item "board"  The Settings for the baord (Only one item allowed) -->
        <!-- L "set_ip"        => The IPv4 Address of the board -->
        <!-- L "set_user"      => The Linux User name of the board  -->
        <!-- L "set_password"  => The Linux User password of the board  -->
        <!-- L "set_flashBoot" => Enable or Disable of the writing of the u-boot bootloader FPGA-Configuration file -->
        <!--    L "Y"  => Enable | "N" => Disable  -->
        <!-- set_quartus_prime_ver Intel Quartus Prime Version to use <Version><Version No> -->
        <!--    L -> Quartus Prime Lite      (e.g. L16.1)  -->
        <!--    S -> Quartus Prime Standard  (e.g. S18.1)  -->
        <!--    P -> Quartus Prime Pro       (e.g. P20.1)  --> 
        <FlashFPGA2Linux>
            <board set_ip="192.168.0.109" set_user="root" set_pw="eit" set_flashBoot="Y" set_quartus_prime_ver="L20.1" />
        </FlashFPGA2Linux>
        ````
        </details>

* **Run the Python script to flash the FPGA-Configuration**
    ````shell
    python3 flashFPGA2rsyocto.py
    ````
    * **Note:** On Windows use `python` instate of `python3`
    <details>
    <summary><strong>Output of the Python script</strong></summary>
    <a name="Pos0"></a>
        
    ````shell
    [INFO] A valid Intel Quartus Prime Cyclone V SoC-FPGA project was found
    [INFO] Start to establish a SSH connection to the SoC-FPGA board with rsyocto
    [INFO] SSH Connection established to rsyocto (83% free disk space remains on the rootfs)
    [INFO] Generating a new FPGA-Configuration file for configuration with the Linux
    [INFO] Generating a new FPGA-Configuration file for configuration during boot
    [INFO] Starting SFTP Data transfer!
    [INFO] Cleanup SSH- and SFTP connection to rsyocto
    [INFO] Start coping the new Linux FPGA-Configuration file to rsyocto
    [INFO] Changing the FPGA-Configuration of FPGA-Fabric with the new one
    [INFO] Running FPGA-Configuration was changed successfully
    [INFO] Removing the old bootloader FPGA-Configuration from rsyocto
    [INFO] Copying the new bootloader FPGA-Configuration to rsyocto
    [INFO] Bootloader FPGA-Configuration was changed successfully
    [INFO] Cleanup SSH- and SFTP connection to rsyocto
    [INFO] SSH Thread and SFTP Data transfer done
    [SUCCESS] Support the author Robin Sebastian (git@robseb.de)
    ````
    </details>

**3. Run the Python Script to complie the *Intel Quartus Prime* FPGA project**

If the Python build script is executed in an *Intel Quartus Prime* FPGA project
where no output file (`.sof`) is available, the FPGA compilation process will be started by the script.
After the output file was created the script will generate the FPGA-Configuration file
and write it to the FPGA-Fabric over the network of your board.

* **Select your *Intel Quartus Prime* Version**
    * Use the following argument to select the *Intel Quartus Prime* Version that will be used to compile the FPGA project
    ````shell
    python3 flashFPGA2rsyocto.py -qv L20.1
    ````
    * **Note:** On Windows use `python` instate of `python3`
    * In the example is *Intel Quartus Prime* Lite 20.1 selected
    * Syntax: `<Version><Version No.>`
        * `L` --> `Intel Quartus Prime Lite`  
        * `S` --> `Intel Quartus Prime Standard`
        * `P` --> `Intel Quartus Prime Pro`
    * For example for *Intel Quartus Prime* Standard 16.1 use `S16.1`
* **Run the Python script**
    ````shell
    python3 flashFPGA2rsyocto.py -cf 1
    ````
<br>


**Optional: Disable the change of the boot (u-boot) FPGA-Configuration file**

The Python script will always overwrite the bootloader FPGA-Configuration file, as well. 
It will be loaded during the boot of the board to the FPGA-Fabric. To disable this feature use the 
following argument:
````shell
python3 flashFPGA2rsyocto.py -fb 0 
````
**Note:** On Windows use `python` instate of `python3`

**Help output**
````shell
D:\Tresorit\Robin\GithubProjects\rsyocvto_relase\v1.042\DE10STDrsyocto>python flashFPGA2rsyocto.py -h
usage: flashFPGA2rsyocto.py [-h] [-ip SET_IPADDRES] [-us SET_USER] [-pw SET_PASSWORD] [-cf EN_COMPLIE_PROJECT]
                            [-fb EN_FLASHBOOT] [-qv SET_QUARTUS_PRIME_VER]

optional arguments:
  -h, --help            show this help message and exit
  -ip SET_IPADDRES, --set_ipaddres SET_IPADDRES
                        Set the IPv4 Address of the board
  -us SET_USER, --set_user SET_USER
                        Set the Linux username of the board
  -pw SET_PASSWORD, --set_password SET_PASSWORD
                        Set the Linux user password of the board
  -cf EN_COMPLIE_PROJECT, --en_complie_project EN_COMPLIE_PROJECT
                        Complile the Intel Quartus Prime FPGA project (use "-cf 1")
  -fb EN_FLASHBOOT, --en_flashBoot EN_FLASHBOOT
                        Enable or Disable of the writing of the u-boot bootloader FPGA-Configuration fileFPGA-
                        Configuration [ 0: Disable]
  -qv SET_QUARTUS_PRIME_VER, --set_quartus_prime_ver SET_QUARTUS_PRIME_VER
                        Set the Intel Quartus Prime Version Note: Only requiered for FPGA Project Compilation! |
                        Quartus Prime Version to use <Version><Version No> | L -> Quartus Prime Lite (e.g. L16.1) | S
                        -> Quartus Prime Standard (e.g. S18.1) | P -> Quartus Prime Pro (e.g. P20.1)
````


[Back to the startpage](https://github.com/robseb/rsyocto)
