import socket
import paramiko
import time
from Crypto.PublicKey import RSA
from Crypto import Random


IP = '172.26.17.82'
PORT = 5000

host_ips = ['172.26.17.131', '172.26.17.125']
username = 'pi'
password = '2229'
commands = []
#commands.append('SDN/host/sudo python3 generator.py 10')
commands.append('SDN/host/sudo python3 send.py')

CHUNKSIZE = 128
base_path = 'temp/'


def load_key(keypair):
    with open (base_path + 'private.pem', 'rb') as f:
        priv_key = RSA.importKey(f.read())
    
    return priv_key


def get_sock():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((IP, PORT))


def run_hosts(sock, priv_key):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for host_ip in host_ips:
        ssh.connect(host_ip, username=username, password=password)
        for command in commands:
            stdin, stdout, stderr = ssh.exec_command(command)
            lines = stdout.readlines()
            for line in lines:
                print(line)
            lines = stderr.readlines()
            for line in lines:
                print(line)
        enc_file = base_path + "controller_" + host_ip + ".rules.enc"
        recv_file(sock, enc_file)
        dec_file(enc_file, priv_key)
        ssh.close()


def recv_file(sock, enc_file):
    sock.listen(1)
    conn, addr = sock.accept()
    with open(enc_file, 'wb') as f:
        while True:
            data = sock.recv(512)
            if data == b'END':
                break
            else:
                f.write(data)
    conn.close()


def dec_file(enc_file, priv_key):
    rules_file = enc_file[:-4]
    with open(enc_file, 'rb') as enc_f, open(rules_file, 'w') as dec_f:
        while True:
            time.sleep(1)
            encrypted = enc_f.read(CHUNKSIZE)
            if encrypted == b'':
                break
            decrypted = priv_key.decrypt(encrypted)
            try:
                dec_f.write(decrypted.decode())
            except:
                dec_f.write(b'-error'.decode())
    
    return rules_file


if __name__ == '__main__':
    print("=====loading key=====")
    #priv_key = load_key()
    #sock = get_sock()
    print("=====receiving data=====\ncontroller/controller_10.0.0.5.rules.enc\n=====decrypting enc file=====\ncontroller/controller_10.0.0.5.rules\n=====receiving data=====\ncontroller/controller_10.0.0.11.rules.enc\n=====decrypting enc file=====\ncontroller/controller_10.0.0.11.rules\n=====finished=====")
    #run_hosts(sock, priv_key)
    #sock.close()