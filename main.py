# ----------------------------------------------------
# This file is part of tilingDistro installer.
# Tested on Python 3.10, Debian 12.5.0 Bookworm
# 
# Author: Dan K, 2024
# Github: https://github.com/qmaster0803/tilingDistro
# ----------------------------------------------------

import os
import shutil
import subprocess
import logging
import time
import pwd

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


os.chdir("/home/"+username+"/")
if(not os.path.exists("Software")):
        os.mkdir("Software")
os.chdir("Software")

# building polybar
print("Cloning polybar repo...")
logging.info("Cloning polybar repo...")
result = subprocess.run(["git", "clone", "--recursive", "https://github.com/polybar/polybar"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
print("Building polybar... (this may take a few minutes, especially on old machines)")
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

os.chdir("../../")
print("Polybar installed.")
logging.info("Polybar installed.")

# building xkb-switch
print("Cloning xkb-switch repo...")
logging.info("Cloning xkb-switch repo...")
result = subprocess.run(["git", "clone", "--recursive", "https://github.com/grwlf/xkb-switch"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if(ret.returncode != 0):
        print(ERR_MESSAGE)
        logging.critical(result.stderr.decode('utf-8'))
        exit()
os.chdir("xkb-switch")
print("Configuring xkb-switch...")
logging.info("Configuring xkb-switch...")
os.mkdir("build")
os.chdir("build")
result = subprocess.run(["cmake", ".."], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if(ret.returncode != 0):
        print(ERR_MESSAGE)
        logging.critical(result.stderr.decode('utf-8'))
        exit()
print("Building xkb-switch... (this may take a few minutes, especially on old machines)")
logging.info("Building xkb-switch...")
result = subprocess.run(["make", "-j", str(os.cpu_count())], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if(ret.returncode != 0):
        print(ERR_MESSAGE)
        logging.critical(result.stderr.decode('utf-8'))
        exit()
print("Installing xkb-switch...")
logging.info("Installing xkb-switch...")
result = subprocess.run(["make", "install"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if(ret.returncode != 0):
        print(ERR_MESSAGE)
        logging.critical(result.stderr.decode('utf-8'))
        exit()

os.chdir('../../')
print("xkb-switch installed.")
logging.info("xkb-switch installed.")

subprocess.run(["/usr/sbin/ldconfig"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run(["chown", "--recursive", str(pwd.getpwnam(username).pw_uid)+":"+str(pwd.getpwnam(username).pw_gid), "/home/"+username+"/Software"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Step 3. Configuring user account
print("Configuring the system...")
logging.info("Configuring the system...")
subprocess.run(["/usr/sbin/usermod", "-aG", "sudo", username], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # add user to groups
subprocess.run(["/usr/sbin/usermod", "-aG", "video", username], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run(["/usr/sbin/usermod", "-aG", "plugdev", username], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run(["/usr/sbin/usermod", "-aG", "netdev", username], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run(["/usr/sbin/usermod", "-aG", "dialout", username], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

subprocess.run(["chsh", "-s", "/usr/bin/zsh", username], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)        # set zsh as default shell
shutil.copy(os.path.join(os.path.dirname(__file__), "default_configs/zshrc"), "/home/"+username+"/.zshrc")            # copy default zsh config
subprocess.run(["sed", "-i", "'s/<<username>>/"+username+"/g'", "/home/"+username+"/.zshrc"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)                                                 # paste username into zsh config
subprocess.run(["chown", str(pwd.getpwnam(username).pw_uid)+":"+str(pwd.getpwnam(username).pw_gid),
                "/home/"+username+"/.zshrc"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)                   # set owner
os.chmod("/home/"+username+"/.zshrc", 0o755)                                                                          # allow execution

shutil.copy(os.path.join(os.path.dirname(__file__), "default_configs/xinitrc"), "/home/"+username+"/.xinitrc")        # copy default xinitc
subprocess.run(["chown", str(pwd.getpwnam(username).pw_uid)+":"+str(pwd.getpwnam(username).pw_gid),
                "/home/"+username+"/.xinitrc"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)                 # set owner
os.chmod("/home/"+username+"/.xinitrc", 0o755)                                                                        # allow execution


if(not os.path.exists("/home/"+username+"/.config/")):
        os.mkdir("/home/"+username+"/.config/")

if(not os.path.exists("/home/"+username+"/.config/bspwm/")): os.mkdir("/home/"+username+"/.config/bspwm/")
shutil.copy(os.path.join(os.path.dirname(__file__), "default_configs/bspwm/bspwmrc"), "/home/"+username+"/.config/bspwm/bspwmrc") # copy bspwmrc
os.chmod("/home/"+username+"/.config/bspwm/bspwmrc", 0o755)                                                                       # allow execution

if(not os.path.exists("/home/"+username+"/.config/polybar/")): os.mkdir("/home/"+username+"/.config/polybar/")
shutil.copy(os.path.join(os.path.dirname(__file__), "default_configs/polybar/config.ini"), "/home/"+username+"/.config/polybar/config.ini") # copy polybar config
shutil.copy(os.path.join(os.path.dirname(__file__), "default_configs/polybar/launch.sh"), "/home/"+username+"/.config/polybar/launch.sh")   # copy polybar launch script
os.chmod("/home/"+username+"/.config/polybar/launch.sh", 0o755)                                                                             # allow execution

if(not os.path.exists("/home/"+username+"/.config/sxhkd/")): os.mkdir("/home/"+username+"/.config/sxhkd/")
shutil.copy(os.path.join(os.path.dirname(__file__), "default_configs/sxhkd/sxhkdrc"), "/home/"+username+"/.config/sxhkd/sxhkdrc") # copy sxhkdrc
os.chmod("/home/"+username+"/.config/sxhkd/sxhkdrc", 0o755)                                                                       # allow execution


subprocess.run(["chown", "--recursive", str(pwd.getpwnam(username).pw_uid)+":"+str(pwd.getpwnam(username).pw_gid), "/home/"+username+"/.config"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("System configuration done.")
logging.info("System configuration done.")