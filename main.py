# ----------------------------------------------------
# This file is part of tilingDistro installer.
# Tested on Python 3.10, Debian 12.5.0 Bookworm
# 
# Author: Dan K, 2024
# Github: https://github.com/qmaster0803/tilingDistro
# ----------------------------------------------------

import os
import logging
import subprocess
import urllib.request

def get_latest_version():
        page = urllib.request.urlopen("https://raw.githubusercontent.com/qmaster0803/tilingDistro/master/VERSION")
        return page.read()

def check_is_newer(version_to_check):
        global VERSION
        curr_split  = list(map(int, VERSION[1:].split('.')))
        check_split = list(map(int, version_to_check[1:].split('.')))

        return curr_split < check_split

def pull_git_repo():
        subprocess.run(["git", "pull"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        

# Get VERSION constant from file
with open("VERSION") as file:
        VERSION = file.read()

# levels:
LOGLEVEL_INFO = 0
LOGLEVEL_WARN = 1
LOGLEVEL_CRIT = 2
def log(message, level=LOGLEVEL_INFO):
        print(message)
        if(level == LOGLEVEL_INFO):   logging.info(message)
        elif(level == LOGLEVEL_WARN): logging.warning(message)
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
        log("This script requires an internet connection.", level=LOGLEVEL_CRITICAL)
        exit()
else:
        log("Connection OK.")

username = input("Please enter your username (not root): ")
logging.info("Username entered: %s.", username)


# Check installation method
if(os.path.exists("/etc/tilingDistro/info.json")): # Update current installation
        latest = get_latest_version()
        if(check_is_newer(latest)):
                pull_git_repo()
                import update
else: # Install from generic Debian
        import install
