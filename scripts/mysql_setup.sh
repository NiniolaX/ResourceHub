#!/usr/bin/bash
# Install and configure MySQL Server

# Update apt repository
sudo apt-get update

# Install mysql
sudo apt-get install mysql-server

# Start mysql service
sudo service mysql start
sudo service mysql restart

# Create Project database and designated user
sudo cat setup_mysql_test.sql | sudo mysql

echo "Database and user created successfully."
