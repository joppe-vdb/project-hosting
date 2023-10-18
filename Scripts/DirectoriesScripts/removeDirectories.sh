#!/bin/bash
# remove the directories
# USER #
# remove the user filed (projects) from the system
sudo rm -r /projects/$1

# ADMIN # 
# remove the config files from the system
sudo rm -r /home/ccs5/projects/$1