#importation des bibliotheques 
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


#mettre le fichier csv dans la variable my_file
my_file = "S05_pluie_7jours.csv"


# lit le CSV
pluie_df = pd.read_csv(my_file)

#affichage du dataframe
print(pluie_df)


#Tableau numpy des noms des 6 noms de communes
communes = pluie_df["commune"].to_numpy()

# affiche les noms des communes
print(communes)

# affiche la forme : (6,)
print(communes.shape)


# Tableau NumPy 6 × 7 des pluies (colonnes j1 à j7), en nombres décimaux  
# pluie = pluie_df[[f"j{i}" for  i  in  range  (1, 8)]].to_numpy().astype=float
pluie = pluie_df[[f"j{i}" for  i  in  range  (1, 8)]].to_numpy(dtype=float)

# affiche la matrice des pluies
print(pluie)

# affiche la forme : (6, 7)
print(pluie.shape)

# Trois contrôles :  forme, type, min
print("forme:",pluie.shape, "| type :", pluie.dtype, "| min :", pluie.min())

# Cumul naïf par commune.
print ("\nCumul naïf (mm):", dict( zip ( communes, pluie.sum(axis=1).tolist())))

#Masque bolean : True  où la station a enregistre le code (-999)
sentinelle = pluie == -999
#Nombre de valeurs sentinelles, dans quelles communes
print("Nombre de valeurs sentinelles par commune :", int(sentinelle.sum()), "->", communes[sentinelle.any(axis=1)])

#Remplacer ces valeurs par NaN (valeur manquante) au lieu de les additioner  # NaN est par defaut a "float".
pluie[sentinelle] = np.nan

# Controle 1: la forme est inchangée, pluviometrie  non negative.
# option advance  : assert pluie.shape == (6,7) and  np.nanmin(pluie) >=0
assert pluie.shape == (6,7)
assert np.nanmin(pluie) >=0

# affiche la matrice avec NaN à la place de -999
print(pluie)

# vérifie la forme
print(pluie.shape)

print("\n\n")

# Nombre de jours avec une mesure valide, par commune. "~" est le NON logique pour les tableaux booléens, il inverse le masque, donc les cases valides  deviennes "True"
jours_valides = (~np.isnan(pluie)).sum(axis=1) # entier de 0 à 7 par commune
print("Jours valides :", dict(zip(communes, jours_valides.tolist())))  # affiche les compteurs
print("\n\n")

#Cumul observe en ignorant les  NaN
cumul_observe= np.nansum(pluie, axis=1) # somme de chaque ligne sans les NaN
print("Cumul observé  (mm) en ignorant les NaN:", dict( zip ( communes, cumul_observe.tolist()))) # affiche les cumuls
print("\n\n")

# Cumul estimé sur 7 jours (hypothèse : jour manquant = moyenne des autres jours)
# moyenne des jours valides x 7 jours ; arrondi à 1 décimale avec .round()
cumul_estime = (cumul_observe / jours_valides * 7).round(1)  # mm estimés sur 7 jours
print("Cumul estimé 7 j (mm) (hypothèse : jour manquant = moyenne des autres):", dict(zip(communes, cumul_estime.tolist())))  # affiche les estimations
print("\n\n")

# Pluie maximale d'une seule journée, par commune
pluie_max = np.nanmax(pluie, axis=1)  # maximum de chaque ligne en ignorant les NaN
print("Pluie maximale d'une seule journée, par commune (mm):", dict(zip(communes, pluie_max.tolist())))  # affiche les maxima
print("\n\n")


# Part de menages vivant en zone inondable (0,1)
exposition = pluie_df["part_menages_zone_inondable"].to_numpy() # tableau des 6 parts
print("Part de menages vivant en zone inondable :", dict( zip ( communes, exposition.tolist()))) # affiche les parts
print("\n\n")


# Indice d'exposition = pluie estimée (mm) x part des ménages exposés
indice = (cumul_estime * exposition).round(1)  # indice arrondi à 1 décimale
print("Indice d'exposition :", dict(zip(communes, indice.tolist())))  # affiche les indices
print("\n\n")


parts = pluie / cumul_observe[:, np.newaxis]  # tableau 6x7 des parts journalières

# Part du 4e jour (indice 3, car Python compte à partir de 0) dans le cumul, en % (0 décimale)
part_jour4 = (parts[:, 3] * 100).round(0)  # colonne d'indice 3 x 100, arrondie à l'entier
print("Part du jour 4 (%):", dict(zip(communes, part_jour4.tolist())))  # affiche les pourcentages
print("\n\n")

i_gonaives = communes.tolist().index("Gonaïves")  # .index() retrouve la position de Gonaïves dans la liste
a_la_main = 12 + 18 + 44 + 96 + 72 + 31 + 20  # addition manuelle des 7 jours de Gonaïves (mm)
assert cumul_observe[i_gonaives] == a_la_main  # le cumul calculé par NumPy doit être identique (293 mm)
print("Contrôle 2 OK : Gonaïves =", a_la_main, "mm")  # confirme que le contrôle a réussi
print("\n\n")


# TABLE FINALE (TABLEAU A)
# Assembler la table finale à partir des tableaux calculés (indice déjà arrondi)
resultat = pd.DataFrame({
    "commune": communes,                      # nom de la commune
    "jours_valides": jours_valides,           # nombre de jours valides (entier 0 à 7)
    "cumul_observe_mm": cumul_observe,        # pluie mesurée sans les NaN (mm)
    "cumul_estime_7j_mm": cumul_estime,       # pluie estimée sur 7 jours (mm)
    "max_journalier_mm": pluie_max,           # pluie maximale en un jour (mm)
    "indice_exposition": indice,              # cumul estimé x part des ménages exposés
})

# Règle : vérification prioritaire si cumul estimé > 300 mm OU maximum journalier > 100 mm
resultat["verification_prioritaire"] = (resultat["cumul_estime_7j_mm"] > 300) | (resultat["max_journalier_mm"] > 100)  # True/False

# Trier de l'indice le plus élevé au plus faible et renuméroter les lignes de 0 à 5
resultat = resultat.sort_values("indice_exposition", ascending=False).reset_index(drop=True)  # tri décroissant

# Afficher la table finale
print("\n\t\t\t\t\t\tTABLEAU A - Table finale\n")  # titre du tableau A
print(resultat.to_string())  # affiche toute la table sans coupure

# TABLEAU B : PART DU JOUR 4
tableau_b = pd.DataFrame({"commune": communes, "part_jour_4 (%)": part_jour4})  # commune + pourcentage
print("\n\tTABLEAU B - Part du jour 4 dans le cumul (%)\n")  # titre du tableau B
print(tableau_b.to_string())  # affiche le tableau B