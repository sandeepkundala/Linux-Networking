************Q6 README************
Requirement:
The user needs to run the script in the tenant namespace.

For VxLAN:
A bridge should be created and connected to the interface at NS which connects to the bridge of the VM. 

*********** GRE TUNNEL***********
     >>>>>Create Tunnel<<<<<<
To create tunnel, run the program createGRETunnel.sh in tenant namespace, pass the arguments tunnel name, local IP, remote IP, private Network
where local IP is the IP of ns's interface to transit NS, remote IP is IP of other ns which is connected to transit NS and Private network is the network which should use the tunnel.
 
	>>>>>Delete Tunnel<<<<<<
To delete the previously created GRE Tunnel, run the program deleteGRETunnel.sh in tenant namespace, pass the argument tunnel name.	

**********VxLAN TUNNEL***********
     >>>>>Create Tunnel<<<<<<
To create tunnel, run the program createVxLANTunnel.sh in tenant namespace, pass the arguments tunnel name, VxLAN ID, local interface, remote IP, bridge name
where VxLAN ID is ID of the tennant, local interface is the ns's interface to transit NS, remote IP is IP of other ns which is connected to transit NS and bridge name is the name of bridge which VxLAN interface needs to be connected.
 
	>>>>>Delete Tunnel<<<<<<
To delete the previously created VxLAN Tunnel, run the program deleteVxLANunnel.sh in tenant namespace, pass the argument tunnel name and bridge name.	
