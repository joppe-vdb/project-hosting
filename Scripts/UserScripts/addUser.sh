#!/bin/bash
# add user to a project
sudo usermod -aG $1 $2
sudo usermod -aG sftpgroup $2
