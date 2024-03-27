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
import re
import sys

VERSION = "0.1"
ERR_MESSAGE = 'Sorry, an error occured. Full log can be found in "tilingDistroInstall.log". Please contact author at qmaster080305@gmail.com.'

def drawProgressbar(message, value, max_value, current_name="", size=30):
        print('\033[2K\033[1G', end='') # jump to the first char in line
        char_weight = max_value / size
        filled_count = round(value/char_weight)
        empty_count = size - filled_count
        print(message, '|'+('#'*filled_count)+(' '*empty_count)+'|', str(value)+'/'+str(max_value), "["+current_name+"]", flush=True, end='')

# levels:
LOGLEVEL_INFO = 0
LOGLEVEL_WARN = 1
LOGLEVEL_CRIT = 2
def log(message, level=LOGLEVEL_INFO):
        print(message)
        if(level == LOGLEVEL_INFO):   logging.info(message)
        elif(level == LOGLEVEL_WARN): logging.warn(message)
        else:                         logging.critical(message)

# Setup logging
logging.basicConfig(format="%(asctime)s [%(levelname)s]: %(message)s", level=logging.INFO, filename="tilingDistroInstall.log")

# Preparations. Check root permission and network connection, ask username.
if(os.geteuid() != 0):
        print("This script must be run as root!")
        exit()
else:
        log("TilingDistro v"+VERSION+" install script.")

log("Checking network connection...")
ret = subprocess.run(["ping", "-c", "4", "google.com"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if(ret.returncode != 0):
        log("This script requires an internet connection.", LOGLEVEL_CRITICAL)
        exit()
else:
        log("Connection OK.")

username = input("Please enter your username (not root): ")
logging.info("Username entered: %s.", username)

# Step 1. Install basic software
while(True):
        answer = input("Do you want to proceed? [Y/n] ")
        if(answer.lower() in ['', 'y']): break
        else:
                print("Aborted.")
                exit()

# Add contrib non-free repo to /etc/apt/sources.list
with open("/etc/os-release") as file:
        codename = list(filter(lambda x: x.startswith("VERSION_CODENAME"), file.read().split('\n')))[0].split("=")[1]

with open("/etc/apt/sources.list", "a") as file:
        file.write("deb http://deb.debian.org/debian/ "+codename+" contrib non-free\n")
        file.write("deb-src http://deb.debian.org/debian/ "+codename+" contrib non-free\n")
        
subprocess.run(["apt-get", "update"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

base_packages = ['sudo', 'xorg', 'bspwm', 'sxhkd', 'rofi', 'alacritty', 'ranger', 'htop', 'zsh', 'pipewire', 'wireplumber', 'pipewire-audio', 'pipewire-pulse', 'pipewire-alsa',
                 'build-essential', 'cmake', 'libxkbfile-dev', 'flameshot', 'network-manager', 'net-tools', 'dunst', 'light', 'git', 'cmake-data', 'pkg-config', 'python3-sphinx',
                 'python3-packaging', 'libuv1-dev', 'libcairo2-dev', 'libxcb1-dev', 'libxcb-util0-dev', 'libxcb-randr0-dev', 'libxcb-composite0-dev', 'python3-xcbgen', 'xcb-proto',
                 'libxcb-image0-dev', 'libxcb-ewmh-dev', 'libxcb-icccm4-dev', 'libxcb-xkb-dev', 'libxcb-xrm-dev', 'libxcb-cursor-dev', 'libasound2-dev', 'libpulse-dev',
                 'libmpdclient-dev', 'libnl-genl-3-dev', 'nvidia-detect', 'python3-pip', 'libnotify-bin']

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

# Removing xterm

# Step 2. Building some packages from source
print("This packages must be built from source: polybar, xkb-switch.")
print("This may take a while, please wait...")


os.chdir("/home/"+username+"/")
if(not os.path.exists("Software")):
        os.mkdir("Software")
os.chdir("Software")

# building polybar
log("Cloning polybar repo...")
result = subprocess.run(["git", "clone", "--recursive", "https://github.com/polybar/polybar"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if(ret.returncode != 0):
        print(ERR_MESSAGE)
        logging.critical(result.stderr.decode('utf-8'))
        exit()
os.chdir("polybar")
log("Configuring polybar...")
os.mkdir("build")
os.chdir("build")
result = subprocess.run(["cmake", ".."], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if(ret.returncode != 0):
        print(ERR_MESSAGE)
        logging.critical(result.stderr.decode('utf-8'))
        exit()
log("Building polybar... (this may take a few minutes, especially on old machines)")
result = subprocess.run(["make", "-j", str(os.cpu_count())], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if(ret.returncode != 0):
        print(ERR_MESSAGE)
        logging.critical(result.stderr.decode('utf-8'))
        exit()
log("Installing polybar...")
result = subprocess.run(["make", "install"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if(ret.returncode != 0):
        print(ERR_MESSAGE)
        logging.critical(result.stderr.decode('utf-8'))
        exit()

os.chdir("../../")
log("Polybar installed.")

# building xkb-switch
log("Cloning xkb-switch repo...")
result = subprocess.run(["git", "clone", "--recursive", "https://github.com/grwlf/xkb-switch"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if(ret.returncode != 0):
        print(ERR_MESSAGE)
        logging.critical(result.stderr.decode('utf-8'))
        exit()
os.chdir("xkb-switch")
log("Configuring xkb-switch...")
os.mkdir("build")
os.chdir("build")
result = subprocess.run(["cmake", ".."], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if(ret.returncode != 0):
        print(ERR_MESSAGE)
        logging.critical(result.stderr.decode('utf-8'))
        exit()
log("Building xkb-switch... (this may take a few minutes, especially on old machines)")
result = subprocess.run(["make", "-j", str(os.cpu_count())], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if(ret.returncode != 0):
        print(ERR_MESSAGE)
        logging.critical(result.stderr.decode('utf-8'))
        exit()
log("Installing xkb-switch...")
result = subprocess.run(["make", "install"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if(ret.returncode != 0):
        print(ERR_MESSAGE)
        logging.critical(result.stderr.decode('utf-8'))
        exit()

os.chdir('../../')
log("xkb-switch installed.")

subprocess.run(["/usr/sbin/ldconfig"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run(["chown", "--recursive", str(pwd.getpwnam(username).pw_uid)+":"+str(pwd.getpwnam(username).pw_gid), "/home/"+username+"/Software"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Step 3. Configuring user account
log("Configuring the system...")
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

with open("/home/"+username+"/.config/polybar/battery_name", "w") as file:
        file.write(list(filter(lambda x: x.startswith('BAT'), os.listdir("/sys/class/power_supply/")))[0])

with open("/home/"+username+"/.config/polybar/adapter_name", "w") as file:
        file.write(list(filter(lambda x: x.startswith('AC'), os.listdir("/sys/class/power_supply/")))[0])
        
with open("/home/"+username+"/.config/polybar/bl_name", "w") as file:
        file.write(os.listdir("/sys/class/backlight/")[0])

if(not os.path.exists("/home/"+username+"/.config/sxhkd/")): os.mkdir("/home/"+username+"/.config/sxhkd/")
shutil.copy(os.path.join(os.path.dirname(__file__), "default_configs/sxhkd/sxhkdrc"), "/home/"+username+"/.config/sxhkd/sxhkdrc") # copy sxhkdrc
os.chmod("/home/"+username+"/.config/sxhkd/sxhkdrc", 0o755)                                                                       # allow execution


subprocess.run(["chown", "--recursive", str(pwd.getpwnam(username).pw_uid)+":"+str(pwd.getpwnam(username).pw_gid), "/home/"+username+"/.config"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

log("System configuration done.")

# Step 4. Checking NVIDIA GPU and installing driver if needed
log("Checking NVIDIA GPU available...")
result = subprocess.run(["nvidia-detect"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if(result.stdout.decode('utf-8').startswith('No NVIDIA GPU detected.')):
        log("No NVIDIA GPU detected, skipping.")
else:
        log("NVIDIA GPU detected.")
        install = True
        while(True):
                answer = input("Do you want to install nvidia-driver? [Y/n] ")
                if(answer.lower() in ['', 'y']): break
                else:
                        install = False
                        break
        if(install):
                package_name = re.search("It is recommended to install the\n(?: *)?([\w-]*)(?: *)?\npackage.", result.stdout.decode('utf-8')).group(1)
                log("Installing "+package_name+" package...")
                result = subprocess.run(["apt-get", "install", "-y", package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if(result.returncode != 0):
                        log(ERR_MESSAGE, LOGLEVEL_CRITICAL)
                        exit()

# Step 5. Configuring monitors
result = subprocess.run(["xrandr"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
connected_monitors = re.findall('([\w-]+) connected', result.stdout.decode('utf-8'))

if(len(connected_monitors) > 1):
        log("Multiple monitors found. ArandR will be launched after starting the X.")
        dynamic_monitors = True
        while(True):
                answer = input("Is this monitor configuration dynamic (will you disconnect monitor(s) from time to time or not?) ? [Y/n] ")
                if(answer.lower() in ['', 'y']): break
                else:
                        install = False
                        break
        if(dynamic_monitors):
                #<TODO> Install script
                pass

#<TODO> workspaces config

# Step 6. Installing additional software
subprocess.run([sys.executable, "-m", "pip", "install", "pick", "--break-system-packages"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

import pick

additional_packages = ["Google Chrome", "Mozilla Firefox", "LibreOffice", "VLC Media Player", "GIMP", "Inkscape",
                        "Telegram Desktop AppImage", "Aria2", "Steam", "OBS", "Discord", "Flatpak", "Helvum",
                        "Transmission", "Gnome text editor", "Sublime text 3", "Sublime text 4",
                        "Helix", "Emacs", "Vim", "NeoVim"]

selected = [i[0] for i in pick.pick(additional_packages, "Select additional software that you want to install:", multiselect=True)]

if("Helvum" in seleced): selected.append("Flatpak")
        
os.chdir("/home/"+username)
if(not os.path.exists("Downloads")):
        os.mkdir("Downloads")
os.chdir("Downloads")
if("Google Chrome" in selected):
        log("Installing Google Chrome...")
        subprocess.run(["wget", "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["apt-get", "install", "-y", "./google-chrome-stable_current_amd64.deb"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["rm", "google-chrome-stable_current_amd64.deb"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if("Mozilla Firefox" in selected):
        log("Installing Mozilla Firefox...")
        subprocess.run(["bash", os.path.join(os.path.dirname(__file__), "scripts/firefox-install.sh")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if("LibreOffice" in selected):
        log("Installing LibreOffice...")
        subprocess.run(["apt-get", "install", "-y", "libreoffice"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if("VLC Media Player" in selected):
        log("Installing VLC Media Player...")
        subprocess.run(["apt-get", "install", "-y", "vlc"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if("GIMP" in selected):
        log("Installing GIMP...")
        subprocess.run(["apt-get", "install", "-y", "gimp"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if("Inkscape" in selected):
        log("Installing Inkscape...")
        subprocess.run(["apt-get", "install", "-y", "inkscape"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if("Telegram Desktop AppImage" in selected):
        log("Installing Telegram Desktop AppImage...")
        subprocess.run(["wget", "https://telegram.org/dl/desktop/linux", "-O", "telegram-desktop-latest.tar.xz"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["tar", "xf", "telegram-desktop-latest.tar.xz", "-C", "/home/"+username+"/Software/"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.chmod("/home/"+username+"/Software/Telegram/Telegram", 0o755)
        print("Telegram installed. Please run it first time manually from ~/Software/Telegram/Telegram")
        subprocess.run(["rm", "telegram-desktop-latest.tar.xz"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if("Aria2" in selected):
        log("Installing Transmission...")
        subprocess.run(["apt-get", "install", "-y", "aria2"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if("Steam" in selected):
        log("Installing Steam...")
        subprocess.run(["wget", "https://cdn.akamai.steamstatic.com/client/installer/steam.deb"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["apt-get", "install", "-y", "./steam.deb"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["rm", "steam.deb"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if("OBS" in selected):
        log("Installing OBS...")
        subprocess.run(["apt-get", "install", "-y", "ffmpeg", "obs-studio"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if("Discord" in selected):
        log("Installing Discord...")
        subprocess.run(["wget", "https://discord.com/api/download?platform=linux&format=deb", "-O", "discord.deb"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["apt-get", "install", "-y", "./discord.deb"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["rm", "discord.deb"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if("Flatpak" in selected):
        log("Installing Flatpak...")
        subprocess.run(["apt-get", "install", "-y", "flatpak"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["flatpak", "remote-add", "--if-not-exists", "flathub", "https://dl.flathub.org/repo/flathub.flatpakrepo"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if("Helvum" in selected):
        log("Installing Helvum...")
        subprocess.run(["flatpak", "install", "flathub", "org.pipewire.Helvum"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if("Transmission" in selected):
        log("Installing Transmission...")
        subprocess.run(["apt-get", "install", "-y", "transmission-gtk"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if("Gnome text editor" in selected):
        log("Installing Gnome text editor...")
        subprocess.run(["apt-get", "install", "-y", "gedit"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if("Sublime text 3" in selected):
        log("Installing Sublime text 3...")
        subprocess.run(["wget", "https://download.sublimetext.com/sublime-text_build-3211_amd64.deb"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["apt-get", "install", "-y", "sublime-text_build-3211_amd64.deb"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["rm", "sublime-text_build-3211_amd64.deb"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if("Sublime text 4" in selected):
        log("Installing Sublime text 4...")
        subprocess.run(["wget", "https://download.sublimetext.com/sublime-text_build-4169_amd64.deb"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["apt-get", "install", "-y", "sublime-text_build-4169_amd64.deb"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["rm", "sublime-text_build-4169_amd64.deb"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if("Helix" in selected):
        log("Building Helix...")
        log("Installing Rust")
        subprocess.run(["apt-get", "install", "-y", "git", "python3-pylsp", "clangd"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["wget", "https://sh.rustup.rs", "-O", "rustup.sh"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["bash", "rustup.sh"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["rm", "rustup.sh"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        log("Cloning Helix repo...")
        os.chdir("/home/"+username+"/Software")
        subprocess.run(["git", "clone", "https://github.com/helix-editor/helix"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.chdir("helix")
        log("Building Helix... (this may take a while, especially on old machines)")
        subprocess.run(["cargo", "install", "--path", "helix_term", "--locked"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        log("Fetching helix grammars...")
        subprocess.run(["hx", "--grammar", "fetch"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        log("Building helix grammars...")
        subprocess.run(["hx", "--grammar", "build"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["hx", "--grammar", "fetch"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["chown", "--recursive", str(pwd.getpwnam(username).pw_uid)+":"+str(pwd.getpwnam(username).pw_gid), "/home/"+username+"/Software/helix"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if("Emacs" in selected):
        log("Installing emacs...")
        subprocess.run(["apt-get", "install", "-y", "emacs"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if("NeoVim" in selected):
        log("Installing NeoVim...")
        subprocess.run(["apt-get", "install", "-y", "neovim"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if("Vim" in selected):
                log("Unable to install Vim and NeoVim simultaneously, skipping Vim", level=LOGLEVEL_WARN)
if("Vim" in selected and "NeoVim" not in selected):
        log("Installing Vim...")
        subprocess.run(["apt-get", "install", "-y", "vim"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
