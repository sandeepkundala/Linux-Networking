import libvirt
import sys
import paramiko
import os
from time import sleep
import lxml.etree as le

hashMAC = {}
conflictingMACs = {}
macs = []
hashIPs = {}
ips = []
conflictingIPs = {}

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

def findConflictingIPs(hypervisorList):
    for hypervisor in hypervisorList:
        for domain in hypervisorList[hypervisor]:
            temp = set(hypervisorList[hypervisor][domain])
            #same vm conflict
            if len(temp)!=len(hypervisorList[hypervisor][domain]):
                common = findDuplicates(hypervisorList[hypervisor][domain])
                
                if hypervisor not in conflictingIPs:
                    conflictingIPs[hypervisor] = {}

                if domain not in conflictingIPs[hypervisor]:
                    conflictingIPs[hypervisor][domain] = common
                else:
                    conflictingIPs[hypervisor][domain].extend(common)
            
            common = [value for value in list(temp) if value in ips] 
     
            if(len(common)>0):
                if hypervisor not in conflictingIPs:
                    conflictingIPs[hypervisor] = {}

                if domain not in conflictingIPs[hypervisor]:
                    conflictingIPs[hypervisor][domain] = common
                else:
                    conflictingIPs[hypervisor][domain].extend(common)
            ips.extend(list(temp))


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
  
    username = "ece792"
    hypervisor = hypervisorId
    conn = libvirt.open("qemu+ssh://" + username + "@" + hypervisor + "/system?keyfile="+privateKey)

    if conn == None:
        print "Qemu connection failed!"
        exit(1)
    #list vm objects
    domains = conn.listDomainsID()
    if len(domains) == 0:
        print ("No active domains in current hypervisor")
    
    #vm_id_list = [] + domainIDs
    if "178" in hypervisorId:
        vmIdList = [50]
    else:
        vmIdList = [] + domains
    vms = []
    for vm in vmIdList:
        vms.append(conn.lookupByID(vm))
    return conn,vms

def fetchMacsandIPs(vmList):
    for vm in vmList:
        print("\n")
        print("\n")
        print("DOMAIN : " + vm.name())
        ifaces = vm.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT, 0)
        hashMAC[vm.name()] = [];
        for (name, val) in ifaces.iteritems():
            macAddr = val['hwaddr']
            if macAddr!="00:00:00:00:00:00":
                output = "Interface :" + name + "MAC Address: "+ macAddr
                if val['addrs']:
                    hashMAC[vm.name()].append(macAddr)
                    li = [];
                    for child in val['addrs']:
                        if child['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV4 and child['addr'] != "127.0.0.1":
                            hashIPs[vm.name()].append(child['addr']+"/"+str(child['prefix']))
                            li.append(child['addr']+"/"+str(child['prefix']))
                    if len(li)>0:
                        output = output + " (IP ADDRESS) " + ', '.join(li)
                else:
                     hashMAC[vm.name()].append(macAddr)             
                print(output)
    
    return hashMAC,hashIPs

def process(hypervisorMAC, hypervisorIP):
    print("Finding Conflicting IP")
    findConflictingIPs(hypervisorIP)
    if not conflictingIPs:
        print("No conflicts found")
    else:
        print("Conflicting IP found in")
        print(conflictingIPs)
        print("Please go and replace the conflicting IPs")
    print("Finding Confilcting MAC")

    findConflictingMacs(hypervisorMAC)
    if not conflictingMACs:
        print("No conflicts found")
    else:
        print("Conflicting MAC found in")
        print(conflictingMACs)

       
 
        for domain in conflictingMACs:
            for vm in conflictingMACs[domain]:            
                deleteMACAndReset(domain,vm, conflictingMACs[domain][vm])
                sleep(10)
   

def main():
    global hashMAC
    global conflictingMACs
    global macs
    global hashIPs 
    global conflictingIPs
    global ips

    hypervisor_list = ['192.168.122.178']
    hypervisorMAC = {}
    hypervisorIP = {}

    while(1):

        for hypervisor_ip in hypervisor_list:
            print("HYPERVISOR: " + str(hypervisor_ip))
            conn,vmList = setup(hypervisor_ip)
            mac, ip = fetchMacsandIPs(vmList)
            hypervisorMAC[hypervisor_ip]= mac
            hypervisorIP[hypervisor_ip] = ip
            
            hashMAC = {}

        process(hypervisorMAC, hypervisorIP)

        if not conflictingMACs:

            print("After resolving conflicts :")
            for hypervisor_ip in hypervisor_list:
           
                print("HYPERVISOR: " + str(hypervisor_ip))
                conn,vmList = setup(hypervisor_ip)
                hypervisorMAC[hypervisor_ip] = fetchMacsandIPs(vmList)
                
                hashMAC = {}
            
            sys.exit(0)

        hashMAC = {}
        macs = []
        ips = []
        hashIPs= {}
        conflictingMACs = {}
        conflictingIPs = {}
        hypervisorMAC={}
        hypervisorIP ={}



if __name__ == '__main__':
    main()



