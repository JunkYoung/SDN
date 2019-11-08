import paramiko
from Crypto.PublicKey import RSA
from Crypto import Random

from config import *


COMMANDS = []
COMMANDS.append('cd SDN/host/ && sudo python3 test_run.py')


def generate_key():
    random_generator = Random.new().read
    keypair = RSA.generate(Config.KEY_LENGTH, random_generator)
    pub_key = keypair.publickey().exportKey()
    with open (Config.BASE_PATH + 'private.pem', 'wb') as f:
        f.write(keypair.exportKey())
    with open (Config.BASE_PATH + 'public.pem', 'wb') as f:
        f.write(pub_key)


def send_key(host_ips):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for ip in host_ips:
        print(ip)
        ssh.connect(ip, username=Config.USERNAME, password=Config.PASSWORD)
        sftp = ssh.open_sftp()
        sftp.put(Config.BASE_PATH + 'public.pem', Config.HOST_BASE_PATH + 'public.pem')
        sftp.close()
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


def send_enc_msg(host_ips):
    print("=====generating key=====")
    generate_key()
    send_key(host_ips)


if __name__ == '__main__':
    send_enc_msg(Config.HOST_IPS)