import os
import socket
import time
from scapy.all import *
from Crypto.PublicKey import RSA
from Crypto import Random


IP = '10.0.2.15'
PORT = 5000
DEST = (IP, PORT)

KEY_LENGTH = 1024
CHUNKSIZE = 128
basePath = 'host/'


def get_ip_name():
    os.system('ifconfig > ' + basePath + 'ip_temp.txt')
    with open(basePath + 'ip_temp.txt', 'r') as f:
        text = f.read()
        if 'nat0' in text:
            nat_idx = text.index('nat0')
            text = text[nat_idx:]
            if 'inet' in text:
                idx = text.index('inet')
                ip_addr = text[idx:idx+30].split()[1][5:]
        elif 'inet' in text:
            idx = text.index('inet')
            ip_addr = text[idx:idx+30].split()[1][5:]
    rules_file = basePath + 'host_' + ip_addr + '.rules'

    return ip_addr, rules_file


def save_iptables(rules_file):
    os.system('iptables-save > ' + rules_file)


def receive_key(filter):
    packet = sniff(filter = filter, count = 1)
    pubkey = bytes_encode(packet[0])[14:-1]
    key = RSA.importKey(pubkey)

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


def send_file(enc_file):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    with open(enc_file, 'rb') as f:
        while True:
            time.sleep(0.01)
            data = f.read(512)
            if data == b'':
                sock.sendto(b'END', DEST)
                break
            sock.sendto(data, DEST)
    sock.close()


if __name__ == '__main__':
    print("=====getting host info=====")
    host_ip, rules_file = get_ip_name()
    print(host_ip)
    print("=====saving iptables=====")
    save_iptables(rules_file)
    print(rules_file)
    print("=====waitting for connect=====")
    key = receive_key('ether proto 0x3030')
    print("=====received key=====")
    print("=====encrypting rules file=====")
    enc_file = enc_file(rules_file, key)
    print(enc_file)
    print("=====sending encrypted file=====")
    send_file(enc_file)
    print("=====end program=====")