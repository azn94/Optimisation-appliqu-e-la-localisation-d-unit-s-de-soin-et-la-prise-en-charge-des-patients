# Projet MOGPL : Optimisation appliquée à la localisation d’unités de soins et à la prise en charge des patients

import csv
from gurobipy import *
import numpy as np

"""

# Paramètre à modifier pour effectuer les test

"""
# Orthographe des villes à insérer dans Unites pour effectuer les test
# ['Toulouse', 'Nice', 'Nantes', 'Montpellier', 'Strasbourg', 'Bordeaux', 'Lille', 'Rennes', 'Reims', 'Saint-étienne', 'Toulon', 'Le Havre', 'Grenoble', 'Dijon', 'Angers']

# Unites : villes possédant une unité spéciale de traitement des patients atteints par une forme sévère d’une nouvelle maladie
Unites = ['Nantes', 'Lille', 'Montpellier'] 

# alpha : paramètre strictement positif valant 0.1 ou 0.2
alpha = 0.1

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
        
        # Ajoute les valeurs aux listes Villes et Populations
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

if len(Unites) <= 0:
    raise ValueError(" Aucune ville donnée")

for ville in Unites:
    if ville not in Villes:
        raise ValueError("Une des villes n'est pas orthographié de la même manière que dans la liste des villes fournis")

if alpha < 0:
    raise ValueError("Alpha doit être strictement positif ")
# --------------------------------------------------------------------------------------------------------------

"""

# Paramètres

"""

# n : nombre de villes situées sur le territoire de référence
n = len(Villes)

# J : l’ensemble des indices de ces villes
J = []
for ville in Unites:
    for i in range(n):
        if Villes[i] == ville:
            J.append(i)
            
# k : nombre d'unité spéciale
k = len(J)

# pop_total : nombre de population total considéré  sur le territoire de référence
pop_total = sum(Populations)

# gamma : la population totale des villes composant un secteur ne doit pas dépasser la quantité gamma
gamma = (1.0 + alpha)/k * pop_total

# d_ij : matrice des distances en annexe

# Remplis la partie triangulaire supérieur de la matrice des distances
for i in range(n):
    for j in range(i+1,n):
        dist[i][j] = dist[j][i]
        
# Transforme la liste de listes dist en matrice d'entiers
d_ij = np.asarray(dist,int)

#  --------------------------------------------------------------------------------------------------------------

"""

# Résolution du PL :

"""

m = Model("Unites_de_soin")

# declaration variables de decision

# x : matrice à 2 dimensions de valeurs 0 ou 1 tel quel x_ij = 1 si les patients de la ville i sont traités dans la ville j
x = m.addMVar((n, k), vtype=GRB.BINARY, name="x")

# définition de l'objectif
obj = 0.0
for i in range(n):
    for j in range(k):
        obj += (d_ij[i][J[j]] * Populations[i] * x[i,j])
obj /= pop_total
            
m.setObjective(obj, GRB.MINIMIZE)

# Definition des contraintes

# une ville n’appartient qu’à un unique secteur 
# pour chaque ville : Somme_j x_ij = 1
for i in range(n):     
    m.addConstr(sum(x[i,:]) == 1, "c%d" % i)

# la population totale des villes composant un secteur ne doit pas dépasser la quantité gamma
# pour chaque secteur : Somme_i v_i * x_ij <= gamma
for j in range(k):
    pop_secteur = 0
    for i in range(n):
        pop_secteur += x[i,j] * Populations[i] 
    m.addConstr(pop_secteur <= gamma, "c%d" % (n+i))
    

# Resolution
m.optimize()
print("")
print("CONTEXTE DU PROBLEME:")
print("")
print("Soit un ensemble de ",n," villes situées sur le territoire de référence.")
print("")
print("Les villes en question sont :",Villes,".")
print("")
print("Elles ont respectivement pour nombre d'habitants", Populations,".")
print("")        
print("Les villes possédants un centre de soins spécialisé sont ",Unites,".")
print("")        
print('Solution optimale (Affichage de la matrice solution pour la définition des',k,'secteurs):')
print(x.X) # Affichage de la matrice x_ij solution pour la définition des k secteurs.
print("") 

# Explicité la matrice x

for col in range(k):
    print("La ville de ", Unites[col]," reçoit les habitants des villes de :")
    affichage = []
    for lig in range(n):
        if(x.X[lig,col] == 1):
            affichage += [Villes[lig]]
    print(affichage)
    print("")
    
print("")
print('Valeur de la fonction objectif :', m.objVal)