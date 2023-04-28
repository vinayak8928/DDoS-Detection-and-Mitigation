import scapy.all
from scapy.all import *

src_ip="10.0.0.1"
target_ip="10.1.0.1"

target_port = 80

ip = IP(src=src_ip, dst=target_ip)

udp = UDP (sport=RandShort(), dport=target_port)

p = ip/udp

send(p, loop=1, verbose=0, count=400)
