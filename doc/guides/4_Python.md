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
5. Afeter a change of the Board, *rsYocto*-Version or the iPv4-Adress **you must be delate the content of this folder**  `C:\Users\<USER Name>\.ssh)` and repaied the Steps 1-4

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
  (change the **HostName** with the **IPv4-Adress of your board**):
``````shell
Host rsYocto
    ForwardAgent yes
    HostName 192.168.2.105
    User root
    IdentityFile ~/.ssh/id_rsa
`````` 
* Save and close this configuration file
* If a error occured close and restart Visual Studio Code Insider and try it again

### III. Connection of the Board with Visual Studio Code Insider
* Open Visual Studio Code Insider
* Select inside the side bar "**Remote SSH**" 
+ under the tap "**Connections**" should not appear the entries for the previously add entry with the name **"rsYocto"**
* right click on this entry and choose **"Connect Host in current Window"**

  ![Alt text](VisualCodeConfig4.jpg?raw=true "Visual Studio Configuration 4")
 
  * The first attach attempt takes a little bit longer, because the Visual Studio downloads and install the Visual Studio Code Server
  * **(Be shure that the board is connected to the internet)**
  * in case the connection to the board is established successfully a green button edge item with *connected symbol* should appear

### IV. Accsing the rootfs files remotly 
*  Visual Studio Code Insider access the rootfs of *rsYocto*
*  On *rsYocto* are some Python samples applications pre-installed
*  Navigate on the Sidebar to **"Explorer"** click the blue **"Open Folder"**
*  Visual Studio Code Insider should now ask for remote directory to add 
  * default: `"/home/root/"` --> user root folder with the Python examples
  * websever: `"/usr/share/apache2/default-site/htdocs"` --> every file inside this folder will by acessebil with a webbrauser
* click okay

 ![Alt text](VisualCodeConfig5.jpg?raw=true "Visual Studio Configuration 5")
* Now you can acces the files of the rootfs

 ![Alt text](VisualCodeConfig6.jpg?raw=true "Visual Studio Configuration 6")


### V. Preparing the Python remote development
* Select inside the sidebar "**Extension**"
* select the prevosly installed extension "**Python**" (by Microsoft)
* Press the green button "**Install on SSH:rsYocto**"

 ![Alt text](VisualCodeConfig7.jpg?raw=true "Visual Studio Configuration 7")
 
* With this imput start Visual Studio Code Server with the installation of the requiered remote python debuging compunents
* Press then  "**reload requiered**" to actavte the changes 
<br>

### VI. Debugging Python Code remotly
* Open any pre-installed Python sample
* Navigate to the sidebar Icon **"Debug and Run"** and click on the "**Debug with Python**" Button
* Then choose in the Drop Down Menue "**Python File**" 

 ![Alt text](VisualCodeConfig8.jpg?raw=true "Visual Studio Configuration 8")
 
 * Alterevly you can configre the Debugger with following json file:
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
  * If not: press the "**Start Debuging**" button or **F5**
  
       ![Alt text](VisualCodeConfig9.jpg?raw=true "Visual Studio Configuration 9")
 
*  select inside the side bar "**Debug**" 
*  choose inside the drop down menu the prevosly configuered debug configuration with the name "**Python curent file remotly**"
*  press the "**Start Debuging**" button or **F5** to debugg the open Python code

### VII.  Use the Python Package Manager PiP
* The pre-installed example "*serialEchoDemo.py*" requiers the [pySerial](https://pyserial.readthedocs.io/en/latest/shortintro.html)-module
* "*rsYocto*" has a full suppored for Python PiP
* You can install almost all PiP-moudles 
* Use the PiP [Homepage](https://pypi.org/) to find a module and then run following comand to install that with *rsYocto*:
     ````bash
      python3 -m pip install --upgrade <moduel to install> --trusted-host pypi.org --trusted-host files.pythonhosted.org 
     ````
* To install *pySerial* use the String:
     ````bash
      python3 -m pip install --upgrade pyserial --trusted-host pypi.org --trusted-host files.pythonhosted.org 
     ````

 ## Continue with the next level: [Analyze your applications with ARM Streamline](5_Streamline.md)
