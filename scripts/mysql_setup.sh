#!/usr/bin/bash
# Install and configure MySQL Server

# Update apt repository
sudo apt-get update

# Install mysql
sudo apt-get install mysql-server

# Start mysql service
sudo service mysql start

# Allow to start with system initialization
sudo service mysql restart

# Check Server status
sudo service mysql status

# sudo echo "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';" | sudo mysql
