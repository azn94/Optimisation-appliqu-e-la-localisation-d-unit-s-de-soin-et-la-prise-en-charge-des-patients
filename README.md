# Optimisation-appliqu-e-la-localisation-d-unit-s-de-soin-et-la-prise-en-charge-des-patients

La lecture du csv est possible si le caractère délimitant est défini à ',' et non à ';'
Le fichier csv utilisé pour notre code est fourni dans le rendu.

1 - Répartition de patients dans les unités de soin :
fichier : 1.2.py
Pour tester le PL avec des villes différentes, il suffit de modifier la liste Unites en y insérant les villes 
dans lesquelles on souhaite placer un centre. On fait varier le paramètre alpha en modifiant directement sa valeur.
Tout le reste est automatiquement pris en charge et l'on récupère la composition des différents secteurs et la valeur 
de la fonction objective.

2- Localisation optimale des unités de soin :

fichier : 2.1.py
Il suffit d'instancier les valeurs souhaitées de k (nombre de centres souhaités) et de alpha dans les premières lignes et d'exécuter le script.
L'affichage retourné précise les k villes choisies comme centres et les secteurs associés.
Les commentaires explicitent chaque variable et chaque contrainte ainsi que la manière dont on récupère les résultats.

fichier : 2.2.py
Il suffit là aussi d'instancier le nombre de centres souhaité (variable k) et le paramètre alpha.
L'affichage des différents secteurs est explicite et la valeur à l'optimum retourne bien la distance max entre les habitants 
d'une ville et leur centre de soin.

3- Equilibrage des charges des unités de soin

fichier : 3.2.py
Il faut choisir les villes acceuillant les centres sur lesquels porte la demande en précisant leur indice dans la variable J.
La demande est quantifiée en précisant dans la liste P la demande relative à chaque centre  en faisant attention à ce que le total ne dépasse pas 500.
