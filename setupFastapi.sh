#!/bin/bash
# update and upgrade system files
sudo apt-get update
sudo apt-get upgrade -y

# make directories and subdirectories
mkdir api
mkdir api/app
echo "directories complete"

# make application files
# move to app directory
cd api/app

# create the files needed for the project -> empty later we will add the code using visual studio code
# main.py, database.py, server.py, auth.py, functions.py
touch main.py
touch database.py
touch server.py
touch auth.py
touch functions.py

# installation
# move up a directory
cd ..

# install pip3 
sudo apt-get install -y python3-pip

# create a requirements.txt
echo "fastapi>=0.76.0
pymysql==1.0.2
pydantic>=1.9.0
uvicorn>=0.15.0
passlib[bycrypt,argon2]
python-jose[cryptography]
oauthlib==3.1.1
requests-oauthlib==1.3.0" > requirements.txt

# install packages from requirements.txt
sudo pip install -r requirements.txt

# create a script that will start the fastapi
echo "#!/bin/bash
# start the fastAPI application with Uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000" >> app/startAPI.sh

# give execute rights
sudo chmod +x app/startAPI.sh



