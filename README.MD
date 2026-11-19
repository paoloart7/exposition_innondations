# Pluie – Matrice des précipitations et de l'exposition aux inondations

Devoir #3 – Module 2 – Scénario 5 (Logique de programmation, NumPy et simulation).

Une semaine de fortes pluies a touché six communes côtières (Gonaïves, Saint-Marc, Cabaret, Léogâne, Petit-Goâve, Jacmel). Ce programme calcule la pluie de chaque commune, son exposition aux inondations et la liste des communes à vérifier en priorité.

> Les données sont synthétiques (pédagogiques) : elles ne décrivent pas une situation réelle.

## Structure du projet

```
pluie/
├── pluie.py                                                         # programme complet, commenté ligne par ligne
├── raport
|        ├──RAPPORT À L’ÉQUIPE DE RÉDUCTION DES RISQUES.pdf          # le fichier word qui a les captures d'ecrans et rapport
├── Module_02_Logique_de_Programmation_et_NumPy_FR.ipynb             #Le notebook donné initialement par le professeur
├── S05_pluie_7jours.csv                                             # données : pluie (mm) par commune et par jour (j1 à j7)
└── README.md                       
```

## Prérequis

- Python 3
- Bibliothèques : pandas et numpy

```bash
pip install pandas numpy
```

## Lancer le programme

1. Ouvrir le dossier `pluie` dans VS Code (Fichier → Ouvrir le dossier).
2. Vérifier que `S05_pluie_7jours.csv` est dans le même dossier que `pluie.py`.
3. Lancer avec le bouton ▶ Run, ou dans un terminal :

```bash
python pluie.py
```

## Ce que fait le programme

1. Lit le CSV avec pandas et construit un tableau NumPy 6 × 7 (communes × jours).
2. Repère la valeur sentinelle **-999** (mesure absente de Petit-Goâve, jour 5) et la remplace par `NaN`.
3. Calcule, par commune :
   - le nombre de jours valides ;
   - le cumul observé (`np.nansum`) ;
   - le cumul estimé sur 7 jours (jour manquant = moyenne des autres jours) ;
   - la pluie maximale d'une journée (`np.nanmax`) ;
   - l'indice d'exposition = cumul estimé × part des ménages en zone inondable.
4. Calcule la part du jour 4 dans le cumul de chaque commune (broadcasting, en %).
5. Vérifie les résultats avec deux contrôles `assert` (pas de pluie négative, cumul de Gonaïves = 293 mm).
6. Produit le **tableau A** (table finale triée par indice décroissant) et le **tableau B** (part du jour 4).

Règle de vérification prioritaire : cumul estimé > 300 mm **ou** maximum journalier > 100 mm.

## Résultats (tableau A)

| commune | jours_valides | cumul_observe_mm | cumul_estime_7j_mm | max_journalier_mm | indice_exposition | verification_prioritaire |
|---|---|---|---|---|---|---|
| Cabaret | 7 | 335.0 | 335.0 | 110.0 | 137.4 | True |
| Petit-Goâve | 6 | 303.0 | 353.5 | 124.0 | 134.3 | True |
| Gonaïves | 7 | 293.0 | 293.0 | 96.0 | 102.6 | False |
| Léogâne | 7 | 218.0 | 218.0 | 75.0 | 65.4 | False |
| Saint-Marc | 7 | 263.0 | 263.0 | 88.0 | 57.9 | False |
| Jacmel | 7 | 250.0 | 250.0 | 81.0 | 45.0 | False |

## Corrections apportées au code vu en classe

- `jours_valides` : `.max()` remplacé par `.sum()` pour compter les jours valides.
- Colonne `"Part"` remplacée par `"part_menages_zone_inondable"`.
- `.astype=float` remplacé par `dtype=float`.
- Lignes `google.colab` supprimées et `display()` remplacé par `print()` (exécution hors Colab).

## Limites

- Le jour manquant de Petit-Goâve est estimé par la moyenne des 6 autres jours (50,5 mm), ce qui peut sous-estimer la pluie réelle.
- L'indice d'exposition est relatif : il compare les communes entre elles et n'a pas d'unité propre.

## Auteur

Karlsen Paul - FSGA (Génie Informatique)

@paoloart7
