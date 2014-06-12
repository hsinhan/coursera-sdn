'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment 2

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta, Muhammad Shahbaz
'''



from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel

class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"
    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        
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

                    
topos = { 'custom': ( lambda: CustomTopo() ) }