[Back to the startpage](https://github.com/robseb/rsyocto)

# Developing a Linux Startup script
Linux Startup scripts are really important for embedded Linux systems. 
Application services should start directly after a boot. This is particularly necessary, because *rsyocto* has a watchdog timer activated and the system can therefore restart unexpectedly.
For this reason, three possible ways to activate startup scripts are shown.

## 1. Adding a startup script during runtime
* For that the tool `udate-rc.d` ([see here](http://manpages.ubuntu.com/manpages/bionic/man8/update-rc.d.8.html)) is pre-installed
* **Create a new Linux Shell script** remotely with *Microsoft Visual Studio Code Insider* or with `nano`
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

## 2. Adding a startup script during image creation
With the *rsyocto* building script it is possible to add startup scripts into an image file. 
That was shown, as well.

## 3. Adding a startup script with the Yocto project
For the development of *rsyocto* I designed a simple way to import startup scripts with the Yocto project. This is a part of the `meta-intelfpga`-layer ([see here](https://github.com/robseb/meta-intelfpga)).

___
 [Back to the startpage](https://github.com/robseb/rsyocto)
 
