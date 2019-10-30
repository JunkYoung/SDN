import socket
import json
import requests
import time
from Crypto.PublicKey import RSA
from Crypto import Random

#from deployer import *


IP = '10.0.2.15'
PORT = 5000
baseUrl = 'http://localhost:8181/restconf'
odl_username = 'admin'
odl_password = 'admin'

KEY_LENGTH = 1024
CHUNKSIZE = 128
basePath = 'controller/'


def read_hosts_switchs():
    odl_url = baseUrl + '/operational/network-topology:network-topology'
    response = requests.get(odl_url, auth=(odl_username, odl_password))
    node_ips = []
    switchs = []
    for nodes in response.json()['network-topology']['topology']:
        node_info = nodes['node']
        for node in node_info:
            try:
                switch = node['node-id']
                if 'openflow' in switch:
                    switchs.append(switch)
                ip_address = node['host-tracker-service:addresses'][0]['ip']
                mac_address = node['host-tracker-service:addresses'][0]['mac']
                tp_id = node['host-tracker-service:attachment-points'][0]['tp-id']
                if IP != ip_address:
                    node_ips.append(ip_address)
            except:
                pass

    return node_ips, switchs


def generate_key():
    random_generator = Random.new().read
    keypair = RSA.generate(KEY_LENGTH, random_generator)
    
    return keypair


def send_key(sock, node, keypair):
    pubkey = keypair.exportKey()
    if node != IP:
        sock.sendto(pubkey, (node, PORT))


def recv_file(sock, enc_file):
    with open(enc_file, 'ab') as f:
        while True:
            data, addr = sock.recvfrom(512)
            if data == b'END':
                break
            else:
                f.write(data)


def dec_file(enc_file, keypair):
    rules_file = enc_file[:-4]
    with open(enc_file, 'rb') as enc_f, open(rules_file, 'w') as dec_f:
        while True:
            time.sleep(1)
            encrypted = enc_f.read(CHUNKSIZE)
            if encrypted == b'':
                break
            decrypted = keypair.decrypt(encrypted)
            try:
                dec_f.write(decrypted.decode())
            except:
                dec_f.write(b'-error'.decode())
    
    return rules_file

        
if __name__ == '__main__':
    print("=====getting node info=====")
    nodes, switchs = read_hosts_switchs()
    print(nodes)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((IP, PORT))
    key = generate_key()
    flow_id = 0
    for node in nodes:
        print("=====sending key to node=====")
        send_key(sock, node, key) 
        print(node)
        print("=====receiving data=====")
        enc_file = basePath + "controller_" + node + ".rules.enc"
        recv_file(sock, enc_file)
        print(enc_file)
        print('=====decrypting enc file=====')
        rules_file = dec_file(enc_file, key)
        print(rules_file)
        #print("=====conversing rules=====")
        #flow_files, flow_id = converse(rules_file, flow_id)
        #print("=====deploying rules=====" + "\n")
        #deploy(flow_files, flow_id, switchs)
    print("=====end program=====")