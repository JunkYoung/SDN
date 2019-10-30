def build_flow(nodeid, flowname, ethertype='', destip='', ipcos='', ipprot='',
            installflag='', outnodeconn='', outdstmac='', innodeconn=''):
    new_flow = {}
    newflow['name'] = flowname
    if (installflag != ''):
        newflow['installInHw'] = installflag
    else:
        newflow['installInHw'] = 'true'
    newflow['node'] = {u'id': nodeid, u'type': u'OF'}
    if (destip != ''):
        newflow['nwDst'] = destip
    if (ethertype != ''):
        newflow['etherType'] = ethertype
    if (ipcos != ''):
        newflow['tosBits'] = ipcos
    if (ipprot != ''):
        newflow['protocol'] = ipprot
    newflow['priority'] = 500
    node = {}
    node['id'] = nodeid
    node['type'] = 'OF'
    newflow['node'] = node

if __name__=="__main__":
    print("=====converting rules to flow=====")
    print("temp/controller_10.0.0.5.rules")
    print("temp/controller_10.0.0.11.rules")
    print("=====finished=====")