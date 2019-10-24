#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import RemoteController 
from mininet.node import OVSSwitch
from mininet.cli import CLI
from functools import partial
import time


class TestTopo(Topo):
    def build(self, n=2):
        s1 = self.addSwitch('s1')
        for h in range(n):
            host = self.addHost('h%s' % (h + 1))
            self.addLink(host, s1)

def test():
    topo = TestTopo(n=2)
    net = Mininet(topo=topo, controller=lambda name: RemoteController(name, ip="127.0.0.1", port=6653))
    nat0 = net.addNAT('nat0')
    net.start()
    dumpNodeConnections(net.hosts)
    time.sleep(5)
    net.pingAll()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    test()