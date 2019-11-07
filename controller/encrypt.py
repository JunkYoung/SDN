import socket
import paramiko
import threading
import time
from Crypto.PublicKey import RSA
from Crypto import Random

from config import *


COMMANDS = []
#COMMANDS.append('cd SDN/host/ && sudo python3 generate.py 200')
COMMANDS.append('cd SDN/host/ && sudo python3 encrypt.py')
#COMMANDS.append('sudo rm -r SDN')
#COMMANDS.append('git clone http://github.com/JunkYoung/SDN.git')


def generate_key():
    random_generator = Random.new().read
    keypair = RSA.generate(Config.KEY_LENGTH, random_generator)
    pub_key = keypair.publickey().exportKey()
    with open (Config.BASE_PATH + 'private.pem', 'wb') as f:
        f.write(keypair.exportKey())
    with open (Config.BASE_PATH + 'public.pem', 'wb') as f:
        f.write(pub_key)

    return pub_key


def get_sock():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    sock.bind((Config.IP, Config.PORT))

    return sock


#run hosts using ssh, and do function fun with thread using sock with that host
def run_hosts(sock, commands, fun, host_ips):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    thread = threading.Thread(target=fun, args=(sock,))
    thread.daemon = True
    thread.start()
    for ip in host_ips:
        print(ip)
        ssh.connect(ip, username=Config.USERNAME, password=Config.PASSWORD)
        for command in commands:
            print(command)
            stdin, stdout, stderr = ssh.exec_command(command)
            lines = stdout.readlines()
            for line in lines:
                print(line)
            lines = stderr.readlines()
            for line in lines:
                print(line)
        ssh.close()


def send_key(sock):
    print("=====generating key=====")
    pub_key = generate_key()
    print("=====waitting connection=====")
    while True:
        sock.listen(1)
        conn, addr = sock.accept()
        conn.send(pub_key)
        while True:
            data = conn.recv(512)
            if (data == b'END'):
                break
        conn.close()


def send_enc_msg():
    sock = get_sock()
    run_hosts(sock, COMMANDS, send_key, Config.HOST_IPS)
    sock.close()


if __name__ == '__main__':
    send_enc_msg()