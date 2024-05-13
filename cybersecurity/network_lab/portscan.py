#!/usr/bin/python3
# -*- coding: utf-8 -*-

###### Import ########

import sys
from scapy.all import *

###### Variable ######

# Dictionnaire pour l'analyse
scans = {}

###### Function ######

def usage(text):
    print(f"[+] {text}\n")

    print("Argument 1 : Fichier pcap")
    print("Argument 2 : Seuil de port à ne pas dépasser en int")

###### Program #######

try:
    packets = rdpcap(sys.argv[1])
except:
    usage("Le fichier n'existe pas")
    exit(1)

try:
    n = int(sys.argv[2])
except:
    usage("Second argument manquant ou n'est pas un int")
    exit(2)

# Let's iterate through every packet
for packet in packets[IP]:
    # print(packet[IP].src,packet[IP].dst,packet[TCP].sport, packet[TCP].dport, packet[UDP].sport, packet[UDP].dport)
    src, dst = packet[IP].src, packet[IP].dst
    # Récupération du port de déstination présent dans le paquet TCP, si présent
    try:
        tcp = packet[TCP].dport
    except:
        tcp = None
    # Récupération du port de déstination présent dans le paquet UDP, si présent
    try:
        udp = packet[UDP].dport
    except :
        udp = None

    # Ajout du port dans la variable
    if (tcp): port = tcp
    if (udp): port = udp

    # Test la présence de tous les variables
    if (src and dst and port):
        # Crétion de la clé pour le dictionnaire
        k = f'{src}-->{dst}'
        # Ajout des informations du paquet dans le dictionnaire avec la clé venant d'être créée
        # Création de la liste si elle n'est pas présente
        try:
            scans[k].append(port)          
        except KeyError:
            scans[k] = []
            scans[k].append(port)

print(f"{'Source -> Destination'.ljust(40, ' ')} | {'Paquets envoyés'.ljust(15, ' ')} | {'Ports scannés'.ljust(15, ' ')} | {'Alerte'.ljust(10, ' ')}")
print(f"{'-'.ljust(85, '-')}")
for i in scans:
    if (len(list(set(scans[i]))) > n) :
        print(f"{i.rjust(40, ' ')} | {str(len(scans[i])).rjust(15, ' ')} | {str(len(list(set(scans[i])))).rjust(15, ' ')} | {'Alerte'.ljust(10, ' ')}")
    else : 
        print(f"{i.rjust(40, ' ')} | {str(len(scans[i])).rjust(15, ' ')} | {str(len(list(set(scans[i])))).rjust(15, ' ')} | ")
