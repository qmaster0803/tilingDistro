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
ERR_MESSAGE = 'Sorry, an error occured. Full log can be found in "tilingDistroInstall.log". Please contact author at qmaster080305@gmail.com.'

def drawProgressbar(message, value, max_value, current_name="", size=30):
        print('\033[2K\033[1G', end='') # jump to the first char in line
        char_weight = max_value / size
        filled_count = round(value/char_weight)
        empty_count = size - filled_count
        print(message, '|'+('#'*filled_count)+(' '*empty_count)+'|', str(value)+'/'+str(max_value), "["+current_name+"]", flush=True, end='')

# Setup logging
logging.basicConfig(format="%(asctime)s [%(levelname)s]: %(message)s", level=logging.INFO, filename="tilingDistroInstall.log")

# Preparations. Check root permission and network connection, ask username.
if(os.geteuid() != 0):
        print("This script must be run as root!")
        exit()
else:
        print("TilingDistro v"+VERSION+" install script.")
        logging.info("TilingDistro Installer v%s", VERSION)

print("Checking network connection...")
logging.info("Checking network connection...")
ret = subprocess.run(["ping", "-c", "4", "google.com"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if(ret.returncode != 0):
        print("This script requires an internet connection.")
        logging.critical("No network detected.")
        exit()
else:
        print("Connection OK.")
        logging.info("Connection OK.")

username = input("Please enter your username (not root): ")
logging.info("Username entered: %s.", username)

# Step 1. Install basic software
while(True):
        answer = input("Do you want to proceed? [Y/n] ")
        if(answer.lower() in ['', 'y']): break
        else:
                print("Aborted.")
                exit()

base_packages = ['sudo', 'xorg', 'bspwm', 'sxhkd', 'rofi', 'alacritty', 'ranger', 'htop', 'zsh', 'pipewire', 'wireplumber', 'pipewire-audio', 'pipewire-pulse', 'pipewire-alsa',
                 'build-essential', 'cmake', 'libxkbfile-dev', 'flameshot', 'network-manager', 'net-tools', 'dunst', 'light', 'git', 'cmake-data', 'pkg-config', 'python3-sphinx',
                 'python3-packaging', 'libuv1-dev', 'libcairo2-dev', 'libxcb1-dev', 'libxcb-util0-dev', 'libxcb-randr0-dev', 'libxcb-composite0-dev', 'python3-xcbgen', 'xcb-proto',
                 'libxcb-image0-dev', 'libxcb-ewmh-dev', 'libxcb-icccm4-dev', 'libxcb-xkb-dev', 'libxcb-xrm-dev', 'libxcb-cursor-dev', 'libasound2-dev', 'libpulse-dev',
                 'libmpdclient-dev', 'libnl-genl-3-dev']

logging.info("Installing base packages...")
for i,package in enumerate(base_packages):
        drawProgressbar("Installing base packages...", i, len(base_packages), package)
        result = subprocess.run(["apt-get", "install", "-y", package], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.info("Installed %s.", package)
        if(result.returncode != 0):
                logging.critical(result.stderr.decode('utf-8'))
                print() # to reset progressbar
                print(ERR_MESSAGE)
                exit()
print() # to reset progressbar
logging.info("Base packages installed.")

# Step 2. Building some packages from source
print("This packages must be built from source: polybar, xkb-switch.")
print("This may take a while, please wait...")

# building polybar
os.chdir("/home/"+username+"/")
os.mkdir("Software", exist_ok=True)
os.chdir("Software")
print("Cloning polybar repo...")
logging.info("Cloning polybar repo...")
result = subprocess.run(["git", "clone", "--recursive", "https://github.com/polybar/polybar"], stderr=subprocess.PIPE)
if(ret.returncode != 0):
        print(ERR_MESSAGE)
        logging.critical(result.stderr.decode('utf-8'))
        exit()
os.chdir("polybar")
print("Configuring polybar...")
logging.info("Configuring polybar...")
os.mkdir("build")
os.chdir("build")
result = subprocess.run(["cmake", ".."], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if(ret.returncode != 0):
        print(ERR_MESSAGE)
        logging.critical(result.stderr.decode('utf-8'))
        exit()
print("Building polybar...")
logging.info("Building polybar...")
result = subprocess.run(["make", "-j", str(os.cpu_count())], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if(ret.returncode != 0):
        print(ERR_MESSAGE)
        logging.critical(result.stderr.decode('utf-8'))
        exit()
print("Installing polybar...")
logging.info("Installing polybar...")
result = subprocess.run(["make", "install"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if(ret.returncode != 0):
        print(ERR_MESSAGE)
        logging.critical(result.stderr.decode('utf-8'))
        exit()


print("Polybar installed.")
logging.info("Polybar installed.")