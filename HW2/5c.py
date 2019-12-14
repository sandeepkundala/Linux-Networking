import libvirt
import sys
import csv
import time

type="CPU"
threshold = 0
if(len(sys.argv)>1):
    type=sys.argv[1]
if(len(sys.argv)>2):
    threshold=long(float(sys.argv[2]))

#source : online
def convMBtoGB(input_megabyte):
        gigabyte = float(9.5367431640625E-7)
        convert_gb = gigabyte * input_megabyte
        return convert_gb

def createAlertRecord(vmName, cpuUsage):
    list = [vmName, time.time(), cpuUsage]
    return list;

conn = libvirt.open('qemu:///system')

memDomain = {}
cpuDomain = {}
for id in conn.listDomainsID():
    dom = conn.lookupByID(id)

    cpu_stats = dom.getCPUStats(True)
    cpuTime1 = (cpu_stats[0]['cpu_time']/1000000)
    
    time.sleep(1)

    cpu_stats = dom.getCPUStats(True)
    cpuUtil = (cpu_stats[0]['cpu_time']/1000000) - cpuTime1

    # checking if threshold is set 
    if threshold!=0 and cpuUtil>=threshold:
        with open('cpuAlert.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(createAlertRecord(dom.name(), cpuUtil))
            csvFile.close()

    cpuDomain[dom.name()] = cpuUtil

    if type=="MEM":
        stats  = dom.memoryStats()
        memUtil = stats['available'] - stats['unused']
        memDomain[dom.name()] = convMBtoGB(memUtil)


if type=="CPU":
    cpuDomain = sorted(cpuDomain.items(), key=lambda kv: kv[1])
    for tuple in cpuDomain:
        print(tuple[0])
else:
    memDomain = sorted(memDomain.items(), key=lambda kv: kv[1])
    for tuple in memDomain:
        print(tuple[0])
