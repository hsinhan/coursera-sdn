#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel

class LinearTopo(Topo):
   "Linear topology of k switches, with one host per switch."
   def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
   #def __init__(self, fanout=2, **opts):
       """Init.
           k: number of switches (and hosts)
           hconf: host configuration options
           lconf: link configuration options"""

       super(LinearTopo, self).__init__(**opts)

       
       anum = 0
       enum = 0
       hnum = 0



       core=self.addSwitch('c1')
       # Create Aggr switches
       for i in range(fanout):
           anum += 1
           aggr = self.addSwitch('a%s' % anum)
           self.addLink(core, aggr ,**linkopts1)

           for j in range(fanout):
               enum += 1
               edge = self.addSwitch('e%s' % enum)
               self.addLink(aggr, edge,**linkopts2)

               for k in range(fanout):
                   hnum += 1
                   host = self.addHost('h%s' % hnum)
                   self.addLink(edge, host,**linkopts3)


def perfTest():
   "Create network and run simple performance test"
   linkopts1 = {'bw':10, 'delay':'5ms', 'loss':1, 'max_queue_size':1000, 'use_htb':True}
   linkopts2 = {'bw':10, 'delay':'5ms', 'loss':1, 'max_queue_size':1000, 'use_htb':True}
   linkopts3 = {'bw':10, 'delay':'5ms', 'loss':1, 'max_queue_size':1000, 'use_htb':True}
   topo = LinearTopo(linkopts1,linkopts2,linkopts3, fanout=2)
   net = Mininet(topo=topo, 
                 host=CPULimitedHost, link=TCLink)
   net.start()
   print "Dumping host connections"
   dumpNodeConnections(net.hosts)
   print "Testing network connectivity"
   net.pingAll()
   print "Testing bandwidth between h1 and h4"
   h1, h4 = net.get('h1', 'h4')
   net.iperf((h1, h4))
   net.stop()

if __name__ == '__main__':
   setLogLevel('info')
   perfTest()
