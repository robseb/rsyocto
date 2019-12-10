
# Analyze your applications with ARM Streamline
With ARM Streamline is a powerfull to Intel EDS included to trace debugg applications on Hardware Level

* ARM Streamline is a part of ARM DS-5 and [Intel SoC FPGA Embedded Development Suite (EDS) 18.1.0.625](https://www.intel.com/content/www/us/en/software/programmable/soc-eds/overview.html)
* For ARM DS-5 is a Software Licence requiered!
* Streamline requiere a server application for embedded Linux Systems called  [gatord](https://github.com/ARM-software/gator)
* The *rsyocto* Linux kernel is configured appropriately for Streamline and the server is started automatically

# Using Streamline to analyzing the system
1. Open Streamline 
2. Insiert as Target the IPc4-Address of your FPGA Board
  ![Alt text]( 	StreamlineConf.jpg?raw=true "Streamline configuration")
3. With a click of the "IC-Symbol" it is posible to selcet the **ARM Cortex A9** as target CPU and evets to capture
4. Pess the "recode-button" to start capuring
5. Choose a location to store the capure file
6. Now should Streamline show the live capured data
<br>


![Alt text](StreamlineExampleRecord.jpg?raw=true "Streamline sample recourd")
**Example: Streamline recourd during C++ compalation**
