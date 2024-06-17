#!/usr/bin/bash
# Prepares and configure Server environment

# Function to install Nginx
install_nginx() {
  if ! command -v nginx &> /dev/null; then
    echo "Nginx not found. Installing Nginx..."
    apt-get update
    apt-get install -y nginx
    service nginx start 
    echo "Nginx installation completed and service started."
  else
    echo "Nginx is already installed."
  fi
}

# Main function
main() {
        install_nginx
}

main
echo "nginx Server installation completed successfully"
