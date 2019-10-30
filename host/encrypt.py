import os
import socket
import time
from Crypto.PublicKey import RSA
from Crypto import Random


SERVER_IP = '172.26.17.82'
SERVER_PORT = 5000

KEY_LENGTH = 1024
CHUNKSIZE = 128
base_path = 'temp/'


def get_ip_name():
    f = os.popen('ifconfig eth0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
    IP = f.read()
    rules_file = base_path + 'host_' + IP + '.rules'

    return IP, rules_file


def save_iptables(rules_file):
    os.system('iptables-save > ' + rules_file)


def get_sock():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, SERVER_PORT))

    return sock


def receive_key(sock):
    sock = get_sock()
    pub_key = sock.recv(KEY_LENGTH).decode()
    sock.send(b'END')
    key = RSA.importKey(pub_key)
    sock.close()

    return key


def enc_file(rules_flie, key):
    enc_file = rules_file + '.enc'
    with open(rules_file, 'r') as f, open(enc_file, 'wb') as enc_f:
        while True:
            time.sleep(0.01)
            data = f.read(CHUNKSIZE)
            if data == '':
                break
            encrypted = key.encrypt(data.encode(), 32)
            enc_f.write(encrypted[0])
    
    return enc_file


if __name__ == '__main__':
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
    enc_file = enc_file(rules_file, key)
    print(enc_file)
    print("=====end program=====")