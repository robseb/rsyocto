# TCL File Generated by Component Editor 18.1
# Mon Apr 20 11:20:55 CEST 2020
# DO NOT MODIFY


# 
# DE10STD7sig "DE10STD7sig" v1.0
# Robin Sebastian  2020.04.20.11:20:55
# 24 Bit Hex Seven Sigment Display Avalon Interface for Terasic DE10 Standard Board 
# 

# 
# request TCL package from ACDS 16.1
# 
package require -exact qsys 16.1


# 
# module DE10STD7sig
# 
set_module_property DESCRIPTION "24 Bit Hex Seven Sigment Display Avalon Interface for Terasic DE10 Standard Board "
set_module_property NAME DE10STD7sig
set_module_property VERSION 1.0
set_module_property INTERNAL false
set_module_property OPAQUE_ADDRESS_MAP true
set_module_property AUTHOR "Robin Sebastian "
set_module_property DISPLAY_NAME DE10STD7sig
set_module_property INSTANTIATE_IN_SYSTEM_MODULE true
set_module_property EDITABLE true
set_module_property REPORT_TO_TALKBACK false
set_module_property ALLOW_GREYBOX_GENERATION false
set_module_property REPORT_HIERARCHY false


# 
# file sets
# 
add_fileset QUARTUS_SYNTH QUARTUS_SYNTH "" ""
set_fileset_property QUARTUS_SYNTH TOP_LEVEL sevenSigDisplay
set_fileset_property QUARTUS_SYNTH ENABLE_RELATIVE_INCLUDE_PATHS false
set_fileset_property QUARTUS_SYNTH ENABLE_FILE_OVERWRITE_MODE false
add_fileset_file D10STDsevenSigDisplay.sv SYSTEM_VERILOG PATH D10STDsevenSigDisplay.sv TOP_LEVEL_FILE
add_fileset_file sevenSigSegmentDriver.sv SYSTEM_VERILOG PATH sevenSigSegmentDriver.sv


# 
# parameters
# 


# 
# display items
# 


# 
# connection point avalon_slave_0
# 
add_interface avalon_slave_0 avalon end
set_interface_property avalon_slave_0 addressUnits WORDS
set_interface_property avalon_slave_0 associatedClock clock50Hz
set_interface_property avalon_slave_0 associatedReset reset
set_interface_property avalon_slave_0 bitsPerSymbol 8
set_interface_property avalon_slave_0 burstOnBurstBoundariesOnly false
set_interface_property avalon_slave_0 burstcountUnits WORDS
set_interface_property avalon_slave_0 explicitAddressSpan 0
set_interface_property avalon_slave_0 holdTime 0
set_interface_property avalon_slave_0 linewrapBursts false
set_interface_property avalon_slave_0 maximumPendingReadTransactions 0
set_interface_property avalon_slave_0 maximumPendingWriteTransactions 0
set_interface_property avalon_slave_0 readLatency 0
set_interface_property avalon_slave_0 readWaitTime 1
set_interface_property avalon_slave_0 setupTime 0
set_interface_property avalon_slave_0 timingUnits Cycles
set_interface_property avalon_slave_0 writeWaitTime 0
set_interface_property avalon_slave_0 ENABLED true
set_interface_property avalon_slave_0 EXPORT_OF ""
set_interface_property avalon_slave_0 PORT_NAME_MAP ""
set_interface_property avalon_slave_0 CMSIS_SVD_VARIABLES ""
set_interface_property avalon_slave_0 SVD_ADDRESS_GROUP ""

add_interface_port avalon_slave_0 write write Input 1
add_interface_port avalon_slave_0 address address Input 1
add_interface_port avalon_slave_0 writedata writedata Input 32
set_interface_assignment avalon_slave_0 embeddedsw.configuration.isFlash 0
set_interface_assignment avalon_slave_0 embeddedsw.configuration.isMemoryDevice 0
set_interface_assignment avalon_slave_0 embeddedsw.configuration.isNonVolatileStorage 0
set_interface_assignment avalon_slave_0 embeddedsw.configuration.isPrintableDevice 0


# 
# connection point reset
# 
add_interface reset reset end
set_interface_property reset associatedClock clock50Hz
set_interface_property reset synchronousEdges DEASSERT
set_interface_property reset ENABLED true
set_interface_property reset EXPORT_OF ""
set_interface_property reset PORT_NAME_MAP ""
set_interface_property reset CMSIS_SVD_VARIABLES ""
set_interface_property reset SVD_ADDRESS_GROUP ""

add_interface_port reset reset_n reset_n Input 1


# 
# connection point clock50Hz
# 
add_interface clock50Hz clock end
set_interface_property clock50Hz clockRate 0
set_interface_property clock50Hz ENABLED true
set_interface_property clock50Hz EXPORT_OF ""
set_interface_property clock50Hz PORT_NAME_MAP ""
set_interface_property clock50Hz CMSIS_SVD_VARIABLES ""
set_interface_property clock50Hz SVD_ADDRESS_GROUP ""

add_interface_port clock50Hz clk_50Mhz clk Input 1


# 
# connection point hex_io0
# 
add_interface hex_io0 conduit end
set_interface_property hex_io0 associatedClock clock50Hz
set_interface_property hex_io0 associatedReset reset
set_interface_property hex_io0 ENABLED true
set_interface_property hex_io0 EXPORT_OF ""
set_interface_property hex_io0 PORT_NAME_MAP ""
set_interface_property hex_io0 CMSIS_SVD_VARIABLES ""
set_interface_property hex_io0 SVD_ADDRESS_GROUP ""

add_interface_port hex_io0 hex0pins readdata Output 7


# 
# connection point hex_io1
# 
add_interface hex_io1 conduit end
set_interface_property hex_io1 associatedClock clock50Hz
set_interface_property hex_io1 associatedReset reset
set_interface_property hex_io1 ENABLED true
set_interface_property hex_io1 EXPORT_OF ""
set_interface_property hex_io1 PORT_NAME_MAP ""
set_interface_property hex_io1 CMSIS_SVD_VARIABLES ""
set_interface_property hex_io1 SVD_ADDRESS_GROUP ""

add_interface_port hex_io1 hex1pins readdata Output 7


# 
# connection point hex_io2
# 
add_interface hex_io2 conduit end
set_interface_property hex_io2 associatedClock clock50Hz
set_interface_property hex_io2 associatedReset reset
set_interface_property hex_io2 ENABLED true
set_interface_property hex_io2 EXPORT_OF ""
set_interface_property hex_io2 PORT_NAME_MAP ""
set_interface_property hex_io2 CMSIS_SVD_VARIABLES ""
set_interface_property hex_io2 SVD_ADDRESS_GROUP ""

add_interface_port hex_io2 hex2pins readdata Output 7


# 
# connection point hex_io3
# 
add_interface hex_io3 conduit end
set_interface_property hex_io3 associatedClock clock50Hz
set_interface_property hex_io3 associatedReset reset
set_interface_property hex_io3 ENABLED true
set_interface_property hex_io3 EXPORT_OF ""
set_interface_property hex_io3 PORT_NAME_MAP ""
set_interface_property hex_io3 CMSIS_SVD_VARIABLES ""
set_interface_property hex_io3 SVD_ADDRESS_GROUP ""

add_interface_port hex_io3 hex3pins readdata Output 7


# 
# connection point hex_io4
# 
add_interface hex_io4 conduit end
set_interface_property hex_io4 associatedClock clock50Hz
set_interface_property hex_io4 associatedReset reset
set_interface_property hex_io4 ENABLED true
set_interface_property hex_io4 EXPORT_OF ""
set_interface_property hex_io4 PORT_NAME_MAP ""
set_interface_property hex_io4 CMSIS_SVD_VARIABLES ""
set_interface_property hex_io4 SVD_ADDRESS_GROUP ""

add_interface_port hex_io4 hex4pins readdata Output 7


# 
# connection point hex_io5
# 
add_interface hex_io5 conduit end
set_interface_property hex_io5 associatedClock clock50Hz
set_interface_property hex_io5 associatedReset reset
set_interface_property hex_io5 ENABLED true
set_interface_property hex_io5 EXPORT_OF ""
set_interface_property hex_io5 PORT_NAME_MAP ""
set_interface_property hex_io5 CMSIS_SVD_VARIABLES ""
set_interface_property hex_io5 SVD_ADDRESS_GROUP ""

add_interface_port hex_io5 hex5pins readdata Output 7
