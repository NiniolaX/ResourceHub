#!/usr/bin/bash
# Creates the ResourceHub main boilerplate

PROJECT_DIR="ResourceHub"

sudo apt-get update 
sudo apt-get install -y python3-pip python3-dev python3-venv

# Create a virtual environment
create_virtual_env() {
	if [ ! -d "hub_env" ]; then
  		python3 -m venv hub_env
  		echo "Virtual environment created in $PROJECT_DIR/hub_env"
	else
  		echo "Virtual environment already exists in $PROJECT_DIR/hub_env"
	fi
}

# Activate the hub_env virtual environment and install app dependencies
install_app_dependencies() {
	source hub_env/bin/activate
	echo "Virtual environment activated"

	# Upgrade pip
	pip install --upgrade pip

	# Install dependencies
	pip install -r requirements.txt

	echo "All App python dependencies installed\n\n"

	pip freeze

	# Deactivate the virtual environment
	deactivate
	echo "Virtual env deactivated.\n\n"
}

# Main function
main() {
	create_virtual_env
	install_app_dependencies
}

main
echo "App setup completed successfull";
