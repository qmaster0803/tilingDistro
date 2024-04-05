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
        return page.read().decode("utf-8")

def check_is_newer(version_to_check):
        global VERSION
        curr_split  = list(map(int, VERSION.split('.')))
        check_split = list(map(int, version_to_check.split('.')))

        return curr_split < check_split

def pull_git_repo():
        subprocess.run(["git", "pull"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
class Logger():
        LOGLEVEL_INFO = 0
        LOGLEVEL_WARN = 1
        LOGLEVEL_CRIT = 2
        
        HIDDEN_INFO = 3
        HIDDEN_WARN = 4
        HIDDEN_CRIT = 5
        def __init__(self):
                logging.basicConfig(format="%(asctime)s [%(levelname)s]: %(message)s", level=logging.INFO, filename="tilingDistroInstall.log")
                
        def log(self, message, level=LOGLEVEL_INFO):
                if(level not in [self.HIDDEN_INFO, self.HIDDEN_WARN, self.HIDDEN_CRIT]): print(message)
                        
                if(level in [self.LOGLEVEL_INFO, self.HIDDEN_INFO]):   logging.info(message)
                elif(level in [self.LOGLEVEL_WARN, self.HIDDEN_WARN]): logging.warning(message)
                else:                                                  logging.critical(message)

# CD to ensure that we are in correct directory (can be different when run from distro-update command, etc.)
os.chdir(os.path.dirname(__file__))

logger = Logger()

# Get VERSION constant from file
with open("VERSION") as file:
        VERSION = file.read().replace('\n', '')

# Preparations. Check root permission and network connection, ask username.
if(os.geteuid() != 0):
        print("This script must be run as root!")
        exit()
else:
        logger.log("TilingDistro v"+VERSION+" install script.")

logger.log("Checking network connection...")
ret = subprocess.run(["ping", "-c", "4", "google.com"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if(ret.returncode != 0):
        logger.log("This script requires an internet connection.", level=logger.LOGLEVEL_CRITICAL)
        exit()
else:
        logger.log("Connection OK.")

username = input("Please enter your username (not root): ")
logger.log("Username entered: "+username, level=logger.HIDDEN_INFO)


# Check installation method
if(os.path.exists("/etc/tilingDistro/info.json")): # Update current installation
        latest = get_latest_version()
        if(check_is_newer(latest)):
                pull_git_repo()
                import update
                update.update(username, VERSION, logger)
        else:
                print("Already up to date!")
else: # Install from generic Debian
        import install
        install.install(username, VERSION, logger)
