from scapy.all import *
import ipaddress
import sys

# Определение портов для сканирования
ports = [25, 80, 53, 443, 445, 8080, 8443]

# Функция сканирования TCP
def syn_scan(host):
    ans, unans = sr(IP(dst=host)/TCP(sport=33333, dport=ports, flags="S"), timeout=2, verbose=0)
    open_ports = [s[TCP].dport for (s, r) in ans if s[TCP].dport == r[TCP].sport and r[TCP].flags == "SA"]
    if open_ports:
        print(f"Open ports at {host}: {', '.join(map(str, open_ports))}")

# Функция сканирования DNS
def dns_scan(host):
    ans, unans = sr(IP(dst=host)/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname="google.com")), timeout=2, verbose=0)
    for sent, received in ans:
        if received.haslayer(DNS) and received.getlayer(DNS).rcode == 0:  # Проверяем, что получен ответ от DNS сервера
            print(f"DNS Server at {host}")
            break

# Функция обработки файла с IP-адресами и сетями
def process_hosts_file(filename):
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if '-' in line:
                start_ip, range_part = line.split('-')
                end_ip = start_ip.split('.')[:-1] + [range_part]
                ip_range = [str(ip) for ip in ipaddress.summarize_address_range(ipaddress.IPv4Address(start_ip), ipaddress.IPv4Address('.'.join(end_ip)))]
            elif '/' in line:
                ip_range = [str(ip) for ip in ipaddress.IPv4Network(line, strict=False)]
            else:
                ip_range = [line]

            for host in ip_range:
                syn_scan(host)
                dns_scan(host)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        hosts_file = sys.argv[1]
        process_hosts_file(hosts_file)
    else:
        host = input("Enter IP Address: ")
        try:
            ipaddress.ip_address(host)
            syn_scan(host)
            dns_scan(host)
        except ValueError:
            print("Invalid address")
            sys.exit(-1)
