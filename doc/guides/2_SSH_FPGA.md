# Windows Kernel Mode Driver (KMDF)
## Installation of the WKD 

+ Step by Step MSDN Guide: [Debug Universal Drivers - Step-by-Step Lab (Echo Kernel Mode) - Windows drivers \| Microsoft Docs](https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/debug-universal-drivers---step-by-step-lab--echo-kernel-mode-)  
+ Requiered Compunents on the Host (machine with Visual Studio)
  + Windows Driver Kit (WDK) (includes Plugin for Visual Studio)
+ Requiered compunents on the traget computer (machine with the Driver under Test)
  + Windows SDK 
+ booth computers must be connected to a domain and looged in with the same acount
+ open an command prompt with admin rights on the **target computer** and run folowing CMDs:
  ````shell
  bcdedit /set {default} DEBUG YES
  bcdedit /set TESTSIGNING ON 
  ````