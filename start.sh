#!/bin/bash
action="\n[\e[93maction\e[0m]"
error="\n[\e[91merror\e[0m]"
info="\n[\e[92minfo\e[0m]"

if [[ $EUID -ne 0 ]]; then
   printf "$error Run me as root!\n" 
   exit 1
fi

clear

printf "$action Starting...\n"
sudo python3 main.py -i wlan0 -s wifi -t captive_login