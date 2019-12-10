#  Debugging C++ applications remotely
This article describes how to use *Microsoft Visual Studio 2019* for *rsYocto* C++ development. 
The newer releasees of *Visual Studio* are capable to work as embedded Linux development IDE for *ARMv7A*. *Visual Studio* can use the for communicating with Linux `gdb-Server` and `SSH`.
On *rsYocto* are all required components for Visual Studio pre-installed. 

The following illustration shows how *rsYocto* and Microsoft Visual Studio work together:

![Alt text](IneractionRsYoctoVisalStudio.jpg?raw=true "rsYocto and Visual Studio")


# Install Microsft Visual Studio for Linux development
1. Download one Version of [**Microsoft Visual Studio 2019 for Windows**](https://visualstudio.microsoft.com/) 
2. Follow the Visual Studio installer and include "**Linux Development for C++**" as workload to your installation
![Alt text](VisualStudioInstalation.png?raw=true "Visual Studio installation")
3. Finish the installation

# Create a new *rsYocto* Linux project
1. Open Mirosoft Visual Studio 2019 and **Create a new project** 
2. Select as langugare "**C++**" and plattform "**Linux**" and choose "**Console App**"
![Alt text](VisulStudioCreateNewProject.jpg?raw=true "Create new Visual Studio Project")
3. Press "**next** and give your project a name
4. A new Visual Studio Solution should be aper with a getting started guide
5. This Guide shows how to connfiure the connection the remote Linux machine
6. Please follow this instructions with the settings
  * Plattform: `ARM`
  * Host Name: `The IPv4-Address of your Board`
  * Port: `22`
  * User name: `root`
  * Authentification type: `Password`
  * Password: `eit`
  * to chnage later the IP-Address navigate to `Tools/Options/Coss Platform`, click there the "Remove"-Button and then "Add" 
 7. At this point you can begin to develop and debug your own C++ applications running on SoC-FPGA 
 
 ![Alt text](VisualStudioDemo.jpg?raw=true "rsYocto and Visual Studio Hello World")
 
 # Use the POSIX Libery with Visul Studio
 * With the Linux Posix Comands have Microsoft Visual Stuio some iusues
 * I solved this problem by creating a special Visual Studio soulution
 * You can use this project as a templat 

 ## Continue with the next level: [Debugging Python applications remotely](4_Python.md)
