#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# Author : 
#           - LE FEL Fannie
#           - LECOCQ Mickael
#           - MORICE Malo
#           - SAUVEGRAIN Emmanuel


###### Import ########

import random

###### Variable ######

# plaintext = [0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0]
# K = [0, 1, 1, 0, 0, 1, 0, 1, 0]
n = 4
n_cbc = 4

S1 = [["101", "010", "001", "110", "011", "100", "111", "000"],
      ["011", "100", "110", "010", "000", "111", "101", "011"]]
S2 = [["100", "000", "110", "101", "111", "001", "011", "010"],
      ["101", "011", "000", "111", "110", "010", "001", "100"]]

###### Function ######

# Fonction Expender
def expander(R):
    if(len(R) == 6):
        Ri = [0, 0, 0, 0, 0, 0, 0, 0]
        Ri[0] = R[0]
        Ri[1] = R[1]
        Ri[2] = R[3]
        Ri[3] = R[2]
        Ri[4] = R[3]
        Ri[5] = R[2]
        Ri[6] = R[4]
        Ri[7] = R[5]
        return Ri

# Gestion des S-Box
def sBoxes(entry, S):
    # entry : 4 bits, S:Sboxes, 2 lists of 8 columns
    column = int("".join([str(i) for i in entry[1:4]]), 2)
    line = S[entry[0]][column]
    box = ([int(i) for i in list(line)])
    return box

# Hénération de la nouvelle clé
def newKi(K, n):
    Ki = K[n::]
    if len(Ki) < 8:
        Ki = Ki + K[:-len(Ki) - 1]
    elif len(Ki) > 8:
        Ki = K[0:8]
    return Ki

# Chiffrement DES simplifié
def cryptoDES(T, K, n):
    L = T[0:6]
    R = T[6:12]
    for i in range(n):
        L1 = R
        Ki = newKi(K, i)
        E = expander(R)
        Ek = [E[j] ^ Ki[j] for j in range(8)]
        SE = sBoxes(Ek[0:4], S1) + sBoxes(Ek[4:8], S2)
        R = [L[j] ^ SE[j] for j in range(6)]
        L = L1
    ciphertext = L + R
    return ciphertext

# Chiffrement DES simplifié avec permutation de L et de R pour la question
def cryptoDESpermut(T, K, n):
    L = T[0:6]
    R = T[6:12]
    for i in range(n):
        L1 = R
        Ki = newKi(K, i)
        E = expander(R)
        Ek = [E[j] ^ Ki[j] for j in range(8)]
        SE = sBoxes(Ek[0:4], S1) + sBoxes(Ek[4:8], S2)
        R = [L[j] ^ SE[j] for j in range(6)]
        L = L1
    ciphertext = R + L
    return ciphertext

# Déchiffrement DES simplifié
def decryptoDES(T, K, n):
    L = T[6:12]
    R = T[0:6]
    for i in reversed(range(n)):
        L1 = R
        R1 = L
        Ki = newKi(K, i)
        E = expander(L1)
        Ek = [E[j] ^ Ki[j] for j in range(8)]
        SE = sBoxes(Ek[0:4], S1) + sBoxes(Ek[4:8], S2)
        R = [R1[j] ^ SE[j] for j in range(6)]
        L = L1
    plaintext = R + L
    return plaintext

# Implémentation de CBC sur DES simplifié, partie chiffrement
def desCBC(plaintext, K, n = 1):
    # Génration de l'IV
	iv = [random.randint(0, 1) for i in range(12)]
    # Création d'un tableau avec blocs de 12 bits chacun
	t = [plaintext[i:i+12] for i in range(0, 48, 12)]
	c = iv
	ciphertext = []
	for i in t:
		cipher = [i[j] ^ c[j] for j in range(12)]
		des = cryptoDES(cipher, K, n)
		[ciphertext.append(j) for j in des]
		c = des
	[ciphertext.append(j) for j in iv]
	return ciphertext

# Implémentation de CBC sur DES simplifié, partie déchiffrement
def ddesCBC(ciphertext, K, n = 1):
    # Création du tableau
	t = [ciphertext[i:i+12] for i in range(0, 60, 12)]
	plaintext = []
    # Récupération de l'IV présent à la fin du ciphertext
	iv = t[-1]
    # Suppression de l'IV
	t = t[:-1]
	p = iv
	for i in t:
		des = decryptoDES(i, K, n)
		plain = [des[j] ^ p[j] for j in range(12)]
		p = i
		[plaintext.append(j) for j in plain]
	return plaintext

###### Program #######

# Comment perdre du temps (récupérer sur un ancien code) :D
print ("#"*100)
print ("""  
                      :::!~!!!!!:.
                  .xUHWH!! !!?M88WHX:.
                .X*#M@$!!  !X!M$$$$$$WWx:.
               :!!!!!!?H! :!$!$$$$$$$$$$8X:
              !!~  ~:~!! :~!$!#$$$$$$$$$$8X:             ____                  _     __  __     
             :!~::!H!<   ~.U$X!?R$$$$$$$$MM!            / ___|_ __ _   _ _ __ | |_  |  \/  | __
             ~!~!!!!~~ .:XW$$$U!!?$$$$$$RMM!           | |   | '__| | | | '_ \| __| | |\/| |/ _ \\
               !:~~~ .:!M"T#$$$$WX??#MRRMMM!           | |___| |  | |_| | |_) | |_  | |  | |  __/
               ~?WuxiW*`   `"#$$$$8!!!!??!!!            \____|_|   \__, | .__/ \__| |_|  |_|\___|
             :X- M$$$$       `"T#$T~!8$WUXU~                       |___/|_|
            :%`  ~#$$$m:        ~!~ ?$$$$$$
          :!`.-   ~T$$$$8xx.  .xWW- ~""##*"
.....   -~~:<` !    ~?T#$$@@W@*?$$      /`
W$@@M!!! .!~~ !!     .:XUW$W!~ `"~:    :
#"~~`.:x%`!!  !H:   !WM$$$$Ti.: .!WUn+!`
:::~:!!`:X~ .: ?H.!u "$$$B$$$!W:U!T$$M~
.~~   :X@!.-~   ?@WTWo("*$$$W$TH$! `
Wi.~!X$?!-~    : ?$$$B$Wu("**$RM!
$R@i.~~ !     :   ~$$$$$B$$en:``
?MXT@Wx.~    :     ~"##*$$$$M~
""")
print ("#"*100)

# Plaintext définie
plaintext = [0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1]
# Clé définie
K = [0, 1, 1, 0, 0, 1, 0, 1, 0]
# Génération d'une clé
K = [random.randint(0, 1) for j in range(9)]

print(f"Plaintext {plaintext}")
print(f"Key       {K}")

print('\nQuestion B exercice 1')
for i in range(1,5):
    print(f'\nItération {i}')
    ciphertext = cryptoDES(plaintext, K, i)
    print(f"Ciphertext {ciphertext}")
    dciphertext = decryptoDES(ciphertext, K, i)
    print(f"Plaintext {dciphertext}")
    if plaintext == dciphertext:
        print("Déchiffrement OK")

print('\nQuestion C exercice 1')
for i in range(1,5):
    print(f'Intération {i}')
    for j in range(0,2**9):
        binary = int(bin(j)[2:])
        binary = '{0:09}'.format(binary)
        key = ([int(k) for k in list(binary)])
        ciphertext = cryptoDES(plaintext, key, i)
        if plaintext == ciphertext:
            print(f'Key {key} faible')
print("Il n'y a pas de clé faible !!")


print('\nQuestion D exercice 1')
for i in range(1,5):
    print(f'Intération {i}')
    for j in range(0,2**9):
        binary = int(bin(j)[2:])
        binary = '{0:09}'.format(binary)
        key = ([int(k) for k in list(binary)])
        ciphertext = cryptoDESpermut(plaintext, key, i)
        if plaintext == ciphertext:
            print(f'Key {key} faible')
print("Il n'y a pas de clé faible !!")

### Exercice 2 a et b
print('\nQuestion A, B exercice 2')
# plaintext = [random.randint(0, 1) for i in range(48)]
# K = [random.randint(0, 1) for i in range(9)]
p1 = [0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0]
p2 = [0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0]
K = [0, 1, 1, 0, 0, 1, 0, 1, 0]

# Chiffrement d'un plaintext
print(f"Plaintext  {p1}")
ciphertext = desCBC(p1, K, n_cbc)
plaintext = ddesCBC(ciphertext, K, n_cbc)
print(f"Ciphertext {ciphertext}")
print(f"Plaintext  {plaintext}")

# Chiffrement d'un plaintext avec la modification du 14ème bit
print(f"\nPlaintext  {p2}")
ciphertext = desCBC(p2, K, n_cbc)
plaintext = ddesCBC(ciphertext, K, n_cbc)
print(f"Ciphertext {ciphertext}")
print(f"Plaintext  {plaintext}")

print('\nLe changement du 14eme bit impacte seulement le 14eme bit du texte chiffré') 