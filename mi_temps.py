"""mi-temps : simulateur de château d'eau un soir de finale.

Pendant le jeu, personne ne quitte le canapé. À chaque pause,
tout le monde se lève en même temps. Le château d'eau tiendra-t-il ?
"""

import argparse

DESSIN = r"""
        _________
       /         \
      |  ~~~~~~~  |
      |___________|
          |   |
          |   |
          |   |
         /     \
"""

CONSO_PAR_FOYER = 0.0005
PART_QUI_SE_LEVE = 0.7
LITRES_PAR_FOYER = 10
DUREE_VAGUE = 3
HAUTEUR_TOUR = 25
HAUTEUR_CUVE = 6

PHASES_DE_JEU = ("Coup d'envoi", "Reprise", "Prolongations")


def programme(prolongations: bool) -> list[tuple[str, int]]:
    """Les phases de la soirée, avec leur durée en minutes."""
    phases = [("Coup d'envoi", 45), ("MI-TEMPS", 15), ("Reprise", 45)]
    if prolongations:
        phases += [("Pause avant prolongations", 5), ("Prolongations", 30)]
    phases.append(("Coup de sifflet final", 15))
    return phases


def consommation(foyers: int, phase: str, minute_de_phase: int) -> float:
    """m³ consommés par le village pendant une minute."""
    base = foyers * CONSO_PAR_FOYER
    if phase in PHASES_DE_JEU:
        return base * 0.4
    conso = base * 1.5
    if minute_de_phase < DUREE_VAGUE:
        conso += foyers * PART_QUI_SE_LEVE * LITRES_PAR_FOYER / 1000 / DUREE_VAGUE
    return conso


def pression(volume: float, cuve: float) -> float:
    """Environ 1 bar tous les 10 mètres de colonne d'eau."""
    if volume <= 0:
        return 0.0
    return (HAUTEUR_TOUR + HAUTEUR_CUVE * volume / cuve) / 10.2


def jauge(volume: float, cuve: float, largeur: int = 20) -> str:
    plein = round(largeur * volume / cuve)
    return "[" + "#" * plein + " " * (largeur - plein) + "]"


def simuler(foyers: int, cuve: float, pompe: float, niveau: float, prolongations: bool):
    volume = cuve * niveau / 100
    minimum = volume
    a_sec = None
    minute = 0

    print(DESSIN)
    print("Le château d'eau tiendra-t-il la finale ?\n")
    print(f"{'Min':>4}  {'Cuve':<22}  {'Niveau':>6}  {'Pression':>9}  Événement")

    for phase, duree in programme(prolongations):
        for t in range(duree):
            apport = pompe if volume < 0.95 * cuve else 0.0
            volume += apport - consommation(foyers, phase, t)
            volume = max(0.0, min(cuve, volume))
            minimum = min(minimum, volume)

            evenement = phase if t == 0 else ""
            if volume == 0 and a_sec is None:
                a_sec = minute
                evenement = "À SEC !"

            if evenement or minute % 5 == 0:
                print(
                    f"{minute:>4}  {jauge(volume, cuve)}  {100 * volume / cuve:>4.0f} %"
                    f"  {pression(volume, cuve):>5.1f} bar  {evenement}"
                )
            minute += 1

    return minimum / cuve, a_sec


def verdict(part_minimale: float, a_sec) -> str:
    if a_sec is not None:
        return (
            f"À sec à la minute {a_sec}. Le village a raté la fin du match "
            "pour aller chercher des packs d'eau."
        )
    if part_minimale < 0.2:
        return "Douches tièdes et filets d'eau : le fontainier n'a pas vu la fin du match."
    if part_minimale < 0.5:
        return "Ça a tangué à la mi-temps, mais tout le monde a pu tirer la chasse."
    return "Le château d'eau a à peine remarqué qu'il y avait un match."


def main() -> None:
    parser = argparse.ArgumentParser(description="Le château d'eau tiendra-t-il la finale ?")
    parser.add_argument("--foyers", type=int, default=1500,
                        help="foyers devant le match (défaut : 1500)")
    parser.add_argument("--cuve", type=float, default=60,
                        help="capacité de la cuve en m³ (défaut : 60)")
    parser.add_argument("--pompe", type=float, default=0.4,
                        help="débit de la pompe en m³/min (défaut : 0,4)")
    parser.add_argument("--niveau", type=float, default=60,
                        help="remplissage au coup d'envoi, en %% (défaut : 60)")
    parser.add_argument("--prolongations", action="store_true",
                        help="ajoute les prolongations, et donc une pause de plus")
    args = parser.parse_args()

    if args.cuve <= 0:
        parser.error("la cuve doit avoir une capacité positive")
    if args.foyers < 0 or args.pompe < 0:
        parser.error("ni les foyers ni le débit de la pompe ne peuvent être négatifs")
    if not 0 <= args.niveau <= 100:
        parser.error("le niveau de départ est un pourcentage, entre 0 et 100")

    part_minimale, a_sec = simuler(args.foyers, args.cuve, args.pompe,
                                   args.niveau, args.prolongations)
    print()
    print(verdict(part_minimale, a_sec))


if __name__ == "__main__":
    main()
