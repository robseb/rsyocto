[Back to the startpage](https://github.com/robseb/rsyocto)

# Developing a Linux Startup script
Linux Startup scripts are for embedded Linux systems really imported. 
Application services should start directly after a boot. This is particularly important, since *rsYocto* has a watshdog timer activated and the system can therefore restart unexpectedly.
For this reason, three possible ways to activate startup scripts are shown.

## 1. Adding of a startup script during runtime
* For that is tool `udate-rc.d` ([see here](http://manpages.ubuntu.com/manpages/bionic/man8/update-rc.d.8.html)) pre-installed
* **Create a new Linux Shell script** remotly with Visual Studio Code Insider or with `nano`
  ````bash
  nano /etc/init.d/myScript.h
  ````
* **Write the script**
  ```console
  #!/bin/sh
  # Your script
  echo "Hello SoC-FPGA"
  ````
* **Activate the script at startup**
  ````bash
  chmod +x /etc/init.d/myScript.h
  update-rc.d myScript.h defaults 100

## 2. Adding of a startup durning image creation
With the *rsYocto* building script it is posibile to add startup scripts into image file. 
That was shown in chapter 5

## 3. Adding of a startup with the Yocto project
For the development of *rsYocto* I designed a simple way import startup scripts with the yocto project. This is now a part of the `meta-rstools`-layer ([see here](https://github.com/robseb/meta-rstools))

___
 [Back to the startpage](https://github.com/robseb/rsyocto)
 
