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
# Python support script for "makersyoctoSDImage.py"
# to change the rootfs automatically with super privileges 
# 
#


import os
import sys
import getopt
import shutil

ROOLBACK_FPGACONF_DIR = '/usr/rsyocto'
ROOLBACK_FPGACONF_NAME = 'running_bootloader_fpgaconfig.rbf'

NETWORKCONF_TMP_NAME = 'network_interface_temp_file.txt'


############################################                                ############################################
############################################             MAIN               ############################################
############################################                                ############################################

if __name__ == '__main__':
    
    rootfs_dir =''
   ############################################ Runtime environment check ###########################################
    if not len(sys.argv) == 3:
        print('ERROR: This script can only called by "makersyoctoSDImage.py" ')
        print('       Please start "makersyoctoSDImage.py" instead !')
        sys.exit()

    # Read the rootfs dir as input argument 
    try:
        opts, args = getopt.getopt(sys.argv[1:],"r:","rootfs_dir=")
    except getopt.GetoptError as ex:
        print('ERROR: This script can only called by "makersyoctoSDImage.py" ')
        print('       Please start "makersyoctoSDImage.py" instead !')
        print('  MSG: '+str(ex))
        sys.exit()

    for opt, arg in opts:
        if opt in ("-r", "--rootfs_dir"):
            rootfs_dir = arg
        else:
            print('ERROR: This script can only called by "makersyoctoSDImage.py" ')
            print('       Please start "makersyoctoSDImage.py" instead !')
            print('  MSG: '+str(ex))
            sys.exit()

    # Check proper Python Version
    if sys.version_info[0] < 3:
        print('ERROR: This script can not work with your Python Version!')
        print("Use Python 3.x for this script!")
        sys.exit()

    # Check that the Version runs on Linux
    if not sys.platform =='linux':
        print('ERROR: This script only works on Linux!')
        print("Please run this script on a Linux Computer!")
        sys.exit()

    if os.geteuid() != 0:
        print('ERROR: This script requires root privileges!')
        sys.exit()

    # Check that the rootfs folder exists  
    if not (os.path.isdir(rootfs_dir+'/bin') and \
        os.path.isdir(rootfs_dir+'/sys')):
        print('ERROR: The rootfs directory is not valid!')
        print('       Dir: "'+rootfs_dir+'"')
        sys.exit()

    print('********************************************************************************')
    print('*                    Changing the rootfs with root privileges                  *')
    print('********************************************************************************\n')

#######################################    ROOTFS Changes   #######################################

    ext = os.getcwd()+'/'

    ################### Changing the SSH authentication to "Linux User Password" ###################

    print("--> Changing the SSH authentication to \"Linux User Password\"")
    
    if os.path.isfile(rootfs_dir+'/etc/ssh/sshd_config'):
        with open(rootfs_dir+"/etc/ssh/sshd_config", "a") as f:
            f.write("\nPermitRootLogin yes\n")
            f.write("Banner etc/issue")
    else:
        print('WARNING: The "/etc/ssh/sshd_config" did not exist')


    # Enable NETBIOS with the machine name
    if  os.path.isfile(rootfs_dir+"/etc/nsswitch.conf"):
        print('--> Enable the NETBIOS')

        fd=open(rootfs_dir+"/etc/nsswitch.conf",'r+') 
        dnsraw=''
        dnstartPos =0

        for x in fd.readlines():
            dnsraw= dnsraw+x

        dnstartPos = dnsraw.find('files dns')
        
        if not (dnstartPos > -1):
            print('WARNING: The "/etc/nsswitch.conf" file is not in the right format')
        else:
            dnsrawNew = dnsraw[:dnstartPos] +" files dns wins \n"+dnsraw[dnstartPos+10:]
            fd.truncate(0)
            fd.close()

            with open(rootfs_dir+"/etc/nsswitch.conf", "a") as f3:
                f3.write(dnsrawNew)

            print('      = Done')
    else:
        print('WARNING: The "/etc/nsswitch.conf" file is not available!')

    # Remove the HWCLOCK Initialization script from the rootFs 
    if os.path.isfile(rootfs_dir+"/etc/init.d/hwclock.sh") : 
        print('-->  Removing the "hwclock.sh" initialization script')
        try:
            os.remove(rootfs_dir+"/etc/init.d/hwclock.sh")
        except IOError:
            print ("\nWARNING: Removing \"hwclock.sh\" failed!")

    # Move the rollback FPGA configuration to the rootfs
    if not os.path.isdir(rootfs_dir+ROOLBACK_FPGACONF_DIR):
        print('\nWARNING: The rootfs FPGA configuration rollback dir does not exist!')
    else:   
        if os.path.isfile(ext+ROOLBACK_FPGACONF_NAME):
            print('--> Move the rollback FPGA configuration file to the rootfs')
            try:
                shutil.move(ext+ROOLBACK_FPGACONF_NAME, \
                    rootfs_dir+ROOLBACK_FPGACONF_DIR+'/')
            except IOError:
                print('\nWARNING: Moving the rollback FPGA configuration file failed!')
        else:
            print ("\nWARNING: Moving the rollback FPGA configuration file does not exist!")

    # Change the Linux network interface configurations

    ################### Change the network configurations  ###################

    # Copy a new network interface file to the rootfs only when the file is there
    if os.path.isfile(ext+NETWORKCONF_TMP_NAME): 
        print('--> Change the Linux network settings')
        try:
            shutil.move(ext+NETWORKCONF_TMP_NAME, rootfs_dir+'/etc/network/interfaces')
        except IOError:
            print('\nWARNING: Failed to move the network interface file to the rootfs!')
    else:
        print('\nWARNING: There is no Linux network interface file available!')


    print('********************************************************************************\n')
#EOF