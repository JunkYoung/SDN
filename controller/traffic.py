import paramiko
import time
from multiprocessing import Process, Queue

from config import *


HOST_COM = 'sudo iperf -s -D -p 5001'
GEN_COM = 'iperf -c 10.0.0.11 -u -b50M -i 1 -t 30 -p 5001'
MAL_COM = 'sudo hping3 -c 15000 -d 120 -S 10.0.0.11 -w 64 -p 80 --flood'


def run_host(host_ip, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host_ip, username=Config.HOST_USERNAME, password=Config.HOST_PASSWORD)
    stdin, stdout, stderr = ssh.exec_command(command)
    lines = stdout.readlines()
    for line in lines:
        print(line)
    lines = stderr.readlines()
    for line in lines:
        print(line)


def run_generator(ip, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username='wits_ids', password=Config.HOST_PASSWORD)
    stdin, stdout, stderr = ssh.exec_command(command)
    lines = stdout.readlines()
    for line in lines:
        print(line)
    lines = stderr.readlines()
    for line in lines:
        print(line)


def run_malicious(ip, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username='root', password=Config.HOST_PASSWORD)
    stdin, stdout, stderr = ssh.exec_command(command)
    lines = stdout.readlines()
    for line in lines:
        print(line)
    lines = stderr.readlines()
    for line in lines:
        print(line)


def generate_traffic():
    procs = []
    for ip in Config.HOST_IPS:
        proc = Process(target=run_host, args=(ip, HOST_COM))
        procs.append(proc)
        proc.start()
    # proc1 = Process(target=run_generator, args=(ip, GEN_COM))
    # procs.append(proc1)
    # proc1.start()
    # proc2 = Process(target=run_malicious, args=(ip, MAL_COM))
    # procs.append(proc2)
    # proc2.start()
    for proc in procs:
        proc.terminate()


if __name__ == '__main__':
    generate_traffic()