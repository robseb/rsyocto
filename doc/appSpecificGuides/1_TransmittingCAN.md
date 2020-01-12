 [Back to the startpage](https://github.com/robseb/rsyocto)

# Writing a python script to transmit CAN-packages
**In this guide shows how simple it is to transmit CAN-packages within a Python script on a running embbeded Linux system.**
It is a part of my "*Mapping HPS Peripherals, like I²C or CAN, over the FPGA fabric to FPGA I/O and using embedded Linux to control them*"-guide, were I show the **complete development process** with the FPGA design and bootloader creation (see [here](https://github.com/robseb/HPS2FPGAmapping)

* To **start the CAN0** execute this command on *rsYocto* to **enable the CAN network Port**:
  ````bash 
  ip link set can0 type can bitrate 125000
  ip link set up can0
  ````
* Install `python-can` with python pip on the running *rsYocto*
  ````bash
  pip install python-can
  ````
 Use *Visual Studio Code Insider* to **debug** this *python-can* application remotely (see [here](https://github.com/robseb/rsyocto/blob/master/doc/guides/4_Python.md)). 
 Or to use the onboard `nano`editor to write the python code.
 
 * Create a new Python file, for example:
   ````bash
   nano sendCanPackage.py
   ````
  * Insert following lines to this python file as shown in the [python-can documentation](https://python-can.readthedocs.io/en/master/)
	````python
	#!/usr/bin/env python
	# coding: utf-8

	#
	#This example shows how sending a single message works.
	#

	import can

	def send_one():

		# this uses the default configuration (for example from the config file)
		# see https://python-can.readthedocs.io/en/stable/configuration.html

		# Using specific buses works similar:
		bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=12500)
		# ...

		msg = can.Message(arbitration_id=0xAC,
			  data=[0xAB, 0xAC, 0xAD, 0xAE],
			  is_extended_id=False)

		try:
			bus.send(msg)
			print("Message sent on {}".format(bus.channel_info))
		except can.CanError:
			print("Message NOT sent")


	if __name__ == '__main__':
		send_one()
	````
  * Save and close this python file or **start a debugging session** with *Visual Studio Code Insider*
  * Connect to the **Adrunio Pin D8** to **CAN TX** and the Pin **D9** to **CAN RX** on a **3.3V Can-Bus Transiver**
  * **Execute the python script**
    ```python 
    python3 sendCanPackage.py
    ````
  * Now the Cyclone V SoC-FPGA **transmits a CAN package through the Arduino header with the ID 0xAC and the Payload 0xABACADAE**:
  	````bash
	root@cyclone5:~# python3 sendCanPackage.py
	Message sent on socketcan channel 'can0'
	````
	
  	![Alt text](CANoszigram.png?raw=true "CAN Osci")

If no one acknowledged this package the *Bosch CAN-Controller* *re-transmit* the package with the maximum available resources automatically until a ACK happen.
The embedded *Bosch CAN-Controller* can also **detect linkage errors**. 
I case of a missing connection to a CAN-Bus member a Kernel Message will be triggered and the **CAN Controller shuts down**.
Use the following command to **restart the CAN-Controller**:
````bash 
link set down can0
ip link set up can0
````
<br>

___
 [Back to the startpage](https://github.com/robseb/rsyocto)
