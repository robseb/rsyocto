#!/usr/bin/env python3
# coding: utf-8
#
#            ########   ######     ##    ##  #######   ######  ########  #######                  
#            ##     ## ##    ##     ##  ##  ##     ## ##    ##    ##    ##     ##           
#            ##     ## ##            ####   ##     ## ##          ##    ##     ##        
#            ########   ######        ##    ##     ## ##          ##    ##     ##       
#            ##   ##         ##       ##    ##     ## ##          ##    ##     ##      
#            ##    ##  ##    ##       ##    ##     ## ##    ##    ##    ##     ##        
#            ##     ##  ######        ##     #######   ######     ##     #######         
#             ___          _   _      _     ___               _                 
#            | _ )  _  _  (_) | |  __| |   / __|  _  _   ___ | |_   ___   _ __  
#            | _ \ | || | | | | | / _` |   \__ \ | || | (_-< |  _| / -_) | '  \ 
#            |___/  \_,_| |_| |_| \__,_|   |___/  \_, | /__/  \__| \___| |_|_|_|
#                                                  |__/                              
#
#
# Robin Sebastian (https://github.com/robseb)
# Contact: git@robseb.de
# Repository: https://github.com/robseb/rsyocto
#
# Python Script for bringing a custom rsyocto Linux 
# flavor to a bootable image file 
# 
#
#10-08-2019 (Vers. 1.4)
# Splash screen integration  
#
#11-08-2019 (Vers. 1.5)
# Support for multiple target Boards 
#
#14-08-2019 (Vers. 1.6)
# Importation of the Bootloader FPGA configuration (16-Bit parallel) to 
# the rootfs 
#
#15-08-2019 (Vers. 1.7)
# SSH Key authentication

#08-11-2019 (Vers. 1.8)
# Adding of support for Arria 10 SoC FPGAs 
#
#18-11-2019 (Vers. 1.9)
# Adding Device Tree Compilation with MAC integration 
#
#
#02-12-2019 (Vers. 2.0)
#  Github ready version
# 
#25-12-2019 (Vers. 2.01)
#  Auto remove of the hwrng 
#
#09-01-2019 (Vers. 2.02)
#  Overjump MAC-Address inserting if the dts file is not valid
#
#
#11-01-2020 (Vers. 2.03)
# Copying network interface settings to the rootfs
#
#16-01-2020 (Vers. 2.04)
#  Allows rootfs changes after the "my_.."-folders were created
#
#21-08-2020 (Vers. 3.00) 
#  Milestone version
#  Using the socfpgaGenerator and LinuxBootImageGenerator for generating 
#  all required components 
#
#02-09-2020 (Vers. 3.01)
#  Generation of a FPGA configuration file that can be written by Linux
#  Configuration of Linux with network interface file 
#
#
version = "3.01"


#
#
#
############################################ Const ###########################################
#
#
#

# SoC-FPGA Platform Generator Script Github
GIT_SOCFPGA_PLATFORMGEN_SCRIPT_URL   = "https://github.com/robseb/socfpgaPlatformGenerator.git"
GIT_SOCFPGA_PLATFORMGEN_NAME         = "socfpgaPlatformGenerator"

IMAGE_FOLDER_NAME         = 'Image_partitions'
# BOARD_ID = 1 -> DE10 Nano
# BOARD_ID = 2 -> DE10 Standard
# BOARD_ID = 3 -> HAN Pilot Arria 10 
# BOARD_ID = 4 -> DE0 Nano SoC
BOARD_ID =0

# SD-Folder Sub folder names
FOLDER_NAME_SOCFPGA = ['','SoCFPGA_CY5','SoCFPGA_CY5','SoCFPGA_A10','SoCFPGA_CY5']
FOLDER_NAME_BOARD   = ['','Board_DE10NANO','Board_DE10STD','Board_HAN','Board_DE0NANOSOC']                   

BOARD_NAME      = [' ','Terasic DE10 Nano','Terasic DE10 Standard', \
                    'Terasic HAN Pilot','Terasic DE0 Nano SoC']

BOARD_FPGA_NAME = ['unknown','Intel Cyclone V','Intel Cyclone V','Intel Arria 10 SX', \
                   'Intel Cyclone V']

DEVICE_ID_LIST = [0,0,0,2,0]

DEVICETREE_OUTPUT_NAME = ['','socfpga_cyclone5_socdk.dts','socfpga_cyclone5_socdk.dts', \
                        '','socfpga_cyclone5_socdk.dts']

BOARD_SUFIX_BOARD  = ['','_nano','_std','_han','_de0']
BOARD_SUFFIX_FPGA  = ['','_cy5','_cy5','_a10','_cy5']

MY_FOLDER_NAME       = ['my_rootdir','my_includes','my_homepage','my_startUpScripts']
MY_FOLDER_ROOTFS_DIR = ['home/root','usr/include','usr/share/apache2/default-site/htdocs', \
                        'etc/init.d']

BOARD_SUFFIX_NAME = ['_unknown','_D10NANO','_DE10STD','_HAN','_DE0']

CONF_XML_FILE_NAME = "rsyoctoConf.xml"

ROOLBACK_FPGACONF_DIR = '/usr/rsyocto/'
ROOLBACK_FPGACONF_NAME = 'running_bootloader_fpgaconfig.rbf'

NETWORKCONF_TMP_NAME = 'network_interface_temp_file.txt'

import os
import sys
from zipfile import ZipFile as zip
import math
import shutil
from datetime import datetime
from datetime import timedelta
import xml.etree.ElementTree as ET

#
#
#
############################################ Github clone function ###########################################
#
#
#

if sys.platform =='linux':
    try:
        import git
        from git import RemoteProgress
        import wget

    except ImportError as ex:
        print('Msg: '+str(ex))
        print('This Python Application requires "git" and "wget"')
        print('Use following pip command to install it:')
        print('$ pip3 install GitPython wget')
        sys.exit()
    

if sys.platform =='linux':
    # @brief to show process bar during github clone
    #
    #
    class CloneProgress(RemoteProgress):
        def update(self, op_code, cur_count, max_count=None, message=''):
            if message:
                sys.stdout.write("\033[F")
                print("    "+message)

######################################## Clone the boot image generator  #########################################
try:
    from socfpgaPlatformGenerator import SocfpgaPlatformGenerator
except ModuleNotFoundError as ex:
    print('--> Cloning "'+GIT_SOCFPGA_PLATFORMGEN_NAME+'" from GitHub')
    print('       please wait...')
    
    try:
        git.Repo.clone_from(GIT_SOCFPGA_PLATFORMGEN_SCRIPT_URL, \
            os.getcwd()+'/'+GIT_SOCFPGA_PLATFORMGEN_NAME, branch='master', progress=CloneProgress())
    except Exception as ex:
        print('ERROR: The cloning failed! Error Msg.:'+str(ex))
        sys.exit()

    if not os.path.isabs(os.getcwd()+'/'+GIT_SOCFPGA_PLATFORMGEN_NAME):
        print('ERROR: Failed to clone "'+GIT_SOCFPGA_PLATFORMGEN_NAME+'"')
        print('       Check your network connection and try it again')
        sys.exit()

    print('--> Copy the content of the cloned folder to the top folder')
    dir = os.getcwd()+'/'+GIT_SOCFPGA_PLATFORMGEN_NAME
    try:
        for file in os.listdir(dir):
            if os.path.isdir(dir +'/' +file) and \
                not os.path.isdir(os.getcwd()+'/'+file):
                shutil.copytree(dir +'/' +file,os.getcwd()+'/' +file)
            elif os.path.isfile(dir +'/' +file) and \
                not os.path.isfile(os.getcwd()+'/'+file):
                shutil.copyfile(dir +'/' +file,os.getcwd()+'/' +file)
        shutil.rmtree(dir)
    except Exception as ex:
        print('ERROR: Failed to copy files! Error Msg.:'+str(ex))
        sys.exit()
    
    
    from socfpgaPlatformGenerator  import SocfpgaPlatformGenerator


############################################                                ############################################
############################################             MAIN               ############################################
############################################                                ############################################

if __name__ == '__main__':
    print('\n##############################################################################')
    print('#                                                                            #')
    print('#    ########   ######     ##    ##  #######   ######  ########  #######     #')        
    print('#    ##     ## ##    ##     ##  ##  ##     ## ##    ##    ##    ##     ##    #')          
    print('#    ##     ## ##            ####   ##     ## ##          ##    ##     ##    #')    
    print('#    ########   ######        ##    ##     ## ##          ##    ##     ##    #')   
    print('#    ##   ##         ##       ##    ##     ## ##          ##    ##     ##    #')  
    print('#    ##    ##  ##    ##       ##    ##     ## ##    ##    ##    ##     ##    #')    
    print('#    ##     ##  ######        ##     #######   ######     ##     #######     #') 
    print('#                                                                            #')
    print("#       AUTOMATIC SCRIPT FOR BRINGING A CUSTOM RSYOCTO LINUX FLAVOR          #")
    print("#                         TO BOOTABLE IMAGE FILE                             #")
    print('#                                                                            #')
    print("#               by Robin Sebastian (https://github.com/robseb)               #")
    print('#                          Contact: git@robseb.de                            #')
    print("#                            Vers.: "+version+"                                     #")
    print('#                                                                            #')
    print('##############################################################################\n\n')


    ############################################ Runtime environment check ###########################################

    # Check proper Python Version
    if sys.version_info[0] < 3:
        print('ERROR: This script can not work with your Python Version!')
        print("Use Python 3.x for this script!")
        sys.exit()

    # Check that the Version runs on Linux
    if not sys.platform =='linux':
        print('ERROR: This script works only on Linux!')
        print("Please run this script on a Linux Computer!")
        sys.exit()

    if os.geteuid() == 0:
        print('ERROR: This script can not run with root privileges!')
        sys.exit()
    
    print('\n################################################################################')
    print('#                                                                              #')
    print('#                     SELECT YOUR DEVELOPMENT BOARD                            #')
    print('#                                                                              #')
    print('--------------------------------------------------------------------------------')
    print('#                    1 -> DE10 Nano                                            #')
    print('#                    2 -> DE10 Standard                                        #')
    print('#                    3 -> HAN Pilot Arria 10                                   #')
    print('#                    4 -> DE0 Nano SoC                                         #') 
    print('#                    Q: Abort                                                  #')
    print('------------------------------------------------------------------------------')

    while True:
        __wait__ = input('Type anything to continue ... ')

        if __wait__ =='q' or __wait__=='Q':
            sys.exit()

        try:
            BOARD_ID = int(__wait__)
        except Exception:
            pass
        
        if BOARD_ID > 0 and BOARD_ID < 5:
            break
        print('#                      Unknown input please try again!                       #')
        print('------------------------------------------------------------------------------')

    ######################################## Read the XML config file ##########################################
    print('\n---> Read the XML blueprint file ')
    try:
        tree = ET.parse(CONF_XML_FILE_NAME) 
        root = tree.getroot()
    except Exception as ex:
        print(' ERROR: Failed to parse "'+CONF_XML_FILE_NAME+'" file!')
        print(' Msg.: '+str(ex))
        sys.exit()
    
    # Load the partition table of XML script 
    print('---> Load the items of XML file ')
    folder_name =''
    mac_addrs=''
    yocto_build=''
    kernel_name=''
    description_txt=''

    # Read the distro items with the Yocto build date,...
    for part in root.iter('distro'):
        try:
            yocto_build = str(part.get('yocto_build'))
            kernel_name = str(part.get('kernel_name'))
            description_txt = str(part.get('description_txt'))
        except Exception as ex:
            print(' ERROR: XML File decoding failed!')
            print(' Msg.: '+str(ex))
            sys.exit()

    # Read the board items with the MAC-Address 
    for part in root.iter('board'):
        try:
            folder_name = str(part.get('folder_name'))
            mac_addrs = str(part.get('mac_addrs'))
        except Exception as ex:
            print(' ERROR: XML File decoding failed!')
            print(' Msg.: '+str(ex))
            sys.exit()

        if folder_name == FOLDER_NAME_BOARD[BOARD_ID]:
            print('     Used MAC-Address: '+mac_addrs)
            break

    if not folder_name == FOLDER_NAME_BOARD[BOARD_ID]:
        print('ERROR: It is no device with "folder_name="'+FOLDER_NAME_BOARD[BOARD_ID]+'"')
        print('        was not found inside the XML configuration file!')
        sys.exit()

    print ('This script will generate the image for the following Board: ' + str(BOARD_NAME[BOARD_ID]))

    
    #############  Input the name of the final image ###################

    print('\n################################################################################')
    print('#                                                                              #')
    print('#                     PLEASE INPUT A VERSION NUMBER                            #')
    print('#                         "rsyocto_X_XX.img"                                   #')
    print('--------------------------------------------------------------------------------')
    print('#                    D: Use a date code                                        #')
    print('#                    Q: Abort                                                  #')
    print('------------------------------------------------------------------------------')

    nb = input('Please input a version Number: rsYocto_')

    if nb =='q' or nb=='Q':
        sys.exit()

    if nb =='d' or nb=='D' or nb=='':
        # Add a datecode to the output file names
        now = datetime.now()
        nb = now.strftime("%Y%m%d_%H%M")

    image_name = 'rsYocto_'+str(nb)+BOARD_SUFFIX_NAME[BOARD_ID]+'.img'
    zip_name = 'rsYocto_'+str(nb)+BOARD_SUFFIX_NAME[BOARD_ID]+'.zip'

    print ('Name of the final image: "'+image_name+'"')
 
    ############################ Run the SoC-FPGA Platform Generator  ######################################

    # Read the execution environment 
    socfpgaGenerator = SocfpgaPlatformGenerator()

    # Check that the Quartus Prime project is compatible to the selected board
    proj_compet = True
    unlicensed_ip_found = False
    gen_boot =0
    if not DEVICE_ID_LIST[BOARD_ID] == socfpgaGenerator.Device_id:
        print('Soc: '+str(socfpgaGenerator.Device_id))
        print('********************************************************************************')
        print('*                     The used Quartus Prime project                           *')
        print('*                     is for a diffrent FPGA Device!                           *')
        print('*    Generation of a new bootloader and FPGA configuration are not possible!   *')
        print('********************************************************************************\n')
        _wait2__ = input('   Please type something to continue (q= Abort)...  ')
        if _wait2__ == 'q' or _wait2__ == 'Q':
            sys.exit()
        proj_compet = False
        gen_boot = 3

    if socfpgaGenerator.unlicensed_ip_found:
        print('********************************************************************************')
        print('*                     Unlicensed IP inside project found!                      *')
        print('*                  Generation of ".rbf" file is not possible!                  *')
        print('********************************************************************************\n')
        _wait2__ = input('   Please type something to continue (q= Abort)...  ')
        if _wait2__ == 'q' or _wait2__ == 'Q':
            sys.exit()
        unlicensed_ip_found = True


    # Create the partition table 
    if not socfpgaGenerator.GeneratePartitionTable():
        sys.exit()

    # Create the required bootloader

    if not socfpgaGenerator.BuildBootloader(gen_boot):
        sys.exit()

    ############################ Copy the depending Linux files to the partition folder #############################
    print('-> Copy the depending Linux files to the partition folder')
    ext = os.getcwd()+'/'
    ext_dir = socfpgaGenerator.Ext_folder_dir+'/'
    fpgaboot_conf_default_dir  =''
    fpgalinux_conf_default_dir =''

    #### Copy the zImage  #######
    print('   Copy the compressed "zImage" file')
    
    # 1. Look for the file inside the Board specific folder
    if os.path.isfile(ext + FOLDER_NAME_BOARD[BOARD_ID]+ '/' + \
                "zImage"+BOARD_SUFIX_BOARD[BOARD_ID]):
        print('     Name: "'+"zImage"+BOARD_SUFIX_BOARD[BOARD_ID]+'"')
        try:
            shutil.copyfile(ext + FOLDER_NAME_SOCFPGA[BOARD_ID]+ '/' + \
                "zImage"+BOARD_SUFIX_BOARD[BOARD_ID], \
                    socfpgaGenerator.Vfat_folder_dir+'/'+ \
                    "zImage")
        except Exception as ex:
            print('ERROR: Failed to copy file! MSG: '+str(ex))
            sys.exit()

    # 2. Look for the file inside the Device specific folder
    elif os.path.isfile(ext + FOLDER_NAME_SOCFPGA[BOARD_ID]+ '/' + \
                "zImage"+BOARD_SUFFIX_FPGA[BOARD_ID]):
        print('     Name: "'+"zImage"+BOARD_SUFFIX_FPGA[BOARD_ID]+'"')
        try:
            shutil.copyfile(ext + FOLDER_NAME_SOCFPGA[BOARD_ID]+ '/' + \
                "zImage"+BOARD_SUFFIX_FPGA[BOARD_ID], \
                    socfpgaGenerator.Vfat_folder_dir+'/'+ \
                    "zImage")
        except Exception as ex:
            print('ERROR: Failed to copy file! MSG: '+str(ex))
            sys.exit()
    else:
        print('ERROR: It is no zImage compressed Linux file available for the board/device')
        sys.exit()

    #### Find the FPGA configuration for u-boot configuration file   #######
    if not proj_compet or unlicensed_ip_found:
        print('   Looking for the default u-boot FPGA configuration file')
        
        # 1. Look for the file inside the Board specific folder
        if os.path.isfile(ext + FOLDER_NAME_BOARD[BOARD_ID]+ '/' + \
                    "socfpga"+BOARD_SUFIX_BOARD[BOARD_ID]+'.rbf'):
            fpgaboot_conf_default_dir= ext + FOLDER_NAME_BOARD[BOARD_ID]+ '/' + \
                    "socfpga"+BOARD_SUFIX_BOARD[BOARD_ID]+'.rbf'
            print('     Name: "'+fpgaboot_conf_default_dir+'.rbf"')
    
        # 2. Look for the file inside the Device specific folder
        elif os.path.isfile(ext + FOLDER_NAME_SOCFPGA[BOARD_ID]+ '/' + \
                    "socfpga"+BOARD_SUFFIX_FPGA[BOARD_ID]+'.rbf'):
            fpgaboot_conf_default_dir=ext + FOLDER_NAME_SOCFPGA[BOARD_ID]+ '/' + \
                    "socfpga"+BOARD_SUFFIX_FPGA[BOARD_ID]+'.rbf'
            print('     Name: "'+fpgaboot_conf_default_dir+'.rbf"')
          
        else:
            print('ERROR: It is no default u-boot FPGA configuration file (.rbf)'+\
                 'available for the board/device')
            sys.exit()
        
        #### Find the FPGA configuration for Linux configuration file   #######
        print('   Looking for the default Linux FPGA configuration file')
        
        # 1. Look for the file inside the Board specific folder
        if os.path.isfile(ext + FOLDER_NAME_BOARD[BOARD_ID]+ '/' + \
                    "socfpga"+BOARD_SUFIX_BOARD[BOARD_ID]+'.rbf'):
            fpgalinux_conf_default_dir= ext + FOLDER_NAME_BOARD[BOARD_ID]+ '/' + \
                    "socfpga_rollback"+BOARD_SUFIX_BOARD[BOARD_ID]+'.rbf'
            print('     Name: "'+fpgalinux_conf_default_dir+'.rbf"')
    
        # 2. Look for the file inside the Device specific folder
        elif os.path.isfile(ext + FOLDER_NAME_SOCFPGA[BOARD_ID]+ '/' + \
                    "socfpga_rollback"+BOARD_SUFFIX_FPGA[BOARD_ID]+'.rbf'):
            fpgalinux_conf_default_dir=ext + FOLDER_NAME_SOCFPGA[BOARD_ID]+ '/' + \
                    "socfpga_rollback"+BOARD_SUFFIX_FPGA[BOARD_ID]+'.rbf'
            print('     Name: "'+fpgalinux_conf_default_dir+'.rbf"')
          
        else:
            print('NOTE: It is no default Linux rollback FPGA configuration file (.rbf)'+\
                 'available for the board/device')

    #### Copy the rootfs.tar.gz  #######
    print('   Copy the compressed rootfs archive file')

    # 2. Look for the file inside the Board specific folder
    if os.path.isfile(ext + FOLDER_NAME_BOARD[BOARD_ID]+ '/rootfs' + \
                BOARD_SUFIX_BOARD[BOARD_ID]+'.tar.gz'):
        print('     Name: "rootfs'+BOARD_SUFIX_BOARD[BOARD_ID]+'.tar.gz"')
        try:
            shutil.copyfile(ext + FOLDER_NAME_SOCFPGA[BOARD_ID]+ '/rootfs' + \
                    BOARD_SUFIX_BOARD[BOARD_ID]+'.tar.gz',ext_dir+'/rootfs.tar.gz')
        except Exception as ex:
            print('ERROR: Failed to copy file! MSG: '+str(ex))
            sys.exit()
    # 2. Look for the file inside the Device specific folder
    elif os.path.isfile(ext + FOLDER_NAME_SOCFPGA[BOARD_ID]+ '/rootfs' + \
                BOARD_SUFFIX_FPGA[BOARD_ID]+'.tar.gz'):
        print('     Name: "rootfs'+BOARD_SUFFIX_FPGA[BOARD_ID]+'.tar.gz"')
        try:
            shutil.copyfile(ext + FOLDER_NAME_SOCFPGA[BOARD_ID]+ '/rootfs' + \
                 BOARD_SUFFIX_FPGA[BOARD_ID]+'.tar.gz',ext_dir+'/rootfs.tar.gz')
        except Exception as ex:
            print('ERROR: Failed to copy file! MSG: '+str(ex))
            sys.exit()
    else:
        print('ERROR: It is no compressed rootfs file available for the board/device')
        sys.exit()

    #### Copy the devicetree file   #######
    print('   Copy the devicetree file')

    # 1. Look for the file inside the Board specific folder
    if os.path.isfile(ext + FOLDER_NAME_BOARD[BOARD_ID]+ '/' + \
                "socfpga"+BOARD_SUFIX_BOARD[BOARD_ID]+'.dts'):
        print('     Name: "'+"socfpga"+BOARD_SUFIX_BOARD[BOARD_ID]+'.dts"')
        try:
            shutil.copyfile(ext + FOLDER_NAME_BOARD[BOARD_ID]+ '/' + \
                "socfpga"+BOARD_SUFIX_BOARD[BOARD_ID]+'.dts', \
                    socfpgaGenerator.Vfat_folder_dir+'/'+ \
                    DEVICETREE_OUTPUT_NAME[BOARD_ID])
        except Exception as ex:
            print('ERROR: Failed to copy file! MSG: '+str(ex))
            sys.exit()
    # 2. Look for the file inside the Device specific folder
    elif os.path.isfile(ext + FOLDER_NAME_SOCFPGA[BOARD_ID]+ '/' + \
                "socfpga"+BOARD_SUFFIX_FPGA[BOARD_ID]+'.dts'):
        print('     Name: "'+"socfpga"+BOARD_SUFFIX_FPGA[BOARD_ID]+'.dts"')
        try:
            shutil.copyfile(ext + FOLDER_NAME_SOCFPGA[BOARD_ID]+ '/' + \
                "socfpga"+BOARD_SUFFIX_FPGA[BOARD_ID]+'.dts', \
                    socfpgaGenerator.Vfat_folder_dir+'/'+ \
                    DEVICETREE_OUTPUT_NAME[BOARD_ID])
        except Exception as ex:
            print('ERROR: Failed to copy file! MSG: '+str(ex))
            sys.exit()
    else:
        print('ERROR: It is no devicetree file available for the board/device')
        sys.exit()

    ### Copy the network interface file   #######
    print('   Copy the network interface file to the exc folder')

    # 1. Look for the file inside the Board specific folder
    network_if_name = ''
    if os.path.isfile(ext + FOLDER_NAME_BOARD[BOARD_ID]+ '/' + \
                "network_interfaces"+BOARD_SUFIX_BOARD[BOARD_ID]+'.txt'):
        network_if_name= "network_interfaces"+BOARD_SUFIX_BOARD[BOARD_ID]+'.txt'
        print('     Name: "'+network_if_name+'"')
        try:
            shutil.copyfile(ext + FOLDER_NAME_BOARD[BOARD_ID]+ '/' + \
                "network_interfaces"+BOARD_SUFIX_BOARD[BOARD_ID]+'.txt', \
                    ext+NETWORKCONF_TMP_NAME)
                    
        except Exception as ex:
            print('ERROR: Failed to copy file! MSG: '+str(ex))
            sys.exit()
    # 2. Look for the file inside the Device specific folder
    elif os.path.isfile(ext + FOLDER_NAME_SOCFPGA[BOARD_ID]+ '/' + \
                "network_interfaces"+BOARD_SUFFIX_FPGA[BOARD_ID]+'.txt'):
        network_if_name= "network_interfaces"+BOARD_SUFFIX_FPGA[BOARD_ID]+'.txt'
        print('     Name: "'+network_if_name+'"')
        try:
            shutil.copyfile(ext + FOLDER_NAME_SOCFPGA[BOARD_ID]+ '/' + \
                "network_interfaces"+BOARD_SUFFIX_FPGA[BOARD_ID]+'.txt', \
                 ext+NETWORKCONF_TMP_NAME)
        except Exception as ex:
            print('ERROR: Failed to copy file! MSG: '+str(ex))
            sys.exit()
    else:
        print('NOTE: It is no network configuration file available for the board/device')
    print('     =Done\n')
        
    #################################  Add the MAC Address to the devicetree  #################################
    
    print("\n--> Open the Device Tree File to insert the new MAC-Address")
    f3=open( socfpgaGenerator.Vfat_folder_dir+'/'+ \
         DEVICETREE_OUTPUT_NAME[BOARD_ID],'r+') 
    dtsraw=''

    for x in f3.readlines():
        dtsraw= dtsraw+x

    if(BOARD_SUFFIX_FPGA[BOARD_ID]=='_a10'):
        # device tree file for Arria 10 SX
        ethstartPos = dtsraw.find('ethernet@ff800000 {')
    elif(BOARD_SUFFIX_FPGA[BOARD_ID]=='_cy5'):
        # device tree file for Cyclone V 
        ethstartPos = dtsraw.find('ethernet@ff702000 {')
    else:
        print('ERROR: The device tree change with the selected '+\
             'device is not supported')
        sys.exit()

    change_dts = True

    if not (ethstartPos > -1):
        print("WARNING: The DTS File is not in the right format\n")
        print("Changing the MAC-Address inside the Device Tree is not possible! ")
        change_dts= False

    if change_dts: 
        macstartPos =  dtsraw.find('mac-address = [',ethstartPos)
        if not (macstartPos > -1):
            print("ERROR: The DTS File is not in the right format (2)\n\n")
            print("Deleting of the local rootFs Folder")
            os.system("sudo rm -r rootfs")
            print('Program stops with error!')
            exit()
        
        macendPos =  dtsraw.find('];',macstartPos)
                
        if not (macstartPos > -1):
            print("ERROR: The DTS File is not in the right format (2)\n\n")
            print("Deleting of the local rootFs Folder")
            os.system("sudo rm -r rootfs")
            print('Program stops with error!')
            exit()

        # Convert the format "XX:XX:XX" to "XX XX XX" 
        # d6:7d:ae:b3:0e:ba
        mac_addrs_new =''
        replace = [':',':',':',':',':',':']

        for i in range(len(replace)):
            mac_addrs_new= mac_addrs.replace(':',' ',i)

        dtsrawNew = dtsraw[:macstartPos+15] +' '+mac_addrs_new+ dtsraw[macendPos:]
        
        f3.truncate(0) 
        f3.close()

        # Write the  MAC Address to the device tree file 
        with open(socfpgaGenerator.Vfat_folder_dir+'/'+ \
         DEVICETREE_OUTPUT_NAME[BOARD_ID], "a") as f3:
            f3.write(dtsrawNew)

        print('     = MAC-Address is included in the Device Tree \n')

     
    #########################################  Register partition files  #########################################
    if not socfpgaGenerator.CopyLinuxFiles2Partition(2):
        sys.exit()

    ###################################  Generate a FPGA boot configuration  #####################################
    # Generate the depending FPGA configuration file 
    #    specified inside the u-boot script
    if proj_compet or not unlicensed_ip_found:
        # Generate a new FPGA configuration for configuration during boot
        if not socfpgaGenerator.GenerateFPGAconf():
            sys.exit()
    else: 
        # Use the default FPGA configuration file
        print('NOTE: Only the default FPGA configuration file will be used!')
        if not socfpgaGenerator.GenerateFPGAconf(True,fpgaboot_conf_default_dir):
            sys.exit()

    ###################################  Generate a rollback FPGA configuration  #####################################
    # Generate the depending FPGA configuration file 

    if proj_compet or not unlicensed_ip_found:
        # Generate a new rollback FPGA configuration for configuration with Linux
        if not socfpgaGenerator.GenerateFPGAconf(boot_linux=True,\
                linux_filename=ROOLBACK_FPGACONF_NAME,\
                linux_copydir=ext):
            sys.exit()
    elif fpgalinux_conf_default_dir!='':
        # Is a default rollback FPGA configuration for configuration with Linux
        if not socfpgaGenerator.GenerateFPGAconf(True,fpgalinux_conf_default_dir,True,
                linux_filename=ROOLBACK_FPGACONF_NAME,\
                linux_copydir=ext):
                # socfpgaGenerator.Ext_folder_dir+'/'+ROOLBACK_FPGACONF_DIR):
            sys.exit()
    else:
        print('NOTE: No rollback FPGA configuration is used!')
        sys.exit()

    ############################## Unzip all available archive files such as the rootfs ##############################
    if not socfpgaGenerator.ScanUnpackagePartitions():
        sys.exit()
    print('--> The rootfs is now unzip and ready to insert files to it')

    ##########################################     Allow user changes      ##########################################
    
    print('\n#############################################################################')
    print('#               Copy files to the "my_folders" the content                   #')
    print('#            will then be copied to the depending rootfs location            #')
    print('#                                                                            #')
    print('#                                 ==========                                 #')
    print('#                                                                            #')
    print('#      Copy files to the partition folders to allow the pre-installment      #')
    print('#                    to the depending image partition                        #')
    print('#                                                                            #')
    print('#                     === Folders for every partition ===                    #')
    for part in socfpgaGenerator.PartitionList:
        print('# Folder: "'+IMAGE_FOLDER_NAME+'/'+part.giveWorkingFolderName(False)+'"| No.: '+ \
                                str(part.id)+' Filesystem: '+part.type+' Size: '+str(part.size_str))
    print('#                                                                            #')
    print('#        C: Compress the output image as .zip                                #')
    print('#        Q: Quit the script                                                  #')
    print('#        Any other input: Continue with the script                           #')
    print('#                                                                            #')
    print('##############################################################################')
    _wait_ = input('#              Please type ...                                               #\n')
    
    compress_output = False
    
    if _wait_ == 'q' or _wait_ == 'Q':
        sys.exit()
    elif _wait_ =='C' or _wait_ =='c':
        compress_output = True
    
    ################################################ ROOTFS Changes ################################################

    #############  Copy the content of the "my_folder"s to the rootfs  ###################
    print('\n--> Copy the content of the "my_folders" to the rootfs ')
    
    ext_dir = socfpgaGenerator.Ext_folder_dir
    if not os.path.isdir(ext_dir):
        print('ERROR: The unzip rootfs folder does not exist')
        sys.exit()

    for i in range(len(MY_FOLDER_NAME)):
        print('     Copy the content of the folder "'+MY_FOLDER_NAME[i]+'"')

        # 1. Look for the files inside the Device specific folder
        dir = ext + FOLDER_NAME_SOCFPGA[BOARD_ID]+ '/' + MY_FOLDER_NAME[i]
        if os.path.isdir(dir):
            if os.path.isdir(ext_dir+'/'+ MY_FOLDER_ROOTFS_DIR[i]):
                try:
                    os.system('sudo cp -r '+ext + FOLDER_NAME_SOCFPGA[BOARD_ID]+ '/' + \
                        MY_FOLDER_NAME[i]+'/. '+ext_dir+'/'+ MY_FOLDER_ROOTFS_DIR[i])
                except Exception as ex:
                    print('ERROR: Failed to copy files! Error Msg.:'+str(ex))
                    sys.exit()
            else: 
                print('WARNING: The folder "'+ext_dir+'/'+ MY_FOLDER_ROOTFS_DIR[i]+\
                    '" does not exist on the rootfs')
        else: 
            print('NOTE: The folder "'+ext + FOLDER_NAME_SOCFPGA[BOARD_ID]+ '/' + \
                    MY_FOLDER_NAME[i]+'" does not exist on the rootfs')

        # 2. Look for the file inside the Board specific folder
        dir = ext + FOLDER_NAME_BOARD[BOARD_ID]+ '/' + MY_FOLDER_NAME[i]
        if os.path.isdir(dir):
            if os.path.isdir(ext_dir+'/'+ MY_FOLDER_ROOTFS_DIR[i]):
                try:
                    os.system('sudo cp -r '+ext + FOLDER_NAME_SOCFPGA[BOARD_ID]+ '/' + \
                        MY_FOLDER_NAME[i]+'/. '+ext_dir+'/'+ MY_FOLDER_ROOTFS_DIR[i])
                except Exception as ex:
                    print('ERROR: Failed to copy files! Error Msg.:'+str(ex))
                    sys.exit()
            else: 
                print('WARNING: The folder "'+ext_dir+'/'+ MY_FOLDER_ROOTFS_DIR[i]+\
                    '" does not exist on the rootfs')
        else: 
            print('NOTE: The folder "'+ext + FOLDER_NAME_SOCFPGA[BOARD_ID]+ '/' + \
                    MY_FOLDER_NAME[i]+'" does not exist on the rootfs')
    print('     =Done')       

    ################################### Generate the rsyocto files        ###################################
    print('--> Generate the rsyocto info files and add them to the rootfs')
    
    # Create the "version.txt" inside the execution folder
    print('    Create the file "/usr/rsyocto/version.txt"')
    if os.path.isfile(ext+'/version.txt'):
        try:
            os.remove(ext+'/version.txt')
        except Exception:
            print('ERROR: Failed to delete "version.txt"')

    # Write the Version No. to the file
    with open(ext+'/version.txt', "a") as f:
        f.write(str(nb))    
    
    # Create the "version.txt" inside the execution folder
    print('    Create the file "/usr/rsyocto/suppBoard.txt"')
    if os.path.isfile(ext+'/suppBoard.txt'):
        try:
            os.remove(ext+'/suppBoard.txt')
        except Exception:
            print('ERROR: Failed to delete "suppBoard.txt"')

    # Write the Board name to the file
    with open(ext+'/suppBoard.txt', "a") as f:
        f.write(BOARD_NAME[BOARD_ID])  

    # Create the "device.txt" inside the execution folder
    print('    Create the file "/usr/rsyocto/device.txt"')
    if os.path.isfile(ext+'/device.txt'):
        try:
            os.remove(ext+'/device.txt')
        except Exception:
            print('ERROR: Failed to delete "device.txt"')

    # Write the SoC-FPGA name to the file
    with open(ext+'/device.txt', "a") as f:
        f.write(BOARD_FPGA_NAME[BOARD_ID])  

    # Create the "rsyocto" folder and copy the files to it
    print('    Copy these files to the rootfs')
    try:
        # Create the folder 
        if not os.path.isdir(ext_dir+'/usr/rsyocto'):
            os.system('sudo mkdir '+ext_dir+'/usr/rsyocto')
        if not os.path.isdir(ext_dir+'/usr/rsyocto'):
            print('ERROR: Failed to create the "rsyocto" folder!')
            sys.exit()

        # Copy the files to it
        os.system('sudo cp '+ext+'/device.txt'+' '+ext_dir+'/usr/rsyocto/device.txt')
        os.system('sudo cp '+ext+'/suppBoard.txt'+' '+ext_dir+'/usr/rsyocto/suppBoard.txt')
        os.system('sudo cp '+ext+'/version.txt'+' '+ext_dir+'/usr/rsyocto/version.txt')

        # Remove the files inside the execution folder
        os.system('sudo rm '+ext+'/device.txt')
        os.system('sudo rm '+ext+'/suppBoard.txt')
        os.system('sudo rm '+ext+'/version.txt')
    except Exception as ex:
        print('ERROR: Failed to copy files to the rootfs!')
        sys.exit()

    print('    = Done ')
    
   ####################################### Script based ROOTFS Changes #######################################
    
    ## Execute the python script "rootfsChange.py" to change the rootfs with root privileges
    if os.path.isfile(ext+'/rootfsChange.py'):
        print('--> Start the rootfs change script with sudo rights\n')
        try:
            os.system('sudo python3 '+ext+'/rootfsChange.py'+' -r '+ext_dir)
        except Exception as ex:
            print('ERROR: Failed execute the "rootfsChange.py" script! Msg.:'+str(ex))
            sys.exit()      
    else:
        print('ERROR:The "rootfsChange.py" file is not available! Msg.:'+str(ex))
        sys.exit()  

  
    ################### add the Bootloader FPGA Configuration to the rootfs ###################


    ################### Generate splash boot screen for the Board ###################
    ## Board Selection 
    print("--> Decoding the Board selection")
    now = datetime.now()
    path = os.getcwd()


    print("\n--> Generating the boot splash screen\n")
    if os.path.isfile(ext+'/issue'):
        try:
            os.remove(ext+'/issue')
        except Exception:
            print('ERROR: Failed to delete "issue"')

    with open(ext+'/issue', "a") as f:   
        f.write("\n")
        f.write("**********************************************************************************************************\n")             
        f.write("*                                                                                                        *\n")  
        f.write("*                     ########   ######     ##    ##  #######   ######  ########  #######                *\n")  
        f.write("*                     ##     ## ##    ##     ##  ##  ##     ## ##    ##    ##    ##     ##               *\n")  
        f.write("*                     ##     ## ##            ####   ##     ## ##          ##    ##     ##               *\n")  
        f.write("*                     ########   ######        ##    ##     ## ##          ##    ##     ##               *\n")  
        f.write("*                     ##   ##         ##       ##    ##     ## ##          ##    ##     ##               *\n")  
        f.write("*                     ##    ##  ##    ##       ##    ##     ## ##    ##    ##    ##     ##               *\n")  
        f.write("*                     ##     ##  ######        ##     #######   ######     ##     #######                *\n") 
        f.write("*                                                                                                        *\n")
        f.write("*                    --    Embedded Yocto based Linux System for Intel SoC-FPGAs          --             *\n")
        f.write("*                    ---        created by Robin Sebastian (github.com/robseb)           ---             *\n")
        f.write("*                    ---                   Contact: git@robseb.de                        ---             *\n")
        f.write("**********************************************************************************************************\n")   
        f.write("\n")
        f.write("-- Git Repository: https://github.com/robseb/rsyocto\n")
        f.write("-- VERSION:       "+str(nb)+"\n")
        f.write('-- KERNEL:        "'+kernel_name+'"\n')
        f.write('-- BUILD:         '+yocto_build+'\n')
        f.write("-- FPGA:          "+BOARD_FPGA_NAME[BOARD_ID]+"\n")
        f.write("-- BOARD:         "+BOARD_NAME[BOARD_ID]+"\n")
        f.write('-- IMAGE:         "'+image_name+'"') 
        f.write('--PACKING DATE:   '+str(now.strftime("%d.%m.%Y"))+"\n")
        f.write('--FOLDER NAME:    '+str(os.path.basename(path))+"\n")
        for x in description_txt:
            f.write(x)
        f.write("***********************************************************************************************************\n\n")   

    try:
        # Remove the files inside the execution folder
        os.system('sudo cp '+ext+'/issue'+' '+ext_dir+'/etc/issue')
        os.system('sudo rm '+ext+'/issue')
    except Exception as ex:
        print('ERROR: Failed to copy files to the rootfs!')
        sys.exit()


    ################################ Generate the bootable image file  ###################################
      
    # Generate with the files inside the partition folder a Image file
    # Use a date code as an output file
    if not socfpgaGenerator.GenerateImageFile(image_name,zip_name,compress_output,True):
        sys.exit()

        
############################################################ Goodby screen  ###################################################
    print('\n################################################################################')
    print('#                                                                              #')
    print('#                        GENERATION WAS SUCCESSFUL                             #')
    print('# -----------------------------------------------------------------------------#')
    print('#              Output file: "'+image_name+'" #')
    if compress_output:
        print('#              Compressed Output file: "'+image_name+'" #')
    print('#              Directory: "'+ext+'" #')                                                
    print('#                                                                              #')
    print('#                           SUPPORT THE AUTHOR                                 #')
    print('#                                                                              #')
    print('#                            ROBIN SEBASTIAN                                   #')
    print('#                     (https://github.com/robseb/)                             #')
    print('#                            git@robseb.de                                     #')
    print('#                                                                              #')
    print('#         rsyocto and socfpgaGenerator are projects, that I have fully         #')
    print('#        developed on my own. No companies are involved in these projects.     #')
    print('#        I am recently graduated as Master of Since of electronic engineering  #')
    print('#                Please support me for further development                     #')
    print('#                                                                              #')
    print('################################################################################')
# EOF
