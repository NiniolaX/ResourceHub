# fabfile.py

from fabric import task, Connection, Config
from getpass import getpass
from datetime import datetime as dt

# Define your server details

# Define the connection details
def get_connection():
    
    host = '54.236.46.38'
    user = 'ubuntu'
    passphrase = getpass("Enter your SSH passphrase (if applicable): ")
    password = getpass("Enter your sudo password: ")  # Use SSH key-based authentication for better security

    connect_kwargs = {
        'key_filename': '/home//mbuchu/.ssh/school',
        'passphrase': passphrase
    }
    config = Config(overrides={'sudo': {'password': password}})

    return Connection(
        host=host,
        user=user,
        connect_kwargs=connect_kwargs,
        config=config
    )

# Define paths on the server
remote_static_path = '/path/to/remote/static/files'
remote_dynamic_path = '/path/to/remote/dynamic/files'
# remote_user_home_path = f'/home/{user}'

# # Define paths in your local project
local_static_path = './web_static'
local_dynamic_path = './app'

# upload static files
def upload(local_path='.',  remote_path=None):
    """
    Upload files from local to remote server recursively.

    Arguments:
    local_path -- Local path or file to upload
    remote_path -- Remote path to upload to
    """
    if remote_path is None:
        remote_path = f"/home/{c.user}/"
    c = get_connection()
    c.put(local_path, remote_path, recursive=True)

# download files
def download(remote_path=None, local_path='.'):
    """
    Download files from remote server to local recursively.

    Arguments:
    remote_path -- Remote path or file to download
    local_path -- Local path to download to (default: current directory)
    """
    c = get_connection()
    if remote_path is None:
        remote_path = f'/home/{c.user}/'
    c.get(remote_path, local_path, recursive=True)

# compress files
def compress(src_path='.', name=None):
    """
    Compress files or directories into a tarball.

    Arguments:
    path -- Path to the file or directory to compress
    name -- Name of the tarball to create
    """
    c = get_connection()
    if name is None:
        compressed_filename = f'{src_path}/archive-{dt.now().strftime("%Y%m%d%H%M%S")}.tar.gz'
    else:
        compressed_filename = f'{src_path}/{name}-{dt.now().strftime("%Y%m%d%H%M%S")}.tar.gz'

    c.local(f'tar -czvf {compressed_filename} {src_path}')

    print(f'Files compressed to: {compressed_filename}')

# decompress files
def decompress(src_path='.', dest_path='.'):
    """
    Decompress a tarball file.

    Arguments:
    src_path -- Path to the tarball file to decompress
    dest_path -- Destination path to extract the files to
    """
    c = get_connection()
    c.local(f'tar -xzvf {src_path} -C {dest_path}')
    print(f'Files decompressed to: {dest_path}')


# Install Nginx
def install_nginx():
    """
    Install Nginx server on the remote server.
    """
    c = get_connection()
    # Run the installation script on the remote server
    c.sudo('bash nginx/install_nginx.sh')
    c.sudo('service nginx restart')
    c.sudo('service nginx status')


# configure nginx sites-available default file and create a link to sites-enabled
def configure_nginx():
    """
    Configure Nginx server to serve the Flask app.
    """
    # Define the path to the Nginx configuration file
    nginx_config_file = '/etc/nginx/sites-available/default'
    symlink_path = '/etc/nginx/sites-enabled/default'
    c = get_connection()
    # remove remote config file and exchange with local config file
    c.sudo('service nginx stop')
    c.sudo(f'rm -f {nginx_config_file}')
    c.put(f'nginx/default', '{nginx_config_file}')
    c.run(f'sudo ln -s {nginx_config_file} {symlink_path}')
    c.sudo('service nginx restart')
    c.sudo('service nginx status')


# Uninstall Nginx server
def uninstall_nginx():
    """
    Uninstall Nginx server from the remote server.
    """
    c = get_connection()
    # Run the uninstallation script on the remote server
    c.sudo('bash nginx/uninstall_nginx.sh')

# Check Nginx status
def check_nginx_status():
    """
    Check the status of the Nginx server on the remote server.
    """
    c = get_connection()   
    c.sudo('service nginx status')

def deploy_static():
    """
    Deploy static files to the remote server.
    """
    c = get_connection()
    print("Deploying static files...")
    c.put(local_static_path, remote_static_path, recursive=True)

def deploy_dynamic():
    """
    Deploy dynamic files (Flask app, Python files) to the remote server.
    """
    c = get_connection()
    print("Deploying dynamic files...")

    with Connection(host=host, user=user, connect_kwargs={'password': password}) as conn:
        # Upload dynamic files
        conn.put(local_dynamic_path, remote_dynamic_path, recursive=True)

def restart_server():
    """
    Restart the server or the application service.
    """
    c = get_connection()
    print("Restarting server...")

    # Example command to restart your application server (adjust as needed)
    c.sudo('systemctl restart your_application_service')

def deploy_all():
    """
    Deploy both static and dynamic files.
    """
    c = get_connection()   
    deploy_static(c)
    deploy_dynamic(c)
    restart_server(c)

# Additional tasks can be added for database migrations, configuration updates, etc.


check_nginx_status()