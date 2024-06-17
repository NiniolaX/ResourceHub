#!/bin/bash

# Uninstall Nginx and remove all configuration files

# Check if the script is run as root
if [ "$(id -u)" -ne 0 ]; then
  echo "Please run as root"
  exit 1
fi

echo "Stopping Nginx service..."
service nginx stop

echo "Disabling Nginx service..."
service nginx disable

echo "Purging Nginx package..."
apt-get purge -y nginx nginx-common nginx-core

echo "Removing remaining configuration files and directories..."
rm -rf /etc/nginx
rm -rf /var/www/html
rm -rf /var/log/nginx
rm -rf /var/cache/nginx

echo "Removing dependencies that are no longer needed..."
apt-get autoremove -y

echo "Cleaning up package cache..."
apt-get clean

echo "Nginx has been completely uninstalled from the system."