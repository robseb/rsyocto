	component base_hps is
		port (
			clk_clk                            : in    std_logic                     := 'X';             -- clk
			hps_0_ddr_mem_a                    : out   std_logic_vector(14 downto 0);                    -- mem_a
			hps_0_ddr_mem_ba                   : out   std_logic_vector(2 downto 0);                     -- mem_ba
			hps_0_ddr_mem_ck                   : out   std_logic;                                        -- mem_ck
			hps_0_ddr_mem_ck_n                 : out   std_logic;                                        -- mem_ck_n
			hps_0_ddr_mem_cke                  : out   std_logic;                                        -- mem_cke
			hps_0_ddr_mem_cs_n                 : out   std_logic;                                        -- mem_cs_n
			hps_0_ddr_mem_ras_n                : out   std_logic;                                        -- mem_ras_n
			hps_0_ddr_mem_cas_n                : out   std_logic;                                        -- mem_cas_n
			hps_0_ddr_mem_we_n                 : out   std_logic;                                        -- mem_we_n
			hps_0_ddr_mem_reset_n              : out   std_logic;                                        -- mem_reset_n
			hps_0_ddr_mem_dq                   : inout std_logic_vector(31 downto 0) := (others => 'X'); -- mem_dq
			hps_0_ddr_mem_dqs                  : inout std_logic_vector(3 downto 0)  := (others => 'X'); -- mem_dqs
			hps_0_ddr_mem_dqs_n                : inout std_logic_vector(3 downto 0)  := (others => 'X'); -- mem_dqs_n
			hps_0_ddr_mem_odt                  : out   std_logic;                                        -- mem_odt
			hps_0_ddr_mem_dm                   : out   std_logic_vector(3 downto 0);                     -- mem_dm
			hps_0_ddr_oct_rzqin                : in    std_logic                     := 'X';             -- oct_rzqin
			hps_0_io_hps_io_emac1_inst_TX_CLK  : out   std_logic;                                        -- hps_io_emac1_inst_TX_CLK
			hps_0_io_hps_io_emac1_inst_TXD0    : out   std_logic;                                        -- hps_io_emac1_inst_TXD0
			hps_0_io_hps_io_emac1_inst_TXD1    : out   std_logic;                                        -- hps_io_emac1_inst_TXD1
			hps_0_io_hps_io_emac1_inst_TXD2    : out   std_logic;                                        -- hps_io_emac1_inst_TXD2
			hps_0_io_hps_io_emac1_inst_TXD3    : out   std_logic;                                        -- hps_io_emac1_inst_TXD3
			hps_0_io_hps_io_emac1_inst_RXD0    : in    std_logic                     := 'X';             -- hps_io_emac1_inst_RXD0
			hps_0_io_hps_io_emac1_inst_MDIO    : inout std_logic                     := 'X';             -- hps_io_emac1_inst_MDIO
			hps_0_io_hps_io_emac1_inst_MDC     : out   std_logic;                                        -- hps_io_emac1_inst_MDC
			hps_0_io_hps_io_emac1_inst_RX_CTL  : in    std_logic                     := 'X';             -- hps_io_emac1_inst_RX_CTL
			hps_0_io_hps_io_emac1_inst_TX_CTL  : out   std_logic;                                        -- hps_io_emac1_inst_TX_CTL
			hps_0_io_hps_io_emac1_inst_RX_CLK  : in    std_logic                     := 'X';             -- hps_io_emac1_inst_RX_CLK
			hps_0_io_hps_io_emac1_inst_RXD1    : in    std_logic                     := 'X';             -- hps_io_emac1_inst_RXD1
			hps_0_io_hps_io_emac1_inst_RXD2    : in    std_logic                     := 'X';             -- hps_io_emac1_inst_RXD2
			hps_0_io_hps_io_emac1_inst_RXD3    : in    std_logic                     := 'X';             -- hps_io_emac1_inst_RXD3
			hps_0_io_hps_io_sdio_inst_CMD      : inout std_logic                     := 'X';             -- hps_io_sdio_inst_CMD
			hps_0_io_hps_io_sdio_inst_D0       : inout std_logic                     := 'X';             -- hps_io_sdio_inst_D0
			hps_0_io_hps_io_sdio_inst_D1       : inout std_logic                     := 'X';             -- hps_io_sdio_inst_D1
			hps_0_io_hps_io_sdio_inst_CLK      : out   std_logic;                                        -- hps_io_sdio_inst_CLK
			hps_0_io_hps_io_sdio_inst_D2       : inout std_logic                     := 'X';             -- hps_io_sdio_inst_D2
			hps_0_io_hps_io_sdio_inst_D3       : inout std_logic                     := 'X';             -- hps_io_sdio_inst_D3
			hps_0_io_hps_io_usb1_inst_D0       : inout std_logic                     := 'X';             -- hps_io_usb1_inst_D0
			hps_0_io_hps_io_usb1_inst_D1       : inout std_logic                     := 'X';             -- hps_io_usb1_inst_D1
			hps_0_io_hps_io_usb1_inst_D2       : inout std_logic                     := 'X';             -- hps_io_usb1_inst_D2
			hps_0_io_hps_io_usb1_inst_D3       : inout std_logic                     := 'X';             -- hps_io_usb1_inst_D3
			hps_0_io_hps_io_usb1_inst_D4       : inout std_logic                     := 'X';             -- hps_io_usb1_inst_D4
			hps_0_io_hps_io_usb1_inst_D5       : inout std_logic                     := 'X';             -- hps_io_usb1_inst_D5
			hps_0_io_hps_io_usb1_inst_D6       : inout std_logic                     := 'X';             -- hps_io_usb1_inst_D6
			hps_0_io_hps_io_usb1_inst_D7       : inout std_logic                     := 'X';             -- hps_io_usb1_inst_D7
			hps_0_io_hps_io_usb1_inst_CLK      : in    std_logic                     := 'X';             -- hps_io_usb1_inst_CLK
			hps_0_io_hps_io_usb1_inst_STP      : out   std_logic;                                        -- hps_io_usb1_inst_STP
			hps_0_io_hps_io_usb1_inst_DIR      : in    std_logic                     := 'X';             -- hps_io_usb1_inst_DIR
			hps_0_io_hps_io_usb1_inst_NXT      : in    std_logic                     := 'X';             -- hps_io_usb1_inst_NXT
			hps_0_io_hps_io_uart0_inst_RX      : in    std_logic                     := 'X';             -- hps_io_uart0_inst_RX
			hps_0_io_hps_io_uart0_inst_TX      : out   std_logic;                                        -- hps_io_uart0_inst_TX
			hps_0_io_hps_io_i2c0_inst_SDA      : inout std_logic                     := 'X';             -- hps_io_i2c0_inst_SDA
			hps_0_io_hps_io_i2c0_inst_SCL      : inout std_logic                     := 'X';             -- hps_io_i2c0_inst_SCL
			hps_0_io_hps_io_gpio_inst_GPIO53   : inout std_logic                     := 'X';             -- hps_io_gpio_inst_GPIO53
			hps_0_io_hps_io_gpio_inst_GPIO54   : inout std_logic                     := 'X';             -- hps_io_gpio_inst_GPIO54
			hps_0_spim0_txd                    : out   std_logic;                                        -- txd
			hps_0_spim0_rxd                    : in    std_logic                     := 'X';             -- rxd
			hps_0_spim0_ss_in_n                : in    std_logic                     := 'X';             -- ss_in_n
			hps_0_spim0_ssi_oe_n               : out   std_logic;                                        -- ssi_oe_n
			hps_0_spim0_ss_0_n                 : out   std_logic;                                        -- ss_0_n
			hps_0_spim0_ss_1_n                 : out   std_logic;                                        -- ss_1_n
			hps_0_spim0_ss_2_n                 : out   std_logic;                                        -- ss_2_n
			hps_0_spim0_ss_3_n                 : out   std_logic;                                        -- ss_3_n
			hps_0_spim0_sclk_out_clk           : out   std_logic;                                        -- clk
			hps_0_spim1_txd                    : out   std_logic;                                        -- txd
			hps_0_spim1_rxd                    : in    std_logic                     := 'X';             -- rxd
			hps_0_spim1_ss_in_n                : in    std_logic                     := 'X';             -- ss_in_n
			hps_0_spim1_ssi_oe_n               : out   std_logic;                                        -- ssi_oe_n
			hps_0_spim1_ss_0_n                 : out   std_logic;                                        -- ss_0_n
			hps_0_spim1_ss_1_n                 : out   std_logic;                                        -- ss_1_n
			hps_0_spim1_ss_2_n                 : out   std_logic;                                        -- ss_2_n
			hps_0_spim1_ss_3_n                 : out   std_logic;                                        -- ss_3_n
			hps_0_spim1_sclk_out_clk           : out   std_logic;                                        -- clk
			hps_0_i2c1_scl_in_clk              : in    std_logic                     := 'X';             -- clk
			hps_0_uart1_cts                    : in    std_logic                     := 'X';             -- cts
			hps_0_uart1_dsr                    : in    std_logic                     := 'X';             -- dsr
			hps_0_uart1_dcd                    : in    std_logic                     := 'X';             -- dcd
			hps_0_uart1_ri                     : in    std_logic                     := 'X';             -- ri
			hps_0_uart1_dtr                    : out   std_logic;                                        -- dtr
			hps_0_uart1_rts                    : out   std_logic;                                        -- rts
			hps_0_uart1_out1_n                 : out   std_logic;                                        -- out1_n
			hps_0_uart1_out2_n                 : out   std_logic;                                        -- out2_n
			hps_0_uart1_rxd                    : in    std_logic                     := 'X';             -- rxd
			hps_0_uart1_txd                    : out   std_logic;                                        -- txd
			hps_0_i2c1_out_data                : out   std_logic;                                        -- out_data
			hps_0_i2c1_sda                     : in    std_logic                     := 'X';             -- sda
			hps_0_i2c1_clk_clk                 : out   std_logic;                                        -- clk
			hps_0_i2c3_scl_in_clk              : in    std_logic                     := 'X';             -- clk
			hps_0_i2c3_clk_clk                 : out   std_logic;                                        -- clk
			hps_0_can0_rxd                     : in    std_logic                     := 'X';             -- rxd
			hps_0_can0_txd                     : out   std_logic;                                        -- txd
			hps_0_i2c3_out_data                : out   std_logic;                                        -- out_data
			hps_0_i2c3_sda                     : in    std_logic                     := 'X';             -- sda
			led_pio_external_connection_export : out   std_logic_vector(7 downto 0);                     -- export
			pb_pio_external_connection_export  : in    std_logic_vector(1 downto 0)  := (others => 'X'); -- export
			sw_pio_external_connection_export  : in    std_logic_vector(3 downto 0)  := (others => 'X'); -- export
			hps_0_h2f_gp_gp_in                 : in    std_logic_vector(31 downto 0) := (others => 'X'); -- gp_in
			hps_0_h2f_gp_gp_out                : out   std_logic_vector(31 downto 0)                     -- gp_out
		);
	end component base_hps;

	u0 : component base_hps
		port map (
			clk_clk                            => CONNECTED_TO_clk_clk,                            --                         clk.clk
			hps_0_ddr_mem_a                    => CONNECTED_TO_hps_0_ddr_mem_a,                    --                   hps_0_ddr.mem_a
			hps_0_ddr_mem_ba                   => CONNECTED_TO_hps_0_ddr_mem_ba,                   --                            .mem_ba
			hps_0_ddr_mem_ck                   => CONNECTED_TO_hps_0_ddr_mem_ck,                   --                            .mem_ck
			hps_0_ddr_mem_ck_n                 => CONNECTED_TO_hps_0_ddr_mem_ck_n,                 --                            .mem_ck_n
			hps_0_ddr_mem_cke                  => CONNECTED_TO_hps_0_ddr_mem_cke,                  --                            .mem_cke
			hps_0_ddr_mem_cs_n                 => CONNECTED_TO_hps_0_ddr_mem_cs_n,                 --                            .mem_cs_n
			hps_0_ddr_mem_ras_n                => CONNECTED_TO_hps_0_ddr_mem_ras_n,                --                            .mem_ras_n
			hps_0_ddr_mem_cas_n                => CONNECTED_TO_hps_0_ddr_mem_cas_n,                --                            .mem_cas_n
			hps_0_ddr_mem_we_n                 => CONNECTED_TO_hps_0_ddr_mem_we_n,                 --                            .mem_we_n
			hps_0_ddr_mem_reset_n              => CONNECTED_TO_hps_0_ddr_mem_reset_n,              --                            .mem_reset_n
			hps_0_ddr_mem_dq                   => CONNECTED_TO_hps_0_ddr_mem_dq,                   --                            .mem_dq
			hps_0_ddr_mem_dqs                  => CONNECTED_TO_hps_0_ddr_mem_dqs,                  --                            .mem_dqs
			hps_0_ddr_mem_dqs_n                => CONNECTED_TO_hps_0_ddr_mem_dqs_n,                --                            .mem_dqs_n
			hps_0_ddr_mem_odt                  => CONNECTED_TO_hps_0_ddr_mem_odt,                  --                            .mem_odt
			hps_0_ddr_mem_dm                   => CONNECTED_TO_hps_0_ddr_mem_dm,                   --                            .mem_dm
			hps_0_ddr_oct_rzqin                => CONNECTED_TO_hps_0_ddr_oct_rzqin,                --                            .oct_rzqin
			hps_0_io_hps_io_emac1_inst_TX_CLK  => CONNECTED_TO_hps_0_io_hps_io_emac1_inst_TX_CLK,  --                    hps_0_io.hps_io_emac1_inst_TX_CLK
			hps_0_io_hps_io_emac1_inst_TXD0    => CONNECTED_TO_hps_0_io_hps_io_emac1_inst_TXD0,    --                            .hps_io_emac1_inst_TXD0
			hps_0_io_hps_io_emac1_inst_TXD1    => CONNECTED_TO_hps_0_io_hps_io_emac1_inst_TXD1,    --                            .hps_io_emac1_inst_TXD1
			hps_0_io_hps_io_emac1_inst_TXD2    => CONNECTED_TO_hps_0_io_hps_io_emac1_inst_TXD2,    --                            .hps_io_emac1_inst_TXD2
			hps_0_io_hps_io_emac1_inst_TXD3    => CONNECTED_TO_hps_0_io_hps_io_emac1_inst_TXD3,    --                            .hps_io_emac1_inst_TXD3
			hps_0_io_hps_io_emac1_inst_RXD0    => CONNECTED_TO_hps_0_io_hps_io_emac1_inst_RXD0,    --                            .hps_io_emac1_inst_RXD0
			hps_0_io_hps_io_emac1_inst_MDIO    => CONNECTED_TO_hps_0_io_hps_io_emac1_inst_MDIO,    --                            .hps_io_emac1_inst_MDIO
			hps_0_io_hps_io_emac1_inst_MDC     => CONNECTED_TO_hps_0_io_hps_io_emac1_inst_MDC,     --                            .hps_io_emac1_inst_MDC
			hps_0_io_hps_io_emac1_inst_RX_CTL  => CONNECTED_TO_hps_0_io_hps_io_emac1_inst_RX_CTL,  --                            .hps_io_emac1_inst_RX_CTL
			hps_0_io_hps_io_emac1_inst_TX_CTL  => CONNECTED_TO_hps_0_io_hps_io_emac1_inst_TX_CTL,  --                            .hps_io_emac1_inst_TX_CTL
			hps_0_io_hps_io_emac1_inst_RX_CLK  => CONNECTED_TO_hps_0_io_hps_io_emac1_inst_RX_CLK,  --                            .hps_io_emac1_inst_RX_CLK
			hps_0_io_hps_io_emac1_inst_RXD1    => CONNECTED_TO_hps_0_io_hps_io_emac1_inst_RXD1,    --                            .hps_io_emac1_inst_RXD1
			hps_0_io_hps_io_emac1_inst_RXD2    => CONNECTED_TO_hps_0_io_hps_io_emac1_inst_RXD2,    --                            .hps_io_emac1_inst_RXD2
			hps_0_io_hps_io_emac1_inst_RXD3    => CONNECTED_TO_hps_0_io_hps_io_emac1_inst_RXD3,    --                            .hps_io_emac1_inst_RXD3
			hps_0_io_hps_io_sdio_inst_CMD      => CONNECTED_TO_hps_0_io_hps_io_sdio_inst_CMD,      --                            .hps_io_sdio_inst_CMD
			hps_0_io_hps_io_sdio_inst_D0       => CONNECTED_TO_hps_0_io_hps_io_sdio_inst_D0,       --                            .hps_io_sdio_inst_D0
			hps_0_io_hps_io_sdio_inst_D1       => CONNECTED_TO_hps_0_io_hps_io_sdio_inst_D1,       --                            .hps_io_sdio_inst_D1
			hps_0_io_hps_io_sdio_inst_CLK      => CONNECTED_TO_hps_0_io_hps_io_sdio_inst_CLK,      --                            .hps_io_sdio_inst_CLK
			hps_0_io_hps_io_sdio_inst_D2       => CONNECTED_TO_hps_0_io_hps_io_sdio_inst_D2,       --                            .hps_io_sdio_inst_D2
			hps_0_io_hps_io_sdio_inst_D3       => CONNECTED_TO_hps_0_io_hps_io_sdio_inst_D3,       --                            .hps_io_sdio_inst_D3
			hps_0_io_hps_io_usb1_inst_D0       => CONNECTED_TO_hps_0_io_hps_io_usb1_inst_D0,       --                            .hps_io_usb1_inst_D0
			hps_0_io_hps_io_usb1_inst_D1       => CONNECTED_TO_hps_0_io_hps_io_usb1_inst_D1,       --                            .hps_io_usb1_inst_D1
			hps_0_io_hps_io_usb1_inst_D2       => CONNECTED_TO_hps_0_io_hps_io_usb1_inst_D2,       --                            .hps_io_usb1_inst_D2
			hps_0_io_hps_io_usb1_inst_D3       => CONNECTED_TO_hps_0_io_hps_io_usb1_inst_D3,       --                            .hps_io_usb1_inst_D3
			hps_0_io_hps_io_usb1_inst_D4       => CONNECTED_TO_hps_0_io_hps_io_usb1_inst_D4,       --                            .hps_io_usb1_inst_D4
			hps_0_io_hps_io_usb1_inst_D5       => CONNECTED_TO_hps_0_io_hps_io_usb1_inst_D5,       --                            .hps_io_usb1_inst_D5
			hps_0_io_hps_io_usb1_inst_D6       => CONNECTED_TO_hps_0_io_hps_io_usb1_inst_D6,       --                            .hps_io_usb1_inst_D6
			hps_0_io_hps_io_usb1_inst_D7       => CONNECTED_TO_hps_0_io_hps_io_usb1_inst_D7,       --                            .hps_io_usb1_inst_D7
			hps_0_io_hps_io_usb1_inst_CLK      => CONNECTED_TO_hps_0_io_hps_io_usb1_inst_CLK,      --                            .hps_io_usb1_inst_CLK
			hps_0_io_hps_io_usb1_inst_STP      => CONNECTED_TO_hps_0_io_hps_io_usb1_inst_STP,      --                            .hps_io_usb1_inst_STP
			hps_0_io_hps_io_usb1_inst_DIR      => CONNECTED_TO_hps_0_io_hps_io_usb1_inst_DIR,      --                            .hps_io_usb1_inst_DIR
			hps_0_io_hps_io_usb1_inst_NXT      => CONNECTED_TO_hps_0_io_hps_io_usb1_inst_NXT,      --                            .hps_io_usb1_inst_NXT
			hps_0_io_hps_io_uart0_inst_RX      => CONNECTED_TO_hps_0_io_hps_io_uart0_inst_RX,      --                            .hps_io_uart0_inst_RX
			hps_0_io_hps_io_uart0_inst_TX      => CONNECTED_TO_hps_0_io_hps_io_uart0_inst_TX,      --                            .hps_io_uart0_inst_TX
			hps_0_io_hps_io_i2c0_inst_SDA      => CONNECTED_TO_hps_0_io_hps_io_i2c0_inst_SDA,      --                            .hps_io_i2c0_inst_SDA
			hps_0_io_hps_io_i2c0_inst_SCL      => CONNECTED_TO_hps_0_io_hps_io_i2c0_inst_SCL,      --                            .hps_io_i2c0_inst_SCL
			hps_0_io_hps_io_gpio_inst_GPIO53   => CONNECTED_TO_hps_0_io_hps_io_gpio_inst_GPIO53,   --                            .hps_io_gpio_inst_GPIO53
			hps_0_io_hps_io_gpio_inst_GPIO54   => CONNECTED_TO_hps_0_io_hps_io_gpio_inst_GPIO54,   --                            .hps_io_gpio_inst_GPIO54
			hps_0_spim0_txd                    => CONNECTED_TO_hps_0_spim0_txd,                    --                 hps_0_spim0.txd
			hps_0_spim0_rxd                    => CONNECTED_TO_hps_0_spim0_rxd,                    --                            .rxd
			hps_0_spim0_ss_in_n                => CONNECTED_TO_hps_0_spim0_ss_in_n,                --                            .ss_in_n
			hps_0_spim0_ssi_oe_n               => CONNECTED_TO_hps_0_spim0_ssi_oe_n,               --                            .ssi_oe_n
			hps_0_spim0_ss_0_n                 => CONNECTED_TO_hps_0_spim0_ss_0_n,                 --                            .ss_0_n
			hps_0_spim0_ss_1_n                 => CONNECTED_TO_hps_0_spim0_ss_1_n,                 --                            .ss_1_n
			hps_0_spim0_ss_2_n                 => CONNECTED_TO_hps_0_spim0_ss_2_n,                 --                            .ss_2_n
			hps_0_spim0_ss_3_n                 => CONNECTED_TO_hps_0_spim0_ss_3_n,                 --                            .ss_3_n
			hps_0_spim0_sclk_out_clk           => CONNECTED_TO_hps_0_spim0_sclk_out_clk,           --        hps_0_spim0_sclk_out.clk
			hps_0_spim1_txd                    => CONNECTED_TO_hps_0_spim1_txd,                    --                 hps_0_spim1.txd
			hps_0_spim1_rxd                    => CONNECTED_TO_hps_0_spim1_rxd,                    --                            .rxd
			hps_0_spim1_ss_in_n                => CONNECTED_TO_hps_0_spim1_ss_in_n,                --                            .ss_in_n
			hps_0_spim1_ssi_oe_n               => CONNECTED_TO_hps_0_spim1_ssi_oe_n,               --                            .ssi_oe_n
			hps_0_spim1_ss_0_n                 => CONNECTED_TO_hps_0_spim1_ss_0_n,                 --                            .ss_0_n
			hps_0_spim1_ss_1_n                 => CONNECTED_TO_hps_0_spim1_ss_1_n,                 --                            .ss_1_n
			hps_0_spim1_ss_2_n                 => CONNECTED_TO_hps_0_spim1_ss_2_n,                 --                            .ss_2_n
			hps_0_spim1_ss_3_n                 => CONNECTED_TO_hps_0_spim1_ss_3_n,                 --                            .ss_3_n
			hps_0_spim1_sclk_out_clk           => CONNECTED_TO_hps_0_spim1_sclk_out_clk,           --        hps_0_spim1_sclk_out.clk
			hps_0_i2c1_scl_in_clk              => CONNECTED_TO_hps_0_i2c1_scl_in_clk,              --           hps_0_i2c1_scl_in.clk
			hps_0_uart1_cts                    => CONNECTED_TO_hps_0_uart1_cts,                    --                 hps_0_uart1.cts
			hps_0_uart1_dsr                    => CONNECTED_TO_hps_0_uart1_dsr,                    --                            .dsr
			hps_0_uart1_dcd                    => CONNECTED_TO_hps_0_uart1_dcd,                    --                            .dcd
			hps_0_uart1_ri                     => CONNECTED_TO_hps_0_uart1_ri,                     --                            .ri
			hps_0_uart1_dtr                    => CONNECTED_TO_hps_0_uart1_dtr,                    --                            .dtr
			hps_0_uart1_rts                    => CONNECTED_TO_hps_0_uart1_rts,                    --                            .rts
			hps_0_uart1_out1_n                 => CONNECTED_TO_hps_0_uart1_out1_n,                 --                            .out1_n
			hps_0_uart1_out2_n                 => CONNECTED_TO_hps_0_uart1_out2_n,                 --                            .out2_n
			hps_0_uart1_rxd                    => CONNECTED_TO_hps_0_uart1_rxd,                    --                            .rxd
			hps_0_uart1_txd                    => CONNECTED_TO_hps_0_uart1_txd,                    --                            .txd
			hps_0_i2c1_out_data                => CONNECTED_TO_hps_0_i2c1_out_data,                --                  hps_0_i2c1.out_data
			hps_0_i2c1_sda                     => CONNECTED_TO_hps_0_i2c1_sda,                     --                            .sda
			hps_0_i2c1_clk_clk                 => CONNECTED_TO_hps_0_i2c1_clk_clk,                 --              hps_0_i2c1_clk.clk
			hps_0_i2c3_scl_in_clk              => CONNECTED_TO_hps_0_i2c3_scl_in_clk,              --           hps_0_i2c3_scl_in.clk
			hps_0_i2c3_clk_clk                 => CONNECTED_TO_hps_0_i2c3_clk_clk,                 --              hps_0_i2c3_clk.clk
			hps_0_can0_rxd                     => CONNECTED_TO_hps_0_can0_rxd,                     --                  hps_0_can0.rxd
			hps_0_can0_txd                     => CONNECTED_TO_hps_0_can0_txd,                     --                            .txd
			hps_0_i2c3_out_data                => CONNECTED_TO_hps_0_i2c3_out_data,                --                  hps_0_i2c3.out_data
			hps_0_i2c3_sda                     => CONNECTED_TO_hps_0_i2c3_sda,                     --                            .sda
			led_pio_external_connection_export => CONNECTED_TO_led_pio_external_connection_export, -- led_pio_external_connection.export
			pb_pio_external_connection_export  => CONNECTED_TO_pb_pio_external_connection_export,  --  pb_pio_external_connection.export
			sw_pio_external_connection_export  => CONNECTED_TO_sw_pio_external_connection_export,  --  sw_pio_external_connection.export
			hps_0_h2f_gp_gp_in                 => CONNECTED_TO_hps_0_h2f_gp_gp_in,                 --                hps_0_h2f_gp.gp_in
			hps_0_h2f_gp_gp_out                => CONNECTED_TO_hps_0_h2f_gp_gp_out                 --                            .gp_out
		);

