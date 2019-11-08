import paramiko

from config import *


HOST_IP = '172.26.17.131'
COM = 'top -b -d 1 -n 100 |grep Cpu'


def cpu_measure():
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	with open('cpu_result.txt', 'a') as f:
		ssh.connect(HOST_IP, username=Config.HOST_USERNAME, password=Config.HOST_PASSWORD)
		stdin, stdout, stderr = ssh.exec_command(COM)
		lines = stdout.readlines()
		for line in lines:
			print(line)
			f.write(line)
		lines = stderr.readlines()
		for line in lines:
			print(line)
			ssh.close()


if __name__=='__main__':
	cpu_measure()