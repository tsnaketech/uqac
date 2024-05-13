#!/usr/bin/python3
# -*- coding: utf-8 -*-

###### Import ########

import hashlib

###### Variable ######

# Dico
d = {}

# List
l = []

# File
dico = "./dict.txt"
user = "./question3.txt"

###### Function ######

def s256(word):
    word = bytes(word.strip(),"UTF-8")
    word = hashlib.sha256(word).hexdigest()
    return word

def s256suffixe(account, hashed):
    if dico:
        with open(dico, 'r') as file:
            for word in file:
                for i in range(0,99):
                    w = word.strip() + (str(i)).zfill(2)
                    h = s256(w)
                    if h == hashed:
                        d[account] = w.strip()

def s256xkcd(account, hashed):
    if dico:
        with open(dico, 'r') as file:
            for word in file:
                l.append(word)
            for word1 in l:
                for word2 in l:
                    word = word1.strip() + word2.strip()
                    h = s256(word)
                    if h == hashed:
                        d[account] = word


###### Program #######

if user:
    with open(user, 'r') as file:
        ty = file.readline()
        ty = ty.split(" ")
        ty = s256suffixe(ty[0], ty[1].strip())
        li = file.readline()
        li = li.split(" ")
        li = s256xkcd(li[0], li[1].strip())

print(d)

exit(0)