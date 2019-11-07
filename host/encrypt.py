import os
import socket
import time
from Crypto.PublicKey import RSA
from Crypto import Random

from config import *


def get_ip_name():
    f = os.popen('ifconfig eth0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
    ip = f.read().strip()
    rules_file = Config.BASE_PATH + 'host_' + ip + '.rules'

    return ip, rules_file


def save_iptables(rules_file):
    os.system('iptables-save > ' + rules_file)


def receive_key():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((Config.SERVER_IP, Config.SERVER_PORT))
    pub_key = sock.recv(Config.KEY_LENGTH).decode()
    sock.send(b'END')
    sock.close()
    key = RSA.importKey(pub_key)

    return key


def encrypt(rules_file, key):
    enc_file = rules_file + '.enc'
    with open(rules_file, 'r') as f, open(enc_file, 'wb') as enc_f:
        while True:
            time.sleep(0.01)
            data = f.read(Config.CHUNK_SIZE)
            print(data)
            if data == '':
                break
            time.sleep(0.01)
            encrypted = key.encrypt(data.encode(), 32)
            print(encrypted[0])
            enc_f.write(encrypted[0])
    
    return enc_file


def make_enc_file():
    print("=====getting host info=====")
    host_ip, rules_file = get_ip_name()
    print(host_ip)
    print("=====saving iptables=====")
    save_iptables(rules_file)
    print(rules_file)
    print("=====waitting for connect=====")
    key = receive_key()
    print("=====received key=====")
    print("=====encrypting rules file=====")
    enc_file = encrypt(rules_file, key)
    print(enc_file)
    print("=====end program=====")


if __name__ == '__main__':
    make_enc_file()
    