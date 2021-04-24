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
# (2021-04-23) Vers.1.0 
#   first Version 
#

version = "1.0"

#
#
#
############################################ Const ###########################################
#
#
#

DELAY_MS = 1 # Delay after critical tasks in milliseconds 

QURTUS_DEF_FOLDER         = "intelFPGA"
QURTUS_DEF_FOLDER_LITE    = "intelFPGA_lite"
EDS_EMBSHELL_DIR          = ["/embedded/embedded_command_shell.sh","\\embedded\\embedded_command_shell.bat"]

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
    '<FlashFPGA2Linux>\n'+\
    '   <board set_ip="192.168.0.165" set_user="root" set_pw="eit" set_flashBoot="Y" />\n'+\
    '</FlashFPGA2Linux>\n'
    

RSYOCTO_BANNER_CHECK_LINE =  ['created by Robin Sebastian (github.com/robseb)', \
                              'Contact: git@robseb.de', \
                              'https://github.com/robseb/rsyocto'\
                             ]
RSYOCTO_FPGAWRITECONF_CHECK = 'Command to change the FPGA fabric configuration'

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
import time
import shutil
import re
from threading import Thread
import subprocess
from subprocess import DEVNULL
import xml.etree.ElementTree as ET
import glob
from pathlib import Path
import argparse

    
# 
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
    board_ip_addrs              : ''  # IPv4 Address of the SoC-FPGA Linux Distribution (rsyocto)
    board_user                  : ''  # SoC-FPGA Linux Distribution (rsyocto) Linux user name
    board_pw                    : ''  # SoC-FPGA Linux Distribution (rsyocto) Linux user password

    ## Network related properties

    __sshClient                 : paramiko # Object of SSH client connection to the baord 

    __SPLM = ['/','\\']               # Slash for Linux, Windows 
    __SPno = 0                        # OS ID 0=Linux | 1=Windows 

    #
    # @brief Constructor
    # @param board_ip_addrs     IPv4 Address of the SoC-FPGA Linux Distribution (rsyocto)
    #                           Format 100.100.100.100
    # @param board_user         SoC-FPGA Linux Distribution (rsyocto) Linux user name
    # @param board_pw           SoC-FPGA Linux Distribution (rsyocto) Linux user password
    #
    def __init__(self,board_ip_addrs, board_user,board_pw):
        
        # Read the input paramters 
        regex_pattern = "^([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$"
        if not bool( re.match( regex_pattern, board_ip_addrs)):
            print('[ERROR] The given IP Address is not in the proper format (0.0.0.0)')
            sys.exit()

        self.board_ip_addrs = board_ip_addrs
        self.board_user     = board_user
        self.board_pw       = board_pw
        
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
        self.Sof_folder = ''
        # Looking in the top folder for the sof file
        for file in os.listdir(self.Quartus_proj_top_dir):
                if ".sof" in file:
                    self.Sof_file_name =file
                    break
        if self.Sof_file_name == '':
            # Looking inside the "output_files" and "output" folders
            if os.path.isdir(self.Quartus_proj_top_dir+'/output_files'):
                self.Sof_folder = '/output_files'
            if os.path.isdir(self.Quartus_proj_top_dir+'/output'):
                self.Sof_folder = '/output'
            for file in os.listdir(self.Quartus_proj_top_dir+self.Sof_folder):
                if ".sof" in file:
                    self.Sof_file_name =file
                    break
            
        # Find the Platform Designer (.qsys) file  
        self.Qsys_file_name = ''
        for file in os.listdir(self.Quartus_proj_top_dir):
                if ".qsys" in file and not ".qsys_edit" in file:
                    self.Qsys_file_name =file
                    break

        # Does the SOF file contains an IP with a test licence, such as a NIOS II Core?
        self.unlicensed_ip_found=False
        if self.Sof_file_name.find("_time_limited")!=-1:
            print('********************************************************************************')
            print('*                 Unlicensed IP inside the project was found!                  *')
            print('*            Generation of the ".rbf"- FPGA-Configuration is not enabled       *')
            print('********************************************************************************\n')
            self.unlicensed_ip_found=True
            sys.exit()


        # Find the Platform Designer folder
        if self.Qsys_file_name=='' or self.Qpf_file_name=='' or self.Sof_file_name=='':
            print('\n[ERROR]  The script was not executed inside the cloned Github- and Quartus Prime project folder!')
            print('           Please clone this script with its folder from Github,')
            print('           copy it to the top folder of your Quartus project and execute the script')
            print('           directly inside the cloned folder!')
            print(' NOTE:     Be sure that the QPF,SOF and QSYS folder was found!')
            print('           These files must be in the top project folder')
            print('           The SOF file can also be inside a sub folder with the name "output_files" and "output"')
            print('           URL: '+GIT_SCRIPT_URL+'\n')
            print('       --- Required folder structure  ---')
            print('          YOUR_QURTUS_PROJECT_FOLDER ')
            print('       |     L-- PLATFORM_DESIGNER_FOLDER')
            print('       |     L-- platform_designer.qsys')
            print('       |     L-- _handoff')
            print('       |     L-- quartus_project.qpf')
            print('       |     L-- socfpgaPlatformGenerator <<<----')
            print('       |         L-- socfpgaPlatformGenerator.py')
            print('       Note: File names can be chosen freely\n')
            print('NOTE: It is necessary to build the Prime Quartus Project for the bootloader generation!')
            sys.exit()

        # Find the handoff folder
        self.Handoff_folder_name = ''
        handoff_folder_start_name =''
        for file in os.listdir(self.Quartus_proj_top_dir):
                if "_handoff" in file:
                    handoff_folder_start_name =file
                    break
        folder_found = False
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
        
            ## NOTE: ADD ARRIA V/ SUPPORT HERE 
        else:
            print('[ERROR]  Your Device ('+device_name_temp+') is not supported right now!')
            print('         I am working on it...')
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

        print('[INFO] A valid Intel Quartus Prime '+device_name_temp+' SoC-FPGA project was found') 


    def __ping(self, host_or_ip, packets=1, timeout=1000):
        ''' Calls system "ping" command, returns True if ping succeeds.
        Required parameter: host_or_ip (str, address of host to ping)
        Optional parameters: packets (int, number of retries), timeout (int, ms to wait for response)
        Does not show any output, either as popup window or in command line.
        Python 3.5+, Windows and Linux compatible (Mac not tested, should work)
        '''
        # The ping command is the same for Windows and Linux, except for the "number of packets" flag.
        if platform.system().lower() == 'windows':
            command = ['ping', '-n', str(packets), '-w', str(timeout), host_or_ip]
            # run parameters: capture output, discard error messages, do not show window
            result = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, creationflags=0x08000000)
            # 0x0800000 is a windows-only Popen flag to specify that a new process will not create a window.
            # On Python 3.7+, you can use a subprocess constant:
            #   result = subprocess.run(command, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
            # On windows 7+, ping returns 0 (ok) when host is not reachable; to be sure host is responding,
            # we search the text "TTL=" on the command output. If it's there, the ping really had a response.
            return result.returncode == 0 and b'TTL=' in result.stdout
        else:
            command = ['ping', '-c', str(packets), '-w', str(timeout), host_or_ip]
            # run parameters: discard output and error messages
            result = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return result.returncode == 0


    #
    # @brief    Check the Network connection from the development machine to the embedded Linux Distribution
    # @return   Pinging the board was successful
    #
    def CheckNetworkConnection2Board(self):
        return self.__ping(self.board_ip_addrs)
        
    #
    # @brief    Establish a SSH connection the SoC-FPGA baord running rsyocto
    # @return   success
    #
    def EstablishSSHcon(self):
        Thread.__init__(self)
        self.start()
        return False


    def __sendCmd(self,cmd=''):
        ssh_stdin, ssh_stdout, ssh_stderr = self.__sshClient.exec_command(cmd)
        err = ssh_stderr.read().decode("utf-8") 
        if not err == '':
            print('[ERROR] Failed to execute a Linux cmd via SSH!\n'+\
                  '        CMD  : "'+cmd+'"\n'+\
                  '        ERROR: "'+err+'"')    
            return ''

        return ssh_stdout.read().decode("utf-8") 

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
    # @breif Override the run() function of Thread class
    #        Thread to for handling the SSH connection to SoC-FPGA baord
    #
    def run(self):
        print('[INFO] Start to establish a SSH connection to the board')

        # Start a new SSH client connection to the development board
        self.__sshClient = None
        self.__sshClient = paramiko.SSHClient()
        self.__sshClient.load_system_host_keys()
        warnings.filterwarnings("ignore")
        self.__sshClient.set_missing_host_key_policy(paramiko.WarningPolicy())
        paramiko.util.log_to_file(self.Quartus_proj_top_dir+self.__SPLM[self.__SPno]+'sshClientlog.txt')
        
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
                self.__sshClient.close()
                sys.exit()
    
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
                self.__sshClient.close()
                sys.exit()

            # Check that the "FPGA-writeConfig" command is available 
            #
            fpga_writecmd_ret = self. __sendCmd("FPGA-writeConfig") 
            if not RSYOCTO_FPGAWRITECONF_CHECK in fpga_writecmd_ret:
                print('[ERROR] The connect rsyocto Linux Distribution has no '+\
                      '"FPGA-writeConfig" Linux command of the rstools installed! \n'+\
                      '        This command allows to write the FPGA-Configuration and is need by this script!')
                self.__sshClient.close()
                sys.exit()
            
            # Check that enough memory space is available on rsyocto for 
            # uploading the FPGA configuration files
            cmd = 'df'
            diskpace = self.__decodeDiskSpace(self. __sendCmd(cmd))
            if diskpace==-1: 
                print('[ERROR] Failed to get the available diskpace from the embedded Linux')  
                self.__sshClient.close()
                sys.exit()
            elif diskpace >= 99:
                print('[ERROR] It is not enough diskspace left on rsyocto on the SoC-FPGA board \n'+\
                      '        for uploading the FPGA-Configuration!\n'+\
                      '        Disk space on the rootfs used: '+str(diskpace)+'%\n'+\
                      '        At least 1% must be free available!')
                self.__sshClient.close()
                sys.exit()

            print('[INFO] SSH Connection established to rsyocto ('+\
                str(100-diskpace)+'% free space remains on the rootfs)')
            
        
        except paramiko.ssh_exception.SSHException as ex: 
            print('[ERROR] Failed to open network connection!\n'+
            '              Msg.: "'+str(ex)+'"')

        self.__sshClient.close()
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
            print('       is for the Arria 10 SX right now not supported!')
            return True

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
                    print('       with the output name "'+linux_filename+'"')

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
                    print('       with the output name "'+linux_filename+'"')

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

    flashBoot_chnaged       = False

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
        parser.add_argument('-fb','--en_flashBoot', required=False, \
                        help='Enable or Disable of the writing of the u-boot bootloader FPGA-Configuration file'\
                            'FPGA-Configuration [ 0: Disable]')

        args = parser.parse_args()

        # Set the IP Address of the Board
        if args.set_ipaddres != None:
            # Check that the input is a vailed IPv4-Address 
            regex_pattern = "^([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$"
            if not bool( re.match( regex_pattern, args.set_ipaddres)):
                print('[ERROR] The given IP Address is not in the proper format (0.0.0.0)')
                sys.exit()
            arg_set_ip = args.set_ipaddres

        # Set the Linux user name of the baord 
        if args.set_user != None: arg_set_user=args.set_user

        # Set the Linux user password of the baord
        if args.set_password != None: arg_set_pw=args.set_password

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
        # Flash settings
        tree.write(FLASHFPGA_SETTINGS_XML_FILE_NAME)

        # In set mode end script here 
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
            arg_set_ip = str(part.get('set_ip'))
            arg_set_user = str(part.get('set_user'))
            arg_set_pw = str(part.get('set_pw'))

            if str(part.get('set_flashBoot'))=='Y':
                arg_set_flashBoot = True
        except Exception as ex:
            print(' [ERROR] Decoding of the XML file "'+FLASHFPGA_SETTINGS_XML_FILE_NAME+\
                '" failed')
            print('         Msg.: '+str(ex))
            sys.exit()


      
    return arg_set_ip, arg_set_user,arg_set_pw,arg_set_flashBoot

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
    arg_set_ip, arg_set_user,arg_set_pw,arg_set_flashBoot = praseInputArgs()
    
    #
    ## 1. Step: Read the execution environment and scan the Intel Quartus Prime FPGA project
    #
    flashFPGA2Linux = FlashFPGA2Linux(arg_set_ip, arg_set_user,arg_set_pw)

    #
    ## 2.Step: Check the network connection to the baord
    #
    if not flashFPGA2Linux.CheckNetworkConnection2Board():
        print('[ERROR] It was not posibile to ping rsyocto with the given IP-Address '+\
              '"'+arg_set_ip+'"!\n'+\
              '        Please check the network connection of this computer'+\
              ' and of the SoC-FPGA board\n'+\
              '        You can change the IP-Address with the attribute: "-ip"')
        sys.exit()

    #
    ## 3. Step: Generate the FPGA-Configuration that can be written with Linux 
    #
    '''
    rbf_dir =  flashFPGA2Linux.Quartus_proj_top_dir+SPLM[SPno]+flashFPGA2Linux.Sof_folder

    # Generate a FPGA Configuration file that can be written by Linux (rsyocto)
    if not flashFPGA2Linux.GenerateFPGAconf(True,'rsyocto_fpga_conf.rbf',rbf_dir):
        print('[ERROR] Failed to generate the Linux FPGA-Configuration file')
        sys.exit()

    # Generate a FPGA Configuration file that can be written by u-boot
    if arg_set_flashBoot:
        if not flashFPGA2Linux.GenerateFPGAconf(False,'socfpga.rbf',rbf_dir):
            print('[ERROR] Failed to generate the u-boot (bootloader) FPGA-Configuration file')
            sys.exit()
    '''
    #
    ## 4. Step: Establish a SSH Connection to the embedded baord
    #
    if not flashFPGA2Linux.EstablishSSHcon():
        sys.exit()

    print('[SUCCESS] Support the author Robin Sebastian (git@robseb.de)')
# EOF
