import libvirt
import sys
import paramiko
import os
from time import sleep
import lxml.etree as le

hypervisorList = {}
hashMAC = {}
conflictingMACs = {}
macs = []
privateKey = "/home/ece792/.ssh/id_rsa"


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

def findConflictingMacs(hypervisorList):
    for hypervisor in hypervisorList:
        for domain in hypervisorList[hypervisor]:
            temp = set(hypervisorList[hypervisor][domain])
            #same vm conflict
            if len(temp)!=len(hypervisorList[hypervisor][domain]):
                common = findDuplicates(hypervisorList[hypervisor][domain])
            
                if hypervisor not in conflictingMACs:
                    conflictingMACs[hypervisor] = {}

                if domain not in conflictingMACs[hypervisor]:
                    conflictingMACs[hypervisor][domain] = common
                else:
                    conflictingMACs[hypervisor][domain].extend(common)
            
            common = [value for value in list(temp) if value in macs] 
     
            if(len(common)>0):
                if hypervisor not in conflictingMACs:
                    conflictingMACs[hypervisor] = {}

                if domain not in conflictingMACs[hypervisor]:
                    conflictingMACs[hypervisor][domain] = common
                else:
                    conflictingMACs[hypervisor][domain].extend(common)
            macs.extend(list(temp))


def deleteMACAndReset(hypervisor_ip, vmName, vmMacList):

    # SSH to hypervisor
    ssh_client = paramiko.SSHClient()
    ssh_client.load_system_host_keys()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    userName = hypervisorList[hypervisor_ip]
    ssh_client.connect(hypervisor_ip, username=userName, port=22, key_filename=privateKey)

    # Copy python script
    os.system("scp -o StrictHostKeyChecking=no resolveConflicts.py "+userName+"@"+hypervisor_ip+":~/")

    # Run script with vmname and mac
    print(vmName)
    print("Resolving")
    for vmm in vmMacList:
        command = "sudo python resolveConflicts.py "+ vmName + " " + vmm
        print(command)
        stdin, stdout, stderr = ssh_client.exec_command(command);
        print("Executing command now")
        print(stdout.read())
        # if "Success" in stdout.read():
        #     print("Success") 
        # else:
        #     print("Failure")
    
    ssh_client.close()

def setup(hypervisorId):
  
    userName = hypervisorList[hypervisorId]
    conn = libvirt.open("qemu+ssh://" + userName + "@" + hypervisorId + "/system?keyfile="+privateKey)

    if conn == None:
        print "Qemu connection failed!"
        exit(1)
    #list vm objects
    domains = conn.listDomainsID()
    if len(domains) == 0:
        print ("No active domains in current hypervisor")
    
    
    vmIdList = [] + domains
    vms=[]
    for vm in vmIdList:
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
            macAddr = val['hwaddr']
            if macAddr!="00:00:00:00:00:00":
                output = "(Interface) " + name + " (MAC Address) "+ val['hwaddr']
                if val['addrs']:
                    hashMAC[vm.name()].append(macAddr)
                    li = [];
                    for child in val['addrs']:
                        if child['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV4 and child['addr'] != "127.0.0.1":
                            li.append(child['addr']+"/"+str(child['prefix']))
                    if len(li)!=0:
                        output = output + " (IP ADDRESS) " + ', '.join(li)
                else:
                     hashMAC[vm.name()].append(macAddr)
                    
                print(output)
    return hashMAC

def process(hypervisorMAC):
    print("\n")
    print("Finding Confilcting MAC")
    print("\n")
    findConflictingMacs(hypervisorMAC)
    if not conflictingMACs:
        print("\n")
        print("No conflicts found")
        print("\n")
    else:
        print("\n")
        print("Conflicting MAC found in")
        print("\n")
        print(conflictingMACs)

        to_resolve = [];
 
        for domain in conflictingMACs:
            for vm in conflictingMACs[domain]:            
                deleteMACAndReset(domain,vm, conflictingMACs[domain][vm])
                sleep(120)
    
   
def main():

    global hypervisorList

    if(len(sys.argv)<2):
        print("Please specify the hypervisor list file!")
        sys.exit(0)
    
    f = open(sys.argv[1], "r")
    for x in f:
       hype = x.split(" ")
       if(len(hype)!=2):
            print("Please specify the hypervisor list in proper format!")
            sys.exit(0)
       hypervisorList[hype[0].rstrip()] = hype[1].rstrip()
    
    global hashMAC
    global conflictingMACs
    global macs

    hypervisorMAC = {}


    while(1):
        for hypervisor in hypervisorList:
            print("HYPERVISOR: " + str(hypervisor))
            conn,vmList = setup(hypervisor)
            hypervisorMAC[hypervisor] = fetchMacsandIPs(vmList)
            hashMAC = {}

        process(hypervisorMAC)

        if not conflictingMACs:
            sys.exit(0)

        print("After resolving conflicts :")


        hashMAC = {}
        macs = []
        conflictingMACs = {}
        hypervisorMAC={}



if __name__ == '__main__':
    main()



