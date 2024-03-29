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
#03-09-2020 (Vers. 3.02)
#  Fixed a bug with copying of the the "my folders"
#
# (2021-02-09) Vers. 3.10
#  Bug Fix with FPGA configuration generation with unlicensed IP
#    projects
#  New selection interface
#  Console input arguments to allow to use a Yocto Project Linux
#    Distribution or to auto generate the Linux Device Tree with  
#  First full supported version for Intel Arria 10 SX SoC-FPGA
#
# (2021-02-17) Vers. 3.11
#  Small bug with the ".zip" archive file output name
#
# (2021-04-12) Vers. 3.12
#  Changend output name to "rsyocto_"
# 

version = "3.11"

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
                          'socfpga_arria10_socdk_sdmmc.dts','socfpga_cyclone5_socdk.dts']

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
import re
from datetime import datetime
from datetime import timedelta
import xml.etree.ElementTree as ET
import argparse

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


#
# @brief Print a selection table that allows user to choose a item
# @param headline:        Main headline that will be displayed in the top of the box 
# @param headline_table:  Headline of the table (column names)
# @param raw1:            List of raw items of the column 1
# @param raw1:            List of raw items of the column 2 (optional)
# @param selectionMode:   Allow the user to select a item
# @param line_offset:     Offset of a raw line
# @return                 Selected item by the user (0 = Error)
#
def printSelectionTable(headline=[], headline_table=[], raw1=[], raw2=[],
        selectionMode=False,line_offset=10):

    singleRaw = True
    if len(raw1)==0 or len(headline_table)==0:
        return 0
    if raw2=='': 
        singleRaw = True
    elif not len(raw2)==0:
        singleRaw = False
    if not singleRaw and len(headline_table)<1:
        return 0

    # Find longest sting in raws
    max_raw_len =0
    for raw1_it in raw1:
        loc = len(raw1_it)
        if loc > max_raw_len:
            max_raw_len=loc

    for head_it in headline_table:
        loc = len(head_it)
        if loc > max_raw_len:
            max_raw_len=loc
    
    if not singleRaw:
        for raw2_it in raw2:
            loc = len(raw2_it)
            if loc > max_raw_len:
                max_raw_len=loc

    max_raw_len+=line_offset

    ### Print the top of the box
    total_raw_len = max_raw_len
    if not singleRaw:
        total_raw_len *=2
    total_raw_len+=10
    filling='#'
    print(' ')
    for i in range(total_raw_len):
        sys.stdout.write('#')
    for i in range(total_raw_len-2):
        filling+=' '
    filling+='#'
    line_sep = filling.replace(' ','-')
    print('')

    ### Print the headline 
    if len(headline)>0:
        for lin in headline:
            lin2 =''
            lin1 =''
            if(len(lin)>total_raw_len-5):
                lin1=lin[:total_raw_len-5]
                lin2 = lin[total_raw_len-5:]
            else:
                lin1 = lin
            print('# '+lin1.center(total_raw_len-3)+'#')
            if lin2!='':
                print('# '+lin2.center(total_raw_len-3)+'#')
    print(filling)
    print(line_sep)
    ### Print the table headline 
    sys.stdout.write('#  '+' No. '+' '.center(3)+'|')

    sys.stdout.write(headline_table[0].center(max_raw_len-(3 if singleRaw else 2)))
    if not singleRaw:
        sys.stdout.write('|'+headline_table[1].center(max_raw_len-2)+'#')
    else:
        sys.stdout.write('#')
    print('')

    # Print a line seperator
    line_sep = filling.replace(' ','-')
    print(line_sep)

    ### Print the content to the raws 
    # Find the number of iteams
    no_it = len(raw1)
    if not singleRaw and len(raw2) > no_it:
        no_it = len(raw2)
    
    # for loop for every raw
    for i in range(no_it):
        sys.stdout.write('# '+str(i+1).center(9)+'|')
        if len(raw1)>=i:
            item_len = len(raw1[i])+(3 if not singleRaw else 4)
            sys.stdout.write(' '+raw1[i]+''.center(max_raw_len-item_len))
            sys.stdout.write('|' if not singleRaw else '#')
        else:
            sys.stdout.write(''.center(max_raw_len-2)+'|')
        if not singleRaw:
            if   len(raw2)>=i:
                item_len = len(raw2[i])+3
                sys.stdout.write(' '+raw2[i]+' '.center(max_raw_len-item_len)+'#')
            else:
                sys.stdout.write(''.center(max_raw_len-2)+'#')
        print('')
    print(line_sep)
    
    # Print the selection interface
    inp_val =0
    if selectionMode:
        st = '#   Select a item by typing a number (1-'+str(no_it)+') [q=Abort]'
        sys.stdout.write(st+' '.center(total_raw_len-len(st)-1)+'#')
        print('')
        while True:
            inp = input('#  Please input a number: $')

            try:
                inp_val = int(inp)
            except Exception:
                pass

            if inp=='Q' or inp=='q':
                print(' Aborting...')
                sys.exit()
            elif inp_val>0 and inp_val <(no_it+1):
                st='# Your Selection: '+str(inp_val)
                if len(raw1)>=inp_val-1:
                    st='# Your Selection: '+str(inp_val)+'" : "'+raw1[inp_val-1]+'"'
                elif len(raw2)>=inp_val-1:
                    st='# Your Selection: '+str(inp_val)+'" : "'+raw2[inp_val-1]+'"'
                sys.stdout.write(st+' '.center(total_raw_len-len(st)-1)+'#')
                print('')
                break
            else:
                st='# Wrong Input! Please try it agin!'
                sys.stdout.write(st+' '.center(total_raw_len-len(st)-1)+'#')
                print('')
    ### Print the bottom of the box
    print(filling)
    for i in range(total_raw_len):
        sys.stdout.write('#')
    print('\n')

    if selectionMode:
        return inp_val
    
    return 1        

#
# @brief prase input arguments to enable to special modes 
#
def praseInputArgs():
    ### Progress the user arguments 
    arg_use_yocto_project           = False 
    arg_use_devicetree_gen          = 0

    # Was the script started with a additional argument specified?
    if len(sys.argv)>1:
        # Select the posibile input arguments 
        parser = argparse.ArgumentParser()
        parser.add_argument('-y','--yocto_linux', required=False, help='Use the Yocto Project zImage,rootfs files ["-y 1"]')
        parser.add_argument('-g','--devicetree_gen', required=False, help='Use SoC EDS DeviceTree Generator '+\
                            '["-g 1 --> no GUI | 2 --> GUI"]')

        args = parser.parse_args()

        # Was use Project Linux Distribution selected 
        if args.yocto_linux != None:
            try: tmp = int(args.yocto_linux)
            except Exception:
                print('ERROR: Failed to convert the [--yocto_linux/-y] input argument!')
                print('       Only integer numbers allowed!')
                sys.exit()
            if tmp>0: arg_use_yocto_project=True
        # Was use SoC EDS DeviceTree Generator selected 
        if args.devicetree_gen != None:
            try: tmp = int(args.devicetree_gen)
            except Exception:
                print('ERROR: Failed to convert the [--devicetree_gen/-g] input argument!')
                print('       Only integer numbers allowed!')
                sys.exit()
            if tmp>0 and tmp<3: arg_use_devicetree_gen=tmp
      
    return arg_use_yocto_project, arg_use_devicetree_gen


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
    
    # Enable and read input arguments 
    arg_use_yocto_project,arg_use_devicetree_gen = praseInputArgs()

    headline = ['SELECT YOUR DEVELOPMENT BOARD']
    headline_table=['Board Name']
    headline_content= BOARD_NAME.copy()
    headline_content.remove(' ')
    BOARD_ID = printSelectionTable(headline,headline_table,headline_content,[],True,47)

    if BOARD_ID > len(FOLDER_NAME_BOARD):
        print('ERROR: The selected board number is outsite of the "FOLDER_NAME_BOARD" list!')
        sys.exit()

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

     # Convert new lines commands 
    description_txt = description_txt.replace('\\n','\r\n',1000)
    
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

    nb = input('Please input a version Number: rsyocto_')

    if nb =='q' or nb=='Q':
        sys.exit()

    if nb =='d' or nb=='D' or nb=='':
        # Add a datecode to the output file names
        now = datetime.now()
        nb = now.strftime("%Y%m%d_%H%M")

    if not re.match("^[a-z0-9_.]+$", nb, re.I):
        print('ERROR: The selected output file with the name:"rsyocto_'+nb+'"')
        print('        has caracters witch are not allowed!')
        sys.exit()

    image_name = 'rsyocto_'+str(nb)+BOARD_SUFFIX_NAME[BOARD_ID]+'.img'
    zip_name = 'rsyocto_'+str(nb)+BOARD_SUFFIX_NAME[BOARD_ID]+'.zip'

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
        sys.exit()
        proj_compet = False
        gen_boot = 3

    if socfpgaGenerator.unlicensed_ip_found:
        print('********************************************************************************')
        print('*                     Unlicensed IP inside project found!                      *')
        print('*                  Generation of ".rbf" file is not possible!                  *')
        print('* You can still generate a bootable image by using a exiting FPGA conf. file.  *')
        print('********************************************************************************\n')
        _wait2__ = input('   Please type something to continue (q= Abort)...  ')
        if _wait2__ == 'q' or _wait2__ == 'Q':
            sys.exit()
        unlicensed_ip_found = True

    ############################ Run the SoC-FPGA Platform Generator  ######################################
    ext = os.getcwd()+'/'
    if arg_use_devicetree_gen >0:
        # if selected:
        if not (socfpgaGenerator.RunDeviceTreeGenerator(ext + FOLDER_NAME_BOARD[BOARD_ID], \
            'socfpga'+BOARD_SUFIX_BOARD[BOARD_ID]+'_reference.dts',arg_use_devicetree_gen==2)):
            print('ERROR: Failed to run the SoC-EDS DeviceTree Generator!')
        else: 
            print('--> A new DeviceTree for reference was generated!')
            print(' Dir: "'+ext + FOLDER_NAME_BOARD[BOARD_ID]+'/'+\
                'socfpga'+BOARD_SUFIX_BOARD[BOARD_ID]+'_reference.dts"')
        print(' End of script...')
        sys.exit()

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
    print('     =Done')
        
    #################################  Add the MAC Address to the devicetree  #################################
    
    print("--> Open the Device Tree File to insert the new MAC-Address")
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
    if not socfpgaGenerator.CopyLinuxFiles2Partition(0 if arg_use_yocto_project else 2 ):
        sys.exit()

    ###################################  Generate a FPGA boot configuration  #####################################
    # Generate the depending FPGA configuration file 
    #    specified inside the u-boot script
    if proj_compet and not unlicensed_ip_found:
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

    if proj_compet and not unlicensed_ip_found:
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
    
    headline = [' Copy files to the "my_folders" the content',\
        'These files will then be copied to the depending rootfs location','==========', \
        'Copy files to the partition folders to allow the pre-installment',\
        'to the depending image partition','Folders for every partition:']
    headline_table=['(ID) Folder Name','Filesystem | Size ']
    content1=[]
    content2=[]
    for part in socfpgaGenerator.PartitionList:
        content1.append('('+str(part.id)+') '+IMAGE_FOLDER_NAME+'/'+part.giveWorkingFolderName(False))
        content2.append(part.type+' | '+str(part.size_str))

    printSelectionTable(headline,headline_table,content1,content2,False,10)

    headline = [' Compress the output image file as ".zip"',\
            'A zip files reduces the image file size by removing the offsets.',\
            'Commen boot disk generation tools can directly work with these files.']
    headline_table=['Task']
    content1=['Compress the output image as ".zip"','Use only a regular ".img" file']

    comprsSel= printSelectionTable(headline,headline_table,content1,[],True,32)
    compress_output = False
    if comprsSel==1:compress_output = True
    
    ################################################ ROOTFS Changes ################################################

    #############  Copy the content of the "my_folder"s to the rootfs  ###################
    print('--> Copy the content of the "my_folders" to the rootfs ')
    
    ext_dir = socfpgaGenerator.Ext_folder_dir
    if not os.path.isdir(ext_dir):
        print('ERROR: The unzip rootfs folder does not exist')
        sys.exit()

    for i in range(len(MY_FOLDER_NAME)):
        print('     Copy the content of the folder "'+MY_FOLDER_NAME[i]+'"')

        # 1. Look for the file inside the Board specific folder
        dir = ext + FOLDER_NAME_BOARD[BOARD_ID]
        if os.path.isdir(dir):
            if os.path.isdir(ext_dir+'/'+ MY_FOLDER_ROOTFS_DIR[i]):
                try:
                    os.system('sudo cp -rv '+dir+ '/' + \
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

        # 2. Look for the files inside the Device specific folder
        dir = ext + FOLDER_NAME_SOCFPGA[BOARD_ID]
        if os.path.isdir(dir):
            if os.path.isdir(ext_dir+'/'+ MY_FOLDER_ROOTFS_DIR[i]):
                try:
                    os.system('sudo cp -rv '+dir+ '/' + \
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
        print('--> Start the rootfs change script with sudo rights')
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


    print("--> Generating the boot splash screen")
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
        f.write("*                    --    Embedded Yocto based Linux Distro for Intel SoC-FPGAs          --             *\n")
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
        f.write('-- IMAGE:         "'+image_name+'"\n') 
        f.write('-- PACKING DATE:  '+str(now.strftime("%d.%m.%Y"))+"\n")
        f.write('-- FPGA PROJECT:  "'+socfpgaGenerator.Qpf_file_name+'"\n') 
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
    # Use a date code as an output file or the user chosen file name 
    if not socfpgaGenerator.GenerateImageFile(image_name,zip_name,compress_output,True):
        print('  Try to remove the "Image_partitions" folder and try it again!')
        sys.exit()

        
############################################################ Goodby screen  ###################################################

    headline = [' GENERATION WAS SUCCESSFUL','------------------------------------------------',\
                'SUPPORT THE AUTHOR','------------------------------------------------',
                'ROBIN SEBASTIAN','(https://github.com/robseb/)','git@robseb.de',' ',\
                'rsyocto and socfpgaGenerator are projects, that I have fully on my own.',
                'No companies are involved in these projects.','I am recently graduated as Master of Since of electronic engineering',\
                'Please support me for further development']
    headline_table=['Output']
    content1=['           Output file: "'+image_name+'"']
    if compress_output:
        content1.append('Compressed Output file: "'+zip_name+'"')
    content1.append('             Directory: "'+ext+'"')

    printSelectionTable(headline,headline_table,content1,[],False,32)
# EOF
