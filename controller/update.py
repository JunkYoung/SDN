import paramiko

from config import *


COMMANDS = []
COMMANDS.append('sudo rm -r SDN')
COMMANDS.append('git clone http://github.com/JunkYoung/SDN.git')
#COMMANDS.append('sudo iptables -F')
#COMMANDS.append('cd SDN/host && sudo python3 generate.py 300')


def update_host(host_ips, commands):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for ip in host_ips:
        print(ip)
        ssh.connect(ip, username=Config.USERNAME, password=Config.PASSWORD)
        for command in commands:
            print(command)
            stdin, stdout, stderr = ssh.exec_command(command)
            lines = stdout.readlines()
            for line in lines:
                print(line)
            lines = stderr.readlines()
            for line in lines:
                print(line)
        ssh.close()


if __name__ == '__main__':
    update_host(Config.HOST_IPS, COMMANDS)