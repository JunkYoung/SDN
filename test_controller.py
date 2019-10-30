import socket
import json
import requests
import time
import base64
from scapy.all import *
from scapy.layers import inet
from Crypto.PublicKey import RSA
from Crypto import Random

from deployer import *


ip = '10.0.2.15'
port = 5000
baseUrl = 'http://localhost:8181/restconf'
odl_username = 'admin'
odl_password = 'admin'

KEY_LENGTH = 1024
CHUNKSIZE = 128
basePath = 'controller/'


def read_hosts_switchs():
    url = baseUrl + '/operational/network-topology:network-topology'
    response = requests.get(url, auth=(odl_username, odl_password))
    switchs = []
    node_egress = []
    for nodes in response.json()['network-topology']['topology']:
        node_info = nodes['node']
        for node in node_info:
            try:
                switch = node['node-id']
                if 'openflow' in switch:
                    switchs.append(switch)
                tp_id = node['host-tracker-service:attachment-points'][0]['tp-id']
                node_egress.append(tp_id)
            except:
                pass

    return node_egress, switchs


def generate_key():
    random_generator = Random.new().read
    keypair = RSA.generate(KEY_LENGTH, random_generator)
    
    return keypair


def send_key(egress, keypair):
    pubkey = keypair.publickey().exportKey()
    packet = '00000000000000' + pubkey.decode()
    payload = base64.b64encode(packet.encode()).decode()

    node_id = egress[:-2]
    url = baseUrl + '/operations/packet-processing:transmit-packet'
    headers = {'Content-Type' : 'application/json'}
    data = { "input":
	    {
	    	"connection-cookie": "123456",
            "egress": "/opendaylight-inventory:nodes/opendaylight-inventory:node[opendaylight-inventory:id='" + node_id + "']/opendaylight-inventory:node-connector[opendaylight-inventory:id='" + egress + "']", 
            "node": "/opendaylight-inventory:nodes/opendaylight-inventory:node[opendaylight-inventory:id='" + node_id + "']", 
            "payload": payload
        }
    }
    response = requests.post(url, auth=(odl_username, odl_password), headers=headers, data=json.dumps(data))


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
    egresses, switchs = read_hosts_switchs()
    print(egresses)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    key = generate_key()
    flow_id = 0
    for egress in egresses:
        print("=====sending key to node=====")
        send_key(egress, key)
        print(egress)
        print("=====receiving data=====")
        enc_file = basePath + "controller_" + egress[:-2] + ".rules.enc"
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