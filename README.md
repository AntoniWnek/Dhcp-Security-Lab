# DHCP Security Analysis
[PL](#polski) | [EN](#english)

<a name="polski"></a>
## Opis projektu
Celem projektu była analiza podatności protokołu DHCP na ataki w warstwie 2 modelu OSI oraz praktyczna implementacja mechanizmów obronnych na fizycznych urządzeniach sieciowych MikroTik.

## Wykorzystane technologie
**Język:** Python (biblioteka Scapy) <br>
**Środowisko:** MikroTik RouterOS (fizyczny switch/router) <br>
**Analiza i weryfikacja:** Wireshark <br>

**Uwaga techniczna**: Skrypty zostały opracowane i przetestowane w kontrolowanym środowisku laboratoryjnym (fizyczne urządzenia MikroTik). Skuteczność ich działania w innych środowiskach zależy od konfiguracji sprzętowej oraz aktywnych mechanizmów zabezpieczających (np. wbudowane funkcje ochrony L2 w innych systemach sieciowych).

## Funkcjonalności skryptów
1. **DHCP Starvation:** Skrypt w Pythonie (Scapy) generujący masowe pakiety DHCP DISCOVER z dynamicznie zmienianym adresem MAC (MAC Spoofing) w celu wyczerpania puli adresowej serwera.
2. **Rogue DHCP:** Implementacja nieautoryzowanego serwera (Rogue Server) pozwalająca na przejęcie roli bramy domyślnej i przeprowadzenie ataku Man-in-the-Middle (MitM).

## Mechanizmy Obronne 
**DHCP Snooping** (podział na porty zaufane/niezaufane). <br>
**Port Security** (limitowanie liczby adresów MAC na port). 

## Disclaimer
To narzędzie służy wyłącznie do celów edukacyjnych oraz legalnych testów penetracyjnych. Może być wykorzystywane jedynie w odizolowanych środowiskach laboratoryjnych lub sieciach, w których uzyskano wyraźną zgodę na przeprowadzenie testów. Nieautoryzowane użycie skryptów przeciwko systemom informatycznym jest nielegalne i podlega odpowiedzialności karnej.

## Autorzy
**Jakub Malisz** 
**Antoni Wnęk**

---

<a name="english"></a>
## Project overview
The goal of this project was to analyze DHCP protocol vulnerabilities in Layer 2 of the OSI model and implement security procedures on networking hardware. 

## Tech stack
**Programming language:** Python (Scapy library) <br>
**Hardware:** MikroTik RouterOS (switch/router) <br>
**Analysis:** Wireshark <br>

**Technical Note**: These scripts were developed and tested in a controlled lab environment using physical MikroTik hardware. Their effectiveness in other environments may vary depending on hardware configuration and active security mechanisms (e.g., built-in L2 protection features in different networking platforms).

## Scripts overview
1. **DHCP Starvation:** A Python script using Scapy to generate mass DHCP DISCOVER messages with random MAC addresses (MAC Spoofing) to exhaust the DHCP server's IP pool.  
2. **Rogue DHCP:** Deployment of an unauthorized DHCP server to redirect client traffic by spoofing Default Gateway and DNS settings (MitM attack).

## Mitigation Strategies
**DHCP Snooping:** Restricting DHCP responses to trusted ports only. <br>
**Port Security:** Limiting the number of source MAC addresses allowed on a single port.

## Disclaimer
This tool is for educational and ethical hacking purposes only. Use it only in isolated lab environments or networks where you have explicit permission. Unauthorized use against systems is illegal.

## Authors
**Jakub Malisz**
**Antoni Wnęk**

