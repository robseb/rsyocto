
module base_hps (
	clk_clk,
	hps_0_ddr_mem_a,
	hps_0_ddr_mem_ba,
	hps_0_ddr_mem_ck,
	hps_0_ddr_mem_ck_n,
	hps_0_ddr_mem_cke,
	hps_0_ddr_mem_cs_n,
	hps_0_ddr_mem_ras_n,
	hps_0_ddr_mem_cas_n,
	hps_0_ddr_mem_we_n,
	hps_0_ddr_mem_reset_n,
	hps_0_ddr_mem_dq,
	hps_0_ddr_mem_dqs,
	hps_0_ddr_mem_dqs_n,
	hps_0_ddr_mem_odt,
	hps_0_ddr_mem_dm,
	hps_0_ddr_oct_rzqin,
	hps_0_io_hps_io_emac1_inst_TX_CLK,
	hps_0_io_hps_io_emac1_inst_TXD0,
	hps_0_io_hps_io_emac1_inst_TXD1,
	hps_0_io_hps_io_emac1_inst_TXD2,
	hps_0_io_hps_io_emac1_inst_TXD3,
	hps_0_io_hps_io_emac1_inst_RXD0,
	hps_0_io_hps_io_emac1_inst_MDIO,
	hps_0_io_hps_io_emac1_inst_MDC,
	hps_0_io_hps_io_emac1_inst_RX_CTL,
	hps_0_io_hps_io_emac1_inst_TX_CTL,
	hps_0_io_hps_io_emac1_inst_RX_CLK,
	hps_0_io_hps_io_emac1_inst_RXD1,
	hps_0_io_hps_io_emac1_inst_RXD2,
	hps_0_io_hps_io_emac1_inst_RXD3,
	hps_0_io_hps_io_sdio_inst_CMD,
	hps_0_io_hps_io_sdio_inst_D0,
	hps_0_io_hps_io_sdio_inst_D1,
	hps_0_io_hps_io_sdio_inst_CLK,
	hps_0_io_hps_io_sdio_inst_D2,
	hps_0_io_hps_io_sdio_inst_D3,
	hps_0_io_hps_io_usb1_inst_D0,
	hps_0_io_hps_io_usb1_inst_D1,
	hps_0_io_hps_io_usb1_inst_D2,
	hps_0_io_hps_io_usb1_inst_D3,
	hps_0_io_hps_io_usb1_inst_D4,
	hps_0_io_hps_io_usb1_inst_D5,
	hps_0_io_hps_io_usb1_inst_D6,
	hps_0_io_hps_io_usb1_inst_D7,
	hps_0_io_hps_io_usb1_inst_CLK,
	hps_0_io_hps_io_usb1_inst_STP,
	hps_0_io_hps_io_usb1_inst_DIR,
	hps_0_io_hps_io_usb1_inst_NXT,
	hps_0_io_hps_io_uart0_inst_RX,
	hps_0_io_hps_io_uart0_inst_TX,
	hps_0_io_hps_io_i2c0_inst_SDA,
	hps_0_io_hps_io_i2c0_inst_SCL,
	hps_0_io_hps_io_gpio_inst_GPIO53,
	hps_0_io_hps_io_gpio_inst_GPIO54,
	hps_0_spim0_txd,
	hps_0_spim0_rxd,
	hps_0_spim0_ss_in_n,
	hps_0_spim0_ssi_oe_n,
	hps_0_spim0_ss_0_n,
	hps_0_spim0_ss_1_n,
	hps_0_spim0_ss_2_n,
	hps_0_spim0_ss_3_n,
	hps_0_spim0_sclk_out_clk,
	hps_0_spim1_txd,
	hps_0_spim1_rxd,
	hps_0_spim1_ss_in_n,
	hps_0_spim1_ssi_oe_n,
	hps_0_spim1_ss_0_n,
	hps_0_spim1_ss_1_n,
	hps_0_spim1_ss_2_n,
	hps_0_spim1_ss_3_n,
	hps_0_spim1_sclk_out_clk,
	hps_0_i2c1_scl_in_clk,
	hps_0_uart1_cts,
	hps_0_uart1_dsr,
	hps_0_uart1_dcd,
	hps_0_uart1_ri,
	hps_0_uart1_dtr,
	hps_0_uart1_rts,
	hps_0_uart1_out1_n,
	hps_0_uart1_out2_n,
	hps_0_uart1_rxd,
	hps_0_uart1_txd,
	hps_0_i2c1_out_data,
	hps_0_i2c1_sda,
	hps_0_i2c1_clk_clk,
	hps_0_i2c3_scl_in_clk,
	hps_0_i2c3_clk_clk,
	hps_0_can0_rxd,
	hps_0_can0_txd,
	hps_0_i2c3_out_data,
	hps_0_i2c3_sda,
	led_pio_external_connection_export,
	pb_pio_external_connection_export,
	sw_pio_external_connection_export,
	hps_0_h2f_gp_gp_in,
	hps_0_h2f_gp_gp_out);	

	input		clk_clk;
	output	[14:0]	hps_0_ddr_mem_a;
	output	[2:0]	hps_0_ddr_mem_ba;
	output		hps_0_ddr_mem_ck;
	output		hps_0_ddr_mem_ck_n;
	output		hps_0_ddr_mem_cke;
	output		hps_0_ddr_mem_cs_n;
	output		hps_0_ddr_mem_ras_n;
	output		hps_0_ddr_mem_cas_n;
	output		hps_0_ddr_mem_we_n;
	output		hps_0_ddr_mem_reset_n;
	inout	[31:0]	hps_0_ddr_mem_dq;
	inout	[3:0]	hps_0_ddr_mem_dqs;
	inout	[3:0]	hps_0_ddr_mem_dqs_n;
	output		hps_0_ddr_mem_odt;
	output	[3:0]	hps_0_ddr_mem_dm;
	input		hps_0_ddr_oct_rzqin;
	output		hps_0_io_hps_io_emac1_inst_TX_CLK;
	output		hps_0_io_hps_io_emac1_inst_TXD0;
	output		hps_0_io_hps_io_emac1_inst_TXD1;
	output		hps_0_io_hps_io_emac1_inst_TXD2;
	output		hps_0_io_hps_io_emac1_inst_TXD3;
	input		hps_0_io_hps_io_emac1_inst_RXD0;
	inout		hps_0_io_hps_io_emac1_inst_MDIO;
	output		hps_0_io_hps_io_emac1_inst_MDC;
	input		hps_0_io_hps_io_emac1_inst_RX_CTL;
	output		hps_0_io_hps_io_emac1_inst_TX_CTL;
	input		hps_0_io_hps_io_emac1_inst_RX_CLK;
	input		hps_0_io_hps_io_emac1_inst_RXD1;
	input		hps_0_io_hps_io_emac1_inst_RXD2;
	input		hps_0_io_hps_io_emac1_inst_RXD3;
	inout		hps_0_io_hps_io_sdio_inst_CMD;
	inout		hps_0_io_hps_io_sdio_inst_D0;
	inout		hps_0_io_hps_io_sdio_inst_D1;
	output		hps_0_io_hps_io_sdio_inst_CLK;
	inout		hps_0_io_hps_io_sdio_inst_D2;
	inout		hps_0_io_hps_io_sdio_inst_D3;
	inout		hps_0_io_hps_io_usb1_inst_D0;
	inout		hps_0_io_hps_io_usb1_inst_D1;
	inout		hps_0_io_hps_io_usb1_inst_D2;
	inout		hps_0_io_hps_io_usb1_inst_D3;
	inout		hps_0_io_hps_io_usb1_inst_D4;
	inout		hps_0_io_hps_io_usb1_inst_D5;
	inout		hps_0_io_hps_io_usb1_inst_D6;
	inout		hps_0_io_hps_io_usb1_inst_D7;
	input		hps_0_io_hps_io_usb1_inst_CLK;
	output		hps_0_io_hps_io_usb1_inst_STP;
	input		hps_0_io_hps_io_usb1_inst_DIR;
	input		hps_0_io_hps_io_usb1_inst_NXT;
	input		hps_0_io_hps_io_uart0_inst_RX;
	output		hps_0_io_hps_io_uart0_inst_TX;
	inout		hps_0_io_hps_io_i2c0_inst_SDA;
	inout		hps_0_io_hps_io_i2c0_inst_SCL;
	inout		hps_0_io_hps_io_gpio_inst_GPIO53;
	inout		hps_0_io_hps_io_gpio_inst_GPIO54;
	output		hps_0_spim0_txd;
	input		hps_0_spim0_rxd;
	input		hps_0_spim0_ss_in_n;
	output		hps_0_spim0_ssi_oe_n;
	output		hps_0_spim0_ss_0_n;
	output		hps_0_spim0_ss_1_n;
	output		hps_0_spim0_ss_2_n;
	output		hps_0_spim0_ss_3_n;
	output		hps_0_spim0_sclk_out_clk;
	output		hps_0_spim1_txd;
	input		hps_0_spim1_rxd;
	input		hps_0_spim1_ss_in_n;
	output		hps_0_spim1_ssi_oe_n;
	output		hps_0_spim1_ss_0_n;
	output		hps_0_spim1_ss_1_n;
	output		hps_0_spim1_ss_2_n;
	output		hps_0_spim1_ss_3_n;
	output		hps_0_spim1_sclk_out_clk;
	input		hps_0_i2c1_scl_in_clk;
	input		hps_0_uart1_cts;
	input		hps_0_uart1_dsr;
	input		hps_0_uart1_dcd;
	input		hps_0_uart1_ri;
	output		hps_0_uart1_dtr;
	output		hps_0_uart1_rts;
	output		hps_0_uart1_out1_n;
	output		hps_0_uart1_out2_n;
	input		hps_0_uart1_rxd;
	output		hps_0_uart1_txd;
	output		hps_0_i2c1_out_data;
	input		hps_0_i2c1_sda;
	output		hps_0_i2c1_clk_clk;
	input		hps_0_i2c3_scl_in_clk;
	output		hps_0_i2c3_clk_clk;
	input		hps_0_can0_rxd;
	output		hps_0_can0_txd;
	output		hps_0_i2c3_out_data;
	input		hps_0_i2c3_sda;
	output	[7:0]	led_pio_external_connection_export;
	input	[1:0]	pb_pio_external_connection_export;
	input	[3:0]	sw_pio_external_connection_export;
	input	[31:0]	hps_0_h2f_gp_gp_in;
	output	[31:0]	hps_0_h2f_gp_gp_out;
endmodule
