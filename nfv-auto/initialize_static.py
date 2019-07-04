from vm_creation import Os_Creation_Modules, data
from delete_os import Os_Deletion_Modules
import os
import logging
from logging.handlers import TimedRotatingFileHandler
import datetime
import time

feature_name = "Initializing_Static"

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


obj=Os_Creation_Modules()
conn=obj.os_connection_creation()
# os.system("openstack aggregate list")
# os.system("openstack flavor list")
# obj.os_sec_group_n_rules_creation(logger, conn, data["static_secgroup"], "Secgroup for icmp,tcp,udp",
# ["tcp", "icmp", "udp"], "0.0.0.0/0")
# obj.os_flavor_creation(logger, conn, "legacy_flavor", 2048, 2, 20)
# obj.os_flavor_sriov_creation(logger, conn, "sriov_flavor", 1024, 2, 40)
# obj.os_image_creation(logger, conn, data["static_image"], data["static_image_path"],data["static_image_format"],"bare")
# obj.os_network_creation(logger, conn, data["network_name"], data["cidr"], data["subnet_name"], data["gateway_ip"])
# obj.os_flavor_ovsdpdk_creation(logger, conn, data["ovsdpdk_flavor"], 1024, 2, 40)
# os.system("openstack keypair list")
# obj.os_router_creation(logger, conn, data["static_router"], data["static_port"], data["static_network"])
obj.os_server_creation(logger, conn, "centos", "m1.medium", "centos", "storage-net", "c11a0ebb-22bb-4658-9804-c20d0053412a", "nova1", "ceph-key", 1, 3)
# obj.os_keypair_creation_with_key_file(logger, conn, data["key_name"], data["key_file_path"])

delete_object = Os_Deletion_Modules()
conn_delete = delete_object.os_connection_creation()


#================Creating Aggregate and Zones=====================#
#================Key Pair Creation========================#
# os.system("openstack keypair create dpdk-key > dpdk-key.pem")
# os.system("openstack keypair create sriov-key > sriov-key.pem")
# os.system("openstack keypair create dvr-key > dvr-key.pem")
# os.system("openstack keypair create static-key > static-key.pem")
# os.system("openstack keypair list")
#=================R146===================#

# list = ["r146-dell-compute-0.r146.nfv.lab",
#     "r146-dell-compute-1.r146.nfv.lab", "r146-dell-compute-2.r146.nfv.lab"]
# c = 0
# for i in list:
#     obj.os_aggregate_creation_and_add_host(logger, conn, "nova%s"%c, availablity_zone="nova%s"%c, host_name=i)
#     c += 1



#==================R153===================#

# list = ["r153-dell-compute-0.r153.nfv.lab", "r153-dell-compute-1.r153.nfv.lab", "r153-dell-compute-2.r153.nfv.lab"]
# c = 0
# for i in list:
#     obj.os_aggregate_creation_and_add_host(logger, conn, "nova%s"%c, availablity_zone="nova%s"%c, host_name=i)
#     c += 1


#==================r154===================#

# list = ["r154-dell-compute-0.r154.nfv.lab",
#     "r154-dell-compute-1.r154.nfv.lab", "r154-dell-compute-2.r154.nfv.lab"]
# c = 0
# for i in list:
#     obj.os_aggregate_creation_and_add_host(logger, conn, "nova%s"%c, availablity_zone="nova%s"%c, host_name=i)
#     c += 1



#================checking 2 compute nodes========================#
# delete_object.delete_2_instances_and_router_with_2_networks(logger, conn_delete,
#                                                             "test_1", "test_2",
#                                                             "net1", "net2",
#                                                             "router",
#                                                             "port1", "port2")
# obj.create_2_instances_on_dif_compute_dif_network(logger, conn, "test_1", "test_2",
#                                                                                 "net1", "net2",
#                                                                                 "subnet1", "subnet2",
#                                                                                 "router",
#                                                                                 "port1","port2",
#                                                                                 "nova1", "nova2",
#                                                                                 "192.168.10.0/24","192.168.10.1",
#                                                                                 "192.168.20.0/24","192.168.20.1",
#                                                                                 "m1.medium", "centos",
#                                                                                 "c11a0ebb-22bb-4658-9804-c20d0053412a",
#                                                                                 assign_floating_ip=False)

# time.sleep(120)

# delete_object.delete_2_instances_and_router_with_2_networks(logger, conn_delete,
#                                                             "test_1", "test_2",
#                                                             "net1", "net2",
#                                                             "router",
#                                                             "port1", "port2")

obj.os_create_instance_snapshot(logger, conn, "centos_snap", "centos-1", wait=True)
#
#
os.system("openstack image list")

obj.os_server_creation(logger, conn, "centos_snap_vm", "m1.medium", "centos_snap", "storage-net", "c11a0ebb-22bb-4658-9804-c20d0053412a", "nova2", "ceph-key", 1, 3)

delete_object.os_delete_server(logger, conn_delete, "centos", 1, 3)
delete_object.os_delete_server(logger, conn_delete, "centos_snap_vm", 1, 3)