#Lettre vers chiffre
def alphaint(c):
    alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    return alphabet.index(c)
#Lettre vers lettre
def alphachar(i):
    alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    return alphabet[i]

#Console
print("Entrer votre mot de passe: ")
chaineMdp = input()
nouvelleChaine = ""

tailleMdp = len(chaineMdp)

i = 0
print("--- ",chaineMdp," ---",i,"\n")

#Boucle pour tester toutes les possibilités de l'alphabet
while i < 26: 
	j = 0

	#Boucle pour incrémenter chaque lettre de la string
	while j < tailleMdp:
		position = alphaint(chaineMdp[j])

		#Recommencer l'alphabet depuis le debut (Z -> A)
		if position == 25:
			position = 0
		else:
			position += 1

		nouveauCarractere = alphachar(position)
		nouvelleChaine += nouveauCarractere
		j += 1

	print("--- ",nouvelleChaine," ---",i+1,"\n")
	#Creation de la chaine solution
	chaineMdp = nouvelleChaine
	nouvelleChaine = ""

	i += 1