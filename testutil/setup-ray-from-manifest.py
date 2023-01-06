"""
This script enables all nodes in a cloudlab cluster to communicate with one another using ssh in normal user mode. It should be run on a computer that can connect to the cloudlab cluster.

The cluster is specified in the file `./cluster_manifest.xml`
"""
import xml.etree.ElementTree as ET
import subprocess

class Node:
	def __init__(self, name, hostname, port):
		self.name = name
		self.hostname = hostname
		self.port = port

manifest_path = "cluster_manifest.xml"		# cluster_manifest.xml is the manifest file generated by cloudlab
username = "xinyu"
ns_str = "http://www.geni.net/resources/rspec/3"
ns_dict = {"ns": ns_str}
tree = ET.parse(manifest_path)
cluster_nodes = []

for node in tree.findall('ns:node', ns_dict):
	if node.get('client_id') == "dsnode":	# skip dataset node
		continue
	services = node.find("ns:services", ns_dict)
	login = services.find("ns:login[@username='xinyu']", ns_dict)
	cluster_nodes.append(Node(
		name = node.get('client_id'),
		hostname = login.get('hostname'),
		port = login.get('port')
	))

for cnode in cluster_nodes:
	print("Find node {}: host={}, port={}".format(cnode.name, cnode.hostname, cnode.port))



kgw_command = """'bash -s' < setup-ssh-script.sh"""	# generate key pairs, write public key
for cnode in cluster_nodes:
	subprocess.Popen(
		"ssh -oStrictHostKeyChecking=no -tt -p {port} {username}@{hostname} {command}".format(
			port=cnode.port,
			username=username,
			hostname=cnode.hostname,
			# command=dummy_command.format(cnode.name, cnode.hostname)
			command=kgw_command,
		),
		shell=True).wait()	# wait one after another, just in case


## Step 2: add public keys of all nodes to all nodes' authorized_keys
handles = []
aut_command = """<< EOF\ncat /nfs/id_agg.pub >> ~/.ssh/authorized_keys\nexit\nEOF""" 
		
for cnode in cluster_nodes: 
	handle = subprocess.Popen(
		"ssh -oStrictHostKeyChecking=no -tt -p {port} {username}@{hostname} {command}".format(
			port=cnode.port,
			username=username,
			hostname=cnode.hostname,
			# command=dummy_command.format(cnode.name, cnode.hostname)
			command=aut_command,
		),
		shell=True)
	handles.append(handle)

for handle in handles:
	handle.wait()	# wait all together, b/c order doesn't matter in this case
