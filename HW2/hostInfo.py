import libvirt
import sys

conn = libvirt.open('qemu:///system')
host = conn.getHostname()
print('Hostname:'+host)

vcpus = conn.getMaxVcpus(None)
print('Maximum support virtual CPUs: '+str(vcpus))

nodeinfo = conn.getInfo()
print('Model: '+str(nodeinfo[0]))
print('Memory size: '+str(nodeinfo[1])+'MB')
print('Number of CPUs: '+str(nodeinfo[2]))
print('MHz of CPUs: '+str(nodeinfo[3]))
print('Number of NUMA nodes: '+str(nodeinfo[4]))
print('Number of CPU sockets: '+str(nodeinfo[5]))
print('Number of CPU cores per socket: '+str(nodeinfo[6]))
print('Number of CPU threads per core: '+str(nodeinfo[7]))

numnodes = nodeinfo[4]
memlist = conn.getCellsFreeMemory(0, numnodes)
cell = 0
for cellfreemem in memlist:
    print('Node '+str(cell)+': '+str(cellfreemem)+' bytes free memory')
    cell += 1

print('Virtualization type: '+conn.getType())

ver = conn.getVersion()
print('Version: '+str(ver))

ver = conn.getLibVersion();
print('Libvirt Version: '+str(ver));

mem = conn.getFreeMemory()
print("Free memory on the node (host) is " + str(mem) + " bytes.")

buf = conn.getMemoryStats(libvirt.VIR_NODE_MEMORY_STATS_ALL_CELLS)
for parm in buf:
    print(parm)

xmlInfo = conn.getSysinfo()
print(xmlInfo)

map = conn.getCPUMap()
print("CPUs: " + str(map[0]))
print("Available: " + str(map[1]))

stats = conn.getCPUStats(0)
print("kernel: " + str(stats['kernel']))
print("idle:   " + str(stats['idle']))
print("user:   " + str(stats['user']))
print("iowait: " + str(stats['iowait']))
conn.close()

