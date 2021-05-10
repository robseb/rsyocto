#!/usr/bin/env python3.7
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
#                                                 |__/                              
#
#
# Robin Sebastian (https://github.com/robseb)
# Contact: git@robseb.de
# Repository: https://github.com/robseb/rsyocto
#
# Python Script to generate FPGA-Configuration files for the Linux and bootloader FPGA Configuration 
# and to copy these file to the depending positions on rsyocto
#
# (2021-04-25) Vers.1.0 
#   first Version 
#
# (2021-04-26) Vers.1.01 
#   fixing a issue with detection of the Intel Quartus Prime FPGA compile mode 
#
# (2021-05-05) Vers.1.10
#   fixing a issue with unlicensed IP during FPGA project compilation 
#   fixing a issue with multiple .sof FPGA files in a project
#   adding the JTAG mode to enable the writing of 
#       unlicensed IP/regular FPGA-Configuration via JTAG 
#
# (2021-05-09) Vers.1.101
#   fixing a ERROR that during a JTAG Connection occurred 
#   new FPGA IP test mode (JTAG) by generating and executing a shell script 
#
# (2021-05-09) Vers.1.102
#   remove .cdf file after shell script executing
#
# (2021-05-09) Vers.1.103
#   JTAG support for Linux
#   removing the second terminal window for the FPGA IP Evaluation Mode
#
# (2021-05-09) Vers.1.104
#   small bug fixes with JTAG mode 
#
# (2021-05-09) Vers.1.105
#   JTAG mode support for regular FPGAs without HPS (Hard Processor System)
#
version = "1.105"

#
#
#
############################################ Const ###########################################
#
#
#

DELAY_MS = 1 # Delay after critical tasks in milliseconds 

QURTUS_DEF_FOLDER_LITE    = "intelFPGA_lite"
QURTUS_DEF_FOLDER         = "intelFPGA"
QURTUS_DEF_FOLDER_PRO     = "intelFPGA_pro"
EDS_EMBSHELL_DIR          = ["/embedded/embedded_command_shell.sh","\\embedded\\embedded_command_shell.bat"]
QUARTUS_CMDSHELL_EXE      = ['quartus_sh','quartus_sh.exe']

#
# @brief default XML settings file name 
#
FLASHFPGA_SETTINGS_XML_FILE_NAME = 'confFlashFPGA2rsyocto.xml'

#
# @brief default XML settings file
#
FLASHFPGA_SETTINGS_XML_FILE ='<?xml version="1.0" encoding = "UTF-8" ?>\n'+\
    '<!-- Used by the Python script "flashFPGA2rsyocto.py" -->\n'+\
    '<!-- to store the settings of the used development board -->\n'+\
    '<!-- Description: -->\n'+\
    '<!-- item "board"  The Settings for the baord (Only one item allowed) -->\n'+\
    '<!-- L "set_ip"        => The IPv4 Address of the board -->\n'+\
    '<!-- L "set_user"      => The Linux User name of the board  -->\n'+\
    '<!-- L "set_password"  => The Linux User password of the board  -->\n'+\
    '<!-- L "set_flashBoot" => Enable or Disable of the writing of the u-boot bootloader FPGA-Configuration file -->\n'+\
    '<!--    L "Y"  => Enable | "N" => Disable  -->\n'+\
    '<!-- set_quartus_prime_ver Intel Quartus Prime Version to use <Version><Version No> -->\n'+\
    '<!--    L -> Quartus Prime Lite      (e.g. L16.1)  -->\n'+\
    '<!--    S -> Quartus Prime Standard  (e.g. S18.1)  -->\n'+\
    '<!--    P -> Quartus Prime Pro       (e.g. P20.1)  --> \n'+\
    '<FlashFPGA2Linux>\n'+\
    '   <board set_ip="192.168.0.165" set_user="root" set_pw="eit" set_flashBoot="Y" set_quartus_prime_ver="L20.1" />\n'+\
    '</FlashFPGA2Linux>\n'
    
RSYOCTO_BANNER_CHECK_LINE =  ['created by Robin Sebastian (github.com/robseb)', \
                              'Contact: git@robseb.de', \
                              'https://github.com/robseb/rsyocto'\
                             ]
RSYOCTO_FPGAWRITECONF_CHECK = 'Command to change the FPGA fabric configuration'


RSYOCTO_TEMPCOPYFOLDER      = '.flashFPGA2rsyocto'
#
#
#
############################################ Github clone function ###########################################
#
#
#
import sys
try:
    import paramiko
except ImportError as ex:
    print('Msg: '+str(ex))
    print('This Python Script uses "paramiko"')
    print('to enable SSH access to SoC-FPGA board')
    print('Use following pip command to install it:')
    print('$ pip3 install paramiko')
    sys.exit()

import os, platform, io, warnings
import time, math
from datetime import datetime
import shutil
import re
from threading import Thread
import subprocess, queue
from subprocess import DEVNULL
import xml.etree.ElementTree as ET
import glob
from pathlib import Path
import argparse

    
# 
# @brief Class for automatization the entry FPGA configuration generation process 
#        and to write the FPGA-Configuration via SSH
#   
class FlashFPGA2Linux(Thread):

    ## Intel Quartus Prime and Intel SoC-EDS related properties 

    EDS_Folder_dir              : str # Directory of the Intel EDS folder
    Quartus_proj_top_dir        : str # Directory of the Quartus Project folder 
    
    Qpf_file_name               : str # Name of the Quartus Project ".qpf"-file
    Sof_file_name               : str # Name of the Quartus Project ".sof"-file
    sopcinfo_file_name          : str # Name of the Quartus Project ".sopcinfo"-file
    Qsys_file_name              : str # Name of the Quartus Project ".qsys"-file
    Handoff_folder_name         : str # Name of the Quartus Project Hand-off folder
    UbootSFP_default_preBuild_dir : str # Directory of the pre-build u-boot for the device 
    Sof_folder                  : str # Name of the Quartus Project folder containing the ".sof"-file 
    U_boot_socfpga_dir          : str # Directory of u-boot SoC-FPGA folder 
    Uboot_default_file_dir      : str # Directory of the pre-build default u-boot file 

    ## SoC-FPGA Development board and rsyocto related properties

    Device_id                   : int # SocFPGA ID (0: Cyclone V; 1: Arria V;2: Arria 10)
    Device_name                 = ['Intel Cyclone V','Intel Arria V','Intel Arria 10']
    unlicensed_ip_found         : bool# Quartus project contains an unlicensed IP (e.g. NIOS II Core) 
    regular_fpga_project        : bool # FPGA Project type: True: regular FPGA | False: SoC-FPGA 
    board_ip_addrs              : ''  # IPv4 Address of the SoC-FPGA Linux Distribution (rsyocto)
    board_user                  : ''  # SoC-FPGA Linux Distribution (rsyocto) Linux user name
    board_pw                    : ''  # SoC-FPGA Linux Distribution (rsyocto) Linux user password
    use_jtag                    : False  # Use JTAG to write the FPGA-Configuration
    __temp_folder_dir           : ''  # Directory of the Temp folder on rsyocto 
    __temp_partfolder_dir       : ''  # Directory of the Temp partition folder 

    
    #
    # @brief Directories to Intel FPGA shells
    #
    shell_quartus_dir                 : str # Directory of the Intel Quartus Prime command shell

    ## Network related properties

    __sshClient                 : paramiko # Object of the SSH client connection to the baord 
    __sftpClient                : paramiko # Object of the SFTP client connection to the board

    __queue                     : queue.Queue # Queue of the SSH Thread

    __SPLM = ['/','\\']               # Slash for Linux, Windows 
    __SPno = 0                        # OS ID 0=Linux | 1=Windows 

    ThreadStatus                  : False # Was the SSH Thread executed successfully?

    #
    # @brief Constructor
    # @param board_ip_addrs     IPv4 Address of the SoC-FPGA Linux Distribution (rsyocto)
    #                           Format 100.100.100.100
    # @param board_user         SoC-FPGA Linux Distribution (rsyocto) Linux user name
    # @param board_pw           SoC-FPGA Linux Distribution (rsyocto) Linux user password
    # @prarm compile_project    Before writing FPGA-Configuration compile the Intel Quartus 
    #                           Prime FPGA project  
    # @param QuartusForceVersion    Quartus Prime Version to use <Version><Version No>
    #                               L -> Quartus Prime Lite      (e.g. L16.1)
    #                               S -> Quartus Prime Standard  (e.g. S18.1)
    #                               P -> Quartus Prime Pro       (e.g. P20.1)
    # @param use_jtag          Use JATG for writing the FPGA-Configuration
    #
    def __init__(self,board_ip_addrs, board_user,board_pw,compile_project,QuartusForceVersion, use_jtag):
        
        # Read the input paramters 
        regex_pattern = "^([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$"
        if not bool( re.match( regex_pattern, board_ip_addrs)):
            print('[ERROR] The given IP Address is not in the proper format (0.0.0.0)')
            sys.exit()

        self.board_ip_addrs = board_ip_addrs
        self.board_user     = board_user
        self.board_pw       = board_pw
        self.use_jtag       = use_jtag
        self.ThreadStatus   = False
        
        ######################################### Find the Intel EDS Installation Path ####################################

        if sys.platform =='linux':
            EDS_Folder_def_suf_dir = os.path.join(os.path.join(os.path.expanduser('~'))) + '/'
            self.__SPno = 0
        else: 
            EDS_Folder_def_suf_dir = 'C:\\' 
            self.__SPno = 1

        # 1.Step: Find the EDS installation path
        quartus_standard_ver = False
        # Loop to detect the case that the free Version of SoC EDS (EDS Standard [Folder:intelFPGA]) and 
        #    the free Version of Quartus Prime (Quartus Lite [Folder:intelFPGA_lite]) are installed together 
        while(True):
            if (os.path.exists(EDS_Folder_def_suf_dir+QURTUS_DEF_FOLDER)) and (not quartus_standard_ver):
                self.EDS_Folder=EDS_Folder_def_suf_dir+QURTUS_DEF_FOLDER
                quartus_standard_ver = True
            elif(os.path.exists(EDS_Folder_def_suf_dir+QURTUS_DEF_FOLDER_LITE)):
                self.EDS_Folder=EDS_Folder_def_suf_dir+QURTUS_DEF_FOLDER_LITE
                quartus_standard_ver = False
            else:
                print('[ERROR]  No Intel SoC EDS Installation Folder was found!')
                sys.exit()

            # 2.Step: Find the latest Intel SoC EDS Version No.
            avlVer = []
            for name in os.listdir(self.EDS_Folder):
                if  os.path.abspath(name):
                    try:
                        avlVer.append(float(name))
                    except Exception:
                        pass

            if (len(avlVer)==0):
                print('[ERROR]  No valid Intel SoC EDS Version was found')
                sys.exit()

            avlVer.sort(reverse = True) 

            highestVer = avlVer[0]
            self.EDS_Folder = self.EDS_Folder +self.__SPLM[self.__SPno]+ str(highestVer)   

            if (not(os.path.realpath(self.EDS_Folder))):
                print('[ERROR]  No valid Intel EDS Installation Folder was found!')
                sys.exit()

            if(highestVer < 18): 
                print('[ERROR]  This script is designed for Intel SoC-EDS Version 18+ (18.1,19.1, 20.1, ...) ')
                print('          You using Version '+str(highestVer)+' please update Intel EDS!')
                sys.exit()
            elif(highestVer > 20.1):
                print('[WARNING] This script was designed for Intel EDS Version 19.1 and 20.1')
                print('          Your version is newer. Errors may occur!')

            # Check if the SOC-EDS Command Shell is available 
            if((not(os.path.isfile(self.EDS_Folder+EDS_EMBSHELL_DIR[self.__SPno])) )):
                if( not quartus_standard_ver):
                    print('[ERROR]  Intel SoC EDS Embedded Command Shell was not found!')
                    sys.exit()
            else:
                break

        ############################### Check that the script runs inside the Quartus project ###############################

        self.Quartus_proj_top_dir =os.getcwd()
        excpath = os.getcwd()
      

        # Find the Quartus project (.qpf) file 
        self.Qpf_file_name = ''
        for file in os.listdir(self.Quartus_proj_top_dir):
            if ".qpf" in file:
                self.Qpf_file_name =file
                break
        self.sopcinfo_file_name = ''
        for file in os.listdir(self.Quartus_proj_top_dir):
            if ".sopcinfo" in file:
                self.sopcinfo_file_name =file
                break

        # Find the Quartus  (.sof) (SRAM Object) file 
        self.Sof_file_name = ''
        Sof_file_name_list =[]

        self.Sof_folder = ''
        # Looking in the top folder for the sof file
        # Sort the file by the modification date (latest date --> first)
        files = [s for s in os.listdir(self.Quartus_proj_top_dir)
            if os.path.isfile(os.path.join(self.Quartus_proj_top_dir, s))]
        files.sort(key=lambda s: os.path.getmtime(\
            os.path.join(self.Quartus_proj_top_dir, s)),reverse=True)

        for file in files:
            if ".sof" in file:
                Sof_file_name_list.append(file)

        if len(Sof_file_name_list)==0:
            # Looking inside the "output_files" and "output" folders
            if os.path.isdir(self.Quartus_proj_top_dir+'/output_files'):
                self.Sof_folder ='output_files'
            if os.path.isdir(self.Quartus_proj_top_dir+'/output'):
                self.Sof_folder = 'output'
            
            # Sort the file by the modification date (latest date --> first)
            files = [s for s in os.listdir(self.Quartus_proj_top_dir+\
                    self.__SPLM[self.__SPno]+self.Sof_folder)
                if os.path.isfile(os.path.join(self.Quartus_proj_top_dir+\
                    self.__SPLM[self.__SPno]+self.Sof_folder, s))]
            files.sort(key=lambda s: os.path.getmtime(\
                os.path.join(self.Quartus_proj_top_dir+self.__SPLM[self.__SPno]+\
                    self.Sof_folder, s)),reverse=True)

            for file in files:
                if ".sof" in file:
                    Sof_file_name_list.append(file)
            
        # Use the latest SOF file available inside the Quartus Prime Project
        self.Sof_file_name==''
        if len(Sof_file_name_list)>0:
            self.Sof_file_name=Sof_file_name_list[0]

        # Check if the file is older then 10min --> raise a warning! 
        current_time =  datetime.now().timestamp()
        modification_time = os.path.getmtime(self.Quartus_proj_top_dir+\
                self.__SPLM[self.__SPno]+self.Sof_folder+\
                self.__SPLM[self.__SPno]+self.Sof_file_name) 
        if modification_time+ 10*60 < current_time:
            mod= datetime.fromtimestamp(modification_time).strftime('%d-%m-%Y %H:%M')
            print('[WARNING] The used output file "'+self.Sof_folder+\
                self.__SPLM[self.__SPno]+self.Sof_file_name+\
                '" is older then 10 min!  Modification Date: '+mod)


        # Find the Platform Designer (.qsys) file  
        self.Qsys_file_name = ''
        for file in os.listdir(self.Quartus_proj_top_dir):
                if ".qsys" in file and not ".qsys_edit" in file:
                    self.Qsys_file_name =file
                    break
        device_name_temp =''
        # Does the SOF file contains an IP with a test licence, such as a NIOS II Core?
        self.unlicensed_ip_found=False
        if self.Sof_file_name.find("_time_limited")!=-1:
            if self.use_jtag==False:
                # Use the network for writting the FPGA-Configuration
                print('********************************************************************************')
                print('*               Unlicensed IP inside the FPGA project was found!               *')
                print('*            Generation of the ".rbf"- FPGA-Configuration is not enabled       *')
                print('*     --> It is not allowed to generate a static FPGA-Configuration file       *')
                print('********************************************************************************')
                print('*                                                                              *')
                print('*       Use the argument "-j 1" to write the FPGA-Configuration via JTAG       *')
                print('*                                                                              *')
                print('********************************************************************************')
                sys.exit()
            else: 
                # Use JTAG
                print('[WARNING] The FPGA project contains unlicensed IP. Only JTAG RAM writing allowed!')
            self.unlicensed_ip_found=True

        # Find the Platform Designer folder
        if self.Qsys_file_name=='' or self.Qpf_file_name=='':
            print('[ERROR] The script was not executed inside the Intel Quartus Prime project folder!')
            print('        Please copy it into the top-project folder of a Intel Quartus Prime FPGA project')
            print('        --- Required folder structure  ---')
            print('        YOUR_QURTUS_PROJECT_FOLDER ')
            print('        |     L-- PLATFORM_DESIGNER_FOLDER')
            print('        |     L-- platform_designer.qsys')
            print('        |     L-- _handoff')
            print('        |     L-- quartus_project.qpf')
            print('        |     L-- flashFPGA2rsyocto.py   <<<<<<<<=====')
            print('        Note: File names can be chosen freely\n')
            sys.exit()
        
        if self.Sof_file_name=='' and not compile_project:
            print('[ERROR] The linked Intel Quartus Prime FPGA Project was not compiled!')
            print('        For FPGA-Configuration file generation is this necessary!')
            print('        Use the argument "-cf 1" to compile this FPGA project')
            print('        and then to write the FPGA-Configuration with rsyocto')
            sys.exit()

        # Find the handoff folder
        self.Handoff_folder_name = ''
        handoff_folder_start_name =''
        for file in os.listdir(self.Quartus_proj_top_dir):
                if "_handoff" in file:
                    handoff_folder_start_name =file
                    break
        folder_found = False
        if not handoff_folder_start_name=='':
            for folder in os.listdir(self.Quartus_proj_top_dir+self.__SPLM[self.__SPno]+handoff_folder_start_name):
                if os.path.isdir(self.Quartus_proj_top_dir+self.__SPLM[self.__SPno]+handoff_folder_start_name+self.__SPLM[self.__SPno]+folder):
                    self.Handoff_folder_name = folder
                    if folder_found:
                        print('[ERROR]  More than one folder inside the Quartus handoff folder "'+self.Handoff_folder_name+'" found! Please delete one!')
                        print('         NOTE: It is necessary to build the Prime Quartus Project for the bootloader generation!')
                        sys.exit()
                    folder_found = True
            self.Handoff_folder_name = handoff_folder_start_name+self.__SPLM[self.__SPno]+self.Handoff_folder_name

            # Find the "hps.xml"-file inside the handoff folder
            handoff_xml_found =False

            for file in os.listdir(self.Quartus_proj_top_dir+self.__SPLM[self.__SPno]+self.Handoff_folder_name):
                if "hps.xml" == file:
                    handoff_xml_found =True
                    break 
            if not handoff_xml_found:
                print('[ERROR]  The "hps.xml" file inside the handoff folder was not found!')
                print('         NOTE: It is necessary to build the Prime Quartus Project for the bootloader generation!')
                sys.exit()
            # Load the "hps.xml" file to read the device name
            try:
                tree = ET.parse(self.Quartus_proj_top_dir+self.__SPLM[self.__SPno]+self.Handoff_folder_name+self.__SPLM[self.__SPno]+'hps.xml') 
                root = tree.getroot()
            except Exception as ex:
                print(' [ERROR]  Failed to parse "hps.xml" file!')
                print('          Msg.: '+str(ex))
                sys.exit()

            device_name_temp =''
            for it in root.iter('config'):
                name = str(it.get('name'))
                if name == 'DEVICE_FAMILY':
                    device_name_temp = str(it.get('value'))
                    break
            if device_name_temp == '':
                print('[ERROR]  Failed to decode the device name inside "hps.xml"')

            # Convert Device name
            if device_name_temp == 'Cyclone V':
                self.Device_id = 0
                '''
                elif device_name_temp == 'Arria V':
                    self.Device_id = 1
                '''
            elif device_name_temp == 'Arria 10':
                self.Device_id = 2
                print('[ERROR] The Arria 10 SX SoC-FPGA is right now not supported!')
                print('         I am working on it...')
                sys.exit()
            
                ## NOTE: ADD ARRIA V/ SUPPORT HERE 
            else:
                print('[ERROR]  Your Device ('+device_name_temp+') is not supported!')
                sys.exit()
        
            # For Arria 10 SX: The early I/O release must be enabled inside Quartus Prime!
            early_io_mode =-1
            if self.Device_id == 2:
                for it in root.iter('config'):
                    name = str(it.get('name'))
                    if name == 'chosen.early-release-fpga-config':
                        early_io_mode = int(it.get('value'))
                        break
                
                if not early_io_mode==1:
                    print('[ERROR]   This build system supports only the Arria 10 SX SoC-FPGA')
                    print('          with the Early I/O release feature enabled!')
                    print('          Please enable Early I/O inside the Intel Quartus Prime project settings')
                    print('          and rebuild the project again')
                    print('Setting: "Enables the HPS early release of HPS IO" inside the general settings')
                    print('Note:     Do not forget to enable it for the EMIF inside Qysis')
                    sys.exit()
                else:
                    print('[INFO] HPS early release of HPS IO for the Intel Arria 10 SX SoC-FPGA is enabled') 
                
        else: 
            # It was no handoff folder found!
            if self.use_jtag==False:
                # Use the network for writting the FPGA-Configuration
                print('********************************************************************************')
                print('*        This is a regular Quartus Prime FPGA project without a HPS            *')
                print('*                (Hard Processor System) implementation!                       *')
                print('*     --> It is not possible to write the FPGA-Conf with the Linux rsyocto!    *')
                print('********************************************************************************')
                print('*                                                                              *')
                print('*       Use the argument "-j 1" to write the FPGA-Configuration via JTAG       *')
                print('*                                                                              *')
                print('********************************************************************************')
                sys.exit()
            else: 
                # Use JTAG
                print('[INFO] The FPGA project has no HPS. FPGA-Config via JTAG is enabled')
                self.regular_fpga_project=True

                ######################################## Force to cyclone V ########################################
                device_name_temp == 'Cyclone V'
                self.Device_id = 0

        print('[INFO] A valid Intel Quartus Prime '+device_name_temp+' SoC-FPGA project was found') 


        ################################ COMPILE THE INTEL QUARTUS PRIME FPGA PROJECT ################################
        if compile_project or use_jtag:
            quVers=0
            if QuartusForceVersion =='':
                print('[ERROR] For the Intel Quartus Prime FPGA Project compilation mode ')
                print('        it is necessary to select the Intel Quartus Prime Version! ')
                print('        Use the argument "-h" for help')
                sys.exit()

            if re.match("^[LSP]+[0-9]+[.]+[0-9]?$", QuartusForceVersion, re.I) == None:
                print('ERROR: The selected Quartus Version is in the wrong format')
                sys.exit()
            # Decode the Version No and Version Type input 
            if not QuartusForceVersion.find('S')==-1:
                quVers=1
            elif not QuartusForceVersion.find('P')==-1:
                quVers=2

            quartus_folder= [QURTUS_DEF_FOLDER_LITE,QURTUS_DEF_FOLDER,QURTUS_DEF_FOLDER_PRO]
            if self.__SPno== 0:
                # Find the Linux default hard drive directory
                sys_folder_dir = os.path.join(os.path.join(os.path.expanduser('~'))) + '/'
            else: 
                # Windows C:// directory 
                sys_folder_dir = 'C:\\' 
        
            self.installDir_Quartus = sys_folder_dir+quartus_folder[quVers]+\
                self.__SPLM[self.__SPno]+QuartusForceVersion[1:]
            
            if not os.path.isdir(self.installDir_Quartus +self.__SPLM[self.__SPno]+"quartus"):
                print('[ERROR] The chosen Intel Quartus Prime Version is not available \n'+\
                      '        on this Computer ("'+self.installDir_Quartus +'")\n'+
                      '        Please install this version or chose a diffrent Intel Quartus Version!\n'+\
                      '        Use the argument "-h" to get help')
                sys.exit()

            # Check if the Quartus Prime "bin64" 64-bit version folder is there
            self.installDir_Quartus_bin= self.installDir_Quartus +self.__SPLM[self.__SPno]+\
                "quartus"+self.__SPLM[self.__SPno]+"bin64"
            if not os.path.isdir(self.installDir_Quartus_bin):
                self.installDir_Quartus_bin= self.installDir_Quartus +self.__SPLM[self.__SPno]+\
                "quartus"+self.__SPLM[self.__SPno]+"bin"
                if not os.path.isdir(self.installDir_Quartus_bin):
                    print('[ERROR] The Intel Quartus Prime bin or bin64 folder does not exist!\n'+\
                          '        search dir: "'+self.installDir_Quartus_bin+'"')
                    self.installDir_Quartus_bin=''
                    sys.exit()

            # Find the Quartus Prime Command Shell    
            self.shell_quartus_dir = self.installDir_Quartus_bin+self.__SPLM[self.__SPno]+\
                QUARTUS_CMDSHELL_EXE[self.__SPno]
            
            if not os.path.isfile(self.shell_quartus_dir):
                print('[ERROR] The Intel Quartus Prime shell  \n'+\
                      '        was not found ("'+self.shell_quartus_dir+'")')
                sys.exit()

            print('[INFO] The vailed Intel Quartus Prime project was found ('+QuartusForceVersion+')') 

            if compile_project:
                print('[INFO] Start compiling the Intel Quartus Prime FPGA project')
                if not self.command_quartusShell_flow():
                        print('[ERROR] Compilation of the Intel Quartus Prime Project failed!')
                        sys.exit()
                print('[INFO] Compiling the Intel Quartus Prime FPGA project is done')

    #
    # @brief Start the Quartus Prime deasign flow compatlation, routing with 
    #        compilation, timing analysis, and programming file generation
    # @param mode
    #               compile      =  Basic compilation
    #               implement    =  Run compilation up to route stage
    #               finalize     =  Perform pre-POF finalization operations
    #               recompile    =  Perform a Rapid Recompile after making a design change
    #               signalprobe  =  Run project signalprobing 
    #           export_database  =  Export database
    #           import_database  =  import database
    # @return success 
    def command_quartusShell_flow(self,mode='compile'):
        if not (mode =='compile' or mode== 'implement' or mode == 'finalize' or \
                mode == 'recompile' or mode== 'signalprobe' or mode =='export_database' or \
                mode == 'import_database'):
            print('[ERROR] The selected input mode is not allowed!') 
            return False
 
        print('--> Start the Quartus Prime project design flow ')
        print('    in the mode "'+mode+'"')
        
        if self.Quartus_proj_top_dir =='': 
            print('[ERROR] The Quartus Project top folder is not specified')
            return False
        
        os.system(self.shell_quartus_dir+' --flow '+mode+' '+self.Quartus_proj_top_dir+\
                self.__SPLM[self.__SPno]+self.Qpf_file_name)
        
        print('\n--> The Design flow command was executed')

        # Check that the output file (".sof") has be changed
        if not os.path.isfile(self.Quartus_proj_top_dir+self.Sof_folder+\
                self.__SPLM[self.__SPno]+self.Sof_file_name):
            print('[ERROR] The output file (".sof") does not exist!')
            

        modification_time = os.path.getmtime(self.Quartus_proj_top_dir+\
                self.__SPLM[self.__SPno]+self.Sof_folder+\
                self.__SPLM[self.__SPno]+self.Sof_file_name) 
        current_time =  datetime.now().timestamp()

        
        # Offset= 10 min 
        new_file=False
        if modification_time+ 10*60 < current_time:
            # Was a new File created 
            files = [s for s in os.listdir(self.Quartus_proj_top_dir+\
                    self.__SPLM[self.__SPno]+self.Sof_folder)
                if os.path.isfile(os.path.join(self.Quartus_proj_top_dir+\
                    self.__SPLM[self.__SPno]+self.Sof_folder, s))]
            files.sort(key=lambda s: os.path.getmtime(\
                os.path.join(self.Quartus_proj_top_dir+self.__SPLM[self.__SPno]+\
                    self.Sof_folder, s)),reverse=True)
            if not len(files)==0:
                for file in files:
                    if ".sof" in file:
                        print(file)
                        modification_time = os.path.getmtime(file)
                        if modification_time+ 400*60 < current_time:
                            print('[ERROR] The compilation failed!')
                            return False
                        self.Sof_file_name=file
                        print('[NOTE] New FPGA-Configuration file name "'+file+'"')
                        new_file = True
                        break
            else:
                return False
            
            if  self.Sof_file_name.find('_time_limited')>-1: self.unlicensed_ip_found=True
            else:                                            self.unlicensed_ip_found=False

            if self.unlicensed_ip_found and not self.use_jtag:
                print('[ERROR] The compilation is done and contains a unlicensed IP!')
                print('        It is not allowed to write a .rbf FPGA-Configuration file with it!')
                print('        Use the argument "-j 1" to write it via JTAG to RAM')
                return False                

            if not new_file:
                print('[ERROR] The comand failed! The output file (".sof") is the same!')
                return False
        
        return True 

    #
    # @brief Write the FPGA-Configuration with JTAG to RAM
    # @return success 
    #
    def command_jtag_writeConfRAM(self):

        if not os.path.isfile(self.Quartus_proj_top_dir+self.__SPLM[self.__SPno]+self.Sof_folder+\
                self.__SPLM[self.__SPno]+self.Sof_file_name):
            print('[ERROR] The output file (".sof") does not exist! --> JTAG Flash impossible!')
            return False
            
        sof_file_dir = self.Quartus_proj_top_dir+self.__SPLM[self.__SPno]+self.Sof_folder

        jtagconfig_cmd_dir = self.installDir_Quartus_bin+self.__SPLM[self.__SPno]
        jtagconfig_cmd_dir+= 'jtagconfig' if self.__SPno==0 else 'jtagconfig.exe'
                            
        '''
        C:\intelFPGA\18.1\quartus\bin64>jtagconfig.exe
        1) DE-SoC [USB-1]
        4BA00477   SOCVHPS
        02D020DD   5CSEBA6(.|ES)/5CSEMA6/..
        '''
        #
        ### 1. Step: Run "jtagconfig" to scan the JTAG Chain 
        #
        out_chain =''
        err =''
        try:
            with subprocess.Popen(jtagconfig_cmd_dir, stdin=subprocess.PIPE,\
                stdout=subprocess.PIPE,stderr = subprocess.PIPE) as edsCmdShell:

                time.sleep(DELAY_MS)
       
                out_chain, err = edsCmdShell.communicate()

            
        except Exception as ex:
            print('[ERROR] Failed to execute the "jtagconfig" command MSG:'+ str(ex))
            return False

        # Check that a vialed JTAG Debugger was connected  
        out_chain= out_chain.decode("utf-8") 
        err= err.decode("utf-8")
        if out_chain=='' or err.find('No JTAG hardware available')>-1:
            print('[ERROR] No supported JTAG Debugger was found!')
            print('        Check the connection between the FPGA device and the debugger')
            err= err.replace('\n','')
            print('        MSG: '+err)
            return False
        if  out_chain=='':
            print('[ERROR] During JTAG Debugger connection attempt unknown Error occurred!')
            err= err.replace('\n','')
            print('        MSG: '+err)
            return False
        
        start_symbol_pos = out_chain.find('1)')
        if self.__SPno==0:
            JTAG_debugger_id_start_pos = out_chain.find('[1-') 
        else: 
            JTAG_debugger_id_start_pos = out_chain.find('[USB-1]')
        
        if start_symbol_pos==-1 or JTAG_debugger_id_start_pos==-1:
            print('[ERROR] No USB JTAG Debugger found! Only USB Debuggers are supported!')
            return False

        # At least one JTAG Debugger was connected --> read the ID of the Debugger
        if self.__SPno==0:
            JTAG_debugger_id = out_chain[start_symbol_pos+3:JTAG_debugger_id_start_pos+6]
        else:
            JTAG_debugger_id = out_chain[start_symbol_pos+3:JTAG_debugger_id_start_pos+7]
        JTAG_debugger_id= JTAG_debugger_id.replace('\n','',100)

        # Are more then one debugger connected --> not supported
        if not out_chain.find('2)',JTAG_debugger_id_start_pos)==-1:
            print('[ERROR] More then one USB JTAG Debugger found! Only one is allowed!')
            print('        Disconnect one JTAG Debugger to use this script!')
            return False

        print('[INFO] A valid JTAG Debugger was found with the ID="'+JTAG_debugger_id+'"')

        #
        ## 2. Step: Create a Chain Description File (.cdf)
        #

        # Check if a CDF file is allready there 
        cdf_file_name=self.Sof_file_name.replace('.sof', '.cdf')
        if os.path.isfile(sof_file_dir+self.__SPLM[self.__SPno]+cdf_file_name):
            try:
                os.remove(sof_file_dir+self.__SPLM[self.__SPno]+cdf_file_name)
            except Exception:
                print('[ERROR] Failed to remove the old CDF File! Please remove it by hand!')
                print('        File dir: "'+of_file_dir+self.__SPLM[self.__SPno]+cdf_file_name+'"')
                return False

        # Analyse the JTAG Chain
        JTAG_id_list = []
        Device_id_list=[]
        first_line =True

        for line in out_chain.splitlines():
            if first_line:
                first_line=False
                continue

            # Format <JTAG ID> <DEVICE ID>
            jtag_id_start=2
            jtag_id_end =0
            # Find the <JTAG_ID>
            for i in range(2,len(line)): 
                jtag_id_end=i
                if not bool(re.match("^[A-F0-9]?$", line[i], re.I)): 
                    break

            if jtag_id_end>0:
                JTAG_id_list.append(line[jtag_id_start:jtag_id_end])
                # Find the <DEVICE ID>
                # Find first non ' ' char pos
                device_id_start=0
                device_id_end=0
                for i in range(jtag_id_end+1,len(line)):
                    if not line[i] ==' ':
                        device_id_start = i
                        break
                if device_id_start > 0: 
                    device_id_end=line.find('(',device_id_start)
                    if device_id_end==-1: device_id_end=len(line)

                    Device_id_list.append(line[device_id_start:device_id_end])

        if (len(JTAG_id_list) ==0 or len(Device_id_list) ==0) or \
            (not len(JTAG_id_list) == len(Device_id_list)):
            print('[ERROR] Failed to decode JTAG Chain Scan output!')
            return False

        if len(JTAG_id_list)>2 or len(Device_id_list)>2:
            print('[ERROR] More then 2 JTAG Devices inside the chain! This is is not supported!')
            return False

        if len(JTAG_id_list)==2 and Device_id_list[0].find('SOC')==-1:
            print('[ERROR] JTAG Chain with 2 Devices found! The first is not the HPS...')
            print('        This is not supported. Single Device or first device must the HPS!')
            return False

        # Check that the JTAG Chain family matches the Quartus Project one
        wrong_device =False
        if len(JTAG_id_list)==2:
            if self.Device_id==0 and Device_id_list[0].find('SOCVHPS')==-1:  wrong_device= True
            if self.Device_id==1 and Device_id_list[0].find('SOVHPS')==-1:   wrong_device= True
            if self.Device_id==2 and Device_id_list[0].find('SOC10HPS')==-1: wrong_device= True
            
        else:
            if self.Device_id==0 and Device_id_list[0].find('5C')==-1:      wrong_device= True
            if self.Device_id==1 and Device_id_list[0].find('5A')==-1:      wrong_device= True
            if self.Device_id==2 and Device_id_list[0].find('10A')==-1:     wrong_device= True

        if wrong_device:
            print('[ERROR] The FPGA Device family of the FPGA project was not found in the JTAG Chain!')
            return False

        cdf_file_content=''
        # Create the JTAG Chain file
        sof_file_dir_2 = sof_file_dir.replace('\\','/',50)+'/'

        cfg_no =0
        if len(JTAG_id_list)==2: cfg_no=1
        # CDF file for FPGAs
        cdf_file_content= '/* Generated file by "flashFPGA2rsyocto.py" by Robin Sebastian (git@robseb.de) */\n' + \
        'JedecChain;\n' + \
        '   FileRevision(JESD32A);\n' + \
        '   DefaultMfr(6E);\n' +'\n'
        if len(JTAG_id_list)==2:
            cdf_file_content+= '   P ActionCode(Ign)\n'
            cdf_file_content+= '	    Device PartName('+Device_id_list[0]+') MfrSpec(OpMask(0));\n'
        cdf_file_content+= '   P ActionCode(Cfg)\n' + \
        '	    Device PartName('+Device_id_list[cfg_no]+') Path("'+sof_file_dir_2+\
            '") File("'+self.Sof_file_name+'") MfrSpec(OpMask(1));\n' + \
        '\n' + \
        'ChainEnd;\n' + '\n' + \
        'AlteraBegin;\n' + \
        '	ChainType(JTAG);\n' + \
        'AlteraEnd;\n'
 

        # Write the CDF File
        cdf_file_dir = sof_file_dir+self.__SPLM[self.__SPno]+cdf_file_name
        with open(cdf_file_dir,"w") as f: 
            f.write(cdf_file_content)

        # 
        ## 3. Step: Write the FPGA-Configuration with "quartus_pgm"
        #

        # quartus_pgm.exe -m JTAG -c 1 D:\Tresorit\Robin\FPGA\DE10STD_NIOS\DE10STDrsyocto_NIOS2_1\output_files\DE10STD.cdf
        quartus_pgm_cmd_dir = self.shell_quartus_dir = self.installDir_Quartus_bin+self.__SPLM[self.__SPno]
        quartus_pgm_cmd_dir+= 'quartus_pgm' if self.__SPno==0 else 'quartus_pgm.exe'
        cmd = quartus_pgm_cmd_dir+' -m JTAG -c 1 '+cdf_file_dir
        '''
        print(cmd)
        if self.__SPno==0:
            # for Linux
            cmd = [quartus_pgm_cmd_dir,' -c 1 ',' -m JTAG ',cdf_file_dir]
        '''

        if self.unlicensed_ip_found: 

            # 
            ## 3.A Step: Write the FPGA-Configuration with "quartus_pgm"
            # Create a BASH or Shell script for executing this command
            #

            # Remove the older BASH/SH File
            sh_file_name=self.Sof_file_name.replace('.sof', '.sh' if self.__SPno==0 else '.bat')
            if os.path.isfile(sof_file_dir+self.__SPLM[self.__SPno]+sh_file_name):
                try:
                    os.remove(sof_file_dir+self.__SPLM[self.__SPno]+sh_file_name)
                except Exception:
                    print('[ERROR] Failed to remove the old SH/BAT File! Please remove it by hand!')
                    print('        File dir: "'+of_file_dir+self.__SPLM[self.__SPno]+sh_file_name+'"')

            # Create a new SH/BAT file
            try:
                with open(sh_file_name, "a") as f:
                    if self.__SPno==0: f.write('#!/bin/sh \n')
                    f.write(cmd+'\n')

                    f.write('echo "********************************************************************************"\n')
                    f.write('echo "*               Unlicensed IP inside the FPGA project was found!               *"\n')
                    f.write('echo "********************************************************************************"\n')
                    f.write('echo "*      The FPGA-Conf. was written and the FPGA IP Evaluation Mode has started. *"\n')
                    f.write('echo "*                  Now it is enabled to test the IP. After this                *"\n')
                    f.write('echo "*                   promped is closed the licence will expire...               *"\n')
                    f.write('echo "********************************************************************************"\n')
                    f.write('echo "*             Support the author Robin Sebastian (git@robseb.de)               *"\n')
                    f.write('echo "********************************************************************************"\n')

                    if self.__SPno==0:
                        f.write('read -p "Type something to exit..." mainmenuinput\n')
                    else:
                        f.write('pause\n')
            except Exception as ex:
                self._print('[ERROR] Failed create the quartus_pgm JTAG flash shell script\n'+\
                            '        MSG: '+str(ex))
                return False

            # Execute the shell script in a new terminal window 
            try:
                #os.startfile(sh_file_name)
                
                #os.system('gnome-terminal -x '+st_dir)
                if self.__SPno==0:
                    st_dir= sh_file_name.replace(os.path.expanduser('~'), '~', 1)
                    os.chmod(sh_file_name, 0o775)
                    os.system('./'+st_dir)
                else: 
                    os.system(sh_file_name)
            except Exception as ex:
                print('[ERROR] Failed start the quartus_pgm JTAG flash shell script!\n'+\
                            '        MSG.: '+str(ex))
                return False

            # Wait for the user
            #inch = input('===> Type something to terminal the FPGA IP Evaluation Mode... $')

            # Remove the Shell script file 
            if os.path.isfile(sof_file_dir+self.__SPLM[self.__SPno]+sh_file_name):
                try:
                    os.remove(sof_file_dir+self.__SPLM[self.__SPno]+sh_file_name)
                except Exception:
                    print('[ERROR] Failed to remove the old SH/BAT File! Please remove it by hand!')
                    print('        File dir: "'+of_file_dir+self.__SPLM[self.__SPno]+sh_file_name+'"')

            # Remove the CDF script file 
            if os.path.isfile(sof_file_dir+self.__SPLM[self.__SPno]+cdf_file_name):
                try:
                    os.remove(sof_file_dir+self.__SPLM[self.__SPno]+cdf_file_name)
                except Exception:
                    print('[ERROR] Failed to remove the old CDF File! Please remove it by hand!')
                    print('        File dir: "'+of_file_dir+self.__SPLM[self.__SPno]+cdf_file_name+'"')

            # Set status to true
            self.ThreadStatus=True

            return True

        # For the case with a full licensed FPGA-Configuration 
        err=''
        out_pgm=''
        try:
            
            if self.__SPno==0:
                cmd = [quartus_pgm_cmd_dir,'-c1','-mJTAG',cdf_file_dir]
            with subprocess.Popen(cmd,\
                stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr = subprocess.PIPE) as edsCmdShell:
                time.sleep(DELAY_MS)
                out_pgm, err = edsCmdShell.communicate()

        except Exception as ex:
            print('[ERROR] Failed to execute the "quartus_pgm" command MSG:'+ str(ex))
            return False
        finally:
            if os.path.isfile(sof_file_dir+self.__SPLM[self.__SPno]+cdf_file_name):
                try:
                    os.remove(sof_file_dir+self.__SPLM[self.__SPno]+cdf_file_name)
                except Exception:
                    print('[ERROR] Failed to remove the old CDF File! Please remove it by hand!')
                    print('        File dir: "'+of_file_dir+self.__SPLM[self.__SPno]+cdf_file_name+'"')

        # Check that the FPGA Configuration was successfull with JTAG
        out_pgm= out_pgm.decode("utf-8") 
        err= err.decode("utf-8")

        if err=='' and out_pgm.find('Info: Quartus Prime Programmer was successful')>-1:
            print('[INFO] FPGA-Configuration was written successfully via JTAG')
        elif out_pgm.find('Intel FPGA IP Evaluation Mode feature that will not work after the hardware evaluation time expires')>-1:
            print('[ERROR] Failed to write the FPGA-Configuration via JTAG!')
            print('        The FPGA-Configuration file contains a unlicensed IP and Intel FPGA IP Evaluation Mode error occurred!')
            print('        It looks like that Intel FPGA IP Evaluation mode server is allready running.')
            print('        Close any currently open FPGA-Configurations with CMD + C and try it agin!')
            print('************************ OUTPUT OF "quartus_pgm" ************************')
            print(out_pgm)
            return False
        else:
            print('[ERROR] Failed to write the FPGA-Configuration via JTAG')
            err= err.replace('\n','')
            print('        MSG: '+err)
            print('        OUT: '+out_pgm)
            return False

        # Set status to true
        self.ThreadStatus=True

        return True

    #
    # @brief Ping a Network device
    # @param host_or_ip     IPv4 address of the device 
    # @param packets        Number of Packages to send
    # @param timeout        Timout in sec
    # @return   Pinging the board was successful
    #
    def __ping(self, host_or_ip, packets=1, timeout=1000):
        if platform.system().lower() == 'windows':
            command = ['ping', '-n', str(packets), '-w', str(timeout), host_or_ip]
            res= subprocess.run(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, \
            stderr=subprocess.DEVNULL, creationflags=0x08000000)
            return res.returncode == 0 and b'TTL=' in res.stdout
        else:
            ping_response =''
            try:
                '''
                ping_response = subprocess.Popen(["/bin/ping", "-c5", "-w100",host_or_ip], stdout=subprocess.PIPE, \
                    stdin=subprocess.DEVNULL).stdout.read()
                ping_response = ping_response.decode("utf-8") 
                '''

                ping_response = subprocess.Popen(["timeout","5","ping", "-c5", "-w100",host_or_ip], stdout=subprocess.PIPE, \
                    stdin=subprocess.DEVNULL).stdout.read()
                ping_response = ping_response.decode("utf-8") 
            except Exception:
                return False
            if ping_response.find('Host Unreachable')==-1:
                return True
            return False


    #
    # @brief    Check the Network connection from the development machine to the embedded Linux Distribution
    # @return   Pinging the board was successful
    #
    def CheckNetworkConnection2Board(self):
        return self.__ping(self.board_ip_addrs)
        
    #
    # @brief    Establish a SSH connection the SoC-FPGA baord running rsyocto
    #
    def EstablishSSHcon(self):
        Thread.__init__(self)
        self.__queue = queue.Queue()
        self.daemon = True
        self.start()

    #
    # @brief Send a Linux Shell command via SSH to rsyocto
    # @param  cmd           Linux Shell command to execute
    #                       as string
    # @param ignore_error   Ignore all errors
    # @return               responce string of the command 
    #
    def __sendCmd(self,cmd='',ignore_error=False):
        ssh_stdin, ssh_stdout, ssh_stderr = self.__sshClient.exec_command(cmd)
        err = ssh_stderr.read().decode("utf-8") 
        if not err == '':
            if not ignore_error:
                print('[ERROR] Failed to execute a Linux cmd via SSH!\n'+\
                    '        CMD  : "'+cmd+'"\n'+\
                    '        ERROR: "'+err+'"')    
            return 'ERROR'

        return ssh_stdout.read().decode("utf-8") 

    #
    # @brief Decode the used diskspace of the
    #        rootfs of rsyocto in %
    # @param str_df     output of the "df" command
    # @return           available diskspace in % 
    #
    def __decodeDiskSpace(self,str_df=''):
        root_pos = str_df.find('/dev/root')
        if root_pos==-1: return -1
        line_end_pos = str_df.find('\n',root_pos)
        if line_end_pos==-1: return -1

        line = str_df[root_pos:line_end_pos]

        '''
        \Filesystem     1K-blocks   Used Available Use% Mounted on
        /dev/root        3978548 640080   3133036  17% /
        '''
        # Find the % character and number
        perc_pos = line.find('%')
        begin_number_pos =-1
        if perc_pos==-1: return -1

        for i in range(perc_pos-1,0,-1):
            try:
                vao = line[i]
                null = int(line[i]) 
            except ValueError:
                begin_number_pos = i+1
                break
        if begin_number_pos==-1: return -1

        number = line[begin_number_pos:perc_pos]
        try:
            number = int(number)
        except ValueError:
            return -1
        return number

    #
    # @brief Decode the partition table of rsyocto
    #        and check that all execpected partitions 
    #        are available 
    # @param str_lsblk      output of the "lsblk" command
    # @param mountingpoint  name of a mounting point to found
    # @return is the partition table vialed
    #
    def __decodePartitions(self,str_lsblk='',mountingpoint=''):
        if str_lsblk.find('mmcblk0p1')==-1 or str_lsblk.find('mmcblk0p2')==-1 or \
           str_lsblk.find('mmcblk0p3')==-1:
            return False
        if not mountingpoint=='' and str_lsblk.find(mountingpoint)==-1:
            return False
        return True 

    #
    # @brief Check that are a FPGA-Configuration file on the rootfs 
    #        with the "ls" command
    # @param str_ls          output of the "ls" command
    # @param fpga_conf_name  name of the FPGA-Configuration file to find
    # @return                was the file found?
    #  
    def __checkforFPGAFiles(self,str_ls='',fpga_conf_name=''):
        if str_ls=='' or fpga_conf_name=='' : return False
        if str_ls.find(fpga_conf_name)==-1:   return False
        return True 

    #
    # @brief Cleanup the SSH/SFTP Connection and the process of 
    #        writing a new FPGA-Configuration to rsyocto
    # @param remove_files       Remove the temp files from the 
    #                           rsyocto rootfs
    # @param close_connection   Close the SSH/SFTP connection 
    #
    def __cleanupSSH(self,remove_files=False, close_connection=True):
        print('[INFO] Cleanup SSH- and SFTP connection to rsyocto')

        if remove_files:
            # Remove the old mounting point if available 
            try: 
                self. __sendCmd('sudo umount '+self.__temp_partfolder_dir,True)
            except Exception:
                pass

            # Remove the temp folder 
            cmd = 'sudo rm -r '+self.__temp_folder_dir
            try:
                rm_mes = self. __sendCmd(cmd,True)
            except Exception:
                pass
        if close_connection:
            if not self.__sftpClient== None: self.__sftpClient.close()
            if not self.__sshClient== None: self.__sshClient.close()


    #
    # @brief Override the run() function of Thread class
    #        Thread to for handling the SSH connection to SoC-FPGA baord
    #
    def run(self):
        print('[INFO] Start to establish a SSH connection to the SoC-FPGA board with rsyocto')

        # Start a new SSH client connection to the development board
        self.__sshClient = None
        self.__sftpClient= None
        self.ThreadStatus= False
        self.__sshClient = paramiko.SSHClient()
        self.__sshClient.load_system_host_keys()
        warnings.filterwarnings("ignore")
        self.__temp_folder_dir = '/home/'+self.board_user+'/'+RSYOCTO_TEMPCOPYFOLDER
        self.__temp_partfolder_dir= self.__temp_folder_dir+'/'+'bootloader'
        self.__sshClient.set_missing_host_key_policy(paramiko.WarningPolicy())
  
        try:
            #
            ## 1. Step: Establish a SSH connection to the board
            #  
            self.__sshClient.connect(self.board_ip_addrs, username=self.board_user, 
                        password=self.board_pw, allow_agent=False,
                look_for_keys=False, banner_timeout=500)

            #
            ##  2. Step: Check that the embedded Linux Distribution is okay for the tasks 
            #

            # Load the rsyocto banner  
            banner = str(self.__sshClient._transport.get_banner())

            # Check the the connected board is really rsyocto
            is_not_rsyocto =False
            for checkstr in RSYOCTO_BANNER_CHECK_LINE:
                if not checkstr in banner:
                    is_not_rsyocto = True
                    break
            
            if is_not_rsyocto:
                print('[ERROR] The connected board does not run rsyocto!\n'+
                      '        This script works only with together with the \n'+\
                      '        embedded Linux Distribution rsyocto!\n'+\
                      '        ==> github.com/robseb/rsyocto')
                self.__cleanupSSH(False,True)
                return False
    
            # Check that the connected rsyocto runs on the same SoC-FPGA family as the 
            # the Intel Quartus Prime project
            cmd = 'cat /usr/rsyocto/device.txt'
            rsyocto_devicename = self. __sendCmd(cmd)
            if not self.Device_name[self.Device_id] in rsyocto_devicename:
                print('[ERROR] SoC-FPGA device of connected Board is incompatible \n'+\
                      '        to this Intel Quartus Prime FPGA project!\n'+\
                      '        Device of the Board          : "'+\
                          rsyocto_devicename+'" \n'+\
                      '        Quartus Prime Project device : "'+\
                          self.Device_name[self.Device_id]+'"')
                self.__cleanupSSH(False,True)
                return False

            # Check that the "FPGA-writeConfig" command is available 
            #
            fpga_writecmd_ret = self. __sendCmd("FPGA-writeConfig") 
            if not RSYOCTO_FPGAWRITECONF_CHECK in fpga_writecmd_ret:
                print('[ERROR] The connect rsyocto Linux Distribution has no '+\
                      '"FPGA-writeConfig" Linux command of the rstools installed! \n'+\
                      '        This command allows to write the FPGA-Configuration and is need by this script!')
                self.__cleanupSSH(False,True)
                return False
            
            # Check that enough memory space is available on rsyocto for 
            # uploading the FPGA configuration files
            cmd = 'df'
            diskpace = self.__decodeDiskSpace(self. __sendCmd(cmd))
            if diskpace==-1: 
                print('[ERROR] Failed to get the available diskpace from the embedded Linux')  
                self.__cleanupSSH(False,True)
                return False
            elif diskpace >= 99:
                print('[ERROR] It is not enough diskspace left on rsyocto on the SoC-FPGA board \n'+\
                      '        for uploading the FPGA-Configuration!\n'+\
                      '        Disk space on the rootfs used: '+str(diskpace)+'%\n'+\
                      '        At least 1% must be free available!')
                self.__cleanupSSH(False,True)
                return False

            # Check that all partitions are available on rsyocto
            # primary the bootloader partition
            cmd = 'lsblk'
            if not self.__decodePartitions(self. __sendCmd(cmd)): 
                print('[ERROR] Not all expected partitions available on rsyocto!\n'+\
                        '        The bootloader partition could not be located!')
                self.__cleanupSSH(False,True)
                return False

            print('[INFO] SSH Connection established to rsyocto ('+\
                str(100-diskpace)+'% free disk space remains on the rootfs)')
            
            #
            ##  3. Step: Transfering the FPGA-Configuration file 
            #            that can be written by Linux to the temp folder
            #
            [rbf_dir,fpga_linux_file,fpga_boot_file] =  self.__queue.get()

            print('[INFO] Starting SFTP Data transfer!')

            #Transfering files to and from the remote machine
            self.__sftpClient = self.__sshClient.open_sftp()
 
            # Remove the temp folder from rsyocto
            self.__cleanupSSH(True,False)

            # Create a new empty temp folder 
            cmd = 'mkdir '+self.__temp_folder_dir
            if not self. __sendCmd(cmd)=='':
                print('[ERROR] Failed to create a new temp folder on rsyocto!')
                self.__cleanupSSH(False,True)
                return False


            # Copy the FPGA configuration file for writing with Linux to the rootfs
            print('[INFO] Start coping the new Linux FPGA-Configuration file to rsyocto')
            local_path = rbf_dir+fpga_linux_file
            try:
                self.__sftpClient.put(local_path, self.__temp_folder_dir+'/'+fpga_linux_file)
            except Exception as ex:
                print('[ERROR] Exception occurred during SFTP File transfer!\n'+\
                      '        MSG.        : "'+str(ex)+'"')
                self.__cleanupSSH(True,True)
                return False

            # Check that the new FPGA-Configuration is now located on the rootfs
            cmd = 'ls '+self.__temp_folder_dir
            if not self.__checkforFPGAFiles(self. __sendCmd(cmd),fpga_linux_file): 
                print('[ERROR] The Linux FPGA-Configuration could not be found \n'+\
                        '        in the bootloader partition!')
                self.__cleanupSSH(True,True)
                return False

            # Write the new FPGA-Configuration to the FPGA-Fabric
            print('[INFO] Changing the FPGA-Configuration of FPGA-Fabric with the new one')
            cmd = 'FPGA-writeConfig -f '+self.__temp_folder_dir+'/'+fpga_linux_file
            if self. __sendCmd(cmd).find('Succses: The FPGA runs now with')==-1:
                print('[ERROR] Failed to write the FPGA Configuration!')
                self.__cleanupSSH(True,True)
                return False

            # Remove the FPGA-Configuration file from the rootfs
            cmd = 'sudo rm '+self.__temp_folder_dir+'/'+fpga_linux_file
            rm_mes = self. __sendCmd(cmd)
            if not rm_mes=='':
                print('[ERROR] Failed to remove the Linux FPGA-Configuration file \n'+\
                        '        from the rootfs!')
                self.__cleanupSSH(True,True)
                return False

            print('[INFO] Running FPGA-Configuration was changed successfully')

            #
            ## 4. Step: Copy the FPGA-Configuration file to the bootloader partition
            #
            #
            if not fpga_boot_file=='':
                # Create a new empty temp folder for the bootloader 
                cmd = 'mkdir '+self.__temp_partfolder_dir
                if not self. __sendCmd(cmd)=='':
                    print('[ERROR] Failed to create a new bootloader temp folder on rsyocto!')
                    self.__cleanupSSH(False,True)
                    return False

                # Remove the old mounting point if available 
                self. __sendCmd('sudo umount '+self.__temp_partfolder_dir,True)

                # Mount the bootloader partition to the temp foler
                self. __sendCmd('sudo mount /dev/mmcblk0p1 '+self.__temp_partfolder_dir)
                
                # Check that the partition was mounted
                cmd = 'lsblk'
                if not self.__decodePartitions(self. __sendCmd(cmd),'/home/root/.flashFP'): 
                    print('[ERROR] The mounting of the bootloader partition on rsyocto failed!')
                    self.__cleanupSSH(True,True)
                    return False

                # Read the bootloader files and look for the FPGA-Configuration file
                cmd = 'ls '+self.__temp_partfolder_dir
                if not self.__checkforFPGAFiles(self. __sendCmd(cmd),fpga_boot_file): 
                    print('[ERROR] The bootloader FPGA-Configuration could not be found \n'+\
                          '        in the bootloader partition!')
                    self.__cleanupSSH(True,True)
                    return False

                # Remove the old FPGA-Configuration file from the bootloader partition
                print('[INFO] Removing the old bootloader FPGA-Configuration from rsyocto')
                cmd = 'sudo rm '+self.__temp_partfolder_dir+'/'+fpga_boot_file
                rm_mes = self. __sendCmd(cmd)
                if not rm_mes=='':
                    print('[ERROR] Failed to remove the old FPGA-Configuration file \n'+\
                          '        from the bootloader partition!')
                    self.__cleanupSSH(True,True)
                    return False
                
                # Copy the new FPGA-Configuration file to the bootloader partition
                print('[INFO] Copying the new bootloader FPGA-Configuration to rsyocto')
                local_path_bootconf = rbf_dir+fpga_boot_file
                try:
                    self.__sftpClient.put(local_path_bootconf, self.__temp_partfolder_dir+'/'+fpga_boot_file)
                except Exception as ex:
                    print('[ERROR] Exception occurred during SFTP File transfer!\n'+\
                        '        MSG.        : "'+str(ex)+'"')
                    self.__cleanupSSH(True,True)
                    return False

                # Check that the new FPGA-Configuration is inside the partition folder 
                cmd = 'ls '+self.__temp_partfolder_dir
                if not self.__checkforFPGAFiles(self. __sendCmd(cmd),fpga_boot_file): 
                    print('[ERROR] The new bootloader FPGA-Configuration could not be found \n'+\
                          '        in the bootloader partition!')
                    self.__cleanupSSH(True,True)
                    return False

                # Remove the old mounting point if available 
                self. __sendCmd('sudo umount '+self.__temp_partfolder_dir,True)

                # Remove the mounting point folder 
                cmd = 'sudo rm -r '+self.__temp_partfolder_dir
                rm_mes = self. __sendCmd(cmd)
                if not rm_mes=='':
                    print('[ERROR] Failed to remove the mounting point folder \n'+\
                            '        from the rootfs!')
                    # ADD CLEAN UP
                    self.__sftpClient.close()
                    self.__sshClient.close()
                    return False

                print('[INFO] Bootloader FPGA-Configuration was changed successfully')

            # Clean up 
            self.__cleanupSSH(True,True)

            print('[INFO] SSH Thread and SFTP Data transfer done')
            self.ThreadStatus= True
            return True
            

        except Exception as ex: 
            print('[ERROR] Failed to open SSH network connection to the board!\n'+
            '              Msg.: "'+str(ex)+'"')
            print('        Maybe try to remove the SSH-Keys from the SSH folder')
            self.__cleanupSSH(True,True)
    #
    #
    # @brief Create a FPGA configuration file for configure the FPGA during boot or with Linux in case this
    #        feature was selected inside the u-boot script
    # @param boot_linux            Generate configuration for
    #                              False : Written during boot (Passive Parallel x8; 
    #                                      File name: <as in uboot script>.rbf)
    #                              True  : Can be written by Linux (Passive Parallel x16;
    #                                      File name: <as in uboot script>_linux.rbf)
    # @param linux_filename        ".rfb" output file name for the configuration with Linux 
    # @param linux_copydir         the location where the output Linux FPGA configuration file should be copied 
    # @return                      success
    #
    def GenerateFPGAconf(self, boot_linux =False, linux_filename='', linux_copydir=''):

        if self.Device_id==2 and boot_linux:
            print('[ERROR]  FPGA configuration file that can be written by Linux (HPS)')
            print('         is for the Arria 10 SX right now not supported!')
            return True # Ignore this message 

        gen_fpga_conf=False
        early_io_mode =False

        # 3.a Generate the FPGA configuration file
        
        if self.Sof_folder =='':
            sof_file_dir = self.Quartus_proj_top_dir
        else:
            sof_file_dir = self.Quartus_proj_top_dir+self.__SPLM[self.__SPno]+self.Sof_folder

        # Remove the old rbf file from the Quartus project top folder
        if os.path.isfile(sof_file_dir+self.__SPLM[self.__SPno]+linux_filename):
            try:
                os.remove(sof_file_dir+self.__SPLM[self.__SPno]+linux_filename)
            except Exception:
                print('[ERROR]  Failed to remove the old project folder FPGA config file')
        try:
            with subprocess.Popen(self.EDS_Folder+\
                EDS_EMBSHELL_DIR[self.__SPno], stdin=subprocess.PIPE,stdout=DEVNULL) as edsCmdShell:

                time.sleep(DELAY_MS)
                if not boot_linux: 
                    print('[INFO] Generating a new FPGA-Configuration file for configuration during boot')

                    sof_file_dir2 = sof_file_dir.replace('\\', '/')
                    b = bytes(' cd '+sof_file_dir2+' \n', 'utf-8')
                    edsCmdShell.stdin.write(b) 

                    # Enable HPS Early I/O Realse mode for the Arria 10 SX 
                    if self.Device_id==2: 
                        pre_fix =' --hps '
                        print('[NOTE] The FPGA configuration wil be in HPS early I/O realse mode generated')
                    else:
                        pre_fix =''
                    
                    b = bytes('quartus_cpf -c '+pre_fix+' '+self.Sof_file_name+' '+linux_filename+' \n','utf-8')
                    edsCmdShell.stdin.write(b) 
                else:
                    print('[INFO] Generating a new FPGA-Configuration file for configuration with the Linux')

                    sof_file_dir2 = sof_file_dir.replace('\\', '/')
                    b = bytes(' cd '+sof_file_dir2+' \n', 'utf-8')
                    edsCmdShell.stdin.write(b) 
    
                    b = bytes('quartus_cpf -m FPP -c '+self.Sof_file_name+' '+linux_filename+' \n','utf-8')
                    edsCmdShell.stdin.write(b) 

                edsCmdShell.communicate()
                time.sleep(DELAY_MS)
            
        except Exception as ex:
            print('[ERROR] Failed to start the Intel SoC EDS Command Shell! MSG:'+ str(ex))
            return False

            # Check that the generated rbf configuration file is now available
        
        if self.Device_id==2: 
            # Configuration file should be generated in early I/O relase mode (Arria 10 SX)
            if not os.path.isfile(sof_file_dir+self.__SPLM[self.__SPno]+rbf_config_name_body+'.periph.rbf') or \
                not os.path.isfile(sof_file_dir+self.__SPLM[self.__SPno]+rbf_config_name_body+'.core.rbf'):
                print('[ERROR]  Failed to generate the FPGA configuration file')
                return False
        else:
            # Configuration file should be generated in normal mode
            if not os.path.isfile(sof_file_dir+self.__SPLM[self.__SPno]+linux_filename):
                print('[ERROR]  Failed to generate the FPGA configuration file')
                return False

        if not boot_linux:
            ## For the uboot FPGA configuration file  
            try:
                if self.Device_id==2: 
                    if not os.path.isfile(self.U_boot_socfpga_dir+'/tools/mkimage'):
                        print('[ERROR]  The mkimage appliation ('+self.U_boot_socfpga_dir+'/tools/mkimage)')
                        print('       does not exist')
                        print('       FPGA Configuration file generation is not possible')
                        print('       --> Runing the u-boot build process once to clone u-boot to "/software"')
                        return False
                    try:
                        shutil.copy2(self.U_boot_socfpga_dir+'/tools/mkimage',sof_file_dir+'/mkimage')
                    except Exception:
                        print('[ERROR]  Failed to copy the "mkimage" application ')
                        return False

                    print('[INFO] Generate the .its HPS Early I/O Realse configuration file ')

                    ITS_FILE_CONTENT = ' /dts-v1/;                                                              '+ \
                                    '/ {                                                                      '+ \
                                    '       description = "FIT image with FPGA bistream";                     '+ \
                                    '       #address-cells = <1>;                                             '+ \
                                    '                                                                         '+ \
                                    '       images {                                                          '+ \
                                    '          fpga-periph-1 {                                                '+ \
                                    '               description = "FPGA peripheral bitstream";                '+ \
                                    '              data = /incbin/("'+rbf_config_name_body+'.periph.rbf'+'"); '+ \
                                    '                type = "fpga";                                           '+ \
                                    '               arch = "arm";                                             '+ \
                                    '               compression = "none";                                     '+ \
                                    '           };                                                            '+ \
                                    '                                                                         '+ \
                                    '           fpga-core-1 {                                                 '+ \
                                    '               description = "FPGA core bitstream";                      '+ \
                                    '               data = /incbin/("'+rbf_config_name_body+'.core.rbf'+'");'+ \
                                    '               type = "fpga";                                            '+ \
                                    '               arch = "arm";                                             '+ \
                                    '               compression = "none";                                     '+ \
                                    '           };                                                            '+ \
                                    '       };                                                                '+ \
                                    '                                                                         '+ \
                                    '       configurations {                                                  '+ \
                                    '           default = "config-1";                                         '+ \
                                    '           config-1 {                                                    '+ \
                                    '               description = "Boot with FPGA early IO release config";   '+ \
                                    '               fpga = "fpga-periph-1";                                   '+ \
                                    '            };                                                           '+ \
                                    '       };                                                                '+ \
                                    '   };                                                                    '
                    
                    if os.path.isfile(sof_file_dir+'/fit_spl_fpga.its'):
                        os.remove(sof_file_dir+'/fit_spl_fpga.its')

                    if os.path.isfile(sof_file_dir+self.__SPLM[self.__SPno]+FIT_FPGA_FILE_NAME):
                        os.remove(sof_file_dir+self.__SPLM[self.__SPno]+FIT_FPGA_FILE_NAME)
                    
                    with open(sof_file_dir+'/fit_spl_fpga.its', "a") as f:
                        f.write(ITS_FILE_CONTENT)
                    
                    
                    print('[INFO] Create the FIT image with the FPGA programming files (used by SFP)')

                    #
                    # mkimage -E -f board/altera/arria10-socdk/fit_spl_fpga.its fit_spl_fpga.itb
                    #  -E => place data outside of the FIT structure
                    #  -f => input filename for FIT source
                    #
                    os.system('cd '+sof_file_dir+' && mkimage -E -f fit_spl_fpga.its '+FIT_FPGA_FILE_NAME+' \n')

                    os.remove(sof_file_dir+'/mkimage')
                    os.remove(sof_file_dir+'/fit_spl_fpga.its')
                    
                    # Check that the output file is generated
                    if not os.path.isfile(sof_file_dir+self.__SPLM[self.__SPno]+FIT_FPGA_FILE_NAME):
                        print('[ERROR]  The .itb FPGA configuration file was not generated!')
                        return False
                    
                    # Copy the file to the VFAT partition
                    if os.path.isfile(self.Vfat_folder_dir+self.__SPLM[self.__SPno]+FIT_FPGA_FILE_NAME):
                        os.remove(self.Vfat_folder_dir+self.__SPLM[self.__SPno]+FIT_FPGA_FILE_NAME)

                    shutil.move(sof_file_dir+self.__SPLM[self.__SPno]+FIT_FPGA_FILE_NAME,  \
                        self.Vfat_folder_dir+self.__SPLM[self.__SPno])
            except Exception as ex:
                print('[ERROR]  Failed to move the rbf configuration '+ \
                    'file to the vfat folder MSG:'+str(ex))
                return False
        return True
    # @param rbf_dir            Direcotory of the FPGA-Configuration file 
    # @param fpga_linux_file    FPGA Configuration file name that are written by Linux
    # @param fpga_boot_file     FPGA Configuration file name that are written by the bootloader
    #                           '' -> Bootloader FPGA-Configuration file change disabled

    def startCopingFPGAconfig(self,rbf_dir,fpga_linux_file,fpga_boot_file):
        if not os.path.isdir(rbf_dir):
            print('[ERROR] The Direcotory of the FPGA-Configuration Folder on the Computer does not exsit!')
            return False
        if not os.path.isfile(rbf_dir+self.__SPLM[self.__SPno]+fpga_linux_file):
            print('[ERROR] The FPGA-Configuration for Linux file on the Computer does not exsit!\n'+\
                  '        File Dir: "'+rbf_dir+self.__SPLM[self.__SPno]+fpga_linux_file+'"')
            return False
        if not fpga_boot_file=='' and not os.path.isfile(rbf_dir+self.__SPLM[self.__SPno]+fpga_boot_file):
            print('[ERROR] The FPGA-Configuration for the bootloader file on the Computer does not exsit!\n'+\
                  '        File Dir: "'+rbf_dir+self.__SPLM[self.__SPno]+fpga_boot_file+'"')
            return False
        # Check that the SSH thread is running
        if not self.is_alive() or self.__queue == None: 
            print('[ERROR] The SSH Clinet Thread is not running!\n'+\
                  '        A upload of the FPGA-Configuration files via SFTP is not posibile!\n'+\
                  '        Check the output of the SSH Thread!')
            return False

        # Write the data to the Queue
        it =  [rbf_dir,fpga_linux_file,fpga_boot_file]
        self.__queue.put(it)

        return True


#
# @brief Prase input arguments to enable to special modes 
#        Read and store settings inside a XML file
#
def praseInputArgs():
    ### Progress the user arguments 
    arg_set_ip              = '' 
    arg_set_user            = ''
    arg_set_pw              = ''
    arg_set_flashBoot       = False
    arg_compile_project     = False
    arg_quartus_ver         = ''
    arg_use_jtag            = False

    flashBoot_chnaged       = False
    quartusver_changed      = False

    # Create the default XML setting file 
    if not os.path.exists(FLASHFPGA_SETTINGS_XML_FILE_NAME):
        with open(FLASHFPGA_SETTINGS_XML_FILE_NAME,"w") as f: 
            f.write(FLASHFPGA_SETTINGS_XML_FILE)
        print('[INFO] The XML setting file "'+FLASHFPGA_SETTINGS_XML_FILE_NAME+'" was created')


    # Was the script started with a additional argument specified?
    if len(sys.argv)>1:
        # Select the posibile input arguments 
        parser = argparse.ArgumentParser()
        parser.add_argument('-ip','--set_ipaddres', required=False, help='Set the IPv4 Address of the board')
        parser.add_argument('-us','--set_user',     required=False, help='Set the Linux username of the board')
        parser.add_argument('-pw','--set_password', required=False, help='Set the Linux user password of the board')
        parser.add_argument('-cf','--en_complie_project', required=False, help='Complile the Intel Quartus Prime '+\
                                  'FPGA project (use "-cf 1")')
        parser.add_argument('-fb','--en_flashBoot', required=False, \
                        help='Enable or Disable of the writing of the u-boot bootloader FPGA-Configuration file'\
                            'FPGA-Configuration [ 0: Disable]')
        
        parser.add_argument('-j','--use_jtag', required=False, \
                        help='Use JTAG via a JTAG Blaster to write the FPGA-Configuration (use "-j 1")')

        parser.add_argument('-qv','--set_quartus_prime_ver',required=False, \
            help=' Set the Intel Quartus Prime Version \n'+\
                 ' Note: Only requiered for FPGA Project Compilation! |\n'+\
                 ' Quartus Prime Version to use <Version><Version No> |\n'+\
                 '     L -> Quartus Prime Lite      (e.g. L16.1) |\n'+\
                 '     S -> Quartus Prime Standard  (e.g. S18.1) | \n'+\
                 '     P -> Quartus Prime Pro       (e.g. P20.1)\n')

        args = parser.parse_args()

        # Set the IP Address of the Board
        if args.set_ipaddres != None:
            # Check that the input is a vailed IPv4-Address 
            regex_pattern = "^([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$"
            if not bool( re.match( regex_pattern, args.set_ipaddres)):
                print('[ERROR] The given IP Address is not in the proper format (0.0.0.0)')
                sys.exit()
            arg_set_ip = args.set_ipaddres
            print('[INFO] IP Address of the board was set to "'+arg_set_ip+'"')

        # Set the Linux user name of the baord 
        if args.set_user != None: arg_set_user=args.set_user

        # Set the Linux user password of the baord
        if args.set_password != None: arg_set_pw=args.set_password

        # Complie the Intel Quartus Prime FPGA project
        if args.en_complie_project != None:
            try: tmp = int(args.en_complie_project)
            except Exception:
                print('[ERROR] Failed to convert the [--en_complie_project/-cf] input argument!')
                print('        Only integer numbers are allowed!')
                sys.exit()
            if tmp >0: 
                arg_compile_project= True
                print('[INFO] Compile the Intel Quartus Pirme FPGA Project is enabeled')

        # Set the Intel Quartus Prime project version
        if args.set_quartus_prime_ver != None:
            if re.match("^[LSP]+[0-9]+[.]+[0-9]?$",args.set_quartus_prime_ver, re.I) == None:
                print('[ERROR] The selected Quartus Version is in the wrong format!')
                print('        Quartus Prime Version to use <Version><Version No> \n'+\
                      '           L -> Quartus Prime Lite      (e.g. L16.1) \n'+\
                      '           S -> Quartus Prime Standard  (e.g. S18.1)  \n'+\
                      '           P -> Quartus Prime Pro       (e.g. P20.1)')
                sys.exit()
            arg_quartus_ver=args.set_quartus_prime_ver
            quartusver_changed = True
            print('[INFO] The Intel Quartus Prime Version is set to "'+arg_quartus_ver+'"')
            

        # Enable or Disable of the writing of the u-boot bootloader FPGA-Configuration file 
        if args.en_flashBoot != None:
            try: tmp = int(args.en_flashBoot)
            except Exception:
                print('[ERROR] Failed to convert the [--en_flashBoot/-fb] input argument!')
                print('        Only integer numbers are allowed!')
                sys.exit()
            flashBoot_chnaged = True
            if tmp==0: 
                print('[INFO] Writing of the u-boot FPGA-Configuration file disbaled')
                arg_set_flashBoot=False
            else:  
                print('[INFO] Writing of the u-boot FPGA-Configuration file enabled')
                arg_set_flashBoot=True

        # Use JTAG
        if args.use_jtag != None:
            try: tmp = int(args.use_jtag)
            except Exception:
                print('[ERROR] Failed to convert the [--use_jtag/-j] input argument!')
                print('        Only integer numbers are allowed!')
                sys.exit()
            if tmp >0: 
                arg_use_jtag= True
                print('[INFO] Use JTAG with a JTAG Blaster instate Network is enabled')


        ############################################ Write settings to a XML file ###########################################

        try:
            tree = ET.parse(FLASHFPGA_SETTINGS_XML_FILE_NAME)
            root = tree.getroot()
        except Exception as ex:
            print('[ERROR] Failed to prase the "'+FLASHFPGA_SETTINGS_XML_FILE_NAME+'" file!')
            print('        Msg.: '+str(ex))
            sys.exit()

        # Write the new IP address to the XML file
        if not arg_set_ip=='':
            for elem in root.iter('board'):
                elem.set('set_ip', arg_set_ip)

        # Write the new Linux User name to the XML file
        if not arg_set_user=='':
            for elem in root.iter('board'):
                elem.set('set_user', arg_set_user)

        # Write the new Linux User password to the XML file
        if not arg_set_pw=='':
            for elem in root.iter('board'):
                elem.set('set_pw', arg_set_pw)
        
        # Write the new Linux User password to the XML file
        if flashBoot_chnaged:
            for elem in root.iter('board'):
                if arg_set_flashBoot: elem.set('set_flashBoot','Y')
                else: elem.set('set_flashBoot','N')
        
        # Write the Intel Quartus Prime Version to the XML file
        if quartusver_changed:
            for elem in root.iter('board'):
                elem.set('set_quartus_prime_ver',arg_quartus_ver)

        # Flash settings
        tree.write(FLASHFPGA_SETTINGS_XML_FILE_NAME)

        # In set mode end script here 
        if  arg_set_ip or  arg_set_user or arg_set_pw or flashBoot_chnaged:
            sys.exit()

    ################################### Read the settings from the XML file  ##################################
    
    try:
        tree = ET.parse(FLASHFPGA_SETTINGS_XML_FILE_NAME)
        root = tree.getroot()
    except Exception as ex:
        print('[ERROR] Failed to prase the "'+FLASHFPGA_SETTINGS_XML_FILE_NAME+'" file!')
        print('        Msg.: '+str(ex))
        sys.exit()

    for part in root.iter('board'):
        try:
            arg_set_ip      = str(part.get('set_ip'))
            arg_set_user    = str(part.get('set_user'))
            arg_set_pw      = str(part.get('set_pw'))
            arg_set_pw      = str(part.get('set_pw'))
            arg_quartus_ver = str(part.get('set_quartus_prime_ver'))

            if str(part.get('set_flashBoot'))=='Y':
                arg_set_flashBoot = True
        except Exception as ex:
            print(' [ERROR] Decoding of the XML file "'+FLASHFPGA_SETTINGS_XML_FILE_NAME+\
                '" failed')
            print('         Msg.: '+str(ex))
            sys.exit()


      
    return arg_set_ip, arg_set_user,arg_set_pw,arg_set_flashBoot,arg_compile_project,arg_quartus_ver,arg_use_jtag

############################################                                ############################################
############################################             MAIN               ############################################
############################################                                ############################################

if __name__ == '__main__':

    ############################################ Runtime environment check ###########################################

    # Check properly Python Version
    if sys.version_info[0] < 3:
        print('[ERROR] This script can not work with your Python Version!')
        print("        Use Python 3.x for this script!")
        sys.exit()

    if sys.platform =='linux': SPno = 0
    else:  SPno = 1

    SPLM = ['/','\\'] # Linux, Windows 

    # Enable and read input arguments or the settings from a XML file
    arg_set_ip, arg_set_user,arg_set_pw,arg_set_flashBoot,\
        arg_compile_project,arg_quartus_ver,arg_use_jtag  = praseInputArgs()

    ############################################################################################################################################
    arg_use_jtag = True
    ############################################################################################################################################

    print('****** Flash FPGA Configuration to rsyocto via SSH/SFTP or JTAG  (Ver.: '+version+') ******')

    #
    ## 1. Step: Read the execution environment and scan the Intel Quartus Prime FPGA project
    #
    flashFPGA2Linux = FlashFPGA2Linux(arg_set_ip, arg_set_user,\
                        arg_set_pw,arg_compile_project,arg_quartus_ver,arg_use_jtag)

    #
    ## 2.Step: Check the network connection to the baord
    #          --> Only requiered for the non JTAG mode
    #
    if not arg_use_jtag:
        if not flashFPGA2Linux.CheckNetworkConnection2Board():
            print('[ERROR] It was not posibile to ping rsyocto with the given IP-Address '+\
                '"'+arg_set_ip+'"!\n'+\
                '        Please check the network connection of this computer'+\
                ' and of the SoC-FPGA board\n'+\
                '        You can change the IP-Address with the attribute: "-ip"')
            sys.exit()
        #
        ## 3. Step: Start the SSH/SFT Thread to establish a connection
        #
        flashFPGA2Linux.EstablishSSHcon()

        #
        ## 4. Step: Generate the FPGA-Configuration files
        #
        rbf_dir =  flashFPGA2Linux.Quartus_proj_top_dir+SPLM[SPno]+flashFPGA2Linux.Sof_folder

        # Generate a FPGA Configuration file that can be written by Linux (rsyocto)
        linux_fpga_file_name = 'rsyocto_fpga_conf.rbf'
        if not flashFPGA2Linux.GenerateFPGAconf(True,linux_fpga_file_name,rbf_dir):
            print('[ERROR] Failed to generate the Linux FPGA-Configuration file')
            sys.exit()

        # Generate a FPGA Configuration file that can be written by u-boot
        boot_fpga_file_name= ''
        if arg_set_flashBoot:
            boot_fpga_file_name= 'socfpga.rbf'
            if not flashFPGA2Linux.GenerateFPGAconf(False,boot_fpga_file_name,rbf_dir):
                print('[ERROR] Failed to generate the u-boot (bootloader) FPGA-Configuration file')
                sys.exit()
        
    #
    ## 5.Step: Coyp the FPGA-Configuration files via SSH to rsyocto and write the FPGA-Fabric with it
    #
    if arg_use_jtag:
        # Write the FPGA-Configuration only with JTAG
        flashFPGA2Linux.command_jtag_writeConfRAM()
    else:
        flashFPGA2Linux.startCopingFPGAconfig(rbf_dir,linux_fpga_file_name,boot_fpga_file_name)

        # Wait until the SSH Thread is done
        flashFPGA2Linux.join()

        # Remove the FPGA-Configuration files from the Intel Quartus Prime Project folder 
        if os.path.isfile(rbf_dir+SPLM[SPno]+linux_fpga_file_name):
            try:
                os.remove(rbf_dir+SPLM[SPno]+linux_fpga_file_name)
            except Exception:
                pass
        if arg_set_flashBoot and os.path.isfile(rbf_dir+SPLM[SPno]+boot_fpga_file_name):
            try:
                os.remove(rbf_dir+SPLM[SPno]+boot_fpga_file_name)
            except Exception:
                pass
    if flashFPGA2Linux.ThreadStatus:
        print('[SUCCESS] Support the author Robin Sebastian (git@robseb.de)')
# EOF
