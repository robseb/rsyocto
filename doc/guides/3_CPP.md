[back](2_FPGA_HARDIP.md)


#  Debugging C++ applications remotely
This article describes how to use *Microsoft Visual Studio 2019* for *rsyocto* C++ development. 
The newer releases of *Visual Studio* are capable to work as embedded Linux development IDE for *ARMv7-A*. *Visual Studio* can use the  `gdb-Server` and `SSH`for communicating with Linux.
On *rsyocto* all required components for Visual Studio are pre-installed. 

The following illustration shows how *Linux* and Microsoft Visual Studio work together:

![Alt text](IneractionRsYoctoVisalStudio.jpg?raw=true "Linux and Visual Studio")

Note: Instate of using the complex *Microsoft Visual Studio* for C++ development and debugging is a more pleasant way with the code editor *Microsoft Visual Studio Code* and `cmake` available. To demonstrate is approach I wrote following **GUIDE XXXXXXXXXXXXX**.
<br>

# Installing Microsoft Visual Studio for Linux development
1. Download one Version of [**Microsoft Visual Studio 2019 for Windows**](https://visualstudio.microsoft.com/) 
2. Follow the *Visual Studio installer* and include "**Linux Development for C++**" as workload to your installation
![Alt text](VisualStudioInstalation.png?raw=true "Visual Studio installation")
3. Finish the installation

# Creating a new Linux project
1. Open *Mirosoft Visual Studio 2019* and **Create a new project** 
2. Select as language "**C++**" and platform "**Linux**" and choose "**Console App**"
![Alt text](VisulStudioCreateNewProject.jpg?raw=true "Create new Visual Studio Project")
3. Press "**next**" and give your project **a name**
4. A new *Visual Studio Solution* should appear with a getting started guide
5. This Guide shows how to configure the connection of the remote Linux machine
6. Please follow this instructions with this settings:
   * **Platform:** `ARM`
   * **Host Name:** `<IPv4-Address of your Board>`
   * **Port:** `22`
   * **User name:** `root`
   * **Authentication type:** `Password`
   * **Password:** `eit`
   * **To change the IP-Address later** navigate to `Tools/Options/Cross Platform` and click the  `Remove`- and then `Add`-Button 
 7. At this point the Visual Studio is ready for Linux C++ development 
 
 ![Alt text](VisualStudioDemo.jpg?raw=true "rsyocto and Visual Studio Hello World")
 <br>

# Known issues with Microsoft Visual Studio and Linux
 * Read the console output only and ingnore the error windows 
 * Ingore the "*rysnc could not start error*" (*rsync* is installed properly)
 * After any issues try to `clean and rebuild the solution`

# Getting Started- and in-depth Demos
I wrote further C++ Demo Visual Studio projects to show how to
  * Interact with the HPS Hard-IP 
  * Interact with FPGA Soft-IP
  * Changing the FPGA Configuration with C++
  * And more...

  The projects and guide is **[Available here](https://github.com/robseb/LinuxVSCppFPGA)**.
<br>


 ## Continue with the next level: [Debugging Python applications remotely](4_Python.md)
