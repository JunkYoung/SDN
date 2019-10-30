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


def get_filename():
    f = os.popen('ifconfig eth0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
    IP = f.read()
    rules_file = base_path + 'host_' + IP + '.rules'

    return rules_file


def get_sock():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, SERVER_PORT))

    return sock


def send_file(enc_file):
    sock = get_sock()
    with open(enc_file, 'rb') as f:
        while True:
            time.sleep(0.01)
            data = f.read(512)
            if data == b'':
                sock.send(b'END')
                break
            sock.send(data)
    sock.close()


if __name__ == '__main__':
    print("=====host encfile=====")
    rules_file = get_filename()
    enc_file = rules_file + '.enc'
    print(enc_file)
    print("=====sending encrypted file=====")
    send_file(enc_file)
    print("=====end program=====")