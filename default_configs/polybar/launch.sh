#! /bin/bash

# default single-monitor config
killall -q polybar
echo "---" | tee -a /home/$USER/.config/polybar/log.log
polybar main >> /home/$USER/.config/polybar/log.log