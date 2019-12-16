# TCL File Generated by Component Editor 18.1
# Tue Dec 03 00:44:10 CET 2019
# DO NOT MODIFY


# 
# DE10STD7sig "DE10STD7sig" v1.0
# Robin Sebastian  2019.12.03.00:44:10
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
add_fileset_file D10STDsevenSigDisplay.sv SYSTEM_VERILOG PATH DE10STD_IP/sevenSigDisplay/D10STDsevenSigDisplay.sv TOP_LEVEL_FILE
add_fileset_file sevenSigSegmentDriver.sv SYSTEM_VERILOG PATH DE10STD_IP/sevenSigDisplay/sevenSigSegmentDriver.sv


# 
# parameters
# 


# 
# display items
# 


# 
# connection point reset
# 
add_interface reset reset end
set_interface_property reset associatedClock clock50Mhz
set_interface_property reset synchronousEdges DEASSERT
set_interface_property reset ENABLED true
set_interface_property reset EXPORT_OF ""
set_interface_property reset PORT_NAME_MAP ""
set_interface_property reset CMSIS_SVD_VARIABLES ""
set_interface_property reset SVD_ADDRESS_GROUP ""

add_interface_port reset reset_n reset_n Input 1


# 
# connection point avalon_slave
# 
add_interface avalon_slave avalon end
set_interface_property avalon_slave addressUnits WORDS
set_interface_property avalon_slave associatedClock clock50Mhz
set_interface_property avalon_slave associatedReset reset
set_interface_property avalon_slave bitsPerSymbol 32
set_interface_property avalon_slave burstOnBurstBoundariesOnly false
set_interface_property avalon_slave burstcountUnits WORDS
set_interface_property avalon_slave explicitAddressSpan 0
set_interface_property avalon_slave holdTime 0
set_interface_property avalon_slave linewrapBursts false
set_interface_property avalon_slave maximumPendingReadTransactions 0
set_interface_property avalon_slave maximumPendingWriteTransactions 0
set_interface_property avalon_slave readLatency 0
set_interface_property avalon_slave readWaitTime 1
set_interface_property avalon_slave setupTime 0
set_interface_property avalon_slave timingUnits Cycles
set_interface_property avalon_slave writeWaitTime 0
set_interface_property avalon_slave ENABLED true
set_interface_property avalon_slave EXPORT_OF ""
set_interface_property avalon_slave PORT_NAME_MAP ""
set_interface_property avalon_slave CMSIS_SVD_VARIABLES ""
set_interface_property avalon_slave SVD_ADDRESS_GROUP ""

add_interface_port avalon_slave write write Input 1
add_interface_port avalon_slave address address Input 1
add_interface_port avalon_slave writedata writedata Input 32
set_interface_assignment avalon_slave embeddedsw.configuration.isFlash 0
set_interface_assignment avalon_slave embeddedsw.configuration.isMemoryDevice 0
set_interface_assignment avalon_slave embeddedsw.configuration.isNonVolatileStorage 0
set_interface_assignment avalon_slave embeddedsw.configuration.isPrintableDevice 0


# 
# connection point clock50Mhz
# 
add_interface clock50Mhz clock end
set_interface_property clock50Mhz clockRate 0
set_interface_property clock50Mhz ENABLED true
set_interface_property clock50Mhz EXPORT_OF ""
set_interface_property clock50Mhz PORT_NAME_MAP ""
set_interface_property clock50Mhz CMSIS_SVD_VARIABLES ""
set_interface_property clock50Mhz SVD_ADDRESS_GROUP ""

add_interface_port clock50Mhz clk_50Mhz clk Input 1


# 
# connection point HEX_IO0
# 
add_interface HEX_IO0 conduit end
set_interface_property HEX_IO0 associatedClock clock50Mhz
set_interface_property HEX_IO0 associatedReset reset
set_interface_property HEX_IO0 ENABLED true
set_interface_property HEX_IO0 EXPORT_OF ""
set_interface_property HEX_IO0 PORT_NAME_MAP ""
set_interface_property HEX_IO0 CMSIS_SVD_VARIABLES ""
set_interface_property HEX_IO0 SVD_ADDRESS_GROUP ""

add_interface_port HEX_IO0 hex0pins readdata Output 7


# 
# connection point HEX_IO1
# 
add_interface HEX_IO1 conduit end
set_interface_property HEX_IO1 associatedClock clock50Mhz
set_interface_property HEX_IO1 associatedReset reset
set_interface_property HEX_IO1 ENABLED true
set_interface_property HEX_IO1 EXPORT_OF ""
set_interface_property HEX_IO1 PORT_NAME_MAP ""
set_interface_property HEX_IO1 CMSIS_SVD_VARIABLES ""
set_interface_property HEX_IO1 SVD_ADDRESS_GROUP ""

add_interface_port HEX_IO1 hex1pins readdata Output 7


# 
# connection point HEX_IO2
# 
add_interface HEX_IO2 conduit end
set_interface_property HEX_IO2 associatedClock clock50Mhz
set_interface_property HEX_IO2 associatedReset reset
set_interface_property HEX_IO2 ENABLED true
set_interface_property HEX_IO2 EXPORT_OF ""
set_interface_property HEX_IO2 PORT_NAME_MAP ""
set_interface_property HEX_IO2 CMSIS_SVD_VARIABLES ""
set_interface_property HEX_IO2 SVD_ADDRESS_GROUP ""

add_interface_port HEX_IO2 hex2pins readdata Output 7


# 
# connection point HEX_IO3
# 
add_interface HEX_IO3 conduit end
set_interface_property HEX_IO3 associatedClock clock50Mhz
set_interface_property HEX_IO3 associatedReset reset
set_interface_property HEX_IO3 ENABLED true
set_interface_property HEX_IO3 EXPORT_OF ""
set_interface_property HEX_IO3 PORT_NAME_MAP ""
set_interface_property HEX_IO3 CMSIS_SVD_VARIABLES ""
set_interface_property HEX_IO3 SVD_ADDRESS_GROUP ""

add_interface_port HEX_IO3 hex3pins readdata Output 7


# 
# connection point HEX_IO4
# 
add_interface HEX_IO4 conduit end
set_interface_property HEX_IO4 associatedClock clock50Mhz
set_interface_property HEX_IO4 associatedReset reset
set_interface_property HEX_IO4 ENABLED true
set_interface_property HEX_IO4 EXPORT_OF ""
set_interface_property HEX_IO4 PORT_NAME_MAP ""
set_interface_property HEX_IO4 CMSIS_SVD_VARIABLES ""
set_interface_property HEX_IO4 SVD_ADDRESS_GROUP ""

add_interface_port HEX_IO4 hex4pins readdata Output 7


# 
# connection point HEX_IO5
# 
add_interface HEX_IO5 conduit end
set_interface_property HEX_IO5 associatedClock clock50Mhz
set_interface_property HEX_IO5 associatedReset reset
set_interface_property HEX_IO5 ENABLED true
set_interface_property HEX_IO5 EXPORT_OF ""
set_interface_property HEX_IO5 PORT_NAME_MAP ""
set_interface_property HEX_IO5 CMSIS_SVD_VARIABLES ""
set_interface_property HEX_IO5 SVD_ADDRESS_GROUP ""

add_interface_port HEX_IO5 hex5pins readdata Output 7

