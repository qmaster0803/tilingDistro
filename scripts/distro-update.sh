#! /bin/zsh
if [[ $UID == 0 || $EUID == 0 ]]; then
  python3 /etc/tilingDistro/distro-update.sh
else
   echo "This command should be run as root."
fi
