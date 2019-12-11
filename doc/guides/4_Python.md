#  	Debugging Python applications remotely

This Guide descripts how to install and configure *Visual Studio Code Insider* to accsess the Linux system remotely over `ssh`. Later on is shown how to use *Visual Studio Code* to remote debug Phyton applications.

*Visual Studio Code* is a code editor build by Microsoft. It is a universal binary application and runs on Windows, Linux and macOS. **Visual Studio Code Insider** is a special beta version and extended Visual Studio Code with advands plugins. Only *Visual Studio Insider* allow a remote access via SSH to *ARMv7A* Linux-devices.

*Visual Studio Code Insider* does allow only *SSH* access with a **SSH-Keygen**. The key must be regenerated after every Board-, SD card or IP-Address switch.

The following step by step guide shows how to setup *Visual Studio Code Insider* for Python application remote development and debugging on *Windows 10* PC.For other systems please follow Microsoft's instructions:
[Visual Studio Code Remote Development Troubleshooting Tips and Tricks](https://code.visualstudio.com/docs/remote/troubleshooting)
(Chapter: Improving your security with a dedicated key)

With the following guide descripts *Microsoft* the function of *Visual Studio Code Insider* by remote debugging:
[Developing on Remote Machines using SSH and Visual Studio Code](https://code.visualstudio.com/docs/remote/ssh)

### I. Generation of the SSH Key with Windows 10
* Open the Windows "**Command Prompt**" (without admin rights)
* Execute following Command inside the Windows Command Prompt:
1.    **Generate a new SSH Key**
      (Windows stores the key under following directory:  `C:\Users\<USER Name>\.ssh)`
      ``````shell 
        ssh-keygen -t rsa -b 4096
       ``````
        * Pres always ENTER (do not enter an extra password or a other name):
2.    **Set the IPv4 Address of the board**
       ``````shell 
        SET REMOTEHOST=root@192.168.2.105
      ``````
      * Here for exmaple with the IP 192.168.2.105
5.    **Copy the generated SSH-Key via SSH to the board**
      * After this command should the *rsYocto* splash screen appear and the linux system should ask for the password: **eit**
      ``````shell       
       scp %USERPROFILE%\.ssh\id_rsa.pub %REMOTEHOST%:~/tmp.pub
      `````` 
4.   **Authenticate and activate the SSH key** 
       Again,after this following command should the *rsYocto* splash screen appear and the linux system should ask for the password: **eit**
      ``````shell 
      ssh %REMOTEHOST% "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat ~/tmp.pub >>  ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys && rm -f ~/tmp.pub"
      ``````
      
### II. Installation of *Visual Studio Code Insider* and configuration of remote access
* Download and install the latest version of **Visual Studio Code Insider**:
  [Download Visual Studio Code Insiders](https://code.visualstudio.com/insiders/)
* Follow the installation Instructions
* After a successful installation open Visual Studio Code Insider
* On sidebar (toolbar on the left hand side) click the **Extension**-icon
* Search for the extension:"**Remote Development**" (by Microsoft) ([Remote Development - Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)) and press the **install**-button to install this extension

  ![Alt text](VisualCodeConfig1.jpg?raw=true "Visual Studio Configuration 1")

* **Restart Visual Studio Code Insider** to accept the changes
* Click on the side bar "**Remote Explorer**"
* Choose in the Drop Down Menu "REMOTE EXPLORER" the **SSH Target**
* Move the mouse of the title **"SSH TARGETS"** and click on the *gear-icon*

  ![Alt text](VisualCodeConfig2.jpg?raw=true "Visual Studio Configuration 2")
 
* Select in the appeared Dropdown menu: **"C:\Users\<USER Name>\.ssh\config"** 

  ![Alt text](VisualCodeConfig3.jpg?raw=true "Visual Studio Configuration 3")
 
* Configure the name and Ip-Address by adding following to the `jason`-configuration file
  (change the **HostName** with the **IPv4-Address of your board**):
``````jason
Host rsYocto
    ForwardAgent yes
    HostName 192.168.2.105
    User root
    IdentityFile ~/.ssh/id_rsa
`````` 
* Save and close this configuration file
* If a error occured close and restart *Visual Studio Code Insider* and try it again

### III. Connection of the *rsYocto* with *Visual Studio Code Insider*
* Open *Visual Studio Code Insider*
* Select on the side bar "**Remote SSH**" 
* Under the tap "**Connections**" should appear the entries for the previously add entry with the name **"rsYocto"**
* Right click on this entry and choose **"Connect Host in current Window"**

  ![Alt text](VisualCodeConfig4.jpg?raw=true "Visual Studio Configuration 4")
 
  * The first attach attempt takes a little bit longer, because the Visual Studio downloads and install the Visual Studio Code Server
  * **(Be sure that the board is connected to the internet)**
  * In case that the connection to the board is established successfully a green iteam with a **connected symbol** should appear

### IV. Accessing the rootfs files remotely
*  *Visual Studio Code Insider* can access the rootfs of *rsYocto*
*  On *rsYocto* are some Python samples applications pre-installed
*  Navigate on the Sidebar to **"Explorer"** click the blue **"Open Folder"**
*  *Visual Studio Code Insider* should now ask for a remote directory to add 
  * Default: `"/home/root/"` --> user *root folder* with the Python examples
  * Web sever: `"/usr/share/apache2/default-site/htdocs"` --> every file inside this folder will be accessible with a web browser
* Click okay

 ![Alt text](VisualCodeConfig5.jpg?raw=true "Visual Studio Configuration 5")
* Now is the rootfs accesibil with the Visual Studio Code Insider File explorer 

 ![Alt text](VisualCodeConfig6.jpg?raw=true "Visual Studio Configuration 6")


### V. Preparing the Python remote development
* Select inside the sidebar "**Extension**"
* Choose the previously installed extension "**Python**" (by Microsoft)
* Press the green button "**Install on SSH:Yocto**"

 ![Alt text](VisualCodeConfig7.jpg?raw=true "Visual Studio Configuration 7")
 
* With this input start *Visual Studio Code Server* with the installation of the required remote python debugging components
* Press  "**reload required**" to activate the changes
<br>

### VI. Debugging Python Code remotely
* Open any pre-installed Python sample
* Navigate to the sidebar Icon **"Debug and Run"** and click on the "**Debug with Python**" Button
* Choose in the Drop Down Menu "**Python File**" 

 ![Alt text](VisualCodeConfig8.jpg?raw=true "Visual Studio Configuration 8")
 
 * Or use following `json`-file to configure the debugger:
      ``````json
            {
            "version": "0.2.0",
            "configurations": [
                  {
                      "type": "python",
                      "request": "launch",
                      "name": "Python curent file remotly",
                      "program": "${file}",
                      "console":"integratedTerminal"
                  }
                ]
            }
      ``````
  * The remote Debugging should start     
  * If not: press the "**Start Debugging**" button or **F5**
  * Now is Visual Studio Code configured to write and debug any python Code directly on *rsYocto*
  
       ![Alt text](VisualCodeConfig9.jpg?raw=true "Visual Studio Configuration 9")
       
___

### VII. Use of the Python Package Manager PiP
* The pre-installed example "*serialEchoDemo.py*" requires the [pySerial](https://pyserial.readthedocs.io/en/latest/shortintro.html)-module
* "*rsYocto*" has a full supported for *Python PiP*
* Use the PiP [Homepage](https://pypi.org/) to find a module
* Run following command to download and install this module with *rsYocto*:
     ````bash
      python3 -m pip install --upgrade <module to install> --trusted-host pypi.org --trusted-host files.pythonhosted.org 
     ````
* To install *pySerial* use the String:
     ````bash
      python3 -m pip install --upgrade pyserial --trusted-host pypi.org --trusted-host files.pythonhosted.org 
     ````
* Now it is possible use Python code, that are designed within large communities (e.g. Raspberry Pi-community), on a SoC-FPGA

 ## Continue with the next level: [Analyzation of applications with ARM DS-5 Streamline](5_Streamline.md)
