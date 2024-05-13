#!/usr/bin/python3
# -*- coding: utf-8 -*-

###### Import ########

import math
import random
import sys
import sympy
import time
from sympy import mod_inverse

###### Variable ######

k = 200
# k = 2048

###### Function ######

class Timer(object):  
    def start(self):  
        if hasattr(self, 'interval'):  
            del self.interval  
        self.start_time = time.time()  
  
    def stop(self):  
        if hasattr(self, 'start_time'):  
            self.interval = time.time() - self.start_time  
            del self.start_time

def pgcd(a,b):
    while b!=0:
        a,b=b,a%b
    return a

def search_e(phi):
    r = 0
    while r != 1:
        e = random.randrange(1, phi)
        r = pgcd(e, phi)
    return e

def modinv(e, phi):
    d_old = 0; r_old = phi
    d_new = 1; r_new = e
    while r_new > 0:
        a = r_old // r_new
        (d_old, d_new) = (d_new, d_old - a * d_new)
        (r_old, r_new) = (r_new, r_old - a * r_new)
    return d_old % phi if r_old == 1 else None

def miller_rabin(n, k):
    if n != int(n):
        return False
    n = int(n)
    if n == 2:
        return True

    if n % 2 == 0:
        return False
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generatePrime(k,H = 10):
    r = H * (math.log(k, 2) + 1)  # number of attempts max
    r = int(r)
    re = r
    while r > 0:
        n = random.randrange(H ** (k - 1), H ** (k))
        r -= 1
        if miller_rabin(n,100):
            return n
    return generatePrime(k)

def factoriser(n):
    b=2
    while b:
        while n%b!=0 :
            b=b+1
        if n/b==1 :
            print("p = ", b)
            # On créé une variable globale p pour la réutiliser hors de la fonction et p=b
            global p
            p = b
            break
        print("\nq = ", b)
        # On créé une variable globale q pour la réutiliser hors de la fonction et q=b
        global q
        q=b
        n=n/b;

def key_generator(p, q):
    n = p * q
    phi = (p-1) * (q-1)
    e = search_e(phi)
    d = mod_inverse(e, phi)
    # print((e * d) % phi)
    return ((e, n), (d, n))

def rsaencrypt(pk, plaintext):
    e, n = pk
    cipher = [pow(ord(c), e, n) for c in plaintext]
    return cipher

def rsadecrypt(pk, ciphertext):
    d, n = pk
    plain = [chr(pow(c, d, n)) for c in ciphertext]
    return ''.join(plain)

###### Program #######

if __name__ == '__main__':
    print("##### RSA Encrypter/Decrypter #####")
    timer = Timer() 
    # p = int(input("Entrez un grand nombre premier p : "))
    # q = int(input("Entrez un grand nombre premier q : "))
    # p, q = generatePQ(2048)
    print("[+] Génération de p et q !!")

    timer.start()  
    p = generatePrime(k)
    timer.stop()
    print(f"[+] Génération de p en {timer.interval} secondes")

    timer.start()  
    q = generatePrime(k)
    timer.stop()
    print(f"[+] Génération de q en {timer.interval} secondes")

    print(f"p = {p}\nq = {q}")

    print("[+] Génération de vos clés publique/privé ...")
    public, private = key_generator(p, q)
    print(f"Clé publique {public}\nClé privé {private}")
    # message = input("[-] Entrer le message à chiffrer avec la clé privé : ")
    message = 'azerty'
    encrypted = rsaencrypt(private, message)
    print(f"[+] Message chiffré : {''.join(map(lambda x: str(x), encrypted))}")
    print(f"[+] Message déchiffré : {rsadecrypt(public, encrypted)}")
    time.sleep(10)