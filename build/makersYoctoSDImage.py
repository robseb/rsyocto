#!/usr/bin/env python
#
#            ########   ######     ##    ##  #######   ######  ########  #######                  
#            ##     ## ##    ##     ##  ##  ##     ## ##    ##    ##    ##     ##           
#            ##     ## ##            ####   ##     ## ##          ##    ##     ##        
#            ########   ######        ##    ##     ## ##          ##    ##     ##       
#            ##   ##         ##       ##    ##     ## ##          ##    ##     ##      
#            ##    ##  ##    ##       ##    ##     ## ##    ##    ##    ##     ##        
#            ##     ##  ######        ##     #######   ######     ##     #######         
#
#
#
# Robin Sebstian (https://github.com/robseb)
#
# 22-05-2019 (Vers. 1.2) 
# Python Script for automatic SD Card image Build with all necessary files
# with automatic rootfs changes 
# with SSH change to user mode 
#
#10-08-2019 (Vers. 1.4)
# Splach screen integration  
#
#11-08-2019 (Vers. 1.5)
# Suppored for multibile target Boards 
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
#02-12-2012 (Vers. 2.0)
#  Github ready version
# 

version = "2.0"

#
# #################### CHANGE HERE THE ADDITIONAL ROOTFS SPACE FOR USER SPACE ####################
#
# Size of the available User Space in Mega Byte (MB) (is exclude changes of rootfs 
#   during the execution of this script)
#
USER_SPACE_SIZE_MB =600 # 600MB 
#
###################################################################################################
#
#

import os
import sys
from zipfile import ZipFile as zip
import math
import shutil
import datetime

def getFolderSize(start_path='.'):
    total_size = 0
    seen = {}
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                stat = os.stat(fp)
            except OSError:
                continue

            try:
                seen[stat.st_ino]
            except KeyError:
                seen[stat.st_ino] = True
            else:
                continue

            total_size += stat.st_size

    return total_size

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "K", "M", "G", "T", "P", "E", "Z", "Y")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = math.ceil(size_bytes / p)
   s = round(s,0)
   s = int(s)
   return "%s %s" % (s, size_name[i])

def extractAll(zipName):
    z = zip(zipName)
    for f in z.namelist():
        if f.endswith('/'):
            os.makedirs(f)
        else:
            z.extract(f)

USER_SPACE_SIZE    = USER_SPACE_SIZE_MB * 1000000

if __name__ == '__main__':
    print("AUTOMATIC SCRIPT FOR BUILDING A SD CARD IMAGE with rsYocto")
    print(" by Robin Sebastian (https://github.com/robseb) Vers.: "+version)
    print("This script requires a SD-Card folder\n\n")

    filesthere = True
    a10detect = False
    includeLinuxRbf = True

    ################################################ Input Check ################################################
    #############  check if all necessary are at this path ###################

    if os.path.isfile("preloader_a10.bin") and os.path.isfile("rootfs_a10.tar.gz"):
        a10detect=True

    if not (os.path.isfile("rootfs_cy5.tar.gz") or  os.path.isfile("rootfs_a10.tar.gz")):
        print("ERROR: The File \"rootfs_cy5.tar.gz\" or \"rootfs_a10.tar.gz\"  is not there!")
        filesthere = False

    if not os.path.isfile("make_sdimage.py")  :
        print("ERROR: The File \"make_sdimage.py\" is not there!")
        filesthere = False

    if not (os.path.isfile("preloader_cy5.bin")  or (a10detect)):
        print("ERROR: The File \"preloader_cy5.bin\" or \"preloader_a10.bin\" is not there!")
        filesthere = False

    if not (os.path.isfile("uboot_cy5.img") or  os.path.isfile("uboot_a10.img")):
        print("ERROR: The File \"uboot_cy5.img\" or \"uboot_a10.img\" is not there!")
        filesthere = False

    if not (os.path.isfile("uboot_cy5.scr")  or  os.path.isfile("uboot_a10.scr")):
        print("ERROR: The File \"uboot_cy5.scr\" or \"uboot_a10.scr\" is not there!")
        filesthere = False

    if not (os.path.isfile("zImage_cy5")  or  os.path.isfile("zImage_a10"))  :
        print("ERROR: The File \"zImage_cy5\" or \"zImage_a10\"  is not there!")
        filesthere = False

    if not (os.path.isfile("socfpga_cy5.dts") or  os.path.isfile("socfpga_a10.dts")) :
        print("ERROR: The File \"socfpga_cy5.dts\" or \"socfpga_a10.dts\" is not there!")
        filesthere = False

    if not (os.path.isfile("socfpga_nano.rbf") or os.path.isfile("socfpga_std.rbf") or os.path.isfile("socfpga_han_periph.rbf")) :
        print("ERROR: The File \"socfpga_nano.rbf\" , \"socfpga_std.rbf\" or \"socfpga_han_periph.rbf\" is not there!")
        filesthere = False

    if (not os.path.isfile("socfpga_han_core.rbf")) and (a10detect):
        print("ERROR: The File \"socfpga_han_core.rbf\" is not there!")
        filesthere = False

    if not os.path.isfile("infoRSyocto.txt") :
        print("ERROR: The File \"infoRSyocto.txt\" is not there!")
        filesthere = False

    if not (os.path.isfile("socfpga_nano_linux.rbf") or os.path.isfile("socfpga_std_linux.rbf") or (a10detect)):
        print("Warning: The File \"socfpga_nano_linux.rbf\" or \"socfpga_std_linux.rbf\"  is not there!")
        includeLinuxRbf = False

    if not filesthere: 
        print("------------------------------------------------------")
        print("Insert the missing files to this folder and try again!")
        print("For more information's please follow the rsYocto documentation\n")
        print("https://github.com/robseb/rsyocto\n")
        sys.exit()
    ################################################ Detect the board Type ################################################

    # BoardType = 0 -> all Boards
    # BoardType = 1 -> DE10 Nano
    # BoardType = 2 -> DE10 Standard
    # BoardType = 3 -> HAN Pilot Arria 10 
    BoardType =0
    BoardCounter =0
    BoardNano =False
    BoardStandard =False
    BoardHan=False

    BoardName = ['Terasic DE10 Standard and Nano','Terasic DE10 Nano','Terasic DE10 Standard','Terasic HAN Pilot']
    FPGAName = ['unknown','Intel Cyclone V','Intel Cyclone V','Intel Arria 10 SX']
    rootfsFolderName = ['rootfs_cy5', 'rootfs_a10']

    if (os.path.isfile("socfpga_nano.rbf")) :
        BoardType = 1
        BoardNano =True
        BoardCounter+=1
    if (os.path.isfile("socfpga_std.rbf")) :
        BoardType = 2
        BoardStandard=True
        BoardCounter+=1
    if (a10detect) :
        BoardType = 3
        BoardHan=True
        BoardCounter+=1

    if(BoardCounter >1):

        print('\n --- Please select the name of the Target Board ---\n')

        if(BoardNano):
            print('  Input : 1 -> Terasic DE10 Nano \n')
        if(BoardStandard):
            print('  Input : 2 -> Terasic DE10 Standard \n')
        if(BoardHan):
             print('  Input : 3 -> Terasic HAN Pilot \n')

        BoardType = input('Please input a version Number:')

        if(not ((BoardType >0) and ((BoardNano) and  (BoardType == 1)) or ((BoardStandard) and  (BoardType == 2 )) or ((BoardHan) and  (BoardType == 3 )) )):
            print("Error the Input is value is not vailed")
            ays.exit()

        BoardNano = False
        BoardStandard  = False
        BoardHan = False 

        if(BoardType == 1):
            BoardNano =True
        elif(BoardType == 2):
            BoardStandard=True
        else:
            BoardHan = True

    print ('This script will generate the image for following Board/s: ' + str(BoardName[BoardType]))

    print('Selected Available User space: '+str(USER_SPACE_SIZE_MB)+' MB\n')

    ################################################ unzip of the rootFs archive  ################################################

    ###### rename the rootfs folder ###### 
    if(BoardNano or BoardStandard):
        os.rename('rootfs_cy5.tar.gz','rootfs.tar.gz') 
    else :
        os.rename('rootfs_a10.tar.gz','rootfs.tar.gz') 

    #############  create rootfs folder ###################
    
    # delate an old rootfs folder
    
    if os.path.isdir("rootfs"):
    #    try:  
    #        os.removedirs("rootfs")
    #    except OSError:  
    #        print ("ERROR: Deleting of the old \"rootfs\" folder failed!")
    #        sys.exit()
        os.system("sudo rm -r rootfs")

    if os.path.isfile("rootfs.tar.gz"):
         # for the standard tar.gz format directly from Yocto's output
        try:  
            os.mkdir("rootfs")
        except OSError:  
            print ("Creation of the new directory \"rootfs\" failed!")
            sys.exit()

        ####### Insert the compressed rootfs to the rootfs folder
        os.system("sudo cp -v rootfs.tar.gz /rootfs")
        os.system("sudo tar -xzpf rootfs.tar.gz -C rootfs")


    if(BoardNano or BoardStandard):
        os.rename('rootfs.tar.gz','rootfs_cy5.tar.gz') 
    else :
        os.rename('rootfs.tar.gz', 'rootfs_a10.tar.gz') 

    #############  input the name of final Image ###################

    nb = input('Please input a version Number:')
    print ('Name of the final image: rsYocto_%s \n' % (nb))


    ################################################ ROOTFS Changes ################################################

    ####################################### User ROOTFS Changes #######################################

    #############  create user interaction folder for the webpage and root folder ###################

    #check if the "my_homepage" folder is there 
    if not os.path.isdir("my_homepage"):
        try:  
            os.mkdir("my_homepage")
        except OSError:  
            print ("Creation of the new directory \"my_homepage\" failed!")
            sys.exit()

    #check if the "my_rootdir" folder is there 
    if not os.path.isdir("my_rootdir"):
        try:  
            os.mkdir("my_rootdir")
        except OSError:  
            print ("Creation of the new directory \"my_rootdir\" failed!")
            sys.exit()

    #check if the "my_includes" folder is there 
    if not os.path.isdir("my_includes"):
        try:  
            os.mkdir("my_includes")
        except OSError:  
            print ("Creation of the new directory \"my_includes\" failed!")
            sys.exit()


 #   cur_dir = os.system("pwd")

 #   print("\n------------------------------------------------------\n\n")
 #   print ("\n Press Enter to start the File-Explorer with Admin right.\n")
 #   print("In this window you can drag and drop your own website via the path \n \'")
 #   print( str(cur_dir)+ "/my_homepage\' or your own files and programs via the address ")
 #   print("\'.../my_rootdir\' to the final image !\n")
 #   print("Navigate over: /home/eit/Desktop ...") 

  #  raw_input ("PRESS ENTER to show the Explorer Window...\n\n")
    #open both folders with nautilus (root rights)
  
 #   cur_dir_str = 'sudo nautilus '+str(cur_dir)
 #   os.system(cur_dir_str.strip('0'))

#    raw_input (" CLOSE this explorer Window and PRESS ENTER to continue after your changes...\n\n")
 
    # copy the user changes to the rootfs folder
    print("------------------------------------------------------\n\n")
    print("--> Copying of your homepage to the rootfs: \n")
    os.system("sudo cp -vr my_homepage/. rootfs/usr/share/apache2/default-site/htdocs")

    print("--> Copying of your rootDir to the rootfs: \n")
    os.system("sudo cp -vr my_rootdir/. rootfs/home/root")

    print("--> Copying of your includes to the include: \n")
    os.system("sudo cp -vr my_includes/. rootfs/usr/include")

    ####################################### Script based ROOTFS Changes #######################################

    ################### chnaging the SSH authentication to "Linux User Password" ###################

    print("\n\nChnaging the SSH authentication to \"Linux User Password \"")
    
    with open("rootfs/etc/ssh/sshd_config", "a") as f:
        f.write("\nPermitRootLogin yes\n")
        f.write("Banner etc/issue")

    #   print("\n\Setup SSH key authentication ")
    #   with open("rootfs/etc/ssh/sshd_config", "a") as f:
    #       f.write("\nHostKey /etc/ssh/ssh_key_rsyocto\n")
    #
    #   os.system("sudo cp ssh_key_rsyocto rootfs/etc/ssh/")
    #  os.system("sudo cp ssh_key_rsyocto.pub rootfs/etc/ssh/")


    # check if the rsYocto folder is inside the rootfs
    if not os.path.isdir("rootfs/usr/rsyocto"):
        try:  
            os.mkdir("rootfs/usr/rsyocto")
        except OSError:  
            print ("Creation of the new directory \"rsYocto\" inside the rootfs failed!")
            sys.exit()
    
    #write the Version No to the rootfs
    print ("--> writing the Version Number to the rootFs\n")    
    try:
        fp = open('rootfs/usr/rsyocto/version.txt')
    except IOError:
        # If not exists, create the file
        fp = open('rootfs/usr/rsyocto/version.txt', 'w+')

    with open("rootfs/usr/rsyocto/version.txt", "a") as f:   
        f.write(str(nb))    

    ## Board Selection 
    print("--> Decoding the Board selection\n")
    now = datetime.datetime.now()
    path = os.getcwd()

    allBoards = False

    if BoardType == 0:
        allBoards = True
        BoardGenCounter =1
    else :
        BoardGenCounter = BoardType

    FileNameRbf      = ['unkown','socfpga_nano.rbf','socfpga_std.rbf']  
    FileNmaeDts       = ['unkown','socfpga_cy5.dts','socfpga_cy5.dts','socfpga_a10.dts']
    FileNmaeLinfRbf      = ['unkown','socfpga_nano_linux.rbf','socfpga_std_linux.rbf']  
    BoardImageSuffix = ['_unknown','_D10NANO','_DE10STD','_HAN']

    allBoardCount = 3



    print('\n ***************\ GENERATING INMAGE FOR  '+BoardName[BoardGenCounter]+" ***************\n")

    ################### add the Bootoader FPGA Configuration to the rootfs ###################

    # Wrting the name of the supported Board to the file System
    try:
        fp = open('rootfs/usr/rsyocto/suppBoard.txt')
    except IOError:
        # If not exists, create the file
        fp = open('rootfs/usr/rsyocto/suppBoard.txt', 'w+')

    print('-->  Writing the name of the supported board to the rootfs\n')
    with open("rootfs/usr/rsyocto/suppBoard.txt", "a") as f:   
        f.write(BoardName[BoardGenCounter])    

    # Copy the Linux FPGA Configuration file to the rootfs
    if (not BoardGenCounter == 3) and includeLinuxRbf:
        # feature is only for CY5 enabled
        print('-->  Copying the FPGA Configuration file to the rootfs\n')
        os.system("sudo cp "+FileNmaeLinfRbf[BoardGenCounter]+" rootfs/usr/rsyocto/")
        try:
            os.rename('rootfs/usr/rsyocto/'+FileNmaeLinfRbf[BoardGenCounter],'rootfs/usr/rsyocto/running_bootloader_fpgaconfig.rbf')
        except IOError:
            print ("Renaming of the Bootloader FPGA Configuration file failed!")
            sys.exit()


    ################### generate splash boot screan for each Board ###################
    print("\n--> Generaing the boot splash screen\n")
    open('rootfs/etc/issue', 'w').close()

    with open("rootfs/etc/issue", "a") as f:   
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
        f.write("*                    ---        created by Robin Sebastian (github.com/robseb)            ---            *\n")
        f.write("**********************************************************************************************************\n")   
        f.write("\n")
        f.write("-- Git Repository: https://github.com/robseb/rsyocto\n")
        f.write("-- VERSION: "+str(nb)+"\n")
        f.write("-- FPGA: "+FPGAName[BoardGenCounter]+"\n")
        f.write("-- SUPPORTED BOARD: "+BoardName[BoardGenCounter]+"\n")
        f.write ('-- IMAGE NAME : rsYocto_'+str(nb)+BoardImageSuffix[BoardGenCounter]+".img") 
        f.write ('     PACKING DATE: '+str(now.strftime("%d.%m.%Y"))+"\n")
        f.write ('-- SD-FOLDER NAME: '+str(os.path.basename(path))+"\n")
        f1=open('infoRSyocto.txt')  
        for x in f1.readlines():
            f.write(x)
        f1.close()
        f.write("***********************************************************************************************************\n\n")   
            
    #############  allow manual rootFs chnages ###################

    print("\n --> Now manual rootFs changes for specific of the Board: "+BoardName[BoardGenCounter]+" posibile!\n")
    raw_input("PRESS ENTER to continue...\n")
    print("------------------------------------------------------\n\n") 

    ################################################  Build the Device Tree  ################################################

    #############  reade the MAC of the info File #############
    f1=open('infoRSyocto.txt') 

    print("-> Change the Device Tree MAC-Address with the \"infoRSyocto.txt\"-MAC Address\n") 

    rsInfoLine = f1.readline()
    f1.close()             # -- MAC: d6:7d:ae:b3:0e:ba
    if  (not rsInfoLine.find('-- MAC: ') == 0):
        print("ERROR: The Mac Address inside the info file is not right format\n")
        exit()

    macStr = rsInfoLine[8:]
    
    macDtsStr = macStr.replace(':',' ')
    macDtsStr = macDtsStr.replace('\n','')

    print("    Opening the Device Tree File and inserting the new  MAC Address")
    f3=open(FileNmaeDts[BoardGenCounter],'r+') 
    dtsraw=''

    for x in f3.readlines():
        dtsraw= dtsraw+x

    if(BoardGenCounter == 3):
        # device tree file for Arria 10 SX
        ethstartPos = dtsraw.find('ethernet@ff800000 {')
    else :
        # device tree file for Cyclone V 
        ethstartPos = dtsraw.find('ethernet@ff702000 {')

    if not (ethstartPos > -1):
        print("ERROR: The DTS File is not in the right format\n")
        print("Deleting of the local rootFs Folder")
        os.system("sudo rm -r rootfs")
        print('Program stops with error!')
        exit()

    macstartPos =  dtsraw.find('mac-address = [',ethstartPos)
    
    if not (macstartPos > -1):
        print("ERROR: The DTS File is not right format (2)\n\n")
        print("Deleting of the local rootFs Folder")
        os.system("sudo rm -r rootfs")
        print('Program stops with error!')
        exit()
    
    macendPos =  dtsraw.find('];',macstartPos)
            
    if not (macstartPos > -1):
        print("ERROR: The DTS File is not right format (2)\n\n")
        print("Deleting of the local rootFs Folder")
        os.system("sudo rm -r rootfs")
        print('Program stops with error!')
        exit()

    dtsrawNew = dtsraw[:macstartPos+15] +' '+macDtsStr+ dtsraw[macendPos:]
    
    f3.truncate(0) # need '0' when using r+
    f3.close()

    with open(FileNmaeDts[BoardGenCounter], "a") as f3:
        f3.write(dtsrawNew)

    print('     MAC Address is included to Device Tree \n')

    #### Compiling the Device Tree ####

    print('--> Begin to compile the Device Tree\n')

    #Delate old device Tree bin file
    if (os.path.isfile("socfpga_a10.dtb") and (BoardGenCounter == 3) ):
        os.remove("socfpga_a10.dtb")
    elif (os.path.isfile("socfpga_cy5.dtb") and (not (BoardGenCounter == 3)) ):
        os.remove("socfpga_cy5.dtb")

    # Compile the Device Tree 
    if(BoardGenCounter == 3):
        os.system('dtc -O dtb -o socfpga_a10.dtb socfpga_a10.dts')
    else:
        os.system('dtc -O dtb -o socfpga_cy5.dtb socfpga_cy5.dts')

    deviceTreeCompFiled = False

    if ((not (os.path.isfile("socfpga_a10.dtb"))) and (BoardGenCounter == 3)):
        deviceTreeCompFiled = True
    elif ((not (os.path.isfile("socfpga_cy5.dtb"))) and (not (BoardGenCounter == 3))):
        deviceTreeCompFiled = True

    if(deviceTreeCompFiled):
        print('\nDeviceTree compilation failed!\n')
        print('Please check your DeviceTree file!\n\n')
        print("Deleting of the local rootFs Folder n")
        os.system("sudo rm -r rootfs")
        print('Program stops with error!')
        exit()
    
    print('    Device Tree compilation is done \n')


    ################################################  Callcation of the required size for the partions ################################################
    
    sizeError = False
    print('--> Begin to calculate the partition sizes\n')

    #Offset Sizes 
    pat1_offset = 20000000     #20M (For Arria 10 required!! )
    pat2_offset = USER_SPACE_SIZE
    pat3_offset =20000000 # 1000000      #1M
    comp_offset =20000000 # 5000000      #5M

    pat1_offsetStr =convert_size(pat1_offset)
    pat2_offsetStr =convert_size(pat2_offset)
    pat3_offsetStr =convert_size(pat3_offset)
    comp_offsetStr =convert_size(comp_offset)

    pat2_size = (convert_size(getFolderSize("rootfs")))

    print('1: '+pat1_offsetStr+ '  2: '+pat2_offsetStr +'  3: '+pat3_offsetStr +'  C: '+comp_offsetStr+' \n')
    print('CS: '+(pat2_size))

    if (not (BoardGenCounter == 3)):
            # CY5
        print('--> Calculating sizes for Cyclone V\n')
        pat1_size = convert_size((os.path.getsize("preloader_cy5.bin")))
        pat3_sizeRaw = os.path.getsize("zImage_cy5") + os.path.getsize(FileNameRbf[BoardGenCounter])+ \
                    os.path.getsize("socfpga_cy5.dtb") + +os.path.getsize("uboot_cy5.scr")+ \
                    os.path.getsize("uboot_cy5.img")

        pat3_size = convert_size(pat3_sizeRaw)
    else :
        # A10 
        print('--> Calculating sizes for Arria 10\n')
        pat1_size = convert_size((os.path.getsize("preloader_a10.bin")))
        pat3_sizeRaw = os.path.getsize("zImage_a10") + os.path.getsize("socfpga_han_periph.rbf")+ \
                    os.path.getsize("socfpga_a10.dtb") + +os.path.getsize("socfpga_han_core.rbf")

        pat3_size = convert_size(pat3_sizeRaw)

    # Check if the sizes are vialed 
    if not pat1_size.find("K") :
        print("ERROR: The size of the Pattison 1 is to small! (>1K)")
        sizeError = True
    
    if not pat2_size.find("M") :
        print("ERROR: The size of the Pattison 2 is to small! (>1M)")
        sizeError = True

    # if  pat2_size.find("G") :
    #     print("ERROR: The size of the Pattison 2 is to great! (<1G)")
    #     sizeError = True

    if not pat2_size.find("M") :
        print("ERROR: The size of the Pattison 3 is to small! (>1M)")
        sizeError = True

    # if  pat3_size.find("G") :
    #     print("ERROR: The size of the Pattison 3 is to great! (<1G)")
    #     sizeError = True

    if sizeError :
        print("Please check your files and then try it again!")
        print('Please check your DeviceTree file!\n\n')
        print("Deleting of the local rootFs Folder n")
        os.system("sudo rm -r rootfs")
        print('Program stops with error!')
        sys.exit()

    #############  Calculate required part sizes ###################
    
    # calculate the final partion sizes 
    if (not (BoardGenCounter == 3)):
        # CY5
        print('--> Calculating sizes for Cyclone V\n')
        pat1_final = convert_size((os.path.getsize("preloader_cy5.bin")+ pat1_offset))
    else :
        # A10
        print('--> Calculating sizes for Arria 10\n')
        pat1_final = convert_size((os.path.getsize("preloader_a10.bin")+ pat1_offset))   

    pat2_final = convert_size((getFolderSize("rootfs")+pat2_offset))
    pat3_final = convert_size((pat3_sizeRaw+pat3_offset))

    pat1_final = pat1_final.replace(" ","")
    pat2_final = pat2_final.replace(" ","")
    pat3_final = pat3_final.replace(" ","")

    # print the Partition Table
    print("\n---- Partition sizes ----")
    print("PAT1 (primary   Bootloader) - size: "+str(pat1_size)+" | offset: "+str(pat1_offsetStr)+" | final: "+str(pat1_final))
    print("PAT2 (rootfs)               - size: "+str(pat2_size)+" | offset: "+str(pat2_offsetStr)+" | final: "+str(pat2_final))
    print("PAT3 (secondary +FPGA ... ) - size: "+str(pat3_size)+" | offset: "+str(pat3_offsetStr)+" | final: "+str(pat3_final))

    # Calcuate the complite size 
    if (not (BoardGenCounter == 3)) :
        # CY5
        compl_size = convert_size((os.path.getsize("preloader_cy5.bin")+ pat1_offset+ \
                    getFolderSize("rootfs")+pat2_offset +pat3_sizeRaw+pat3_offset+comp_offset))
    else :
        # A10
        compl_size = convert_size((os.path.getsize("preloader_a10.bin")+ pat1_offset+ \
                    getFolderSize("rootfs")+pat2_offset +pat3_sizeRaw+pat3_offset+comp_offset))

    compl_size = compl_size.replace(" ","")

    print("\nComplite offset: "+str(comp_offsetStr)+" size:"+str(compl_size)+"\n")
    print("---- --------------- ----")



    if (not (BoardGenCounter == 3)) :
        os.rename(FileNameRbf[BoardGenCounter],'socfpga.rbf')   
        os.rename('zImage_cy5','zImage')  
        os.rename('socfpga_cy5.dtb','socfpga.dtb') 
        os.rename('preloader_cy5.bin','preloader-mkpimage.bin') 
        os.rename('uboot_cy5.scr','u-boot.scr')
        os.rename('uboot_cy5.img','u-boot.img')  
        
        #############  Build the Image  for Cyclone V ###################

        print("The Syntax of the Altera Script (CY5) for the run: ")
        print("sudo python ./make_sdimage.py -f \n"+ \
                    "-P preloader-mkpimage.bin,num=3,format=raw,size="+str(pat1_final)+",type=A2 \n"+ \
                    "-P rootfs/*,num=2,format=ext3,size="+str(pat2_final)+" \n"+ \
                    "-P zImage,socfpga.rbf,socfpga.dtb,u-boot.scr,u-boot.img,num=1,format=vfat,size="+str(pat3_final)+" \n"+ \
                    "-s "+str(compl_size)+" \n"+ \
                    "-n rsYocto_"+str(nb)+BoardImageSuffix[BoardGenCounter]+".img\n")


        print("\n+++ START of the ALTERA Image Script for CY5 +++")
        os.system("sudo python ./make_sdimage.py -f "+ \
                    "-P preloader-mkpimage.bin,num=3,format=raw,size="+str(pat1_final)+",type=A2 "+ \
                    "-P rootfs/*,num=2,format=ext3,size="+str(pat2_final)+" "+ \
                    "-P zImage,socfpga.rbf,socfpga.dtb,u-boot.scr,u-boot.img,num=1,format=vfat,size="+str(pat3_final)+" "+ \
                    "-s "+str(compl_size)+" "+ \
                    "-n rsYocto_"+str(nb)+BoardImageSuffix[BoardGenCounter]+".img")

        os.rename('socfpga.rbf',FileNameRbf[BoardGenCounter])  

        os.rename('preloader-mkpimage.bin','preloader_cy5.bin') 
        os.rename('u-boot.scr','uboot_cy5.scr')
        os.rename('u-boot.img','uboot_cy5.img')  
        os.rename('zImage','zImage_cy5')  
        os.rename('socfpga.dtb','socfpga_cy5.dtb') 

    else :      
        #############  Build the Image  for Arria 10 ###################
        os.rename('zImage_a10','zImage')
        os.rename('socfpga_han_periph.rbf','socfpga.periph.rbf')   
        os.rename('socfpga_han_core.rbf','ghrd_10as066n2.core.rbf') 
        os.rename('socfpga_a10.dtb','socfpga_arria10_socdk_sdmmc.dtb') 
        os.rename('preloader_a10.bin','uboot_w_dtb-mkpimage.bin')
        os.rename('uboot_a10.img','u-boot.img')
        os.rename('uboot_a10.scr','u-boot.scr') 

        print("The Syntax of the Altera Script (A10) for the run: ")
        print("sudo python make_sdimage.py  \
                -f \
                -P uboot_w_dtb-mkpimage.bin,num=3,format=raw,size="+str(pat1_final)+",type=A2  \
                -P rootfs/*,num=2,format=ext3,size="+str(pat2_final)+" "+ \
                "-P zImage,ghrd_10as066n2.core.rbf,socfpga.periph.rbf,socfpga_arria10_socdk_sdmmc.dtb,u-boot.scr,u-boot.img,num=1,format=vfat,size="+str(pat3_final)+" "+ \
                "-s "+str(compl_size)+" "+ \
                "-n rsYocto_"+str(nb)+BoardImageSuffix[BoardGenCounter]+".img")


        print("\n+++ START of the ALTERA Image Script for A10 +++")

        os.system("sudo python make_sdimage.py  \
                -f \
                -P uboot_w_dtb-mkpimage.bin,num=3,format=raw,size="+str(pat1_final)+",type=A2  \
                -P rootfs/*,num=2,format=ext3,size="+str(pat2_final)+" "+ \
                "-P zImage,ghrd_10as066n2.core.rbf,socfpga.periph.rbf,socfpga_arria10_socdk_sdmmc.dtb,u-boot.scr,u-boot.img,num=1,format=vfat,size="+str(pat3_final)+" "+ \
                "-s "+str(compl_size)+" "+ \
                "-n rsYocto_"+str(nb)+BoardImageSuffix[BoardGenCounter]+".img")

        print("\n+++ END of the ALTERA Image Script +++")

        os.rename('zImage','zImage_a10')
        os.rename('socfpga.periph.rbf','socfpga_han_periph.rbf')   
        os.rename('ghrd_10as066n2.core.rbf','socfpga_han_core.rbf') 
        os.rename('socfpga_arria10_socdk_sdmmc.dtb','socfpga_a10.dtb') 
        os.rename('uboot_w_dtb-mkpimage.bin','preloader_a10.bin')
        os.rename('u-boot.img','uboot_a10.img')
        os.rename('u-boot.scr','uboot_a10.scr') 

    # Check if the ALTERA script execution was succsesful 
    if not (os.path.isfile("rsYocto_"+str(nb)+BoardImageSuffix[BoardGenCounter]+".img")): 
        print("\n\nERROR: The execution of the ALTERA Script failed!")
        print('Please follow the report of the ALTERA Script\n\n')
        print('Program stops with error!')
        sys.exit()

    print('\n ***************\ END GENERATING INMAGE FOR  '+BoardName[BoardGenCounter]+" ***************\n\n\n")
    print("\n\nend")

    #############  Delate rootFs Folder  ###################
    print("--> Delating of the local rootFs Folder n")
    os.system("sudo rm -r rootfs")
    print(" New custum rsYocto Image is created SCUCCESSFUL!\n")
    print(" Use any command boot-image-creating tool to boot this rsYocto-version\n")