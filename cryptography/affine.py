#!/usr/bin/python3
# -*- coding: utf-8 -*-

###### Import ########

import signal

###### Variable ######

MENU = "\n1 -> Chiffrer\n2 -> Déchiffrer\n3 -> Quit\n"

###### Function ######

def signal_exit(sig, frame):
        print('You pressed Ctrl + C !')
        exit(0)
signal.signal(signal.SIGINT, signal_exit)

def pgcd(a,b):
    while b!=0:
        a,b=b,a%b
    return a

def alphaint(c):
    alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    return alphabet.index(c)

def alphachar(i):
    alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    return alphabet[i]

# Calcul de l'inverse d'un nombre modulo 26
def inverse(a):
        x=0
        while (a*x%26!=1):
                x=x+1
        return x

def encrypt(a,b,C):
    x = alphaint(C)
    return alphachar((a*x+b)%26)

def decrypt(a,b,C):
    x = alphaint(C)
    return alphachar((inverse(a)*(x-b))%26)
                
def acrypt(M,a,b):
    if (pgcd(a,26)==1):
        word = []
        c = ""
        for i in M:
            for j in range(0, len(i)):
                c = c + str(encrypt(a,b,i[j]))
            word.append(c)
            c = ""
        return " ".join(word)
    else:
        return "Chiffrement impossible. Veuillez choisir un nombre premier avec 26."

def adecrypt(M,a,b):
    if (pgcd(a,26)==1):
        word = []
        c = ""
        for i in M:
            for j in range(0, len(i)):
                c = c + str(decrypt(a,b,i[j]))
            word.append(c)
            c = ""
        return " ".join(word)
    else:
        return "Déchiffrement impossible. Le nombre a n'est pas premier avec 26."

###### Program #######

while 1:
    choice = input(MENU + "\nChoice : ")
    if choice == '1':
        M = input("[+] Entrer votre phrase à chiffrer : ").strip().upper().split(" ")
        a = int(input("[+] Entrer la valeur de x : ").strip())
        b = int(input("[+] Entrer la valeur de y : ").strip())
        print('\n' + acrypt(M, a, b))
    elif choice == '2':
        M = input("[+] Entrer votre phrase à déchiffrer : ").strip().upper().split(" ")
        a = int(input("[+] Entrer la valeur de x : ").strip())
        b = int(input("[+] Entrer la valeur de y : ").strip())
        print('\n' + adecrypt(M, a, b))
    elif choice == '3':
        exit()