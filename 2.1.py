# Projet MOGPL : Optimisation appliquée à la localisation d’unités de soins et à la prise en charge des patients

import csv
from gurobipy import *
import numpy as np

"""

# Paramètre à modifier pour effectuer les test

"""

# k : nombre d'unité spéciale défini par l'utilisateur
k = 5

# alpha : paramètre strictement positif valant 0.1 ou 0.2
alpha = 0.2

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

if alpha < 0:
    raise ValueError("Alpha doit être strictement positif ")
# --------------------------------------------------------------------------------------------------------------

"""

# Paramètres

"""

# n : nombre de villes situées sur le territoire de référence
n = len(Villes)

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

# --------------------------------------------------------------------------------------------------------------

"""

# Résolution du PL :

"""

m = Model("Unites_de_soin")

# declaration variables de decision

# x : matrice à 2 dimensions de valeurs 0 ou 1 tel quel x_ij = 1 si les patients de la ville i sont traités dans la ville j
#x = np.array([[m.addVar(vtype=GRB.BINARY) for ind in range(n)] for ind in range(n)])
x = m.addMVar((n, n), vtype=GRB.BINARY, name="x")

# Opt : liste de booléen qui indique à l'indice i que la i-ème ville possède une unité de soin
#Opt = [ m.addVar(vtype=GRB.BINARY) for ind in range(n) ]
Opt = m.addMVar(n, vtype=GRB.BINARY, name="Opt")

# Definition des contraintes

# une ville n’appartient qu’à un unique secteur 
# pour chaque ville : Somme_j x_ij = 1
for i in range(n):     
    m.addConstr(sum(x[i,:]) == 1, "c%d" % i)

# la population totale des villes composant un secteur ne doit pas dépasser la quantité gamma
# pour chaque secteur : Somme_i v_i * x_ij <= gamma
for j in range(n):
    pop_secteur = 0
    for i in range(n):
        pop_secteur += x[i,j] * Populations[i] 
    m.addConstr(pop_secteur <= gamma, "c%d" % (n+i))
    
# Si les patients d'une ville i se font traités dans la ville j, alors la ville j possède une unité de soin
# pour chaque secteur potentiel, on vérifie chaque ville : x_ij <= Opt_j
for j in range(n):
    for i in range(n):
         m.addConstr(x[i,j] <= Opt[j], "c%d" % (2*n + j*n+i))

# Il y a exactement k ville(s) possédant une unité de soin
# Somme_j Opt_j = k
m.addConstr(sum(Opt) == k, "c%d" % (2*n + n*n + 1))

# définition de l'objectif
obj = 0.0
for i in range(n):
    for j in range(n):
        obj += (d_ij[i][j] * Populations[i] * x[i,j])
obj /= pop_total
            
m.setObjective(obj, GRB.MINIMIZE)

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
print("Voici la matrice x_ij que l'on obtient:")
print(x.X)
print("")  

# J : indice des villes possédant une unité de soin
J = []

# On cherche les villes qui possède une unité de soin et on récupère leur indice
for j in range(n):
    for i in range(n):
        if(Opt[j].X == 1.0):
            J.append(j)
            break;

# Unites : villes possédant une unité spéciale de traitement des patients atteints par une forme sévère d’une nouvelle maladie
Unites = [Villes[ind] for ind in J]

print("On déduit de la matrice x_ij la localisation optimale des ",k,"secteurs :")
print(Unites) 
print("")      
print('Solution optimale (Affichage de la matrice solution pour la définition des',k,'secteurs):')
print("")

# res : matrice solution avec pour i les villes et j les unités de soins
res = np.zeros((n,k))

# Remplir la matrice res
for i in range(n):
    for j in range(k):    
        res[i][j] = x[i,J[j]].X  
        
print(res)
print("") 

# Explicité la matrice res
for col in range(k):
    print("La ville de ", Villes[J[col]]," reçoit les habitants des villes de :")
    affichage = []
    for lig in range(n):
        if(res[lig,col] == 1):
            affichage += [Villes[lig]]
    print(affichage)
    print("")
    
print('Valeur de la fonction objectif :', m.objVal)