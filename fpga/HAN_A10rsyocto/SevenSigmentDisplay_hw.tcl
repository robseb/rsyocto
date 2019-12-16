# TCL File Generated by Component Editor 18.1
# Mon Dec 16 13:30:08 CET 2019
# DO NOT MODIFY


# 
# SevenSigmentDisplay "SevenSigmentDisplay" v1.0
# Robin Sebastian 2019.12.16.13:30:08
# 
# 

# 
# request TCL package from ACDS 16.1
# 
package require -exact qsys 16.1


# 
# module SevenSigmentDisplay
# 
set_module_property DESCRIPTION ""
set_module_property NAME SevenSigmentDisplay
set_module_property VERSION 1.0
set_module_property INTERNAL false
set_module_property OPAQUE_ADDRESS_MAP true
set_module_property GROUP "Basic Functions/I/O"
set_module_property AUTHOR "Robin Sebastian"
set_module_property DISPLAY_NAME SevenSigmentDisplay
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
add_fileset_file sevenSigDispaly.sv SYSTEM_VERILOG PATH A10_IP/sevenSigDisplay/sevenSigDispaly.sv TOP_LEVEL_FILE


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
set_interface_property avalon_slave_0 associatedClock clock50
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
set_interface_property reset associatedClock clock50
set_interface_property reset synchronousEdges DEASSERT
set_interface_property reset ENABLED true
set_interface_property reset EXPORT_OF ""
set_interface_property reset PORT_NAME_MAP ""
set_interface_property reset CMSIS_SVD_VARIABLES ""
set_interface_property reset SVD_ADDRESS_GROUP ""

add_interface_port reset reset_n reset_n Input 1


# 
# connection point clock50
# 
add_interface clock50 clock end
set_interface_property clock50 clockRate 0
set_interface_property clock50 ENABLED true
set_interface_property clock50 EXPORT_OF ""
set_interface_property clock50 PORT_NAME_MAP ""
set_interface_property clock50 CMSIS_SVD_VARIABLES ""
set_interface_property clock50 SVD_ADDRESS_GROUP ""

add_interface_port clock50 clk_50Mhz clk Input 1


# 
# connection point IO_HEX_D0
# 
add_interface IO_HEX_D0 conduit end
set_interface_property IO_HEX_D0 associatedClock clock50
set_interface_property IO_HEX_D0 associatedReset reset
set_interface_property IO_HEX_D0 ENABLED true
set_interface_property IO_HEX_D0 EXPORT_OF ""
set_interface_property IO_HEX_D0 PORT_NAME_MAP ""
set_interface_property IO_HEX_D0 CMSIS_SVD_VARIABLES ""
set_interface_property IO_HEX_D0 SVD_ADDRESS_GROUP ""

add_interface_port IO_HEX_D0 HEX0_D readdata Output 7


# 
# connection point IO_HEX_D1
# 
add_interface IO_HEX_D1 conduit end
set_interface_property IO_HEX_D1 associatedClock clock50
set_interface_property IO_HEX_D1 associatedReset reset
set_interface_property IO_HEX_D1 ENABLED true
set_interface_property IO_HEX_D1 EXPORT_OF ""
set_interface_property IO_HEX_D1 PORT_NAME_MAP ""
set_interface_property IO_HEX_D1 CMSIS_SVD_VARIABLES ""
set_interface_property IO_HEX_D1 SVD_ADDRESS_GROUP ""

add_interface_port IO_HEX_D1 HEX1_D readdata Output 7


# 
# connection point IO_HEX_DP0
# 
add_interface IO_HEX_DP0 conduit end
set_interface_property IO_HEX_DP0 associatedClock clock50
set_interface_property IO_HEX_DP0 associatedReset reset
set_interface_property IO_HEX_DP0 ENABLED true
set_interface_property IO_HEX_DP0 EXPORT_OF ""
set_interface_property IO_HEX_DP0 PORT_NAME_MAP ""
set_interface_property IO_HEX_DP0 CMSIS_SVD_VARIABLES ""
set_interface_property IO_HEX_DP0 SVD_ADDRESS_GROUP ""

add_interface_port IO_HEX_DP0 HEX0_DP writeresponsevalid_n Output 1


# 
# connection point IO_HEX_DP1
# 
add_interface IO_HEX_DP1 conduit end
set_interface_property IO_HEX_DP1 associatedClock clock50
set_interface_property IO_HEX_DP1 associatedReset reset
set_interface_property IO_HEX_DP1 ENABLED true
set_interface_property IO_HEX_DP1 EXPORT_OF ""
set_interface_property IO_HEX_DP1 PORT_NAME_MAP ""
set_interface_property IO_HEX_DP1 CMSIS_SVD_VARIABLES ""
set_interface_property IO_HEX_DP1 SVD_ADDRESS_GROUP ""

add_interface_port IO_HEX_DP1 HEX1_DP writeresponsevalid_n Output 1

