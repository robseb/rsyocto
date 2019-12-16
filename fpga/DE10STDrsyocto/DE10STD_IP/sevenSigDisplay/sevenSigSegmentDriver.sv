/////////////////////////////////////////////////////////////////////
// 			Robin Sebastian (robin@rockdocs.de) 				   //	
// 			4-Bit Seven Sigment HEX Interface  					   //											
//						NOV-2019								   //																					
/////////////////////////////////////////////////////////////////////

module sevenSigSegmentDriver(
	input logic clk_ref,    // Reference Clock 
	input logic reset_n, 
	input logic   [3:0] value2show,
	output logic  [6:0] sig_pins
	);
	initial 
		sig_pins <= 7'hC0; 
		
	

	always_ff@(posedge clk_ref)
	begin
		if(reset_n==1'b0)
			sig_pins <=3'hC0; //  0 
		else 
			case(value2show)			// values are invertet!
				4'h0 : sig_pins <= 7'hC0;		// 0
				4'h1 : sig_pins <= 7'hF9;		// 1
				4'h2 : sig_pins <= 7'hA4;		// 2
				4'h3 : sig_pins <= 7'hB0;		// 3
				4'h4 : sig_pins <= 7'h99;		// 4
				4'h5 : sig_pins <= 7'h92;		// 5
				4'h6 : sig_pins <= 7'h82;		// 6
				4'h7 : sig_pins <= 7'hF8;		// 7
				4'h8 : sig_pins <= 7'h80;		// 8
				4'h9 : sig_pins <= 7'h98;		// 9
				4'hA : sig_pins <= 7'h88;		// A
				4'hB : sig_pins <= 7'h83;		// B
				4'hC : sig_pins <= 7'hc6;		// C
				4'hD : sig_pins <= 7'hA1;		// D
				4'hE : sig_pins <= 7'h86;		// E
				4'hF : sig_pins <= 7'h8E;		// F
				default : sig_pins <= 7'h0;		
		endcase
	end
	
	endmodule
	