#!/usr/bin/python3
# -*- coding: utf-8 -*-

###### Import ########

import hashlib
import time

###### Variable ######

# Dico
d1 = {}
d2 = {}

# File
dico = "./dict.txt"
user = "./hashedPasswordFile.txt"

###### Function ######

def s256(word):
    word = bytes(word.strip(),"UTF-8")
    word = hashlib.sha256(word).hexdigest()
    return word

###### Program #######

if dico and user:
    with open(dico, 'r') as file:
        for word in file:
            h = s256(word)
            d1[h] = word.strip()

    with open(user, 'r') as file:
        for line in file:
            line = line.strip()
            h = line.split(" ")
            for i in h:
                if len(i) == 0:
                    continue
                elif len(i) == 64 :
                    a = i
                elif len(i) != 0 :
                    b = i
            d2[a] = b
else:
	print("Fichier absent à la racine du programme !!!")
	time.sleep(5)
	exit(1)


for h2 in d2.keys():
    for h1 in d1.keys():
        if h2 == h1:
            print("Password : {0:9} = Hash : {1}".format(d1[h1], h1))

exit(0)