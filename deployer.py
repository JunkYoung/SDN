import sys
import requests

from controller import *


basePath = 'controller/'

username = 'admin'
password = 'admin'
priority = '1'
table_id = '0'
name = 'test'


def converse(rules_file, flow_id=0):
    flow_files = []
    with open(rules_file, 'r') as f:
        rules = f.readlines()
        for rule in rules:
            if '-A' in rule:
                is_ip_source = 0
                is_ip_dest = 0
                is_port_source = 0
                is_port_dest = 0
                is_udp = 0
                is_tcp = 0
                is_drop = 0
                rule = rule.split()
                if '-s' in rule:
                    is_ip_source = 1
                    idx = rule.index('-s')
                    ip_source = rule[idx+1]
                if '-d' in rule:
                    is_ip_dest = 1
                    idx = rule.index('-d')
                    ip_dest = rule[idx+1]
                if '--sport' in rule:
                    is_port_source = 1
                    idx = rule.index('--sport')
                    port_source = rule[idx+1]
                if '--dport' in rule:
                    is_port_dest = 1
                    idx = rule.index('--dport')
                    port_dest = rule[idx+1]
                if '-p' in rule:
                    idx = rule.index('-p')
                    if 'tcp' == rule[idx+1]:
                        is_tcp = 1
                    elif 'udp' == rule[idx+1]:
                        is_udp = 1
                if '-j' in rule:
                    idx = rule.index('-j')
                    if 'DROP' == rule[idx+1]:
                        is_drop = 1
                flow = ''
                flow = flow + '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
                flow = flow + '<flow xmlns="urn:opendaylight:flow:inventory">\n'
                flow = flow + '<priority>' + priority + '</priority>\n'
                flow = flow + '<flow-name>' + name + '</flow-name>\n'
                flow = flow + '<table_id>' + table_id + '</table_id>\n'
                flow = flow + '<id>' + str(flow_id) +'</id>\n'
                flow = flow + '<match>\n'
                flow = flow + '<ethernet-match>\n'
                flow = flow + '<ethernet-type>\n'
                flow = flow + '<type>2048</type>\n'
                flow = flow + '</ethernet-type>\n'
                flow = flow + '</ethernet-match>\n'
                if is_ip_source:
                    flow = flow + '<ipv4-source>' + ip_source + '</ipv4-source>\n'
                if is_ip_dest:
                    flow = flow + '<ipv4-destination>' + ip_dest + '</ipv4-destination>\n'
                if is_tcp:
                    flow = flow + '<ip-match>\n'
                    flow = flow + '<ip-protocol>6</ip-protocol>\n'
                    flow = flow + '<ip-dscp>2</ip-dscp>\n'
                    flow = flow + '<ip-ecn>2</ip-ecn>\n'
                    flow = flow + '</ip-match>\n'
                    if is_port_source:
                        flow = flow + '<tcp-source-port>' + port_source + '</tcp-source-port>\n'
                    if is_port_dest:
                        flow = flow + '<tcp-destination-port>' + port_dest + '</tcp-destination-port>\n'
                elif is_udp:
                    flow = flow + '<ip-match>\n'
                    flow = flow + '<ip-protocol>17</ip-protocol>\n'
                    flow = flow + '<ip-dscp>8</ip-dscp>\n'
                    flow = flow + '<ip-ecn>3</ip-ecn>\n'
                    flow = flow + '</ip-match>\n'
                    if is_port_source:
                        flow = flow + '<udp-source-port>' + port_source + '</udp-source-port>\n'
                    if is_port_dest:
                        flow = flow + '<udp-destination-port>' + port_dest + '</udp-destination-port>\n'
                flow = flow + '</match>\n'
                flow = flow + '<instructions>\n'
                flow = flow + '<instruction>\n'
                flow = flow + '<order>0</order>\n'
                flow = flow + '<apply-actions>\n'
                flow = flow + '<action>\n'
                flow = flow + '<order>0</order>\n'
                if is_drop:
                    flow = flow + '<dec-nw-ttl/>\n'
                flow = flow + '</action>\n'
                flow = flow + '</apply-actions>\n'
                flow = flow + '</instruction>\n'
                flow = flow + '</instructions>\n'
                flow = flow + '</flow>\n'

                flow_file = basePath + 'flow' + str(flow_id) + '.xml'
                with open(flow_file, 'w') as f:
                    f.write(flow)
                flow_files.append(flow_file)
                flow_id += 1

    return flow_files, flow_id


def deploy(flow_files, switchs):
    for flow_file in flow_files:
        flow_id = int(flow_file[15:-4])
        for switch in switchs:
            URL = 'http://localhost:8181/restconf/config/opendaylight-inventory:nodes/node/'+switch+'/table/'+table_id+'/flow/'+str(flow_id)
            headers = {'Content-Type': 'application/xml', 'Accept': 'application/xml'}
            data = open(flow_file, 'r').read()

            response = requests.put(URL, headers=headers, data=data, auth=(username, password))


if __name__=='__main__':
    print("=====conversing and deploying rules=====")
    nodes, switchs = read_hosts_switchs()
    flow_id = 0
    for node in nodes:
        try:
            rules = basePath + 'controller_' + node + '.rules'
            flow_files, flow_id = converse(rules, flow_id)
            print(rules + " has conversed")
            deploy(flow_files, switchs)
            print(rules + " has deployed")
        except:
            print("no rules of " + node)
            pass
    print("=====end program=====")