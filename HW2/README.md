README

q4:
a.
to create the network:
sudo ansible-playbook networkCreation.yaml --extra-vars "ansible_sudo_pass=<password>"

to create the vm:
sudo ansible-playbook vmCreation.yaml --extra-vars "ansible_sudo_pass=<password>"

b. 
To make the script run, we had to add sudo password and other parameters. Since we have to create/update the file inside var folder which requires root access, we need to run the script with sudo.

The following configuration was added to the /etc/ansible/hosts file.

[vm]
127.0.0.1 ansible_connection=local ansible_user=ece792 ansible_ssh_private_key_file=/home/ece792/.ssh/id_rsa ansible_become_pass=Avent@2506 ansible_become=true
192.168.123.151 ansible_connection=ssh ansible_user=jcsk ansible_ssh_private_key_file=/home/ece792/.ssh/id_rsa ansible_become_pass=Avent@2506 ansible_become=true
192.168.123.126 ansible_connection=ssh ansible_user=jcsk ansible_ssh_private_key_file=/home/ece792/.ssh/id_rsa ansible_become_pass=Avent@2506 ansible_become=true

To run the ansible script, use the following command

ansible-playbook -i /etc/ansible/hosts hw2_ansible.yaml --extra-vars "time=1"

Keep the script file in the landing directory of the VMs.


5) 
a) hostInfo.py

b) guestInfo.py

c) 
python 5c.py CPU 1000

Here, the command line arguments are CPU/MEM and threshold value for CPU in milliseconds	
The alert message is stored in the cpuAlert.csv file in the current folder.

Bonus:

python bonus.py MEM 2 4
Here, the first parameter is the type (CPU/MEM) and the second parameter is the polling interval and the third is the moving interval.
