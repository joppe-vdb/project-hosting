#!/bin/bash
# remove user from a project group
sudo gpasswd -d $1 $2
