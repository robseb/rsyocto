
//
//            ########   ######     ##    ##  #######   ######  ########  #######                  
//            ##     ## ##    ##     ##  ##  ##     ## ##    ##    ##    ##     ##           
//            ##     ## ##            ####   ##     ## ##          ##    ##     ##        
//            ########   ######        ##    ##     ## ##          ##    ##     ##       
//            ##   ##         ##       ##    ##     ## ##          ##    ##     ##      
//            ##    ##  ##    ##       ##    ##     ## ##    ##    ##    ##     ##        
//            ##     ##  ######        ##     #######   ######     ##     #######         
//
//		    rsYocto reference FPGA project of the Terasic DE10 Nano Board
//    		 created by Robin Sebastian (https://github.com/robseb) 
//
//



//`define ENABLE_DDR4A
//`define ENABLE_DDR4B
`define ENABLE_DDR4H
//`define ENABLE_HDMI_TX
//`define ENABLE_HDMI_RX
//`define ENABLE_PCIE
//`define ENABLE_SATA
//`define ENABLE_SFP
//`define ENABLE_DP
`define ENABLE_HPS
//`define ENABLE_TYPEC
//`define ENABLE_TYPEC_USB3_XCVR

module a10s(

      ///////// CLOCK /////////
      input              CLKUSR_100,
      input              CLK_50_B2H,
      input              CLK_50_B3H,

      ///////// Buttons /////////
      input              CPU_RESET_n,
      input    [ 1: 0]   KEY, //KEY is Low-Active

      ///////// Swtiches /////////
      input    [ 1: 0]   SW,

      ///////// LED /////////
      output   [ 1: 0]   LED, //LED is Low-Active

      ///////// HEX0 /////////
      output   [ 6: 0]   HEX0_D,
      output             HEX0_DP,

      ///////// HEX1 /////////
      output   [ 6: 0]   HEX1_D,
      output             HEX1_DP,

`ifdef ENABLE_DDR4A
      ///////// DDR4A /////////
      input              DDR4A_REFCLK_p,
      output   [16: 0]   DDR4A_A,
      output   [ 1: 0]   DDR4A_BA,
      output   [ 1: 0]   DDR4A_BG,
      output             DDR4A_CK,
      output             DDR4A_CK_n,
      output             DDR4A_CKE,
      inout    [ 8: 0]   DDR4A_DQS,
      inout    [ 8: 0]   DDR4A_DQS_n,
      inout    [71: 0]   DDR4A_DQ,
      inout    [ 8: 0]   DDR4A_DBI_n,
      output             DDR4A_CS_n,
      output             DDR4A_RESET_n,
      output             DDR4A_ODT,
      output             DDR4A_PAR,
      input              DDR4A_ALERT_n,
      output             DDR4A_ACT_n,
      input              DDR4A_EVENT_n,
      output   [ 1: 0]   DDR4A_AC_R,
      output   [ 1: 0]   DDR4A_C,
      input              DDR4A_RZQ,
      inout              DDR4A_SCL,
      inout              DDR4A_SDA,
      
`endif /*ENABLE_DDR4A*/

`ifdef ENABLE_DDR4B
      ///////// DDR4B /////////
      input              DDR4B_REFCLK_p,
      output   [16: 0]   DDR4B_A,
      output   [ 1: 0]   DDR4B_BA,
      output   [ 1: 0]   DDR4B_BG,
      output             DDR4B_CK,
      output             DDR4B_CK_n,
      output             DDR4B_CKE,
      inout    [ 3: 0]   DDR4B_DQS,
      inout    [ 3: 0]   DDR4B_DQS_n,
      inout    [31: 0]   DDR4B_DQ,
      inout    [ 3: 0]   DDR4B_DBI_n,
      output             DDR4B_CS_n,
      output             DDR4B_RESET_n,
      output             DDR4B_ODT,
      output             DDR4B_PAR,
      input              DDR4B_ALERT_n,
      output             DDR4B_ACT_n,
      input              DDR4B_RZQ,
`endif /*ENABLE_DDR4B*/

`ifdef ENABLE_DDR4H
      ///////// DDR4H /////////
      input              DDR4H_REFCLK_p,
      output   [16: 0]   DDR4H_A,
      output   [ 1: 0]   DDR4H_BA,
      output   [ 0: 0]   DDR4H_BG,
      output             DDR4H_CK,
      output             DDR4H_CK_n,
      output             DDR4H_CKE,
      inout    [ 3: 0]   DDR4H_DQS,
      inout    [ 3: 0]   DDR4H_DQS_n,
      inout    [31: 0]   DDR4H_DQ,
      inout    [ 3: 0]   DDR4H_DBI_n,
      output             DDR4H_CS_n,
      output             DDR4H_RESET_n,
      output             DDR4H_ODT,
      output             DDR4H_PAR,
      input              DDR4H_ALERT_n,
      output             DDR4H_ACT_n,
      input              DDR4H_RZQ,
`endif /*ENABLE_DDR4H*/

`ifdef ENABLE_HDMI_TX
      ///////// HDMI /////////
      input              HDMI_REFCLK_p,
      output             HDMI_TX_CLK_p,
      output   [ 2: 0]   HDMI_TX_D_p,
      inout              HDMI_TX_SCL,
      inout              HDMI_TX_SDA,
      inout              HDMI_TX_HPD,
      inout              HDMI_TX_CEC,
`endif /*ENABLE_HDMI*/


`ifdef ENABLE_HDMI_RX
      ///////// HDMI /////////
      input              HDMI_RX_CLK_p,
      input    [ 2: 0]   HDMI_RX_D_p,
      inout              HDMI_RX_SCL,
      inout              HDMI_RX_SDA,
      inout              HDMI_RX_HPD,
      input              HDMI_RX_5V_n,
      inout              HDMI_RX_CEC,
      inout              DDCSCL_RX,
      inout              DDCSDA_RX,
`endif /*ENABLE_HDMI*/



      ///////// I2C /////////
      inout              I2C_INT,

      ///////// I2Cs /////////
      inout              FPGA_I2C_SCL,
      inout              FPGA_I2C_SDA,
      inout              REFCLK0_SCL,
      inout              REFCLK0_SDA,
      inout              REFCLK1_SCL,
      inout              REFCLK1_SDA,
      inout              CDCM6208_SCL,
      inout              CDCM6208_SDA,
      input              FAN_ALERT_n,
      input              PM_ALERT_n,

      ///////// FMC /////////
      inout              FMC_CLK2_BIDIR_p,
      inout              FMC_CLK2_BIDIR_n,
      inout              FMC_CLK3_BIDIR_p,
      inout              FMC_CLK3_BIDIR_n,
      input    [ 1: 0]   FMC_CLK_M2C_p,
      input    [ 1: 0]   FMC_CLK_M2C_n,
      inout    [23: 0]   FMC_HA_p,
      inout    [23: 0]   FMC_HA_n,
      inout    [21: 0]   FMC_HB_p,
      inout    [21: 0]   FMC_HB_n,
      inout    [33: 0]   FMC_LA_p,
      inout    [33: 0]   FMC_LA_n,
      input    [ 1: 0]   FMC_GBTCLK_M2C_p,
      input              FMC_REFCLK_p,
      output   [ 9: 0]   FMC_DP_C2M_p,
      input    [ 9: 0]   FMC_DP_M2C_p,
      inout    [ 1: 0]   FMC_GA,
      input              FMC_RZQ,
      inout              FMC_SCL,
      inout              FMC_SDA,



`ifdef ENABLE_PCIE
      ///////// PCIE /////////
      input              OB_PCIE_REFCLK_p,
      input              PCIE_REFCLK_p,
      output   [ 3: 0]   PCIE_TX_p,
      input    [ 3: 0]   PCIE_RX_p,
      input              PCIE_PERST_n,
      output             PCIE_WAKE_n,
`endif /*ENABLE_PCIE*/

`ifdef ENABLE_SATA
      ///////// SATA /////////
      input              SATA_HOST_REFCLK_p,
      output   [ 1: 0]   SATA_HOST_TX_p,
      input    [ 1: 0]   SATA_HOST_RX_p,
      input              SATA_DEVICE_REFCLK_p,
      output   [ 1: 0]   SATA_DEVICE_TX_p,
      input    [ 1: 0]   SATA_DEVICE_RX_p,
`endif /*ENABLE_SATA*/

`ifdef ENABLE_SFP
      ///////// SFP+ x4 /////////
      output             SFPA_TXDISABLE,
      input              SFPA_TXFAULT,
      output             SFPA_TX_p,
      input              SFPA_RX_p,
      input              SFPA_LOS,
      input              SFPA_MOD0_PRSNT_n,
      inout              SFPA_MOD1_SCL,
      inout              SFPA_MOD2_SDA,
      output   [ 1: 0]   SFPA_RATESEL,
      output             SFPB_TXDISABLE,
      input              SFPB_TXFAULT,
      output             SFPB_TX_p,
      input              SFPB_RX_p,
      input              SFPB_LOS,
      input              SFPB_MOD0_PRSNT_n,
      inout              SFPB_MOD1_SCL,
      inout              SFPB_MOD2_SDA,
      output   [ 1: 0]   SFPB_RATESEL,
      output             SFPC_TXDISABLE,
      input              SFPC_TXFAULT,
      output             SFPC_TX_p,
      input              SFPC_RX_p,
      input              SFPC_LOS,
      input              SFPC_MOD0_PRSNT_n,
      inout              SFPC_MOD1_SCL,
      inout              SFPC_MOD2_SDA,
      output   [ 1: 0]   SFPC_RATESEL,
      output             SFPD_TXDISABLE,
      input              SFPD_TXFAULT,
      output             SFPD_TX_p,
      input              SFPD_RX_p,
      input              SFPD_LOS,
      input              SFPD_MOD0_PRSNT_n,
      inout              SFPD_MOD1_SCL,
      inout              SFPD_MOD2_SDA,
      output   [ 1: 0]   SFPD_RATESEL,
      input              SFP_REFCLK_p,
`endif /*ENABLE_SFP*/


`ifdef ENABLE_DP
      ///////// DP /////////
      input              DP_REFCLK_p,
      output   [ 3: 0]   DP_TX_p,
      inout              DP_AUX_SEL,
      output             DP_AUX_p,
      inout              DP_DX_SEL,
      input    [ 3: 0]   DP_RX_p, // Reserved for future
`endif /*ENABLE_DP*/

      ///////// ETH /////////
      output             ETH_TX_p,
      input              ETH_RX_p,
      input              ETH_INT_n,
      output             ETH_MDC,
      inout              ETH_MDIO,
      output             ETH_RST_n,


`ifdef ENABLE_HPS
      ///////// HPS /////////
//      inout              HPS_CLK_25,
      inout    [5: 0]    HPS_DIO,
      inout    [3: 0]    HPS_GPIO,
		
      output             HPS_ENET_GTX_CLK,
      output             HPS_ENET_MDC,
      inout              HPS_ENET_MDIO,
      input              HPS_ENET_RX_CLK,
      input    [ 3: 0]   HPS_ENET_RX_DATA,
      input              HPS_ENET_RX_DV,
      output   [ 3: 0]   HPS_ENET_TX_DATA,
      output             HPS_ENET_TX_EN,
		
      inout              HPS_I2C0_SCLK,
      inout              HPS_I2C0_SDAT,
		
      inout              HPS_KEY,
      inout              HPS_LED,
		
//      inout              HPS_RESET_n,
      input              HPS_RXD,
      output             HPS_TXD,
		
      input              HPS_USB_CLKOUT,
      inout    [ 7: 0]   HPS_USB_DATA,
      input              HPS_USB_DIR,
      input              HPS_USB_NXT,
      output             HPS_USB_STP,
//      inout              HPS_WARM_RST_n, // note lowcase _n
`endif /*ENABLE_HPS*/

      ///////// MPU /////////
      inout              MPU_INT,

      ///////// SRC /////////
      inout              SRC_DP_HPD,

`ifdef ENABLE_TYPEC
      ///////// TYPEC /////////
      input              TYPEC_5V_EN,
      inout              TYPEC_PD_SLAVE_SCL,
      inout              TYPEC_PD_SLAVE_SDA,
      inout              TYPEC_PD_SCL, 
      inout              TYPEC_PD_SDA,
      
      ///////// USB20 Switch Control /////////
      inout              USB20_SW,
      inout              USB20_OE_n,

      ///////// DisplayPort CorssBar Setting /////////
      input   [ 2: 0]    USBDP_SW_CNF,      
`endif /*ENABLE_TYPEC*/

`ifdef ENABLE_TYPEC_USB3_XCVR
      ///////// USB3  /////////
      inout              USB_HOST_DEV_OE_n,
      inout              USB_HOST_DEV_SEL_n,
      inout              USB_SSFX3_PATH_OE_n,
      inout              USB_SSFX3_PATH_SEL_n,
      input              USB_REFCLK_p,
      output             USB_TX_p,
      input              USB_RX_p,
`endif /*ENABLE_USB*/


      ///////// USBFX3 /////////
      inout              USBFX3_RESET_n,
      inout              USBFX3_PCLK,
      inout              USBFX3_CTL0_SLCS_n,
      inout              USBFX3_UART_TX,
      inout              USBFX3_UART_RX,
      inout              USBFX3_CTL10,
      input              USBFX3_CTL11_A1,
      inout              USBFX3_CTL12_A0,
      inout              USBFX3_CTL15_INT_n,
      inout              USBFX3_CTL1_SLWR_n,
      inout              USBFX3_CTL2_SLOE_n,
      inout              USBFX3_CTL3_SLRD_n,
      inout              USBFX3_CTL4_FLAGA,
      inout              USBFX3_CTL5_FLAGB,
      inout              USBFX3_CTL6,
      inout              USBFX3_CTL7_PKTEND_n,
      inout              USBFX3_CTL8,
      inout              USBFX3_CTL9,
      inout    [31: 0]   USBFX3_DQ,
      inout              USBFX3_OTG_ID,


      ///////// SMA /////////
      input              SMA_CLKIN_p,
      output             SMA_CLKOUT_p

);


//=======================================================
//  REG/WIRE declarations
//=======================================================

// internal wires and registers declaration
  wire [1:0]  fpga_debounced_buttons;
  wire [27:0] stm_hw_events;
  wire        hps_fpga_reset;
  wire [2:0]  hps_reset_req;
  wire        hps_cold_reset;
  wire        hps_warm_reset;
  wire        hps_debug_reset;


//=======================================================
//  Structural coding
//=======================================================

// connection of internal logics
  assign stm_hw_events    = {{24{1'b0}}, SW, fpga_debounced_buttons};

// fan control
assign RESET_N  = fpga_debounced_buttons[0]; 
assign MANU_AUTO_SW =0;// SW[0] ; // 1:Test,0:Auto by Temperature 


 a10s_ghrd u0 (
	  .clk_100_clk                              (CLKUSR_100),    
		.clk_50_clk                              (CLK_50_B2H),               //                                 clk.clk
	  .reset_reset_n                            (CPU_RESET_n),              //                               reset.reset_n
	  .hps_fpga_reset_reset                     (hps_fpga_reset),           //                      hps_fpga_reset.reset
	  
	  // DDR4_H
	  .emif_a10_hps_pll_ref_clk_clock_sink_clk  (DDR4H_REFCLK_p),  			// emif_a10_hps_pll_ref_clk_clock_sink.clk
	  .emif_a10_hps_oct_conduit_end_oct_rzqin   (DDR4H_RZQ),     				//        emif_a10_hps_oct_conduit_end.oct_rzqin
	  .emif_a10_hps_mem_conduit_end_mem_ck      (DDR4H_CK),      				//        emif_a10_hps_mem_conduit_end.mem_ck
	  .emif_a10_hps_mem_conduit_end_mem_ck_n    (DDR4H_CK_n),    				//                                    .mem_ck_n
	  .emif_a10_hps_mem_conduit_end_mem_a       (DDR4H_A),       				//                                    .mem_a
	  .emif_a10_hps_mem_conduit_end_mem_act_n   (DDR4H_ACT_n),   				//                                    .mem_act_n
	  .emif_a10_hps_mem_conduit_end_mem_ba      (DDR4H_BA),      				//                                    .mem_ba
	  .emif_a10_hps_mem_conduit_end_mem_bg      (DDR4H_BG),      				//                                    .mem_bg
	  .emif_a10_hps_mem_conduit_end_mem_cke     (DDR4H_CKE),     				//                                    .mem_cke
	  .emif_a10_hps_mem_conduit_end_mem_cs_n    (DDR4H_CS_n),    				//                                    .mem_cs_n
	  .emif_a10_hps_mem_conduit_end_mem_odt     (DDR4H_ODT),     				//                                    .mem_odt
	  .emif_a10_hps_mem_conduit_end_mem_reset_n (DDR4H_RESET_n), 				//                                    .mem_reset_n
	  .emif_a10_hps_mem_conduit_end_mem_par     (DDR4H_PAR),     				//                                    .mem_par
	  .emif_a10_hps_mem_conduit_end_mem_alert_n (DDR4H_ALERT_n), 				//                                    .mem_alert_n
	  .emif_a10_hps_mem_conduit_end_mem_dqs     (DDR4H_DQS),     				//                                    .mem_dqs
	  .emif_a10_hps_mem_conduit_end_mem_dqs_n   (DDR4H_DQS_n),   				//                                    .mem_dqs_n
	  .emif_a10_hps_mem_conduit_end_mem_dq      (DDR4H_DQ),      				//                                    .mem_dq
	  .emif_a10_hps_mem_conduit_end_mem_dbi_n   (DDR4H_DBI_n),   				//                                    .mem_dbi_n
	  
	  // ETHERNET
	  .hps_io_hps_io_phery_emac0_TX_CLK         (HPS_ENET_GTX_CLK),         //                              hps_io.hps_io_phery_emac0_TX_CLK
	  .hps_io_hps_io_phery_emac0_TXD0           (HPS_ENET_TX_DATA[0]),      //                                    .hps_io_phery_emac0_TXD0
	  .hps_io_hps_io_phery_emac0_TXD1           (HPS_ENET_TX_DATA[1]),      //                                    .hps_io_phery_emac0_TXD1
	  .hps_io_hps_io_phery_emac0_TXD2           (HPS_ENET_TX_DATA[2]),      //                                    .hps_io_phery_emac0_TXD2
	  .hps_io_hps_io_phery_emac0_TXD3           (HPS_ENET_TX_DATA[3]),      //                                    .hps_io_phery_emac0_TXD3
	  .hps_io_hps_io_phery_emac0_RX_CTL         (HPS_ENET_RX_DV),         	//                                    .hps_io_phery_emac0_RX_CTL
	  .hps_io_hps_io_phery_emac0_TX_CTL         (HPS_ENET_TX_EN),         	//                                    .hps_io_phery_emac0_TX_CTL
	  .hps_io_hps_io_phery_emac0_RX_CLK         (HPS_ENET_RX_CLK),         	//                                    .hps_io_phery_emac0_RX_CLK
	  .hps_io_hps_io_phery_emac0_RXD0           (HPS_ENET_RX_DATA[0]),      //                                    .hps_io_phery_emac0_RXD0
	  .hps_io_hps_io_phery_emac0_RXD1           (HPS_ENET_RX_DATA[1]),      //                                    .hps_io_phery_emac0_RXD1
	  .hps_io_hps_io_phery_emac0_RXD2           (HPS_ENET_RX_DATA[2]),      //                                    .hps_io_phery_emac0_RXD2
	  .hps_io_hps_io_phery_emac0_RXD3           (HPS_ENET_RX_DATA[3]),      //                                    .hps_io_phery_emac0_RXD3
	  .hps_io_hps_io_phery_emac0_MDIO           (HPS_ENET_MDIO),           	//                                    .hps_io_phery_emac0_MDIO
	  .hps_io_hps_io_phery_emac0_MDC            (HPS_ENET_MDC),            	//                                    .hps_io_phery_emac0_MDC
	 
	  // SD CARD
	  .hps_io_hps_io_phery_sdmmc_CMD            (HPS_DIO[1]),             	//                                    .hps_io_phery_sdmmc_CMD
	  .hps_io_hps_io_phery_sdmmc_D0             (HPS_DIO[0]),             	//                                    .hps_io_phery_sdmmc_D0
	  .hps_io_hps_io_phery_sdmmc_D1             (HPS_DIO[3]),             	//                                    .hps_io_phery_sdmmc_D1
	  .hps_io_hps_io_phery_sdmmc_D2             (HPS_DIO[4]),             	//                                    .hps_io_phery_sdmmc_D2
	  .hps_io_hps_io_phery_sdmmc_D3             (HPS_DIO[5]),             	//                                    .hps_io_phery_sdmmc_D3
	  .hps_io_hps_io_phery_sdmmc_CCLK           (HPS_DIO[2]),             	//                                    .hps_io_phery_sdmmc_CCLK
	  
	  // USB
	  .hps_io_hps_io_phery_usb0_DATA0           (HPS_USB_DATA[0]),        	//                                    .hps_io_phery_usb0_DATA0
	  .hps_io_hps_io_phery_usb0_DATA1           (HPS_USB_DATA[1]),        	//                                    .hps_io_phery_usb0_DATA1
	  .hps_io_hps_io_phery_usb0_DATA2           (HPS_USB_DATA[2]),        	//                                    .hps_io_phery_usb0_DATA2
	  .hps_io_hps_io_phery_usb0_DATA3           (HPS_USB_DATA[3]),        	//                                    .hps_io_phery_usb0_DATA3
	  .hps_io_hps_io_phery_usb0_DATA4           (HPS_USB_DATA[4]),        	//                                    .hps_io_phery_usb0_DATA4
	  .hps_io_hps_io_phery_usb0_DATA5           (HPS_USB_DATA[5]),        	//                                    .hps_io_phery_usb0_DATA5
	  .hps_io_hps_io_phery_usb0_DATA6           (HPS_USB_DATA[6]),        	//                                    .hps_io_phery_usb0_DATA6
	  .hps_io_hps_io_phery_usb0_DATA7           (HPS_USB_DATA[7]),        	//                                    .hps_io_phery_usb0_DATA7
	  .hps_io_hps_io_phery_usb0_CLK             (HPS_USB_CLKOUT),         	//                                    .hps_io_phery_usb0_CLK
	  .hps_io_hps_io_phery_usb0_STP             (HPS_USB_STP),            	//                                    .hps_io_phery_usb0_STP
	  .hps_io_hps_io_phery_usb0_DIR             (HPS_USB_DIR),            	//                                    .hps_io_phery_usb0_DIR
	  .hps_io_hps_io_phery_usb0_NXT             (HPS_USB_NXT),            	//                                    .hps_io_phery_usb0_NXT
	  
	  // UART
	  .hps_io_hps_io_phery_uart1_RX             (HPS_RXD),                  //                                    .hps_io_phery_uart1_RX
	  .hps_io_hps_io_phery_uart1_TX             (HPS_TXD),                  //                                    .hps_io_phery_uart1_TX
	  
	  // I2C
	  .hps_io_hps_io_phery_i2c0_SDA             (HPS_I2C0_SDAT),            //                                    .hps_io_phery_i2c0_SDA
	  .hps_io_hps_io_phery_i2c0_SCL             (HPS_I2C0_SCLK),            //                                    .hps_io_phery_i2c0_SCL
	  
	  // GPIO
	  .hps_io_hps_io_gpio_gpio1_io1             (HPS_LED),                  //                                    .hps_io_gpio_gpio1_io1
	  .hps_io_hps_io_gpio_gpio1_io4             (HPS_KEY),                  //                                    .hps_io_gpio_gpio1_io4
	  
	  .hps_io_hps_io_gpio_gpio2_io8             (HPS_GPIO[0]),             //                                    .hps_io_gpio_gpio2_io8
	  .hps_io_hps_io_gpio_gpio2_io9             (HPS_GPIO[1]),             //                                    .hps_io_gpio_gpio2_io9
	  .hps_io_hps_io_gpio_gpio2_io10            (HPS_GPIO[2]),            //                                    .hps_io_gpio_gpio2_io10
	  .hps_io_hps_io_gpio_gpio2_io11            (HPS_GPIO[3]),            //                                    .hps_io_gpio_gpio2_io11
	  
	  .led_pio_external_connection_export       (LED),       //         led_pio_external_connection.export 
	  .button_pio_external_connection_export    (fpga_debounced_buttons),   //      button_pio_external_connection.export
	  .dipsw_pio_external_connection_export     (SW),     						//       dipsw_pio_external_connection.export
	  
	  .f2h_cold_reset_req_reset_n               (~hps_cold_reset),          //                  f2h_cold_reset_req.reset_n
	  .f2h_debug_reset_req_reset_n              (~hps_debug_reset),         //                 f2h_debug_reset_req.reset_n
	  .f2h_warm_reset_req_reset_n               (~hps_warm_reset),          //                  f2h_warm_reset_req.reset_n
	  .f2h_stm_hw_events_stm_hwevents           (stm_hw_events),            //                   f2h_stm_hw_events.stm_hwevents
	  .issp_hps_resets_source                   (hps_reset_req),             //                     issp_hps_resets.source
	  
	  ///////////////////////////////////////// Seven Sig Display ////////////////////////////////////////////	  
	  
	  .sevensig_io_hex_d0_readdata              (HEX0_D),              //                  sevensig_io_hex_d0.readdata
	  .sevensig_io_hex_d1_readdata              (HEX1_D),              //                  sevensig_io_hex_d1.readdata
	  .sevensig_io_hex_dp0_writeresponsevalid_n (HEX0_DP), //                 sevensig_io_hex_dp0.writeresponsevalid_n
	  .sevensig_io_hex_dp1_writeresponsevalid_n (HEX1_DP),  //  
 
		////////////////////////////////////////// FAN Controll ////////////////////////////////////////////////
		
	  .fancmd_fan_alert_beginbursttransfer      (FAN_ALERT_n),      //                    fancmd_fan_alert.beginbursttransfer
        .fancmd_io_i2c_scl_writeresponsevalid_n   (FPGA_I2C_SCL),   //                   fancmd_io_i2c_scl.writeresponsevalid_n
        .fancmd_io_i2c_sda_export                 (FPGA_I2C_SDA),                 //                   fancmd_io_i2c_sda.export
        .fancmd_status_led_writeresponsevalid_n   (),   //       
 
 );
 
 


// Debounce logic to clean out glitches within 1ms
debounce debounce_inst (
  .clk                                  (CLKUSR_100),
  .reset_n                              (~hps_fpga_reset),  
  .data_in                              (KEY),
  .data_out                             (fpga_debounced_buttons)
);
  defparam debounce_inst.WIDTH = 2;
  defparam debounce_inst.POLARITY = "LOW";
  defparam debounce_inst.TIMEOUT = 100000;              // at 100Mhz this is a debounce time of 1ms
  defparam debounce_inst.TIMEOUT_WIDTH = 32;            // ceil(log2(TIMEOUT))
 

altera_edge_detector pulse_cold_reset (
  .clk       (CLKUSR_100),
  .rst_n     (~hps_fpga_reset),
  .signal_in (hps_reset_req[0]),
  .pulse_out (hps_cold_reset)
);
  defparam pulse_cold_reset.PULSE_EXT = 6;
  defparam pulse_cold_reset.EDGE_TYPE = 1;
  defparam pulse_cold_reset.IGNORE_RST_WHILE_BUSY = 1;

altera_edge_detector pulse_warm_reset (
  .clk       (CLKUSR_100),
  .rst_n     (~hps_fpga_reset),
  .signal_in (hps_reset_req[1]),
  .pulse_out (hps_warm_reset)
);
  defparam pulse_warm_reset.PULSE_EXT = 2;
  defparam pulse_warm_reset.EDGE_TYPE = 1;
  defparam pulse_warm_reset.IGNORE_RST_WHILE_BUSY = 1;

altera_edge_detector pulse_debug_reset (
  .clk       (CLKUSR_100),
  .rst_n     (~hps_fpga_reset),
  .signal_in (hps_reset_req[2]),
  .pulse_out (hps_debug_reset)
);
  defparam pulse_debug_reset.PULSE_EXT = 32;
  defparam pulse_debug_reset.EDGE_TYPE = 1;
  defparam pulse_debug_reset.IGNORE_RST_WHILE_BUSY = 1;


endmodule
