import os
import sys
import random


def generate_rules(num):
    rules = []
    for i in range(num):
        rule = 'iptables -A INPUT'
        rand = random.randint(0, 1)
        if rand == 0:
            rand_ip = str(random.randint(0, 255)) + '.' + str(random.randint(0, 255)) + '.' + str(random.randint(0, 255)) + '.' + str(random.randint(0, 255))
            rule += ' -s ' + rand_ip
        rand = random.randint(0, 1)
        if rand == 0:
            rand_ip = str(random.randint(0, 255)) + '.' + str(random.randint(0, 255)) + '.' + str(random.randint(0, 255)) + '.' + str(random.randint(0, 255))
            rule += ' -d ' + rand_ip
        rand = random.randint(0, 1)
        if rand == 0:
            rule += ' -p tcp'
            rand_port = str(random.randint(0, 65535))
            rule += ' --sport ' + rand_port
            rand_port = str(random.randint(0, 65535))
            rule += ' --dport ' + rand_port
        else:
            rule += ' -p udp'
            rand_port = str(random.randint(0, 65535))
            rule += ' --sport ' + rand_port
            rand_port = str(random.randint(0, 65535))
            rule += ' --dport ' + rand_port

        rule += ' -j DROP'
        rules.append(rule)

    return rules


def apply_rules(rules):
    for rule in rules:
        try:
            os.system(rule)
        except:
            print("failed apply rule: " + rule)


if __name__=='__main__':
    print("=====generating rules=====")    
    rules = generate_rules(int(sys.argv[1]))
    print("=====applying rules=====")
    apply_rules(rules)
    print("=====end program=====")