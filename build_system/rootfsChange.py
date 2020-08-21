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


############################################                                ############################################
############################################             MAIN               ############################################
############################################                                ############################################

if __name__ == '__main__':
    
    rootfs_dir =''
   ############################################ Runtime environment check ###########################################
    if not len(sys.argv) == 3:
        print('ERROR: This script can only called by "makersyoctoSDImage.py" ')
        print('       Please start "makersyoctoSDImage.py" instate !')
        sys.exit()

    # Read the rootfs dir as input argument 
    try:
        opts, args = getopt.getopt(sys.argv[1:],"r:","rootfs_dir=")
    except getopt.GetoptError as ex:
        print('ERROR: This script can only called by "makersyoctoSDImage.py" ')
        print('       Please start "makersyoctoSDImage.py" instate !')
        print('  MSG: '+str(ex))
        sys.exit()

    for opt, arg in opts:
        if opt in ("-r", "--rootfs_dir"):
            rootfs_dir = arg
        else:
            print('ERROR: This script can only called by "makersyoctoSDImage.py" ')
            print('       Please start "makersyoctoSDImage.py" instate !')
            print('  MSG: '+str(ex))
            sys.exit()

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

    if os.geteuid() != 0:
        print('ERROR: This script requirers root privileges!')
        sys.exit()

    # Check that the rootfs folder exist  
    if not (os.path.isdir(rootfs_dir+'/bin') and \
        os.path.isdir(rootfs_dir+'/sys')):
        print('ERROR: The rootfs directory is not valied!')
        print('       Dir: "'+rootfs_dir+'"')
        sys.exit()

    print('********************************************************************************')
    print('*                    Change the rootfs with root privileges                    *')
    print('********************************************************************************\n')

####################################### Script based ROOTFS Changes #######################################

    ################### Changing the SSH authentication to "Linux User Password" ###################

    print("--> Changing the SSH authentication to \"Linux User Password\"")
    
    if os.path.isfile(rootfs_dir+'/etc/ssh/sshd_config'):
        with open(rootfs_dir+"/etc/ssh/sshd_config", "a") as f:
            f.write("\nPermitRootLogin yes\n")
            f.write("Banner etc/issue")
    else:
        print('WARNING: The "/etc/ssh/sshd_config" did not exist')

    '''
    # Check if the rsyocto folder is inside the rootfs
    if not os.path.isdir(rootfs_dir+"/usr/rsyocto"):
        try:  
            os.mkdir(rootfs_dir+"/usr/rsyocto")
        except OSError:  
            print ("Creation of the new directory \"rsyocto\" inside the rootfs failed!")
            sys.exit()
    
    # Write the Version No to the rootfs
    print ("--> Writing the Version Number to the rootfs\n")    
    try:
        fp = open(rootfs_dir+'/usr/rsyocto/version.txt')
    except IOError:
        # If it do not exist, create the file
        fp = open(rootfs_dir+'/usr/rsyocto/version.txt', 'w+')

    with open(rootfs_dir+"/usr/rsyocto/version.txt", "a") as f:   
        f.write(str(nb))    

    '''
    '''
    # Copy a new network interface file to the rootfs only when the file is there
    if nwifcopy: 
        shutil.copyfile('network_interfaces.txt', rootfs_dir+'/etc/network/interfaces') 
        print ("--> the network interface settings are written\n")    
    '''

    ## Board Selection 
    '''
    print("--> Decoding the Board selection\n")
    now = datetime.datetime.now()
    path = os.getcwd()

    print('\n ***************\ GENERATING IMAGE FOR  '+BOARD_NAME[BOARD_ID]+" ***************\n")

    ################### add the Bootloader FPGA Configuration to the rootfs ###################

    # Writing the name of the supported Board to the file System
    try:
        fp = open(rootfs_dir+'/usr/rsyocto/suppBoard.txt')
    except IOError:
        # If it does not exist, create the file
        fp = open(rootfs_dir+'/usr/rsyocto/suppBoard.txt', 'w+')

    print('-->  Writing the name of the supported board to the rootfs\n')
    with open(rootfs_dir+"/usr/rsyocto/suppBoard.txt", "a") as f:   
        f.write(BOARD_NAME[BOARD_ID])    
    '''

    # Enable NETBIOS with the machine name
    if  os.path.isfile(rootfs_dir+"/etc/nsswitch.conf"):
        print('--> Enable the NETBIOS\n')

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

    # Remove the HWCLOCK Init script from the rootFs 
    if os.path.isfile(rootfs_dir+"/etc/init.d/hwclock.sh") : 
        print('-->  Removing the "hwclock.sh" init script')
        try:
            os.remove(rootfs_dir+"/etc/init.d/hwclock.sh")
        except IOError:
            print ("WARNING: Removing \"hwclock.sh\" failed!")

   
    print('********************************************************************************\n')
#EOF