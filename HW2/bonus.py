import libvirt
import sys
import time 

type="CPU"
pollingInterval = 0
windowSize = 0
cpuTime1 = -1

if(len(sys.argv)>3):
    type=sys.argv[1]
    pollingInterval= int(sys.argv[2])
    windowSize = int(sys.argv[3])

# source: online
def convMBtoGB(input_megabyte):
        gigabyte = float(9.5367431640625E-7)
        convert_gb = gigabyte * input_megabyte
        return convert_gb

def movingAverages(interval, size):
    moving_sum = {}
    global cpuTime1
    if cpuTime1 != -1 and type=="CPU":
        cpu_stats = dom.getCPUStats(True)
        cpuTime1 = (cpu_stats[0]['cpu_time']/1000000)
    
    for i in range(0,size):
        time.sleep(interval)
        u_list = computeUsage()
        for vm in u_list:
            if i == 0:
                moving_sum[vm] = u_list[vm]
            else:
                moving_sum[vm] = (moving_sum[vm]+u_list[vm])/(i+1)
        moving_sum_t = sorted(moving_sum.items(), key=lambda kv: kv[1])
        unzipped = zip(*moving_sum_t)
        print(list(unzipped[0]))
        

def computeUsage():
    usage = {}
    for id in conn.listDomainsID():
        dom = conn.lookupByID(id)
         
        if type=="CPU":
            global cpuTime1
            cpu_stats = dom.getCPUStats(True)
            cpuUtil = (cpu_stats[0]['cpu_time']/1000000) - cpuTime1
            usage[dom.name()] = cpuUtil
            cpuTime1 = cpuUtil
        else:
            stats  = dom.memoryStats()
            memUtil = stats['available'] - stats['unused']
            usage[dom.name()] = convMBtoGB(memUtil)
    return usage


conn = libvirt.open('qemu:///system')
movingAverages(pollingInterval, windowSize)
