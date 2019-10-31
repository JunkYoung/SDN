import socket
import paramiko
from Crypto.PublicKey import RSA
from Crypto import Random

from config import *


commands = []
#commands.append('SDN/host/sudo python3 generate.py 10')
commands.append('SDN/host/sudo python3 encrypt.py')


def generate_key():
    random_generator = Random.new().read
    keypair = RSA.generate(Config.KEY_LENGTH, random_generator)
    with open (Config.BASE_PATH + 'private.pem', 'wb') as f:
        f.write(keypair.privatekey().exportKey())
    with open (Config.BASE_PATH + 'public.pem', 'wb') as f:
        f.write(keypair.publickey().exportKey())
    pub_key = keypair.publickey.exportKey()

    return pub_key


#run hosts using ssh, and do function fun with args using sock with that host
def run_hosts(fun, *args):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((Config.IP, Config.PORT))
    for ip in Config.HOST_IPS:
        ssh.connect(ip, username=Config.USERNAME, password=Config.PASSWORD)
        for command in commands:
            stdin, stdout, stderr = ssh.exec_command(command)
            lines = stdout.readlines()
            for line in lines:
                print(line)
            lines = stderr.readlines()
            for line in lines:
                print(line)
        fun(sock, *args)
        ssh.close()
    sock.close()


def send_key(sock, pub_key):
    sock.listen(1)
    conn, addr = sock.accept()
    conn.send(pub_key.encode())
    while True:
        data = sock.recv(512)
        if (data == b'END'):
            break
    conn.close()


def send_enc_msg():
    print("=====generating key=====")
    pub_key = generate_key()
    print("=====sending key=====")
    run_hosts(send_key, pub_key)


if __name__ == '__main__':
    send_enc_msg()