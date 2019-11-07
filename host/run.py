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


def receive_key(sock):
    print("connected")
    time.sleep(0.01)
    pub_key = sock.recv(Config.KEY_LENGTH).decode()
    sock.send(b'END')
    key = RSA.importKey(pub_key)

    return key


def encrypt(rules_file, key):
    enc_file = rules_file + '.enc'
    with open(rules_file, 'r') as f, open(enc_file, 'wb') as enc_f:
        while True:
            data = f.read(Config.CHUNK_SIZE)
            if data == '':
                break
            encrypted = key.encrypt(data.encode(), 32)
            enc_f.write(encrypted[0])
    
    return enc_file


def send_file(sock, enc_file):
    with open(enc_file, 'rb') as f:
        while True:
            time.sleep(0.01)
            data = f.read(512)
            if data == b'':
                sock.send(b'END')
                break
            sock.send(data)


def make_enc_file(sock):
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


def send(sock):
    ip, rules_file = get_ip_name()
    enc_file = rules_file + '.enc'
    print("=====sending encrypted file=====")
    send_file(sock, enc_file)
    print("=====end program=====")


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((Config.SERVER_IP, Config.SERVER_PORT))
    if sys.argv[1] == '-enc':
        make_enc_file(sock)
    if sys.argv[1] == '-send':
        send(sock)
    sock.close()
    