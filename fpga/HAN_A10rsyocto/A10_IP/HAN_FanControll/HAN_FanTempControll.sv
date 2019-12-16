`define USE_TEMP_LED

module HAN_FanTempControll
(
        //////////// Avalon Bus Interface  //////////
        input logic clk_50Mhz,                  // 50MHZ
        input logic reset_n, read,              // Avalon Bus Interface
        input logic address,                    // Avalon Bus Interface
        output logic [31:0] readdata,           // Avalon Bus Interface

        //////////// Signal Ouptut pins  //////////
        output logic Temp_HI,	                // FPGA TEMPERATURE IS HIGH >37 degree C
	    output logic Temp_OK,                   // FPGA TEMPERATURE IS SAFE 32-37 degree C 
	    output logic Temp_LOW,                   // FPGA TEMPERATURE IS LOW < 32 degree C 
        
`ifdef USE_TEMP_LED
        output  logic Temp_LED,
`endif
        //////////// I/O Pins  //////////
        output   I2C_SCL_TempFan,      // I2C SCL with the connected Temp Sensor and FAN controller  
        inout 	 I2C_SDA_TempFan,          // I2C SDA with the connected Temp Sensor and FAN controller  
        input 	 FAN_ALERT_n               // FAN controller ISR output pin 

);

    //=======================================================
    //  temp values to avoid warnings
    //=======================================================

    logic       dataRedy,temp_hi,temp_ok,temp_low,temp_led, i2c_scl;
    logic       [31:0] outputReg [1:0];

    //=======================================================
    //  read Registers 
    //=======================================================

    logic [7:0] FPGA_TEMP_C;
    logic [7:0] BOARD_TEMP_C; 
    logic [15:0]FAN_RPM;

    logic [7:0] FAN_DAC;
    logic [7:0] ALARM_STATUS;
    

    ///////////////////// Avalon Register Set /////////////////////
    ///             ------------- write -------------            //
    ///                            none                          //
    ///             ------------- read  -------------            //   
    ///                        0 - SENSORS                       //
    ///                        1 - ALARM                         //
    ///////////////////////////////////////////////////////////////

    /////////////////////// SENSOR REGISTER ///////////////////////////
    ////  Bit  0-7  :  internel FPGA Temperature in degree C        ///
    ////  Bit  8-15 :  Board Temerature I2C Sensor in degree C      ///
    ////  Bit 16-31 :  Fan rotations per minute (RPM)               ///
    ///////////////////////////////////////////////////////////////////

    /////////////////////// ALARM REGISTER ////////////////////////////
    ///   Bit  0-7  :  Alarm Status Code                            ///
    ///   Bit 16-23 :  Fan controller DAC value                     ///
    ///                                                             ///
    ///////////////////////////////////////////////////////////////////


    //=======================================================
    //  temp value assignment  to avoid warnings
    //=======================================================
    assign Temp_HI = temp_hi;
    assign Temp_OK = temp_ok;
    assign Temp_LOW = temp_low;
    assign Temp_LED = temp_led;
    assign I2C_SCL_TempFan = i2c_scl;


    //=======================================================
    // data latching
    //=======================================================
    /// buffer data in case the data is reday 
    always_ff@(negedge reset_n or posedge dataRedy)  begin 
        if(!reset_n) begin 
            outputReg[0] = 32'd0;
            outputReg[1] = 32'd0;
        end
        else if (dataRedy) begin 
            outputReg[0] = {FPGA_TEMP_C,BOARD_TEMP_C,FAN_RPM};
            outputReg[1] = {ALARM_STATUS,FAN_DAC};
        end
    end 


    always_ff@(posedge clk_50Mhz)
    if(reset_n==1'b0)
        readdata <=32'b0;
    else begin 
        if(read) 
            readdata <= outputReg[address];
    end

    //=======================================================
    //  STATUS LED output  
    //=======================================================
    // Temperature 32-37 degree C -> LED ON (OK)
    // Tempeature  < 32 degree C  -> LED OFF (LOW)
    // Tempeature  > 32 degree C  -> LED flashing 10Hz (HIGH) 
`ifdef USE_TEMP_LED
    logic flashClk; 
    CLOCKMEM k10( .CLK(clk_50Mhz),.CLK_FREQ (5000000),.CK_1HZ(flashClk)  ) ; 

    always_ff@(posedge clk_50Mhz) begin 
        if(!reset_n)
            temp_led <= 1'b0;
        else if (flashClk) begin 
            if (temp_hi)
                temp_led <=!temp_led;
            else if((!reset_n) || (temp_ok))  
                temp_led <= 1'b0;
            else if (temp_low) 
                temp_led <= 1'b1; 
        end
    end 

`endif 

    //=======================================================
    //  Module 
    //=======================================================

    //-------- FAN_IP  ---
    TEMP_FAN_LOOP  lp(  
    .OSC_50       ( clk_50Mhz  ),        // 50MHZ CLOCK 
    .RESET_N      ( reset_n       ) ,    // RESET    
    .I2C_SCL      ( i2c_scl),            // I2C SCLK ( FAN & TEMPERATURE IC )
    .I2C_SDA      ( I2C_SDA_TempFan),    // I2C SDA  ( FAN & TEMPERATURE IC )
                                                
    .MANU_AUTO_SW ( 0),                  // 1:Test,0:Auto by Temperature 
    .FPGA_T_ISM   ( ) ,                  // Simulatet Temeture Values for test 
    .FAN_ALERT_n  ( FAN_ALERT_n ),       // FAN ALARM PIN 
    .ALARM_STATUS ( ALARM_STATUS) ,      // FAN ALARM STATUS 
    .FAN_DAC      ( FAN_DAC) ,           // FAN DAC 
    .FAN_RPM      ( FAN_RPM) ,           // FAN RPM 
    .BUSY         ( dataRedy   ),        // GO HI , DATA is SAFE (READY ) 
    .TEMP_HI      ( temp_hi) ,           // "1" FPGA TEMPERATURE IS HIGH >37 degree C
    .TEMP_OK      ( temp_ok) ,           // "1" FPGA TEMPERATURE IS SAFE 32~37 degree C 
    .TEMP_LO      ( temp_low) ,          // "1" FPGA TEMPERATURE IS LOW < 32 degree C 
    .FPGA_TEMP_C  ( FPGA_TEMP_C ) ,      // FPGA TEMPERATURE degree C 
    .BOARD_TEMP_C ( BOARD_TEMP_C) ,      // BOARD TEMPERATURE degree C 
    //--test--
    .BUSY_GO_HI   (  )
    );
        
endmodule