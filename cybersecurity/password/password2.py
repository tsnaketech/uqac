#!/usr/bin/python3
# -*- coding: utf-8 -*-

###### Import ########

import hashlib

###### Variable ######

# Dico
d1 = {}

# File
user = "./user.txt"
out = "./hashed.txt"

###### Function ######

def s256login(login):
    login = bytes(login.strip(),"UTF-8")
    sel = hashlib.sha256(login).hexdigest()
    return sel

def s256password(word, sel):
    word = word + sel
    word = bytes(word.strip(),"UTF-8")
    h = hashlib.sha256(word).hexdigest()
    return h

###### Program #######

if user:
    with open(user, 'r') as file:
        for line in file:
            line = line.strip()
            h = line.split(" ")
            d1[h[0]] = h[1]

    with open(out, 'w+') as file:
        for h1 in d1.keys():
            sel = s256login(h1)
            h = s256password(d1[h1], sel)
            file.write("{0:9} {1} {2}\n".format(h1, sel , h))

exit(0)

