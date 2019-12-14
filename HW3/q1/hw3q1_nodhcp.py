import libvirt
import sys
import lxml.etree as le
from time import sleep


hashMAcs = {}
hashIPs = {}
ips = []
conflictingMacs = {}
macs = []
conflictingIPS = {}

def findDuplicates(macList):
    seen = {}
    dupes = []

    for x in macList:
        if x not in seen:
            seen[x] = 1
        else:
            if seen[x] == 1:
                dupes.append(x)
            seen[x] += 1
    return dupes

def findConflictingMacs():
    for domain in hashMAcs:
        temp = set(hashMAcs[domain])
        #same vm conflict
        if len(temp)!=len(hashMAcs[domain]):
            common = findDuplicates(hashMAcs[domain])
            if domain not in conflictingMacs:
                conflictingMacs[domain] = common
            else:
                conflictingMacs[domain].extend(common)
        
        common = [value for value in list(temp) if value in macs] 
        
        if(len(common)>0):
            if domain not in conflictingMacs:
                conflictingMacs[domain] = common
            else:
                conflictingMacs[domain].extend(common)
        macs.extend(list(temp))

def findConflictingIPs():
    for domain in hashIPs:
        temp = set(hashIPs[domain])
        #same vm conflict
        if len(temp)!=len(hashIPs[domain]):
            common = findDuplicates(hashIPs[domain])
            if domain not in conflictingIPS:
                conflictingIPS[domain] = common
            else:
                conflictingIPS[domain].extend(common)
        
        common = [value for value in list(temp) if value in ips] 
        
        if(len(common)>0):
            if domain not in conflictingIPS:
                conflictingIPS[domain] = common
            else:
                conflictingIPS[domain].extend(common)
        ips.extend(list(temp))



def deleteMacsAndReset(conn, vm):
    xml_path = "/etc/libvirt/qemu/"+vm+".xml"
    final = ""
    with open(xml_path,'r') as f:
        doc=le.parse(f)
        for elem in doc.xpath('//*[attribute::address]'):
            if elem.attrib['address'] in hashMAcs[vm]:
                elem.attrib.pop('address')
                parent=elem.getparent()
                parent.remove(elem)
        final = le.tostring(doc)
    f = open(xml_path,"w")
    f.write(final)
    f.close()
    dom = conn.createXML(final, 0)
    if dom == None:
        print 'Unable to define persistent guest configuration.'
        exit(1)

def setup():
    conn = libvirt.open('qemu:///system')
    if conn == None:
        print "Qemu connection failed!"
        exit(1)
    #list vm objects
    domains = conn.listDomainsID()
    if len(domains) == 0:
        print ("No active domains in current hypervisor")
    
    vmIds = [] + domains
    vms = []
    for vm in vmIds:
        vms.append(conn.lookupByID(vm))
    return conn,vms

def fetchMacsandIPs(vmList):
    for vm in vmList:
        print("\n")
        print(" DOMAIN : " + vm.name())
        print("\n")
        ifaces = vm.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT, 0)
        hashMAcs[vm.name()] = [];
        hashIPs[vm.name()] = [];
        for (name, val) in ifaces.iteritems():
            if val['hwaddr']!="00:00:00:00:00:00":
                output = "(Interface) " + name + " (MAC Address) "+ val['hwaddr']
                if val['addrs']:
                    hashMAcs[vm.name()].append(val['hwaddr'])
                    li = [];
                    for child in val['addrs']:
                        if child['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV4 and child['addr'] != "127.0.0.1":
                            hashIPs[vm.name()].append(child['addr']+"/"+str(child['prefix']))
                            li.append(child['addr']+"/"+str(child['prefix']))
                    if len(li)>0:
                        output = output + " (IP ADDRESS:) " + ', '.join(li)
                else:
                     hashMAcs[vm.name()].append(val['hwaddr'])
                     
                print(output)
        

def process():
    conn,vmList = setup()
    fetchMacsandIPs(vmList)

    print("\n")
    print("Finding Conflicting IPs")
    findConflictingIPs()
    if not conflictingMacs:
        print("\n")
        print("No conflicts found")
        print("\n")
    else:
        print("\n")
        print("Conflicting Ips found in")
        print("\n")
        print(conflictingMacs)
        print("\n")
        print("Please go and update them!")
        print("\n")

    print("\n")
    print("Finding Confilcting MAC")
    findConflictingMacs()
    if not conflictingMacs:
        print("\n")
        print("No conflicts found")
        print("\n")
    else:
        print("\n")
        print("Conflicting MAC found in")
        print("\n")
        print(conflictingMacs)
        print("\n")
        for vm in conflictingMacs:
            dom = conn.lookupByName(vm)
            dom.shutdown()
            dom.destroy()
            deleteMacsAndReset(conn, vm)
            sleep(60)



def main():
    global hashMAcs 
    global conflictingMacs
    global macs
    global hashIPs 
    global conflictingIPS
    global ips

    while(1):
        process()
        if not conflictingMacs:
            sys.exit(0)

        hashMAcs = {}
        macs = []
        conflictingMacs = {}
        hashIPs = {}
        ips = []
        conflictingIPS = {}

        print("After resolving conflicts :")
        conn,vmList = setup()
        fetchMacsandIPs(vmList)


if __name__ == '__main__':
    main()



