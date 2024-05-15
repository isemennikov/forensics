from scapy.all import *
import ipaddress
import sys

ports = [25, 80, 53, 443, 445, 8080, 8443]

def syn_scan(host):
    ans, unans = sr(IP(dst=host)/TCP(sport=33333, dport=ports, flags="S"), timeout=2, verbose=0)
    open_ports = [s[TCP].dport for (s, r) in ans if s[TCP].dport == r[TCP].sport and r[TCP].flags == "SA"]
    if open_ports:
        print(f"Open ports at {host}: {', '.join(map(str, open_ports))}")

def dns_scan(host):
    ans, unans = sr(IP(dst=host)/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname="google.com")), timeout=2, verbose=0)
    for sent, received in ans:
        if received.haslayer(DNS) and received.getlayer(DNS).rcode == 0:  # Проверяем, что получен ответ от DNS сервера
            print(f"DNS Server at {host}")
            break

if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else input("Enter IP Address: ")
    try:
        ipaddress.ip_address(host)
        syn_scan(host)
        dns_scan(host)
    except ValueError:
        print("Invalid address")
        sys.exit(-1)