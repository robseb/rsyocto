#  	Debugging Python applications remotely

## Configuration of Visual Studio Code Insiders remote access for Python debugging

This Guide descripts how to install and configure Visual Studio Code Insider to accsess the Linux system remotely over ssh. Later on is shown how to use Visual Studio Code to remote debug Phyton applications.

Visual Studio Code is light way and powerfull code editor build by Microsoft. Visual Studio Code is universal binary and runs on Windows, Linux and Mac OS. **Visual Studio Code Insider** is a spezial beata version and exteands Visual Studio Code with more advands plugins. Only with Visual Studio Insider alows remote acess via SSH to ARMv7A.  

But Visual Studio Code Insider does only SSH access with a SSH-Keygen. The key must be regenerated every Board-, SD Card or ip Adress change. 

The following step by step guide descriptes how to setup Visual Studio Code Insider for Python remote development and debuging on Windows 10. For other systems please follow Microsofts instructions: 
[Visual Studio Code Remote Development Troubleshooting Tips and Tricks](https://code.visualstudio.com/docs/remote/troubleshooting)
Chapter: Improving your security with a dedicated key

With the following guide description Microsoft the function of Visual Studio Code Insider with remote debugging:
[Developing on Remote Machines using SSH and Visual Studio Code](https://code.visualstudio.com/docs/remote/ssh)

### I. Generation of the SSH Key with Windows 10
* Open the Windows "**Command Prompt**" (without admin rights)
* Execute following Command inside the Windows Command Prompt:
1.    **Generate a new SSH Key**
      (Windows stores the key under following directory:  `C:\Users\<USER Name>\.ssh)`
      * Pres allways enter (do not enter a extra password or a other name)
      ``````shell 
      ssh-keygen -t rsa -b 4096
       ``````
2.    **Set the IPv4 Adress of the board**
      here for exmaple with the IP 192.168.2.105
       ``````shell 
       SET REMOTEHOST=root@192.168.2.105
      ``````
5.    **Copy the generated SSH-Key to the board via SSH**
      after this command should the *rsYocto* splash screen appear and the linux system           should ask for the password: **eit**
      ``````shell       
      scp %USERPROFILE%\.ssh\id_rsa.pub %REMOTEHOST%:~/tmp.pub
      `````` 
4.   **Authenticate and activate the SSH key** 
      again,after this command should the *rsYocto* splash screen appear and the linux             system should ask for the password: **eit**
      ``````shell 
      ssh %REMOTEHOST% "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat ~/tmp.pub >>  ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys && rm -f ~/tmp.pub"
      ``````
5. Afeter a change of the Board, *rsYocto*-Version* or the iPv4-Adress you must delate the content of folloging folder  `C:\Users\<USER Name>\.ssh)` and repaied the Steps 1-4

### II. Installation Visual Studio Code Insider and configuration of remote access
* Download and install the latest version of **Visual Studio Code Insider**:
  [Download Visual Studio Code Insiders](https://code.visualstudio.com/insiders/)
* Follow the installation Instructions
* After the isntallation is complite open Visual Studio Code Insider
* On sidebar (toolbar on the left hand side) click the **Extenstion**-icon 
* Serche for the extansion:"**Remote Development**" (by Microsoft) ([Remote Development - Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)) and press the **install**-button to install this extansion

  ![Alt text](VisualCodeConfig1.jpg?raw=true "Visual Studio Configuration 1")
 
* Repead this steps for following extansions: "**Remote - SSH**"(by Microsoft) ([Remote - SSH - Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh)) and for the extansion **"Python"** (by Microsoft)
<br>

* **Restart Visual Studio Code Insuder** to accept the changes
* Open on the side bar "**Remote Explorer**"
* Choose in the Drop Down Menue "REMOTE EXPLORER" the **SSH Target**
* Move the mouse of the titel "SSH TARGETS" and click on the *gear-icon*

  ![Alt text](VisualCodeConfig2.jpg?raw=true "Visual Studio Configuration 2")
 
* Select in the appered Dropdown menu **"C:\Users\<USER Name>\.ssh\config"** 

  ![Alt text](VisualCodeConfig3.jpg?raw=true "Visual Studio Configuration 3")
 
* Configure the name and Ip-Address by adding following to the conf-file
  (change the **HostName** with the **IPv4-Adress of remote board**):
``````shell
Host rsYocto
    ForwardAgent yes
    HostName 192.168.2.105
    User root
    IdentityFile ~/.ssh/id_rsa
`````` 
* Save and close this configuration file
* If a error occured close and restart Visual Studio Code Insider and try it again

### III. Connection of the Board with Visual Studio Code insider
* open Visual Studio Code Insider
* select inside the side bar "**Remote SSH**" 
+ under the tap "**Connections**" should not appear the entries for the previously add entry with the name **"rsYocto"**
* right click on this entry and choose **"Connect Host in current Window"**

  ![Alt text](VisualCodeConfig4.jpg?raw=true "Visual Studio Configuration 4")
 
  * the first attach attempt takes a little bit longer, because the Visual Studio downloads and install the Visual Studio Code Server
  **(Be shure that the board is connected to the internet)**
  * in case the connection to the board is established successfully a green button edge item with *connected symbol* should appear

### IV. Accsing remotly files 
* be sure that a proper SSH connection is established
* select inside the side bar "**Explorer**" 
* press here the button "**Open Folder**"
* Visual Studio Code Insider should now ask for remote directory to add 
  * default: *"/home/root/"* --> user root folder
  * websever: *"/usr/share/apache2/default-site/htdocs"* --> every file inside this folder will by acessebil with a webbrauser
* click okay


### V.  Preparing the Python remote development
* be shure that a proper SSH connection is established
* select inside the sidebar "**Extension**"
* select the prevosly installed extension "**Python**" (by Microsoft)
* press the green button "**Install on SSH:rs.yocto**"
* with this imput start Visual Studio Code Server to install the requiered remote python debuging compunents
* press the "**reload requiered**" to actavte the changes 
<br>
* select inside the side bar "**Debug**" 
* Add a new debugging configuration by selecting the menueiteam **"Debug/Add Configuration.."**
* a json file should appear
*  insiered following to this file:
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
* save and close the file

### VI.  Debugging Python code remotly
*  be shure that a proper SSH connection is established
*  open remotly any Python code file 
*  select inside the side bar "**Debug**" 
*  choose inside the drop down menu the prevosly configuered debug configuration with the name "**Python curent file remotly**"
*  press the "**Start Debuging**" button or **F5** to debugg the open Python code

### VII.  Show system resource
* to show the CPU load, Memory usage and more insde Visual Studio Code install the extension **"Resource Monitor"** (by mutantdino) ([Resource Monitor - Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=mutantdino.resourcemonitor))
* add install this extation to remote boar with the button: "**Install on SSH:rs.yocto**"
* reload Visual Studio Code Insider
* now should aper at the button of the window a bar with the system resources
