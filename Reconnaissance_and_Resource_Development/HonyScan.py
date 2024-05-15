
from scapy.all import *

ip_address = "172.16.249.136"
open_ports = [53, 80]
honey_ports = [8080, 8443]
blocked_hosts = ["172.16.249.1"]


def create_response(packet, flags):
    layer = IP if packet.haslayer(IP) else IPv6
    response = (
            Ether(src=packet[Ether].dst, dst=packet[Ether].src) /
            layer(src=packet[layer].dst, dst=packet[layer].src) /
            TCP(sport=packet[TCP].dport, dport=packet[TCP].sport, ack=packet[TCP].seq + 1, flags=flags)
    )
    return response


def analyze_packets(packet):
    if not packet.haslayer(TCP) or packet[TCP].flags != "S":
        return

    source = packet[IP].src if packet.haslayer(IP) else packet[IPv6].src
    port = packet[TCP].dport

    if source in blocked_hosts:
        flags = "RA" if port in open_ports else ("SA" if port in honey_ports else None)
    else:
        if port not in open_ports + honey_ports:
            blocked_hosts.append(source)
            flags = "SA" if port in honey_ports else None

    if flags:
        response = create_response(packet, flags)
        sendp(response, verbose=False)
        if flags == "RA":
            print(f"Sending {flags} packet in response to traffic from {source} on port {port}")


filter_rule = f"dst host {ip_address} and tcp"
sniff(filter=filter_rule, prn=analyze_packets)
