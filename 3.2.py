# Projet MOGPL : Optimisation appliquée à la localisation d’unités de soins et à la prise en charge des patients

import csv
from gurobipy import *
import numpy as np

"""

# Paramètre à modifier pour effectuer les test

"""

# J : indice des villes possédant une unité de soin
J = [5, 2, 6, 10, 13] # Même ville que l'exo 2.2
J.sort() 

#J= [5,8,10,13,14] # Pour les test

# k : nombre d'unité spéciale défini par l'utilisateur
k = len(J)

# P = liste tel que P_j correspond au nombre de patients du secteur j nécessitant une prise en charge
P = [150, 150, 25, 150, 25]
#P=[150, 25, 125, 50, 75]

# --------------------------------------------------------------------------------------------------------------

"""

# Récupération des données du fichier `villes.csv` dans le dictionnaire reader

"""

with open('villes.csv', newline='', encoding="latin") as csvfile:
    reader = csv.DictReader(csvfile)
    
    # Villes : liste des villes
    # Populations : liste du nombre de population de chaque ville
    # dist : liste de listes des distances en annexe

    Villes, Populations, dist = [], [], []
    
    # Parcours le dictionnaire reader
    for row in reader:
        
        # Ajoute les valeurs aux listes Villes et Population
        Villes += [row['Ville']]
        Populations += [int(row['Population'])]
        
        # liste qui correspond à une ligne du tableau de l'annexe
        ligne = []
        
        # Parcours les valeurs des distances du tableau de l'annexe
        for key,value in row.items():   
            if key != 'Population' and key != 'Ville':
                ligne.append(value)
                
        # Ajoute la ligne dans la liste dist
        dist.append(ligne)

# --------------------------------------------------------------------------------------------------------------
"""

# Vérification des paramètres entrées par l'utilisateur

"""

if k <= 0:
    raise ValueError(" Aucune ville donnée")

if(sum(P) < 0 or sum(P) > 500):
    raise ValueError("Erreur la somme des valeurs de P ne peut pas être négative ou supérieur strictement à 500")

# --------------------------------------------------------------------------------------------------------------

"""

# Paramètres

"""
# n : nombre de villes situées sur le territoire de référence
n = len(Villes)

# d_ij : matrice des distances en annexe

# Remplis la partie triangulaire supérieur de la matrice des distances
for i in range(n):
    for j in range(i+1,n):
        dist[i][j] = dist[j][i]
        
# Transforme la liste de listes dist en matrice d'entiers
d_ij = np.asarray(dist,int)

# --------------------------------------------------------------------------------------------------------------

"""

# Résolution du PL :

"""

m = Model("Unites_de_soin")

# declaration variables de decision

# x : matrice de taille 5x5 de valeurs 0 à 100 tel quel x_ij indique le nombre de personne se déplaçant du secteur i au secteur j pour se faire traiter
x = m.addMVar((k, k), vtype=GRB.INTEGER, name="x")

# définition de l'objectif
obj = 0

for i in range(k):
    for j in range(k):
        obj += x[i,j] * d_ij[J[i],J[j]]
    
m.setObjective(obj, GRB.MINIMIZE)

# Definition des contraintes

# chaque unité de soin peut accueillir jusqu'à 100 patients
# Pour chaque unité situé en secteur j : Somme_i X_ij <= 100
for j in range(k):     
    m.addConstr(sum(x[:,j]) <= 100, "c%d" % j)

# le nombre de patient en provenance du secteur i doit être égal au nombre P[i] ( P[i] : nombre de patients du secteur i nécessitant une prise en charge)
# pour chaque secteur de provenance i : Somme_j x_ij = P_i
for i in range(k):
    m.addConstr(sum(x[i,:]) == P[i], "c%d" % (k+i))
    
# Resolution
m.optimize()
print("")
print("CONTEXTE DU PROBLEME:")
print("")
print("Soit un ensemble de ",k," unités de soins situées sur le territoire de référence.")
print("")
print("Les villes en question sont : ", end="")

for j in range(k):
    if j !=k-1:
        print(Villes[J[j]], ", ", end="")
    else:
        print(Villes[J[j]], ".")
print("")        
print('Solution optimale:')
print("")   
print("Voici la matrice x_ij que l'on obtient:")
print(x.X)
print("")       
# Explicité la matrice x  
for i in range(k):
    print (P[i], "patients sont affectés au secteur",Villes[J[i]],":")
    for j in range(k):
        if i == j:
            print('\t *',int(x[i,j].X), "patients restent à",Villes[J[j]],"pour se faire traiter.")
        elif x[i,j].X != 0:
            print('\t *',int(x[i,j].X), "patients de",Villes[J[i]],"ce déplace à", Villes[J[i]]," pour se faire traiter.")
    print("")
print('Valeur de la fonction objectif :', m.objVal)