
# Analyzation of applications with ARM DS-5 Streamline
With *ARM DS-5 Streamline* is a trace debug applications on the Hardware Level inside *Intel EDS* available.

* ARM Streamline is a part of the ARM DS-5 Studio and [Intel SoC FPGA Embedded Development Suite (EDS) 18.1.0.625](https://www.intel.com/content/www/us/en/software/programmable/soc-eds/overview.html)
* For ARM DS-5 is a Software Licence required!
* Streamline works a server application running on the target  embedded Linux Systems called  [gatord](https://github.com/ARM-software/gator)
* The *rsyocto* Linux kernel is configured appropriately for Streamline and the server starts automatically

# Using Streamline to analyzing the system
1. Open *ARM DS-5 Streamline*
2. Insert  as Target the IPv4-Address of your FPGA Board
  ![Alt text]( 	StreamlineConf.jpg?raw=true "Streamline configuration")
3. With a click of the "IC-Symbol" it is possible to select the **ARM Cortex A9** as target CPU and events to capture
4. Press the "record-button" to start capturing
5. Choose a location to store the capture file
6. Now should Streamline show the live recorded data
<br>


![Alt text](StreamlineExampleRecord.jpg?raw=true "Streamline sample recourd")
**Example: Streamline record during C++ compilation**

 ## Continue with the next level: [Developing a new FPGA configuration](6_newFPGAconf.md)
