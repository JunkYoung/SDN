import sys
import requests



basePath = 'controller/'

username = 'admin'
password = 'admin'
priority = '1'
table_id = '0'
name = 'test'


def deploy(flow_files, switchs):
    for flow_file in flow_files:
        flow_id = int(flow_file[15:-4])
        for switch in switchs:
            URL = 'http://localhost:8181/restconf/config/opendaylight-inventory:nodes/node/'+switch+'/table/'+table_id+'/flow/'+str(flow_id)
            headers = {'Content-Type': 'application/xml', 'Accept': 'application/xml'}
            data = open(flow_file, 'r').read()

            response = requests.put(URL, headers=headers, data=data, auth=(username, password))


if __name__=='__main__':
    # print("=====conversing and deploying rules=====")
    # nodes, switchs = read_hosts_switchs()
    # flow_id = 0
    # for node in nodes:
    #     try:
    #         rules = basePath + 'controller_' + node + '.rules'
    #         #flow_files, flow_id = convert(rules, flow_id)
    #         print(rules + " has conversed")
    #         deploy(flow_files, switchs)
    #         print(rules + " has deployed")
    #     except:
    #         print("no rules of " + node)
    #         pass
    # print("=====end program=====")
    print("=====deploying flows=====")
    print("switch1")
    print("switch2")
    print("=====finished=====")
