import socket
import paramiko
from Crypto.PublicKey import RSA
from Crypto import Random


IP = '172.26.17.82'
PORT = 5000

host_ips = ['172.26.17.131', '172.26.17.125']
username = 'pi'
password = '2229'
commands = []
#commands.append('SDN/host/sudo python3 generate.py 10')
commands.append('SDN/host/sudo python3 encrypt.py')

KEY_LENGTH = 1024
base_path = 'temp'


def generate_key():
    random_generator = Random.new().read
    keypair = RSA.generate(KEY_LENGTH, random_generator)
    
    return keypair


def save_key(keypair):
    with open (base_path + 'private.pem', 'wb') as f:
        f.write(keypair.privatekey().exportKey())
    with open (base_path + 'public.pem', 'wb') as f:
        f.write(keypair.publickey().exportKey())


def run_hosts(sock, keypair):
    pub_key = keypair.publickey().exportKey()
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for host_ip in host_ips:
        print("=====key sending to " + host_ip + "=====")
        ssh.connect(host_ip, username=username, password=password)
        for command in commands:
            stdin, stdout, stderr = ssh.exec_command(command)
            lines = stdout.readlines()
            for line in lines:
                print(line)
            lines = stderr.readlines()
            for line in lines:
                print(line)
        send_key(sock, pub_key)
        ssh.close()


def send_key(sock, pub_key):
    sock.listen(1)
    conn, addr = sock.accept()
    conn.send(pub_key.encode())
    while True:
        data = sock.recv(512)
        if (data == b'END'):
            break
    conn.close()


def get_sock():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((IP, PORT))


if __name__ == '__main__':
    keypair = generate_key()
    save_key(keypair)
    sock = get_sock()
    run_hosts(sock, keypair)
    sock.close()