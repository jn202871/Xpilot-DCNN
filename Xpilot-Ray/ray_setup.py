import os
import paramiko
from getpass import getpass

def create_cluster(username, password, head_ip, worker_ips, files_to_transfer, remote_dir):
    setup_ray_cluster(username, password, head_ip, worker_ips, files_to_transfer, remote_dir)
    #for ip in worker_ips:
        #ssh_command(username, password, ip, "pip install paramiko")
        #ssh_command(username, password, ip, "pip install ray[default]")
        #ssh_command(username, password, ip, "sudo apt install xvfb")
        #install_pip_packages_on_node(ip, username, password, remote_dir, 'requirements.txt')
    print("Cluster created and all nodes initialized.")

def shutdown_cluster(username, password, worker_ips, assets_directory, remote_dir):
    files_to_transfer = list_files_in_directory(assets_directory)
    os.system("ray stop --force")
    for ip in worker_ips:
        try:
            ssh_command(username, password, ip, "ray stop --force")
            cleanup_remote_temp_files(username, password, ip, files_to_transfer, remote_dir)
        except Exception as e:
            print(e)
            print(ip)
    print("Cluster shut down and all files cleaned up.")

def ssh_command(username, password, hostname, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)
    stdin, stdout, stderr = client.exec_command(command)
    client.close()

def list_files_in_directory(directory):
    """List all files in a given directory."""
    return [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def transfer_files_dir(username, password, hostname, local_files, remote_path='/tmp'):
    """Transfer files to a remote machine via SFTP."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)
    sftp = client.open_sftp()
    for local_file in local_files:
        filename = os.path.basename(local_file)
        remote_file = os.path.join(remote_path, filename)
        sftp.put(local_file, remote_file)
        #print(f"Transferred {local_file} to {remote_file} on {hostname}")
    sftp.close()
    client.close()

def cleanup_remote_temp_files(username, password, hostname, files, remote_path='/tmp'):
    """Remove temporary files from the remote machine."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)
    for file in files:
        remote_file = os.path.join(remote_path, os.path.basename(file))
        command = f"rm -f {remote_file}"
        client.exec_command(command)
        #print(f"Removed temporary file {remote_file} on {hostname}")
    client.close()

def setup_ray_cluster(username, password, head_ip, worker_ips, files_to_transfer, remote_dir):
    """Setup ray worker machines"""
    manager_resource = f'{{"manager_resource": 1}}'
    head_command = f"ray start --include-dashboard=True --head --port=6379 --num-cpus=8 --num-gpus=1 --resources='{manager_resource}'"
    os.system(head_command)
    for i, ip in enumerate(worker_ips):
        try:
            worker_resource = f'{{"worker": 1}}'
            worker_command = f"ray start --address='{head_ip}:6379' --num-cpus=4 --resources='{worker_resource}'"
            transfer_files_dir(username, password, ip, files_to_transfer, remote_dir)
            ssh_command(username, password, ip, worker_command)
        except Exception as e:
            print(e)
            print(ip)

def install_pip_packages_on_node(node_ip, username, password, remote_dir, requirements_file):
    # SSH into the node and install Python packages
    os.system(f"ssh {username}@{node_ip} 'pip install -r -y {os.path.join(remote_dir, requirements_file)}'")
