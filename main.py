#Fresnel foguimgang kemloh, 2440103, fresnelkemloh
import argparse
import sys

from PySide6.QtWidgets import QApplication

from app.core.storage import Coffre
from app.ui.main_window import MainFenetre

"""Point d'entree du gestionnaire du mots de passe (Mode: cli et graphique)"""
from app.core.generator import PasswordGenerator

def configurer_cli() -> argparse.ArgumentParser:
    """Construit le parseur d'arguments de la ligne de commande"""
    parser = argparse.ArgumentParser(description="Genere mots de passe")
    parser.add_argument("--length",type=int,default=16,help="longueur mots de passe 16 par defaut")
    parser.add_argument("--no-lower",action="store_true", help="pas de lettre minuscules")
    parser.add_argument("--no-upper",action="store_true", help="pas de lettre majuscules")
    parser.add_argument("--no-digits",action="store_true", help="pas de chiffre")
    parser.add_argument("--no-symbols",action="store_true", help="pas de symboles")
    parser.add_argument("--validate",action="store_true", help="force un caractere de chaque type")
    parser.add_argument("--no-gui",action="store_true", help="Pour la generation de mots de passe sans l'interface")
    parser.add_argument("--vault_file", default="vault.json", help="Fichier json du coffre fort . Par defaut vault.json")
    return parser

def demarrer_cli(args) -> None:
    """génère un mot de passe avec les options reçues et l'affiche en mode CLI."""
    try:
        generateur = PasswordGenerator(
            longueur=args.length,
            avec_minuscules= not args.no_lower,
            avec_majuscules= not args.no_upper,
            avec_chiffres= not args.no_digits,
            avec_symboles= not args.no_symbols,
            valider=args.validate
        )
        print(generateur.generer_mot_de_passe())
    except ValueError as e:
        print(f"Erreur : {e}")

def demarrer_gui(args) -> None:
    """ouvre la fenêtre du coffre-fort avec le fichier choisi en mode graphique"""
    app = QApplication(sys.argv)
    fenetre = MainFenetre(Coffre(args.vault_file))
    fenetre.show()
    sys.exit(app.exec())

def main():
    """Lance le mode CLI ou le mode graphique"""
    parser = configurer_cli()
    args = parser.parse_args()

    if args.no_gui:
        demarrer_cli(args)
    else:
        demarrer_gui(args)

if __name__ == "__main__":
    main()