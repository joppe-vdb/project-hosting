#!/bin/bash
# DIRECTORIES FOR ADMIN #
# move to the correct directory
cd /home/ccs5/projects

# create the the main directory + config directory for project
mkdir -p $1/config

# DIRECTORIES FOR USER #
# move to the correct directory
cd /projects

# create the main directory
mkdir $1

# create the subdirectories
cd $1
mkdir files
mkdir mysql

# create a group
sudo groupadd $1

# give only root and group access to the files
sudo chown root:$1 /projects/$1
sudo chown root:$1 /projects/$1/files
sudo chown root:$1 /projects/$1/mysql

sudo chmod 777 /projects/$1
sudo chmod 777 /projects/$1/files
sudo chmod 777 /projects/$1/mysql   