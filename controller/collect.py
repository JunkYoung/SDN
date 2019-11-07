import socket
import paramiko
import time
from Crypto.PublicKey import RSA
from Crypto import Random

from config import *
from encrypt import *

COMMANDS = []
COMMANDS.append('cd SDN/host/ && sudo python3 send.py')


def load_key():
    with open (Config.BASE_PATH + 'private.pem', 'rb') as f:
        priv_key = RSA.importKey(f.read())
    
    return priv_key


def recv_file(sock):
    while True:
        sock.listen(1)
        conn, addr = sock.accept()
        enc_file = Config.BASE_PATH + "controller" + conn.getpeername()[0] + ".rules.enc"
        with open(enc_file, 'wb') as f:
            while True:
                data = conn.recv(512)
                if data == b'END':
                    break
                else:
                    f.write(data)
        conn.close()


def dec_files(priv_key):
    for ip in Config.HOST_IPS:
        enc_file = Config.BASE_PATH + "controller" + ip + ".rules.enc"
        rules_file = enc_file[:-4]
        with open(enc_file, 'rb') as enc_f, open(rules_file, 'w') as dec_f:
            while True:
                encrypted = enc_f.read(Config.CHUNK_SIZE)
                if encrypted == b'':
                    break
                decrypted = priv_key.decrypt(encrypted)
                try:
                    dec_f.write(decrypted.decode())
                    print(decrypted.decode())
                except:
                    dec_f.write(b'-error'.decode())


def collect_all():
    print("=====loading key=====")
    priv_key = load_key()
    print("=====receiving data=====")
    run_hosts(COMMANDS, recv_file)
    print("=====decrypting data=====")
    dec_files(priv_key)
    print("=====end program=====")


if __name__ == '__main__':
    collect_all()