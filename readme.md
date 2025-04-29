# Boids Typography Project

Une simulation interactive de boids formant des lettres en utilisant Python et Pygame.

## Description

Ce projet combine l'algorithme des boids avec la typographie pour créer une visualisation dynamique où des agents autonomes (boids) se déplacent collectivement pour former des lettres. Le système utilise trois groupes de boids avec des couleurs différentes qui s'organisent pour former des lettres superposées.

## Fonctionnalités

- Simulation de boids avec règles de séparation, alignement et cohésion
- Rendu de lettres vectorielles personnalisées
- Trois groupes de boids avec des couleurs distinctes
- Animation fluide avec Pygame
- Effet de profondeur avec superposition des lettres

## Prérequis

- Python 3.x
- Pygame
- NumPy

## Installation

1. Clonez le dépôt :

```bash
git clone https://github.com/votre-username/boidsProject.git
cd boidsProject
```

2. Installez les dépendances :

```bash
pip install -r requirements.txt
```

## Utilisation

Lancez le programme principal :

```bash
python app.py
```

## Structure du Projet

- `app.py` - Programme principal et boucle de jeu
- `boid.py` - Classe Boid et logique de mouvement
- `letter.py` - Classe Letter pour la génération des formes de lettres
