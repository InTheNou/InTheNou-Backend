#!/bin/bash

# run script with sudo privileges, within the InTheNou-Backend Directory
apt-get update

# Install Docker Dependencies.
apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common

# Setup Docker Repository.
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
   
# Install Docker.
apt-get install docker-ce docker-ce-cli containerd.io

curl -L "https://github.com/docker/compose/releases/download/1.25.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

chmod +x /usr/local/bin/docker-compose

# Create host machine storage directory for persistance of data.
mkdir /InTheNou
mkdir /InTheNou/Database_data

mkdir /InTheNou/private
mkdir /InTheNou/private/var
mkdir /InTheNou/private/var/lib
mkdir /InTheNou/private/var/lib/pgadmin
chmod 777 /InTheNou/private/var/lib/pgadmin

mkdir ./nginx/ssl


# Used to generate self-signed ssh key for testing. Fill out with some info.
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ./nginx/ssl/example.key -out ./nginx/ssl/example.crt

# Build database and pgadmin images and containers.
docker-compose build
docker-compose up -d --remove-orphans