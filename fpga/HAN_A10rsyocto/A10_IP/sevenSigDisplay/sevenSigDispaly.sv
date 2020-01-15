module sevenSigDisplay
(
        //////////// Avalon Bus Interface  //////////
        input logic              clk_50Mhz,              // 50MHZ
        input logic         reset_n, write,              // Avalon Bus Interface
        input logic                 address,            // Avalon Bus Interface
        input logic [31:0]         writedata,           // Avalon Bus Interface

        //////////// 7sig I/O pins  //////////
        output	logic	          	HEX0_DP,
        output	logic	[6:0]		HEX0_D,
        output	logic          	    HEX1_DP,
        output	logic	[6:0]		HEX1_D

);

    //=======================================================
    //  temp values to avoid warnings
    //=======================================================
    logic       [31:0] inputReg;

    //=======================================================
    //  read Registers 
    //=======================================================
    localparam TRAGET_FRQ				= 12;     //[Hz]
    localparam ClOCK_CYCELS 		= 50000000; // Speed / OSCI_SPEED

    ///////////////////// Avalon Register Set /////////////////////
    ///             ------------- write -------------            //
    ///               0: Seven Sigment Output Byte               //
    ///             ------------- read  -------------            //  
    ///                          none                            // 
    ///////////////////////////////////////////////////////////////

    ////////////////////// SEVENSIG REGISTER /////////////////////////
    ////  Bit  0-3  :  lower Seven Sigment Display  (HEX0)         ///
    ////  Bit  4-7  :  uper Seven Sigment Display   (HEX1)         ///
    ////  Bit   8   :  HEX0 Dot point                              ///
    ////  Bit   9   :  HEX0 Dot point                              ///
    //////////////////////////////////////////////////////////////////
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

    logic refClk; 
    assign refClk = (time_base_counter == pres) ? 1'b1 : 1'b0; 

    //=======================================================
    //  Seven Sigment Output  
    //=======================================================


    always_ff@(posedge clk_50Mhz) begin 
    	if(reset_n==1'b0) begin 
			HEX0_D <=3'b1000000; //  0 
            HEX1_D <=3'b1000000; //  0 
            HEX0_DP<=0;
            HEX1_DP<=0;
        end
		else if(refClk) begin 
            // lower case seven Sigment Display
			case(inputReg[3:0])	
				4'h0 : HEX0_D <= 7'b1000000;		// 0
			    4'h1 : HEX0_D <= 7'b1111001;		// 1
				4'h2 : HEX0_D <= 7'b0100100;		// 2
				4'h3 : HEX0_D <= 7'b0110000;		// 3
			    4'h4 : HEX0_D <= 7'b0011001;		// 4
				4'h5 : HEX0_D <= 7'b0010010;		// 5
				4'h6 : HEX0_D <= 7'b0000010;		// 6
				4'h7 : HEX0_D <= 7'b1111000;		// 7
				4'h8 : HEX0_D <= 7'b0000000;		// 8
				4'h9 : HEX0_D <= 7'b0011000;		// 9
				4'hA : HEX0_D <= 7'b0001000;		// A
				4'hB : HEX0_D <= 7'b0000011;		// B
				4'hC : HEX0_D <= 7'b1000110;		// C
				4'hD : HEX0_D <= 7'b0100001;		// D
				4'hE : HEX0_D <= 7'b0000110;		// E
				4'hF : HEX0_D <= 7'b0001110;		// F
				default : HEX0_D <= 7'b1000000;		
		    endcase
            // uper case seven Sigment Display 
            case(inputReg[7:4])	
                4'h0 : HEX1_D <= 7'b1000000;		// 0
                4'h1 : HEX1_D <= 7'b1111001;		// 1
                4'h2 : HEX1_D <= 7'b0100100;		// 2
                4'h3 : HEX1_D <= 7'b0110000;		// 3
                4'h4 : HEX1_D <= 7'b0011001;		// 4
                4'h5 : HEX1_D <= 7'b0010010;		// 5
                4'h6 : HEX1_D <= 7'b0000010;		// 6
                4'h7 : HEX1_D <= 7'b1111000;		// 7
                4'h8 : HEX1_D <= 7'b0000000;		// 8
                4'h9 : HEX1_D <= 7'b0011000;		// 9
                4'hA : HEX1_D <= 7'b0001000;		// A
                4'hB : HEX1_D <= 7'b0000011;		// B
                4'hC : HEX1_D <= 7'b1000110;		// C
                4'hD : HEX1_D <= 7'b0100001;		// D
                4'hE : HEX1_D <= 7'b0000110;		// E
                4'hF : HEX1_D <= 7'b0001110;		// F
                default : HEX1_D <= 7'b1000000;		
            endcase
            // write Dot points 
            HEX0_DP <= ~inputReg[8];
            HEX1_DP <= ~inputReg[9];
        end
    end 
endmodule