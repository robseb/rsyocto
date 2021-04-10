[back](4_Python.md)


# Analyzation of applications with ARM DS-5 Streamline

With **ARM Development Studio (DS-5) Streamline** is a trace debugging application on the Hardware Level inside *Intel SoC-EDS* available. It can use the embedded **ARM CoreSight** Trace port debugging unit of the *Intel SoC-FPGAs* for real-time trace analyzation to show and qualify the behavior of the embedded SoC in hardware level. Streamline can use a JTAG-connection with a supported ARM debugger or can just use the Ethernet network interface. The JTAG interface brings the benefit to log the executed ARM instructions in real-time and to analyse the ARM cores in **TrustZone Secure Mode** (*privileged mode*). The **Intel (ALTERA) FPGA JTAG Blaster** of the *Terasic* development boards are supported by the Intel SoC-EDS ARM DS-5 Version via JTAG. In this guide the approach with the network interface is shown. The way with JTAG works in the same way. 

* *ARM Streamline* is a part of the *ARM Development Studio (DS-5)* and [Intel SoC FPGA Embedded Development Suite (EDS) 18.1.0.625 and later](https://www.intel.com/content/www/us/en/software/programmable/soc-eds/overview.html)
* For it a software licence is required!
* *Streamline* works as a server application running on the target embedded Linux Distribution. The server is called  [**"`gatord`"**](https://github.com/ARM-software/gator)
* The *rsyocto* Linux Kernel is configured appropriately for enabling *Streamline* support and the server starts automatically during the boot

# Using Streamline to analyzing the system
1. Open *ARM DS-5 Streamline*
2. Insert the target the **IPv4-Address**, the Linux user `root` and password `eit` of your FPGA Board
  ![Alt text]( 	StreamlineConf.jpg?raw=true "Streamline configuration")
3. With a click of the "**`IC-Symbol`**" it is possible to select the *ARMv7-A* **ARM Cortex-A9** as target CPU and the events you want to capture
4. Press the "**`record-button`**" to start capturing
5. Choose a location to store the capture file
6. Now *Streamline* shows the live data
<br>


![Alt text](StreamlineExampleRecord.jpg?raw=true "Streamline sample recourd")
**Example: ARM Development Studio Streamline record during C++ compilation with trace data**

 ## Continue with the next level: [Developing a new FPGA configuration](6_newFPGAconf.md)
