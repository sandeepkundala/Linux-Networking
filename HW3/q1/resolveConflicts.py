import sys
from time import sleep
import collections
import libvirt
import lxml.etree as le
from xml.dom import minidom

def main():

	conn = libvirt.open('qemu:///system')
    if conn == None:
        print "Qemu connection failed!"
        exit(1)


    vm_name = sys.argv[1]   
    dom = conn.lookupByName(vm_name)
	dom.shutdown()
	dom.destroy()  

    
    
    # MAC address
    mac_address = sys.argv[2]
	to_write = ""
	path = "/etc/libvirt/qemu/"+vm_name+".xml"
	with open(path,'r') as f:
	    doc=le.parse(f)
	    for elem in doc.xpath('//*[attribute::address]'):
	        if elem.attrib['address'] in mac_address:
	            elem.attrib.pop('address')
	            parent=elem.getparent()
	            parent.remove(elem)
	    to_write = le.tostring(doc)
	f = open(path,"w")
	f.write(to_write)
	f.close()
	dom = conn.createXML(to_write, 0)
	if dom == None:
		print 'Unable to define persistent guest configuration.'
		return "Error"
	else:
		print("Success")
		return "Success"
	return 0

if __name__ == "__main__":

    main()
