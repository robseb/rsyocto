#-----------------------------------------------------------------------------
#                                  TOOLS
#-----------------------------------------------------------------------------

CAT 	:= cat
CP	:= cp -rf
CHMOD 	:= chmod
DIFF 	:= diff
DTC 	:= dtc
ECHO 	:= echo
PATCH 	:= patch
MKDIR 	:= mkdir -p
RM 	:= rm -rf
TOUCH 	:= touch
UNTAR 	:= tar xzf

#-----------------------------------------------------------------------------
#                              HELPER FUNCTIONS
#-----------------------------------------------------------------------------

define stamp
@$(MKDIR) $(@D)
@$(TOUCH) $@
endef

define untar_recipe
$(UNTAR) $(if $1,$1,$(if $<,$<,$(error ERROR: no input provided to gnu make function untar_recipe)))
endef


#-----------------------------------------------------------------------------
#                              WINDOWS SUPPORT
#-----------------------------------------------------------------------------

HOSTOS := $(shell uname -o 2>/dev/null | tr [:upper:] [:lower:])

ifeq ($(HOSTOS),cygwin)

# When using UBoot build system on Windows 
# use cygwin's GNU make
MAKE := $(shell cygpath -m "/bin/make")
MAKE_ARGS += MAKE=/bin/make

CYGPATH := $(shell cygpath -m "$(shell which cygpath)")
MAKE_ARGS += CYGPATH=$(CYGPATH)

UNAME_M := $(shell uname -m)
ifeq ($(UNAME_M),x86_64)
HOST_CROSS_COMPILE := x86_64-w64-mingw32-
else
HOST_CROSS_COMPILE := i686-pc-mingw32-
endif

MAKE_ARGS += HOSTCC=$(HOST_CROSS_COMPILE)gcc HOSTSTRIP=$(HOST_CROSS_COMPILE)strip

# Under cygwin, overload the untar_recipe function to use unix stype paths. This is required for cygwin tar
define untar_recipe
$(UNTAR) $(shell cygpath --unix "$(if $1,$1,$(if $<,$<,$(error ERROR: no input provided to gnu make function untar_recipe)))")
endef

else # if HOSTOS != cygwin

ifdef WINDIR
$(error ERROR: Windows build of preloader requires cygwin build environment. Ensure this makefile is executed from the SoC EDS Command Shell)
endif
ifdef windir
$(error ERROR: Windows build of preloader requires cygwin build environment. Ensure this makefile is executed from the SoC EDS Command Shell)
endif

endif # HOSTOS == cygwin


#-----------------------------------------------------------------------------
#                                 SETTINGS
#-----------------------------------------------------------------------------

include config.mk

####################
# Static Settings

DTS := devicetree.dts

TGZ := $(SOCEDS_DEST_ROOT)/host_tools/altera/bootloaders/u-boot/uboot-socfpga.tar.gz

PREBUILT_DIR := $(SOCEDS_DEST_ROOT)/host_tools/altera/bootloaders/u-boot/prebuilt

CROSS_COMPILE := arm-altera-eabi-

DEVICE_FAMILY := arria10
####################

MKPIMAGE_HEADER_VERSION := 1

MAKE_ARGS += CROSS_COMPILE=$(CROSS_COMPILE)

DTC_ARGS :=

DTB := $(patsubst %.dts,%.dtb,$(DTS))

PRELOADER_SRC_DIR := $(patsubst %.tar.gz,%,$(shell basename $(TGZ)))

UBOOT_SRC_DIR = $(patsubst %.tar.gz,%,$(notdir $(TGZ)))

UBOOT.ELF := $(UBOOT_SRC_DIR)/u-boot

UBOOT.BINARY := $(UBOOT_SRC_DIR)/u-boot.bin

UBOOT.BINARY_W_DTB := u-boot_w_dtb.bin

UBOOT.MKPIMAGE_BINARY_W_DTB := uboot_w_dtb-mkpimage.bin

UBOOT.MKPIMAGE_SIGNED_BINARY_W_DTB := uboot_w_dtb-mkpimage-signed.abin

UBOOT.MKPIMAGE_ENCRYPTED_BINARY_W_DTB := uboot_w_dtb-mkpimage-encrypted.abin

UBOOT.MKPIMAGE_ENCRYPTED_SIGNED_BINARY_W_DTB := uboot_w_dtb-mkpimage-encrypted-signed.abin

SOCFPGA_BOARD_CONFIG.QSPI = socfpga_$(DEVICE_FAMILY)_qspi_defconfig
SOCFPGA_BOARD_CONFIG.NAND = socfpga_$(DEVICE_FAMILY)_nand_defconfig
SOCFPGA_BOARD_CONFIG.SDMMC = socfpga_$(DEVICE_FAMILY)_config
SOCFPGA_BOARD_CONFIG := $(SOCFPGA_BOARD_CONFIG.$(BOOT_DEVICE))

ifeq ($(SOCFPGA_BOARD_CONFIG),)
$(error ERROR: SOCFPGA_BOARD_CONFIG not set. Check your Settings and Regenerate your Bootloader)
endif

STAMP_DIR ?= $(UBOOT_SRC_DIR)

#-----------------------------------------------------------------------------
#                                 TARGETS
#-----------------------------------------------------------------------------

# On windows, we do not yet support building u-boot.
# Only dtb creation for uboot
# is supported
ifeq ($(HOSTOS),cygwin)
ifneq ($(DISABLE_UBOOT_BUILD),1)
$(error ERROR: DISABLE_UBOOT_BUILD is not set to 1. U-Boot Build is not supported on Windows. Generate your bootloader with --set uboot.disable_uboot_build true)
endif
endif

.PHONY: all	
all: $(DTB) $(UBOOT.MKPIMAGE_BINARY_W_DTB)

ifeq ($(ENABLE_BOOTLOADER_SIGNING),1)
ifeq ($(ENABLE_BOOTLOADER_ENCRYPTION),1)
UBOOT.SECURE_BINARY := $(UBOOT.MKPIMAGE_ENCRYPTED_SIGNED_BINARY_W_DTB)
UBOOT.SECURE_BINARYx4 := $(patsubst %.abin,%-x4.abin,$(UBOOT.SECURE_BINARY))
all: $(UBOOT.SECURE_BINARYx4)
endif
endif

ifneq ($(ENABLE_BOOTLOADER_ENCRYPTION),1)
ifeq ($(ENABLE_BOOTLOADER_SIGNING),1)
UBOOT.SECURE_BINARY := $(UBOOT.MKPIMAGE_SIGNED_BINARY_W_DTB)
UBOOT.SECURE_BINARYx4 := $(patsubst %.abin,%-x4.abin,$(UBOOT.SECURE_BINARY))
all: $(UBOOT.SECURE_BINARYx4)
endif
endif

ifneq ($(ENABLE_BOOTLOADER_SIGNING),1)
ifeq ($(ENABLE_BOOTLOADER_ENCRYPTION),1)
UBOOT.SECURE_BINARY := $(UBOOT.MKPIMAGE_ENCRYPTED_BINARY_W_DTB)
UBOOT.SECURE_BINARYx4 := $(patsubst %.abin,%-x4.abin,$(UBOOT.SECURE_BINARY))
all: $(UBOOT.SECURE_BINARYx4)
endif
endif

################
# Build DTB

.PHONY: dtb
dtb: $(DTB)

$(DTB): $(DTS)
	$(DTC) -O dtb -o $@ -I dts $(DTC_ARGS) $<

################
# Untar

UNTAR_SRC := $(STAMP_DIR)/.untar

.PHONY: src
src: $(UNTAR_SRC)

$(UNTAR_SRC): $(TGZ)
	@$(RM) $(PRELOADER_SRC_DIR)
	$(untar_recipe)
	@$(CHMOD) -R 755 $(PRELOADER_SRC_DIR)
	$(stamp)


################
# Config

CONFIG := $(STAMP_DIR)/.socfpga_config

.PHONY: config
config: $(CONFIG)

$(CONFIG): $(UNTAR_SRC) config.mk
	$(MAKE) $(MAKE_ARGS) -C $(UBOOT_SRC_DIR) $(SOCFPGA_BOARD_CONFIG)
	$(stamp)


################
# Build

.PHONY: uboot
uboot: $(UBOOT.BINARY)

ifneq ($(DISABLE_UBOOT_BUILD),1)

$(UBOOT.BINARY): $(CONFIG)
	$(MAKE) $(MAKE_ARGS) -C $(UBOOT_SRC_DIR) all

else # if uboot build is disabled, copy over a prebuilt u-boot binary that matches board config requested

$(UBOOT.BINARY): $(PREBUILT_DIR)/$(SOCFPGA_BOARD_CONFIG)/u-boot.bin $(UBOOT.ELF) config.mk
	@$(MKDIR) $(@D)
	$(CP) $< $@

$(UBOOT.ELF): $(PREBUILT_DIR)/$(SOCFPGA_BOARD_CONFIG)/u-boot config.mk
	@$(MKDIR) $(@D)
	$(CP) $< $@

endif


$(UBOOT.BINARY_W_DTB): $(UBOOT.BINARY) $(DTB)
	@$(MKDIR) $(@D)
	$(CAT) $(UBOOT.BINARY) $(DTB) > $@

MKPIMAGE := mkpimage

ifeq ($(ENABLE_BOOTLOADER_SIGNING),1)
MKPIMAGE_USE_SINGLE_IMAGE := 1
endif
ifeq ($(ENABLE_BOOTLOADER_ENCRYPTION),1)
MKPIMAGE_USE_SINGLE_IMAGE := 1
endif

MKPIMAGE_ARGS += --header-version $(MKPIMAGE_HEADER_VERSION)
ifeq ($(MKPIMAGE_USE_SINGLE_IMAGE),1)
MKPIMAGE_ARGS += --alignment 0 -o $@ $<
else # use normal quad version of mkpimage
MKPIMAGE_ARGS += -o $@ $< $< $< $<
endif

$(UBOOT.MKPIMAGE_BINARY_W_DTB): $(UBOOT.BINARY_W_DTB)
	@$(MKDIR) $(@D)
	$(MKPIMAGE) $(MKPIMAGE_ARGS)

# Signing Flows are known not to work with RedHat 5, use RedHat >= 6

ALT_SIGN_ARGS += --rootkey-type=$(SIGNING_KEY_TYPE)
ALT_SIGN_ARGS += --keypair=$(SIGNING_KEY_PAIR_FILE)

ifeq ($(SIGNING_KEY_TYPE),fpga)
ALT_SIGN_ARGS += --fpga-key-offset=$(SIGNING_KEY_FPGA_OFFSET)
endif

# Add --pubkeyout=pubkeyout.bin if SIGN_KEY_TYPE is fpga or fuse
ifneq ($(filter fpga fuse,$(SIGNING_KEY_TYPE)),)
ALT_SIGN_ARGS += --pubkeyout=pubkeyout.bin
endif

ALT_ENCRYPT_ARGS += --key="$(ENCRYPTION_KEY_FILE):$(ENCRYPTION_KEY_NAME)"

$(UBOOT.MKPIMAGE_SIGNED_BINARY_W_DTB): $(UBOOT.MKPIMAGE_BINARY_W_DTB) $(SIGNING_KEY_PAIR_FILE)
	alt-secure-boot sign $(ALT_SIGN_ARGS) --inputfile=$< --outputfile=$@

$(UBOOT.MKPIMAGE_ENCRYPTED_BINARY_W_DTB): $(UBOOT.MKPIMAGE_BINARY_W_DTB) $(ENCRYPTION_KEY_FILE)
	alt-secure-boot encrypt $(ALT_ENCRYPT_ARGS) --inputfile=$< --outputfile=$@

$(UBOOT.MKPIMAGE_ENCRYPTED_SIGNED_BINARY_W_DTB): $(UBOOT.MKPIMAGE_ENCRYPTED_BINARY_W_DTB) $(SIGNING_KEY_PAIR_FILE)
	alt-secure-boot sign $(ALT_SIGN_ARGS) --inputfile=$< --outputfile=$@


ALT_IMAGE_CAT_ARGS += --alignment=256

ifneq ($(UBOOT.SECURE_BINARYx4),)
ifneq ($(UBOOT.SECURE_BINARY),)
$(UBOOT.SECURE_BINARYx4): $(UBOOT.SECURE_BINARY)
	alt-image-cat $< $(ALT_IMAGE_CAT_ARGS) --output_image=$@ 
endif
endif

ifneq ($(SIGNING_KEY_PAIR_FILE),)
ifeq ($(wildcard $(SIGNING_KEY_PAIR_FILE)),)
$(SIGNING_KEY_PAIR_FILE):
	$(error Error: Signing Key Pair File '$@' does not exist. Run 'make generate-signing-key-pair-file' to generate this file)
endif
endif

.PHONY: generate-signing-key-pair-file
generate-signing-key-pair-file:
ifeq ($(SIGNING_KEY_PAIR_FILE),)
	$(error ERROR: SIGNING_KEY_PAIR_FILE variable not set. Ensure bootloader signing is enabled)
endif
ifneq ($(wildcard $(SIGNING_KEY_PAIR_FILE)),)
	$(error ERROR: Signing Key Pair File '$(SIGNING_KEY_PAIR_FILE)' already exists. Delete this file if you really want to regenerate it)
endif
	openssl ecparam -genkey -name prime256v1 -out $(SIGNING_KEY_PAIR_FILE)


ifneq ($(ENCRYPTION_KEY_FILE),)
ifeq ($(wildcard $(ENCRYPTION_KEY_FILE)),)
$(ENCRYPTION_KEY_FILE):
	$(error Error: Encryption Key File '$@' does not exist. Run 'make generate-example-encryption-key-file' to generate an example key file that can be used as a reference)
endif
endif

.PHONY: generate-example-encryption-key-file
generate-example-encryption-key-file:
ifeq ($(ENCRYPTION_KEY_FILE),)
	$(error ERROR: ENCRYPTION_KEY_FILE variable not set. Ensure bootloader encryption is enabled)
endif
ifneq ($(wildcard $(ENCRYPTION_KEY_FILE)),)
	$(error ERROR: Encryption Key File '$(ENCRYPTION_KEY_FILE)' already exists. Delete this file if you really want to regenerate it)
endif
	@echo '# This is an example key file' > $(ENCRYPTION_KEY_FILE)
	@echo '# The .key file is a plain text file in which each line represents a key unless the line starts with "#"' >> $(ENCRYPTION_KEY_FILE)
	@echo '# The "#" symbol is used to denote comments. Each valid key line has the following format:' >> $(ENCRYPTION_KEY_FILE)
	@echo '# <key identity><white space><256-bit hexadecimal key>.' >> $(ENCRYPTION_KEY_FILE)
	@echo 'key1 0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF' >> $(ENCRYPTION_KEY_FILE)
	@echo 'key2 ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789' >> $(ENCRYPTION_KEY_FILE)


################
# Clean

CLEAN_FILES += $(DTB) $(CONFIG) $(UBOOT.ELF) $(UBOOT.BINARY) $(UBOOT.BINARY_W_DTB) $(UBOOT.MKPIMAGE_BINARY_W_DTB) $(UBOOT.MKPIMAGE_ENCRYPTED_BINARY_W_DTB) $(UBOOT.MKPIMAGE_SIGNED_BINARY_W_DTB) $(UBOOT.SECURE_BINARY) $(UBOOT.SECURE_BINARYx4) pubkeyout.bin

.PHONY: clean
clean:
ifneq ($(wildcard $(UBOOT_SRC_DIR)/Makefile),)
	$(MAKE) $(MAKE_ARGS) -C $(UBOOT_SRC_DIR) mrproper
endif
	$(RM) $(CLEAN_FILES)

.PHONY: clean-all
clean-all:
	$(RM) $(UBOOT_SRC_DIR) $(CLEAN_FILES)



###############################################################################
#
# Applying patch files
#

# GNU MAKE >= 3.81 is required to apply patch files correctly
.SECONDEXPANSION:

# Patch files are discovered in current directory and in the directory adjacent
# to the tarball (TGZ) directory

PATCH.FILES := $(strip \
	$(sort $(wildcard $(patsubst %.tar.gz,%.patch,$(TGZ))/*.patch)) \
	$(sort $(wildcard $(patsubst %.tar.gz,%.patch,$(TGZ))/$(HOSTOS)/*.patch)) \
	$(sort $(wildcard $(abspath .)/*.patch)) \
	$(EXTRA_PATCH_FILES))

PATCH.APPLY_TARGETS := $(strip $(foreach patchfile,$(PATCH.FILES), \
 $(eval patchfile_target := $(notdir $(basename $(patchfile)))) \
 $(eval $(patchfile_target).PATCH_FILE := $(patchfile)) \
 $(PRELOADER_SRC_DIR)/.applypatch.$(patchfile_target) \
))

.PHONY: patch-apply
patch-apply: $(PATCH.APPLY_TARGETS)

$(PATCH.APPLY_TARGETS): $(PRELOADER_SRC_DIR)/.applypatch.%: $$(%.PATCH_FILE) $(UNTAR_SRC)
	@$(ECHO) Applying Patch: $<
	$(PATCH) -p1 --directory=$(PRELOADER_SRC_DIR) --input=$<
	$(stamp)

###############################################################################


###############################################################################
#
# Creating a patch file
#

PATCH.USER_FILE := user.patch

.PHONY: patch-create
patch-create: $(if $(PATCH.SKIP_CLEAN),,clean)
ifeq ($(wildcard $(PRELOADER_SRC_DIR).orig),)
	$(error ERROR: $(PRELOADER_SRC_DIR).orig does not exist)
endif
	$(DIFF) -rupN $(PRELOADER_SRC_DIR).orig/ $(PRELOADER_SRC_DIR)/ > $(PATCH.USER_FILE) || true
ifeq ($(HOSTOS),cygwin)
	dos2unix $(PATCH.USER_FILE)
endif
	$(CAT) $(PATCH.USER_FILE)

###############################################################################
