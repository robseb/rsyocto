#  Debugging C++ applications remotely
This article shows how to use Microsft Viusal Studio 2019 as C++ IDE of *rsYocto*. 
The newer relasese allow Linux develempent on ARMv7A with the main advantige over clasical exclipse-based IDEs to 
use by default the GDB Server remotely over the network. Also can Visual Studio use the compilers on the remote machine. 
On *rsYocto* are all requiered components for Visual Studio pre-installed. Now it is for C++ developer really easy to install Visual Studio on an Windows Computer. If the same requirements would be achieved with Eclipse, the Installieraufwand on Windows is much more complicated.
The following ilustration shows how *rsYocto* and Microsoft Visual Studio work together:


![Alt text](IneractionRsYoctoVisalStudio.jpg?raw=true "rsYocto and Visual Studio")


# Install Microsft Visual Studio for Linux development
1. Download one Version of [**Microsoft Visual Studio 2019 for Windows**] (https://visualstudio.microsoft.com/) (all Versions are fine) 
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
