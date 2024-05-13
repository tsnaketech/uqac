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

def alphaint(c):
    alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    return alphabet.index(c)

def alphachar(i):
    alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    return alphabet[i]

def encrypt(a,b):
    a = alphaint(a)
    b = alphaint(b)
    return alphachar((a+b)%26)

def decrypt(a,b):
    a = alphaint(a)
    b = alphaint(b)
    return alphachar((a-b)%26)

def addapt(w,n):
    plaintext = ""
    l = []
    c = ""
    plaintext = w.replace(' ', '').upper()
    for i in range(0,len(plaintext)):
        c = c + str(plaintext[i])
        if len(c)%n == 0:
            l.append(c)
            c = ""       
    l.append(c)
    return l

def vcrypt():
    l = []
    c = ""
    plaintext = input("[+] Entrer votre phrase à chiffrer : ").strip()  
    key = input("[+] Entrer votre mot de passe : ").upper()
    plaintext = addapt(plaintext,len(key))
    for i in plaintext:
        for j in range(0, len(key)):
            try:
                c = c + encrypt(i[j], key[j])
            except:
                break
            if len(c)%len(key) == 0 :
                l.append(c)
                c = "" 
    l.append(c)          
    ciphertext = " ".join(l)
    print("[+] Voici votre text chiffrer !\n")
    print(ciphertext)
    return ciphertext

def vdecrypt():
    l = []
    c = ""
    ciphertext = input("[+] Entrer votre phrase chiffrée :").strip() 
    key = input("[+] Entrer votre mot de passe : ").upper()
    ciphertext = addapt(ciphertext,len(key))
    for i in ciphertext:
        for j in range(0, len(key)):
            try:
                c = c + decrypt(i[j], key[j])
            except:
                break
            if len(c)%len(key) == 0 :
                l.append(c)
                c = "" 
    l.append(c)          
    plaintext = " ".join(l)
    print("[+] Voici votre text déchiffré !\n")
    print(plaintext)
    return plaintext

###### Program #######


while 1:
    choice = input(MENU + "\nChoice : ")
    if choice == '1':
        vcrypt()
    elif choice == '2':
        vdecrypt()
    elif choice == '3':
        exit()