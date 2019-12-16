/////////////////////////////////////////////////////////////////////
// 			Robin Sebastian (robin@rockdocs.de) 				   //	
// AVALON BUS Seven Sigment 24-Bit seven Sigment Dsipaly Interface //
//			for Terasic DE10-STANDARD Board 					   //												
//						NOV-2019								   //																					
/////////////////////////////////////////////////////////////////////

module sevenSigDisplay
(
        //////////// Avalon Bus Interface  //////////
        input logic         clk_50Mhz,              // 50MHZ
        input logic         reset_n, write,              // Avalon Bus Interface
        input logic         address,            // Avalon Bus Interface
        input logic [31:0]  writedata,           // Avalon Bus Interface

        //////////// 7sig I/O pins  //////////
		output logic [6:0] hex0pins,
		output logic [6:0] hex1pins,
		output logic [6:0] hex2pins,
		output logic [6:0] hex3pins,
		output logic [6:0] hex4pins,
		output logic [6:0] hex5pins

);
//=======================================================
//  Clock configuration 
//=======================================================
localparam TRAGET_FRQ				= 12;     //[Hz]
localparam ClOCK_CYCELS 		= 50000000; // Speed / OSCI_SPEED

//=======================================================
//  temp values to avoid warnings
//=======================================================
logic       [31:0] inputReg;

//=======================================================
//  read Registers 
//=======================================================


///////////////////// Avalon Register Set /////////////////////
///             ------------- write -------------            //
///               0: Seven Sigment Output Byte               //
///             ------------- read  -------------            //  
///                          none                            // 
///////////////////////////////////////////////////////////////

////////////////////// SEVENSIG REGISTER /////////////////////////
////  Bit  0-3    :  Sigment Display 0  (HEX0)         		   ///
////  Bit  4-7    :  Sigment Display 1  (HEX1)         		   ///
////  Bit  8-11   :  Sigment Display 2  (HEX2)         		   ///
////  Bit  12-15  :  Sigment Display 3  (HEX3)         		   ///
////  Bit  16-19  :  Sigment Display 4  (HEX4)         		   ///
////  Bit  20-23  :  Sigment Display 5  (HEX5)         		   ///
//////////////////////////////////////////////////////////////////


//=======================================================
// Load Display Value to buffer  
//=======================================================

logic update; 
assign update = (write && !address);

always_ff@(posedge clk_50Mhz)
	if(reset_n==1'b0)
		inputReg <=32'b0;
	else begin 
		if(update) 
			inputReg <= writedata;
	end


//=======================================================
// Generate refrech clock   
//=======================================================

localparam pres  = (ClOCK_CYCELS/TRAGET_FRQ);

logic [31:0] time_base_counter = 32'd0;
always_ff@(posedge clk_50Mhz)
	if(reset_n==1'b0)
		time_base_counter <=32'd0;
	else
	begin
		if(time_base_counter<pres)
			time_base_counter <=time_base_counter+1'b1; 
		else 
			time_base_counter =0;
	end

logic CountClk; 
assign CountClk = (time_base_counter == pres) ? 1'b1 : 1'b0; 

//=======================================================
//  Seven Sigment Output  
//=======================================================


sevenSigSegmentDriver hex0 (
								.clk_ref(CountClk),
								.reset_n(reset_n),
								.value2show(inputReg[3:0]),
								.sig_pins(hex0pins)
								);
								
sevenSigSegmentDriver hex1 (
								.clk_ref(CountClk),
								.reset_n(reset_n),
								.value2show(inputReg[7:4]),
								.sig_pins(hex1pins)
								);
									
sevenSigSegmentDriver hex2 (
									.clk_ref(CountClk),
									.reset_n(reset_n),
									.value2show(inputReg[11:8]),
									.sig_pins(hex2pins)
);

sevenSigSegmentDriver hex3 (
									.clk_ref(CountClk),
									.reset_n(reset_n),
									.value2show(inputReg[15:12]),
									.sig_pins(hex3pins)
);

sevenSigSegmentDriver hex4 (
									.clk_ref(CountClk),
									.reset_n(reset_n),
									.value2show(inputReg[19:16]),
									.sig_pins(hex4pins)
);
sevenSigSegmentDriver hex5 (
									.clk_ref(CountClk),
									.reset_n(reset_n),
									.value2show(inputReg[23:20]),
									.sig_pins(hex5pins)
);

endmodule