#!/usr/bin/python
import commands
from ssh_funcs_api import ssh_functions
from vm_creation import Os_Creation_Modules
from delete_os import Os_Deletion_Modules
import iperf3_funcs
import pdb
import time
import openstack
import sys
import os
import json
import time
#########################logger code start
import logging
from logging.handlers import TimedRotatingFileHandler
import datetime

feature_name = "OVSDPDK_SRIOV"

monthdict = {"01": "JAN", "02": "FEB" ,"03": "MAR", "04": "APR", "05": "MAY", "06": "JUNE", "07": "JULY",
             "08": "AUG", "09": "SEPT", "10": "OCT", "11": "NOV", "12": "DEC"}

# Noting starting time to check the elapsed time
start = time.time()

# making directory 'logs' if it does not exits
if not os.path.isdir("logs"):
    os.makedirs("logs")

# Noting starting time and date to name the log file
current = datetime.datetime.now().replace(second=0, microsecond=0)
name = str(datetime.datetime.strptime(str(current), "%Y-%m-%d %H:%M:%S")).split(" ")
out_file = feature_name + str(name[0].split("-")[2]) + monthdict[str(name[0].split("-")[1])] + \
           str(name[0].split("-")[0]) + "-" + str(name[1][:2]) + "-" + str(name[1][3:5])

# Logger configuration
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(message)s')
if not logger.handlers:
    timedRotatingFileHandler = logging.handlers.TimedRotatingFileHandler("logs/%s.log" % out_file, when='midnight',
                                                                         interval=1, backupCount=30)
    streamHandler = logging.StreamHandler()
    timedRotatingFileHandler.setFormatter(formatter)
    streamHandler.setFormatter(formatter)
    logger.addHandler(timedRotatingFileHandler)
    logger.addHandler(streamHandler)
    logger.setLevel(logging.INFO)
else:
    pass
#########################logger code end

ssh_obj = ssh_functions()
creation_object = Os_Creation_Modules()
delete_object = Os_Deletion_Modules()

conn_create = creation_object.os_connection_creation()
conn_delete = delete_object.os_connection_creation()

if os.path.exists("vlan_aware_setup.json"):
    vlan_data = None
    try:
        with open('vlan_aware_setup.json') as data_file:
            vlan_data = json.load(data_file)
        vlan_data = {str(i): str(j) for i, j in vlan_data.items()}
    except:
        print "\nFAILURE!!! error in vlan_aware_setup.json file!"

else:
    print ("\nFAILURE!!! vlan_aware_setup.json file not found!!!\nUnable to execute script\n\n")

def test_case1():
    """"1. ssh to controller node
        2. $ sudo docker ps | grep neutron
        3. $ sudo docker exec -it <neutron_api_contid> bash
        4. # cat /etc/neutron/neutron.conf | grep service_plugins"""
    print("==========================================================================================================")
    print("====         VLAN AWARE VMS CASE 1:      Verify trunk plugin is enabled in controller nodes.         =====")
    print("==========================================================================================================")
    try:
        ssh_obj.ssh_to(logger, "controler_ip","heat-admin")
        res = ssh_obj.execute_command_return_output(logger, "sudo docker ps | grep neutron_api")
        out = res.split("\n")
        #print out
        l3_agent_id_control = str(out[0].split(" ")[0])
        #print l3_agent_id_control.strip()
        res = ssh_obj.execute_command_return_output(logger, "sudo docker exec -t %s cat /etc/neutron/neutron.conf | grep \"service_plugins\"" %l3_agent_id_control)
        # res1 = ssh_obj.execute_command_return_output(logger, "sudo docker exec --help")
        # print res1
        # res = ssh_obj.execute_command_return_output(logger, "sudo docker exec -t cbc18421d202 cat /etc/neutron/l3_agent.ini")
        #print res.split("\n")
        if "trunk" in str(res):
            print ("TEST SUCCESSFUL")
        else:
            print ("TEST FAILED")
        ssh_obj.ssh_close()
        return res
    except:
        print "Unable to execute test case 11"
        print ("\nError: " + str(sys.exc_info()[0]))
        print ("Cause: " + str(sys.exc_info()[1]))
        print ("Line No: %s \n" % (sys.exc_info()[2].tb_lineno))

def test_case2():
    """Run the following command to verify the trunk extension:
        $ openstack extension list --network | grep -i trunk"""
    print("==========================================================================================================")
    print("====         VLAN AWARE VMS CASE 2:      Check if the API extensions are enabled.                    =====")
    print("==========================================================================================================")
    try:
        res = ssh_obj.locally_execute_command(logger, "openstack extension list --network | grep -i trunk")
        if "enabled" in str(res):
            print ("TEST SUCCESSFUL")
        else:
            print ("TEST FAILED")
        ssh_obj.ssh_close()
        return res
    except:
        print "Unable to execute test case 11"
        print ("\nError: " + str(sys.exc_info()[0]))
        print ("Cause: " + str(sys.exc_info()[1]))
        print ("Line No: %s \n" % (sys.exc_info()[2].tb_lineno))

def test_case3(delete_all=False):
    """1. ssh to director node.
        2. To create the parent ports, execute the following command:
      $ openstack port create --network <network-name> <port name>
        3. Create  trunks using the parent ports
      $ openstack network trunk create --parent-port <parent-port-name> <trunk-name>
        4. Next step is the creation of sub-ports for the trunk ports:
      $ openstack port create --network <network-name> --mac-address <mac-addr-of-parent-port> <subport-name>
        5. Associate the subports to the desired trunk port
      $ openstack network trunk set --subport port=<sub-portname>,segmentation-type=vlan,segmentation-id=210 <trunk-name>
        6. Now create vms using parent-ports
      $ openstack server create --nic port-id=<parent-port> --key-name <key-name> --image rhel --flavor m1.small vm1
        7. ssh to vm-1
      $ sudo -i
        # cd /etc/sysconfig/network-scripts/
        # cp ifcfg-eth0 ifcfg-eth0.210
        # cp ifcfg-eth0 ifcfg-eth0.220
        # vi ifcfg-eth0.210
        #vi ifcfg-eth0.220
        # cat ifcfg-eth0.210                                                REPLACED PARAMS
    DEVICE="eth0.210"                                                       DEVICE="eth0.210"
    BOOTPROTO="dhcp"                                                        BOOTPROTO=none
    BOOTPROTOv6="dhcp"                                                      IPADDR=sub-port-IP
    ONBOOT="yes"                                                            ONBOOT=yes
    USERCTL="yes"                                                           USERCTL=yes
    PEERDNS="yes"                                                           PEERDNS=no
    IPV6INIT="yes"                                                          NETMASK=255.255.255.0
    PERSISTENT_DHCLIENT="1"                                                 DEFROUTE=no
    VLAN=yes                                                                VLAN=yes
        8. # cat ifcfg-eth0.220
    DEVICE="eth0.220"
    BOOTPROTO="dhcp"
    BOOTPROTOv6="dhcp"
    ONBOOT="yes"
    USERCTL="yes"
    PEERDNS="yes"
    IPV6INIT="yes"
    PERSISTENT_DHCLIENT="1"
    VLAN=yes
        9. up the vlan-interfaces
        # ifup eth0.210
        # ifup eth0.220
        # ip a
        10. Create another instance as vm-2
        11. ssh to Vm-2
        12.Repeat the same procedure for the vm-2 and ping from vm2 the interfaces eth0.210 and eth0.220 of vm1
        13. ping -I <interface-of-vm1-in-same-vlan> <ip-address-of-interface>
            e.g "ping -I eth0.210 192.168.210.19"
    Trunk port creation API defination
        $ openstack port create --network last vlanvm_port #######PARENT PORT CREATION###########
        $ openstack network trunk  create --parent-port vlanvm_port --subport port=vlanvm_port,segmentation-type=vlan,segmentation-id=200 vlanvm_trunk """
    parent_network = vlan_data["parent_network"]
    parentport_name = vlan_data["parentport_name"]
    subport_network = vlan_data["subport_network"]
    subport_name = vlan_data["subport_name"]
    trunk_name = vlan_data["trunk_name"]
    flavor_name = vlan_data["static_flavor"]
    availability_zone = vlan_data["zone3"]
    image_name = vlan_data["static_image"]
    server_name = vlan_data["server_name"]
    security_group = vlan_data["static_secgroup"]
    segmentation_id = vlan_data["segmentation_id"]
    segmentation_type = vlan_data["segmentation_type"]
    old_eth_file_path = vlan_data["old_eth_file_path"]
    old_route_file_path = vlan_data["old_route_file_path"]
    gateway = vlan_data["gateway"]
    metricnumber=vlan_data["metricnumber"]
    key_file_path=vlan_data["key_file_path"]
    print("==========================================================================================================")
    print("====         VLAN AWARE VMS CASE 3:      Launch the instance with the vlan aware interface.          =====")
    print("==========================================================================================================")
    output = None
    new_eth_file_path = "/etc/sysconfig/network-scripts/ifcfg-eth0.%s" % vlan_data["segmentation_id"]
    new_route_file_path = "/etc/sysconfig/network-scripts/route-eth0.%s" % vlan_data["segmentation_id"]
    try:
        pdb.set_trace()
        output =  creation_object.os_create_vlan_aware_instance(logger, conn_create, parent_network=parent_network,
                                                                parentport_name=parentport_name,
                                                                subport_network=subport_network,
                                                                subport_name=subport_name,
                                                                trunk_name=trunk_name,
                                                                flavor_name=flavor_name,
                                                                availability_zone=availability_zone,
                                                                image_name=image_name,
                                                                server_name=server_name,
                                                                sec_group=security_group,
                                                                segmentation_id=segmentation_id,
                                                                segmentation_type=segmentation_type)
        server_ip = output[2]
        print server_ip
        subport_ip = output[3]
        print subport_ip
        ssh_obj.ssh_vlan_aware_vm(logger, ip_of_instance=server_ip,
                                  username_of_instance=image_name,
                                  key_file_path=key_file_path,
                                  new_eth_file_path=new_eth_file_path,
                                  new_route_file_path=new_route_file_path,
                                  subport_ip=subport_ip,
                                  old_eth_file_path=old_eth_file_path,
                                  old_route_file_path=old_route_file_path,
                                  gateway=gateway,
                                  segmentation_id=segmentation_id,
                                  metricnumber=metricnumber)

        if delete_all:
            delete_object.os_delete_server(logger, conn_delete, server_name=server_name)
            os.system("bash /home/osp_admin/ahmed_synced/input_files/delete-trunks.sh %s %s %s"%(trunk_name,
                                                                                                 parentport_name,
                                                                                                 subport_name))
        return output
    except:
        print "Unable to execute test case 3"
        print ("\nError: " + str(sys.exc_info()[0]))
        print ("Cause: " + str(sys.exc_info()[1]))
        print ("Line No: %s \n" % (sys.exc_info()[2].tb_lineno))
        # dele = delete_object.os_delete_vlanaware_server(logger, conn_delete, server_name, parentport_name, subport_name, trunk_name, delete_parentport=True, delete_subport=True, delete_trunk=True, network_name=None)
        delete_object.os_delete_server(logger, conn_delete, server_name=server_name)
        os.system("bash /home/osp_admin/ahmed_synced/input_files/delete-trunks.sh %s %s %s" % (trunk_name, parentport_name, subport_name))
        return output

def test_case4():
    """1. ssh to controller
        2. sudo ip netns exec <dhcp namespace> -i <key-location> username@ip-address"""
    print("==========================================================================================================")
    print("====         VLAN AWARE VMS CASE 4:      ssh to vlan aware instance with tenant-network address.     =====")
    print("==========================================================================================================")
    try:
        # instance_private_ip =
        ssh_obj.ssh_to(logger, controller_ip,"heat-admin")
        res = ssh_obj.execute_command_show_output(logger, "sudo ip netns exec qdhcp-%s ssh -i key.pem centos@%s"%(namespace_id, instance_private_ip))
        res = ssh_obj.execute_command_show_output(logger, "ifconfig")
        if instance_private_ip in res:
            print ("TEST SUCCESSFUL")
        else:
            print("TEST FAILED")
        ssh_obj.ssh_close()

        return instance_private_ip
    except:
        print "Unable to execute test case 11"
        print ("\nError: " + str(sys.exc_info()[0]))
        print ("Cause: " + str(sys.exc_info()[1]))
        print ("Line No: %s \n" % (sys.exc_info()[2].tb_lineno))


def test_case5():
    """1. ssh to director node
        2. Assign the vlan aware instance a floating ip through horizon.
         3. ssh -i <key-name> username@floating-ip"""
    print("==========================================================================================================")
    print("====         VLAN AWARE VMS CASE 5:      ssh to vlan aware instance through floating-ip.             =====")
    print("==========================================================================================================")
    try:
        # instance_private_ip =
        ssh_obj.ssh_with_key(logger, instance_floating_ip, username="centos", key_file_name="~/key.pem")
        res = ssh_obj.execute_command_show_output(logger, "ifconfig")
        if instance_private_ip in res:
            print ("TEST SUCCESSFUL")
        else:
            print("TEST FAILED")
        ssh_obj.ssh_close()
        return instance_private_ip
    except:
        print "Unable to execute test case 11"
        print ("\nError: " + str(sys.exc_info()[0]))
        print ("Cause: " + str(sys.exc_info()[1]))
        print ("Line No: %s \n" % (sys.exc_info()[2].tb_lineno))


def test_case6():
    """Create two instances from different parent ports and ping the vm-1's vlan-interface ip from vm-2's interface on the same vlan network"""
    print("==========================================================================================================")
    print("====         VLAN AWARE VMS CASE 6:Create two instances from different parent ports                  =====")
    print("====         Ping the vm-1's vlan-interface ip from vm-2's interface on the same vlan network        =====")
    print("==========================================================================================================")
    try:
        print("========             SERVER 1 CREATING WITH DIFFERENT PARENT PORT                                =====")
        output = creation_object.os_create_vlan_aware_instance(logger, conn_create, parent_network, parentport_name,
                                                               subport_network, subport_name,
                                                               trunk_name, flavor_name, availability_zone, image_name,
                                                               server_name, sec_group,
                                                               segmentation_id, segmentation_type)

        pdb.set_trace()
        server_ip = output[2]
        subport_ip = output[3]
        ssh_obj.ssh_vlan_aware_vm(logger, server_ip, old_eth_file_path, new_eth_file_path, old_route_file_path,
                                  new_route_file_path, subport_ip, gateway, segmentation_id, metricnumber)
        print("========             SERVER 2 CREATING WITH DIFFERENT PARENT PORT                                =====")
        res = creation_object.os_create_vlan_aware_instance(logger, conn_create, parent_network, parentport_name,
                                                               subport_network, subport_name,
                                                               trunk_name, flavor_name, availability_zone, image_name,
                                                               server_name, sec_group,
                                                               segmentation_id, segmentation_type)

        pdb.set_trace()
        server_ip = res[2]
        subport_ip = res[3]
        ssh_obj.ssh_vlan_aware_vm(logger, server_ip, old_eth_file_path, new_eth_file_path, old_route_file_path,
                                  new_route_file_path, subport_ip, gateway, segmentation_id, metricnumber)
    except:
        print "Unable to execute test case 11"
        print ("\nError: " + str(sys.exc_info()[0]))
        print ("Cause: " + str(sys.exc_info()[1]))
        print ("Line No: %s \n" % (sys.exc_info()[2].tb_lineno))


def test_case7():
    """1. ssh to director node.
        2. Create vlan-aware instance"vm-1" according the method given in test case above.
        3. Create another instance "vm-3" on the same network as the first instance. Dont create interfaces on this instance.
        4. ssh to vm-3
        5. ping the the vm-1's vlan-aware interface from the vm-3"""
    print("==========================================================================================================")
    print("====         VLAN AWARE VMS CASE 7:      verify flow of untagged traffic.                            =====")
    print("==========================================================================================================")
    try:
        pass
    except:
        pass

test_case3(delete_all=True)





