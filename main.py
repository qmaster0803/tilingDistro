# ----------------------------------------------------
# This file is part of tilingDistro installer.
# Tested on Python 3.10, Debian 12.5.0 Bookworm
# 
# Author: Dan K, 2024
# Github: https://github.com/qmaster0803/tilingDistro
# ----------------------------------------------------

import os
import subprocess

# Preparations. Check root permission.
if(os.geteuid() != 0):
        print("This script must be run as root!")
        exit()
else:
        print("TilingDistro v0.1 install script.")

# Step 1. Install basic software
while(True):
        answer = input("Do you want to proceed? [Y/n] ")
        if(answer.lower() in ['', 'y']): break
        else:
                print("Aborted.")
                exit()

base_packages = ['sudo', 'xorg', 'bspwm', 'sxhkd', 'rofi', 'alacritty', 'ranger']
try:
        ret = subprocess.check_output(["apt-get", "install"] + base_packages, stderr=subprocess.STDOUT)
except subprocess.CalledProcessError:
        print('Sorry, an error occured. Full log can be found in "tilingDistroInstall.log". Please contact author at qmaster080305@gmail.com.')