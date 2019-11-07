import os
import socket
import time
from Crypto.PublicKey import RSA
from Crypto import Random

from config import *
from encrypt import *


def send_file(enc_file):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((Config.SERVER_IP, Config.SERVER_PORT))
    print("connected")
    with open(enc_file, 'rb') as f:
        while True:
            data = f.read(512)
            print(data)
            if data == b'':
                sock.send(b'END')
                break
            sock.send(data)
    sock.close()


def send():
    ip, rules_file = get_ip_name()
    enc_file = rules_file + '.enc'
    print("=====sending encrypted file=====")
    send_file(enc_file)
    print("=====end program=====")


if __name__ == '__main__':
    send()