import json

from config import *


def get_rules_files():
    rules_files = []
    for ip in Config.HOST_IPS:
        rules_file = Config.BASE_PATH + 'controller' + ip + '.rules'
        rules_files.append(rules_file)
    
    return rules_files


def convert(rules_file, flow_id):
    with open(rules_file, 'r') as f:
        rules = f.readlines()
        for switch, idx in Config.SWITCHS:
            for rule in rules:
                if '-A' in rule:
                    is_ip_source = False
                    is_ip_dest = False
                    is_port_source = False
                    is_port_dest = False
                    is_udp = False
                    is_tcp = False
                    is_drop = False
                    rule = rule.split()
                    if '-s' in rule:
                        is_ip_source = True
                        idx = rule.index('-s')
                        ip_source = rule[idx+1]
                    if '-d' in rule:
                        is_ip_dest = True
                        idx = rule.index('-d')
                        ip_dest = rule[idx+1]
                    if '--sport' in rule:
                        is_port_source = True
                        idx = rule.index('--sport')
                        port_source = rule[idx+1]
                    if '--dport' in rule:
                        is_port_dest = True
                        idx = rule.index('--dport')
                        port_dest = rule[idx+1]
                    if '-p' in rule:
                        idx = rule.index('-p')
                        if 'tcp' == rule[idx+1]:
                            is_tcp = True
                        elif 'udp' == rule[idx+1]:
                            is_udp = True
                    if '-j' in rule:
                        idx = rule.index('-j')
                        if 'DROP' == rule[idx+1]:
                            is_drop = True

                flow_name = 'sw' + idx + '_flow' + str(flow_id)
                new_flow = {}
                new_flow['name'] = flow_name
                new_flow['installInHw'] = 'true'
                new_flow['node'] = {u'id': switch, u'type': u'OF'}
                new_flow['etherType'] = 0x800
                if (is_ip_source):
                    pass
                if (is_ip_dest):
                    new_flow['nwDst'] = ip_dest
                if (is_tcp):
                    new_flow['protocol'] = 'tcp'
                if (is_udp):
                    new_flow['protocol'] = 'udp'
                if (is_port_source):
                    pass
                if (is_port_dest):
                    pass
                new_flow['priority'] = 500
                #node = {}
                #node['id'] = switch
                #node['type'] = 'OF'
                #new_flow['node'] = node
                if (is_drop):
                    new_flow['actions'] = ['DROP']
                with open(Config.BASE_PATH + flow_name + '.json', 'w') as f:
                    f.write(json.dump(new_flow))


def convert_all():
    rules_files = get_rules_files()
    for rules_file in rules_files:
        convert(rules_file)


if __name__=="__main__":
    convert_all()