# ----------------------------------------------------
# This file is part of tilingDistro installer.
# Tested on Python 3.10, Debian 12.5.0 Bookworm
# 
# Author: Dan K, 2024
# Github: https://github.com/qmaster0803/tilingDistro
# ----------------------------------------------------

import os
import subprocess
import logging
import time

VERSION = "0.1"

def drawProgressbar(message, value, max_value, current_name=""):
        print('\u001b[100D', end='') # jump to the first char in line
        char_weight = max_value / 50
        filled_count = round(value/char_weight)
        empty_count = 50 - filled_count
        print(message, '|'+('#'*filled_count)+(' '*empty_count)+'|', str(value)+'/'+str(max_value), current_name, flush=True, end='')

# Setup logging
logging.basicConfig(format="%(asctime)s [%(levelname)s]: %(message)s", level=logging.INFO, filename="tilingDistroInstall.log")
logging.info("TilingDistro Installer v%s", VERSION)

# Preparations. Check root permission.
if(os.geteuid() != 0):
        print("This script must be run as root!")
        exit()
else:
        print("TilingDistro v"+VERSION+" install script.")

# Step 1. Install basic software
while(True):
        answer = input("Do you want to proceed? [Y/n] ")
        if(answer.lower() in ['', 'y']): break
        else:
                print("Aborted.")
                exit()

base_packages = ['sudo', 'xorg', 'bspwm', 'sxhkd', 'rofi', 'alacritty', 'ranger', 'htop', 'zsh', 'build-essential', 'cmake', 'libxkbfile-dev', 'flameshot', 'network-manager', 'net-tools', 'dunst', 'light']
logging.info("Installing base packages...")
drawProgressbar("Installing base packages...", 0, len(base_packages), base_packages[0])
for package in base_packages:
        result = subprocess.run(["apt-get", "install", "-y", package], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        drawProgressbar("Installing base packages...", 1, len(base_packages), package)
        logging.info("Installed %s", package)
        if(result.returncode != 0):
                logging.critical(result.stderr.decode('utf-8'))
                print() # to reset progressbar
                print('Sorry, an error occured. Full log can be found in "tilingDistroInstall.log". Please contact author at qmaster080305@gmail.com.')
                exit()
print() # to reset progressbar
logging.info("Base packages installed.")