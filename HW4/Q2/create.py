import csv
import sys
import subprocess

image = sys.argv[1]
filename = sys.argv[2]
with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile) 
    next(csvreader)
    count = 50 
    for row in csvreader: 
        print('Executing :', row)
        if row[2] == 'Bridge':
            command = 'sudo ansible-playbook bridge_mode.yaml -e image_name=' + image + ' -e CS1=' + row[0] + ' -e CS2=' + row[1] + ' -e ip_net=' + str(count)
            print(command)
            subprocess.call([command],shell=True)
            count += 1
        elif row[2] == 'L3':
            command = 'sudo ansible-playbook l3_mode.yaml -e image_name=' + image + ' -e CS1=' + row[0] + ' -e CS2=' + row[1] + ' -e ip_net=' + str(count)
            print(command)
            subprocess.call([command],shell=True)
            count += 1
        elif row[2] == 'VXLAN':
            command = 'sudo ansible-playbook vxlan_mode.yaml -e image_name=' + image + ' -e CS1=' + row[0] + ' -e CS2=' + row[1] + ' -e ip_net=' + str(count)
            print(command)
            subprocess.call([command],shell=True)
            count += 1
        elif row[2] == 'GRE':
            command = 'sudo ansible-playbook gre_mode.yaml -e image_name=' + image + ' -e CS1=' + row[0] + ' -e CS2=' + row[1] + ' -e ip_net=' + str(count)
            print(command)
            subprocess.call([command],shell=True)
            count += 1
        else:
            print("ERROR!!! Network Type - UNKNOWN!!!")
