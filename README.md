# mi-temps

Simulateur de château d'eau un soir de finale.

Quand on s'appelle Doe, il suffit qu'un collègue ajoute « Chato » devant pour que tout le monde vous appelle château d'eau. Autant assumer, et en profiter pour vérifier une légende tenace : à la mi-temps d'un grand match, tout le monde tirerait la chasse en même temps.

## Lancer une simulation

```bash
python mi_temps.py
python mi_temps.py --prolongations
python mi_temps.py --cuve 400 --pompe 3
```

La première commande simule une soirée tendue avec un château d'eau sous-dimensionné, la deuxième ajoute les prolongations (en pire), et la troisième met un vrai château d'eau, beaucoup moins drôle. Toutes les options : `python mi_temps.py --help`

## Le modèle

- Pendant le jeu, personne ne quitte le canapé : la consommation chute.
- À chaque pause, 70 % des foyers se lèvent en même temps (chasse d'eau, mains, bouilloire) et vident la cuve en trois minutes.
- La pompe remplit tant que la cuve n'est pas pleine, à son rythme.
- La pression au robinet dépend de la hauteur d'eau : environ 1 bar tous les 10 mètres.

Spoiler : un vrai château d'eau encaisse très bien la mi-temps, c'est même exactement pour ça qu'on les construit. Les valeurs par défaut décrivent donc un château d'eau franchement sous-dimensionné, sinon il ne se passe rien.
