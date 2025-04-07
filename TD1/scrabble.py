#On ouvre le fichier et on charge la liste des mots dans une listes
mots = []
f = open("frenchssaccent.dic", "r")
for ligne in f.readlines():
    mots.append(ligne[0:len(ligne)-1])#On enlève le caractère de fin de ligne
f.close()

def mot_possible(tirage, mot):
    '''Prend une liste de lettres et un mot, et renvoie si on peut écrire le mot avec le tirage'''
    cp = tirage[::]#Copie du tirage car on va le modifier
    for lettre in mot:
        if not lettre in cp:#La lettre n'est pas dans le tirage donc on ne peut pas écrire le mot
            return False
        cp.remove(lettre)#On utilise la lettre, donc on l'enlève
    return True

def liste_mots_possibles(tirage):
    '''Renvoie la liste des mots français qu'on peut écrire avec le tirage'''
    mots_possibles = []
    for mot in mots:
        if mot_possible(tirage, mot):
            mots_possibles.append(mot)
    return mots_possibles

def mot_plus_long(tirage):
    '''Renvoie le mot le plus long qu'on peut écrire avec le tirage'''
    mots_possibles = liste_mots_possibles(tirage)
    solution = ""
    taille = 0
    for mot in mots_possibles:
        mtaille = len(mot)
        if mtaille > taille:
            taille = mtaille
            solution = mot
    return solution

tirage1 = ['b', 'p', 'd', 'w', 's', 'y', 'w', 'i']
print(liste_mots_possibles(tirage1))
print(mot_plus_long(tirage1))
tirage2 = ['a', 'r', 'b', 'g', 'e', 's', 'c', 'j']
print(liste_mots_possibles(tirage2))
print(mot_plus_long(tirage2))

### QUESTION 3

def lettre_point(e):
    '''Renvoie le point d'une lettre'''
    if e in 'aeilnorstu':
        return 1
    if e in 'dgm':
        return 2
    if e in 'bcp':
        return 3
    if e in 'fhv':
        return 4
    if e in 'jq':
        return 8
    if e in 'kwxyz':
        return 10
    return 0

def score(mot):
    '''Renvoie le score du mot en ajoutant le score de toutes les lettres'''
    out = 0
    for lettre in mot:
        out += lettre_point(lettre)
    return out

def max_score(mots):
    if len(mots) == 0:
        return ("", 0)
    solution = ""
    bscore = 0
    for mot in mots:
        mscore = score(mot)
        if mscore > bscore:
            bscore = mscore
            solution = mot
    return solution, bscore

print(max_score(['rte', 'ver', 'ce', 'etc', 'cet', 'ex', 'cr', 'et', 'ter', 'te', 'ct']))
### QUESTION 4

def mot_possible_joker(tirage, mot):
    '''Renvoie si on peut écrire le mot en prenant en compte l'utilisation d'un joker, renvoie aussi la lettre remplacée'''
    cp = tirage[::]#Une copie du tirage
    assert cp.count("?") <= 1#Un seul joker au plus
    jokerAvailable = "?" in cp
    jokerReplace = ""
    for lettre in mot:
        if lettre in cp:
            cp.remove(lettre)
        elif jokerAvailable:
            jokerAvailable = False
            jokerReplace = lettre
        else:
            return False, ""
    return True, jokerReplace

def max_score_joker(tirage):
    '''Renvoie le mot avec le meilleur score quand le tirage peut avoir un joker'''
    possibles = []
    for mot in mots:
        boolean, lettre = mot_possible_joker(tirage, mot)
        if boolean:
            possibles.append((mot, lettre))
    solution = ""
    bscore = 0
    for (mot, lettre) in possibles:
        mscore = score(mot) - score(lettre)#On enlève le score de la lettre qu'on a remplacé par un joker
        if mscore > bscore:
            bscore = mscore
            solution = mot
    return solution, bscore

print(max_score_joker(list("zxcvrrt?")))