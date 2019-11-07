import socket
import paramiko
import time
from Crypto.PublicKey import RSA
from Crypto import Random

from config import *
from encrypt import *


COMMANDS = []
COMMANDS.append('cd SDN/host/ && sudo python3 send.py')

RETRY = []
RETRY.append('cd SDN/host/ && sudo python3 encrypt.py')
RETRY.append('cd SDN/host/ && sudo python3 send.py')


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


def dec_files(priv_key, host_ips):
    retry_hosts = []
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
                except:
                    retry_hosts.append(ip)
                    dec_f.write(b'-error'.decode())
                    break

    return retry_hosts


def retry(sock, retry_hosts):
    #run_hosts(sock, [RETRY[0]], send_key, retry_hosts)
    priv_key = load_key()
    run_hosts(sock, [RETRY[1]], recv_file, retry_hosts)
    retry_hosts = dec_files(priv_key, retry_hosts)
    if retry_hosts:
        retry(sock, retry_hosts)


def collect_all():
    sock = get_sock()
    print("=====loading key=====")
    priv_key = load_key()
    print("=====receiving data=====")
    run_hosts(sock, COMMANDS, recv_file, Config.HOST_IPS)
    print("=====decrypting data=====")
    retry_hosts = dec_files(priv_key, Config.HOST_IPS)
    if retry_hosts:
        retry(sock, retry_hosts)
    print("=====end program=====")
    sock.close()


if __name__ == '__main__':
    collect_all()