from scapy.all import PcapReader
from scapy.utils import wrpcap

def pcap_trunc(filepath, max_count=10):
	trunc_packets = []
	count = 0
	for packet in PcapReader(filepath):
		if count % 10000 == 0:
			print("Packet read: {:8d}".format(count), end="\r")
		trunc_packets.append(packet)
		count += 1
		if count == max_count:
			print("Packet read: {:8d}".format(count), end="\r")
			break
	print()
	wrpcap("/nfs/NetShare/traces/testpcap/testpcap.pcap", trunc_packets)


filepath = "/nfs/NetShare/traces/caida/raw.pcap"
max_count = 1e3
pcap_trunc(filepath, max_count)
