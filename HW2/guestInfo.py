import libvirt
import sys

conn = libvirt.open('qemu:///system')

for id in conn.listDomainsID():
    dom = conn.lookupByID(id)
    infos = dom.info()
    print 'ID = %d' % id
    print 'UUID = %s' % dom.UUIDString()
    print 'OS type = %s' %dom.OSType()
    print 'Name =  %s' % dom.name()
    print 'State = %d' % infos[0]
    print 'Max Memory MB = %d' % infos[1]
    print 'Number of virt CPUs = %d' % infos[3]
    print 'CPU Time (in ns) = %d' % infos[4]
    print 'Domain Active = %s' % str(dom.isActive())
    cpu_stats = dom.getCPUStats(False)
    print 'CPU time:'
    for (i, cpu) in enumerate(cpu_stats):
        print('  CPU '+str(i)+' Time: '+str(cpu['cpu_time'] / 1000000000.))
    stats  = dom.memoryStats()
    print('Memory used:')
    for name in stats:
        print('  '+name+': '+str(stats[name]))
    print 'Interface Details:'
    ifaces = dom.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_LEASE)
    def toIPAddrType(addrType):
        if addrType == libvirt.VIR_IP_ADDR_TYPE_IPV4:
            return "ipv4"
        elif addrType == libvirt.VIR_IP_ADDR_TYPE_IPV6:
            return "ipv6"
    if (ifaces == {}):
        print " No domain interfaces found"
    else:
        for (name, val) in ifaces.iteritems():
            print " {0:10} {1:20} {2:12} {3}".format("Interface", "MAC address", "Protocol", "Address")
            if val['addrs']:
                for addr in val['addrs']:
                    print " {0:10} {1:19}".format(name, val['hwaddr']),
                    print " {0:12} {1}/{2} ".format(toIPAddrType(addr['type']), addr['addr'], addr['prefix']),
                    print '\n'
            else:
                print " {0:10} {1:19}".format(name, val['hwaddr']),
                print " {0:12} {1}".format("N/A", "N/A"),
                print '\n'
    print '\n'

conn.close()

