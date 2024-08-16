import paramiko
import socket
from paramiko.ssh_exception import NoValidConnectionsError, AuthenticationException, SSHException

def ssh_to_ip(ip, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(ip, username=username, password=password, timeout=5)
        stdin, stdout, stderr = client.exec_command("hostname")
        hostname = stdout.read().decode().strip()
        print(f"Success: {ip} - Hostname: {hostname}")
        return True
    except (AuthenticationException, SSHException, NoValidConnectionsError, socket.error) as e:
        print(f"Fail: {ip} - {str(e)}")
        return False
    finally:
        client.close()

def main():
    username = "jnash1"
    password = "Ruggles72"

    base_ip = "136.244.224."
    
    for i in range(1, 255):
        ip = base_ip + str(i)
        ssh_to_ip(ip, username, password)

if __name__ == "__main__":
    main()

