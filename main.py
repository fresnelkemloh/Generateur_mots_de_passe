#Fresnel foguimgang kemloh, 2440103, fresnelkemloh
import argparse
"""Configuration CLI"""
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
    return parser

def main():
    """Point d'entrée du mode CLI"""
    parser = configurer_cli()
    args = parser.parse_args()

    try:
        passwordgenerate = PasswordGenerator(longueur=args.length, avec_minuscules= not args.no_lower, avec_majuscules= not args.no_upper,avec_chiffres= not args.no_digits, avec_symboles= not args.no_symbols, valider=args.validate)
        print(passwordgenerate.generer_mot_de_passe())
    except ValueError as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    main()