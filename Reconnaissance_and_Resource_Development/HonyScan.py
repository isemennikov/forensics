
from scapy.all import *

ip_address = "172.16.249.136"
open_ports = [53, 80]
honey_ports = [8080, 8443]
blocked_hosts = []


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

    # Проверяем, исходит ли пакет от заблокированного хоста
    if source in blocked_hosts:
        # Если пакет пришел на открытый порт, отправляем флаги RST и ACK
        if port in open_ports:
            flags = "RA"
            print(f"Sending RST+ACK in response to traffic from {source} on open port {port}")
        # Если пакет пришел на "медовый" порт, отправляем флаги SYN и ACK
        elif port in honey_ports:
            flags = "SA"
            print(f"Sending SYN+ACK in response to traffic from {source} on honey port {port}")
        else:
            # Если пакет пришел на порт, который не является открытым или "медовым", не отправляем ответ
            return
    else:
        # Если исходящий хост не заблокирован, проверяем порт
        if port not in open_ports and port not in honey_ports:
            # Порт не открыт и не "медовый", добавляем хост в заблокированные
            blocked_hosts.append(source)
            print(f"Adding {source} to blocked hosts, no response sent")
            return
        elif port in honey_ports:
            # Порт "медовый" и хост не заблокирован, отправляем флаги SYN и ACK
            flags = "SA"
            print(f"Sending SYN+ACK in response to traffic from {source} on honey port {port}")
        else:
            # Пакет пришел на открытый порт, не отправляем ответ
            return

    # Создаем и отправляем ответный пакет
    response = create_response(packet, flags)
    sendp(response, verbose=False)

filter_rule = f"dst host {ip_address} and tcp"
sniff(filter=filter_rule, prn=analyze_packets)
