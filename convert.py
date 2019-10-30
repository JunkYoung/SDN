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