import libvirt
import sys
import lxml.etree as le
from time import sleep


hashMAC = {}
conflictingMACs = {}
macs = []


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
    for domain in hashMAC:
        temp = set(hashMAC[domain])
        #same vm conflict
        if len(temp)!=len(hashMAC[domain]):
            common = findDuplicates(hashMAC[domain])
            if domain not in conflictingMACs:
                conflictingMACs[domain] = common
            else:
                conflictingMACs[domain].extend(common)
        
        common = [value for value in list(temp) if value in macs] 
        
        if(len(common)>0):
            if domain not in conflictingMACs:
                conflictingMACs[domain] = common
            else:
                conflictingMACs[domain].extend(common)
        macs.extend(list(temp))



def deleteMacsAndReset(conn, vm):
    xml_path = "/etc/libvirt/qemu/"+vm+".xml"
    final = ""

    with open(xml_path,'r') as f:
        doc=le.parse(f)
        for elem in doc.xpath('//*[attribute::address]'):
            if elem.attrib['address'] in hashMAC[vm]:
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
    
  
    vmIds= [] + domains
    vms = []
    for vm in vmIds:
        vms.append(conn.lookupByID(vm))
    return conn,vms

def fetchMacsandIPs(vmList):
    for vm in vmList:
        print("\n")
        print("DOMAIN : " + vm.name())
        print("\n")
        ifaces = vm.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT, 0)
        hashMAC[vm.name()] = [];
        for (name, val) in ifaces.iteritems():
            if val['hwaddr']!="00:00:00:00:00:00":
                output = "(Interface) " + name + " (MAC Address) "+ val['hwaddr']
                if val['addrs']:
                    hashMAC[vm.name()].append(val['hwaddr'])
                    li = [];
                    for child in val['addrs']:
                        if child['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV4 and child['addr'] != "127.0.0.1":
                            li.append(child['addr']+"/"+str(child['prefix']))
                    if len(li)!=0:
                        output = output + " (IP ADDRESS) " + ', '.join(li)
                else:
                     hashMAC[vm.name()].append(val['hwaddr'])
                    
                print(output)

        

def process():
    conn,vmList = setup()
    fetchMacsandIPs(vmList)
    print("\n")
    print("Finding Confilcting MAC")
    findConflictingMacs()
    if not conflictingMACs:
        print("\n")
        print("No conflicts found")
        print("\n")
    else:
        print("\n")
        print("Conflicting MAC found in")
        print("\n")
        print(conflictingMACs)
        print("\n")
        for vm in conflictingMACs:
            dom = conn.lookupByName(vm)
            dom.shutdown()
            dom.destroy()
            deleteMacsAndReset(conn, vm)
            sleep(60)


def main():
    global hashMAC 
    global conflictingMACs
    global macs

    while(1):
        process()
        if not conflictingMACs:
            sys.exit(0)

        print("After resolving conflicts : ")
        conn,vmList = setup()
        fetchMacsandIPs(vmList)

        hashMAC = {}
        macs = []
        conflictingMACs = {}
        

if __name__ == '__main__':
    main()



