#!/usr/bin/python3
# -*- coding: utf-8 -*-

###### Import ########

import numpy as np
import random
from numpy.linalg import det
from sympy import mod_inverse

###### Variable ######

MENU = "\n1 -> Chiffrer\n2 -> Déchiffrer\n3 -> Quit\n"
mat = []

###### Function ######

def pgcd(a,b):
    while b!=0:
        a,b=b,a%b
    return a

def alphaint(c):
    alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","A"]
    return alphabet.index(c)

def alphachar(i):
    alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","A"]
    return alphabet[i]

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

def matrice():
    l = []
    dim = int(input("\n[+] Entrer la dimention de la matrice : "))
    print()
    for i in range(1, dim+1):
        j = input(f"[+] Entrer la/les valeur(s) de la ligne {i} : ")
        if ',' in j:
            j = j.split(",")
        elif ' ' in j:
            j = j.split(" ")
        if len(j) != dim :
            print("Merci de réitérer le programme en insérant comme séparateur soit un point-virgule ';' ou un espace ' ' ")
            exit(1)
        j = [int(i)%26 for i in j]
        l.append(j)
    mat = np.array(l)
    return mat, dim

def hcrypt(mat, plaintext, dim):
    result = []
    ciphertext = ""
    plaintext = addapt(plaintext,dim)
    for i in plaintext:
        if len(i) == 0:
            break
        elif len(i) != dim:
            c = i
            for j in range(0,dim - len(i)):
                c = c + 'X'
                print(c)
            i = c
        result = [alphaint(j) for j in list(i)]
        result = np.dot(result,mat)%26
        result = [alphachar(int(round(j))) for j in result]
        ciphertext = ciphertext + str("".join(result))    
    return ciphertext


def hdecrypt(mat, ciphertext, dim):
    result = []
    plaintext = ""
    ciphertext = addapt(ciphertext,dim)
    deter = int(round(det(mat)))
    if (pgcd(deter, 26) != 1):
        print("Le pgcd du déterminant de la matrice et de 26 n'est pas égal à 1 !")
        exit(1)
    inverse = np.linalg.inv(mat)
    inverse = inverse.dot(deter)
    modulo_inv = mod_inverse(deter, 26)
    mat_inverse = np.dot(modulo_inv,inverse)%26
    for i in ciphertext:
        if len(i) == 0:
            break
        elif len(i) != dim:
            c = i
            for j in range(0,dim - len(i)):
                c = c + 'X'
                print(c)
            i = c
        result = [alphaint(j) for j in list(i)]
        result = np.dot(result,mat_inverse)%26
        result = [alphachar(int(round(j))) for j in result]
        plaintext = plaintext + str("".join(result))
    return plaintext

###### Program #######

while 1:
    choice = input(MENU + "\nChoice : ")
    if choice == '1':
        mat, dim = matrice()
        plaintext = input("\n[+] Entrer votre phrase à chiffrer : ").strip().upper()
        print('\n' + hcrypt(mat, plaintext, dim))
    elif choice == '2':
        mat, dim = matrice() 
        ciphertext = input("\n[+] Entrer votre phrase chiffrée : ").strip().upper()
        print('\n' + hdecrypt(mat, ciphertext, dim))
    elif choice == '3':
        exit()