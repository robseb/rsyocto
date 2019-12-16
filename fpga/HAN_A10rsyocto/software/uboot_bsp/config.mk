# Altera config.mk

################################################################################
#                             BSP Information                                  #
################################################################################

# BSP type
# 
BSP_TYPE := uboot

# BSP version
# 
BSP_VERSION := 1.0

# BSP settings File
# 
BSP_SETTINGS_FILE := /home/daibitao/file2_svn/de10_advanced/test_revD/will/a10s_ghrd/software/uboot_bsp/settings.bsp


################################################################################
#                                BSP Settings                                  #
################################################################################

# Boot Source
# 
# uboot.boot_device = SDMMC
# 
BOOT_DEVICE := SDMMC

# Disable the U-Boot build. This is useful if you only require the generated device tree source and device tree blob. This must be enabled on Windows because the uboot build is not yet supported on Windows.
# 
# uboot.disable_uboot_build = 0
# 
DISABLE_UBOOT_BUILD := 0

# Encrypt Bootloader using key file specified
# 
# uboot.secureboot.enable_bootloader_encryption = false
# 
ENABLE_BOOTLOADER_ENCRYPTION := 0

# Sign Bootloader using key pair file specified
# 
# uboot.secureboot.enable_bootloader_signing = false
# 
ENABLE_BOOTLOADER_SIGNING := 0

# Key File used for Bootloader Encryption
# 
# uboot.secureboot.encryption_key_file = encrypt.key
# 
ENCRYPTION_KEY_FILE := encrypt.key

# Key Name to use within Key File for Bootloader Encryption
# 
# uboot.secureboot.encryption_key_name = key1
# 
ENCRYPTION_KEY_NAME := key1

# Offset from H2F Bridge Base Address (0xC0000000) to location of root-public-key
# 
# uboot.secureboot.signing_key_fpga_offset = 0x0
# 
SIGNING_KEY_FPGA_OFFSET := 0x0

# Key Pair File to use when signing is enabled. You can generate this file with the command: 'make generate-signing-key-pair-file'
# 
# uboot.secureboot.signing_key_pair_file = root_key.pem
# 
SIGNING_KEY_PAIR_FILE := root_key.pem

# Sign Bootloader using key pair file specified
# 
# uboot.secureboot.signing_key_type = user
# 
SIGNING_KEY_TYPE := user

