#Fresnel foguimgang kemloh, 2440103, fresnelkemloh
from random import randint
""" Logique de generation de mots de passe """

class PasswordGenerator:
    MINUSCULES= "abcdefghijklmnopqrstuvwxyz"
    MAJUSCULES = MINUSCULES.upper()
    CHIFFRES = "0123456789"
    SYMBOLES = "!@#$%^&*()-_=+[]{};:,.?/"

    def __init__(self, longueur:int=16, avec_minuscules:bool = True, avec_majuscules:bool = True,avec_chiffres:bool = True, avec_symboles:bool = True, valider:bool = False):
        self._longueur = None
        self._avec_minuscules = None
        self._avec_majuscules = None
        self._avec_chiffres = None
        self._avec_symboles = None
        self._valider = None

        self.longueur = longueur
        self.avec_minuscules = avec_minuscules
        self.avec_majuscules = avec_majuscules
        self.avec_chiffres = avec_chiffres
        self.avec_symboles = avec_symboles
        self.valider = valider

    @property
    def longueur(self) -> int:
        """Retourne la longueur du mots de passe"""
        return self._longueur
    @longueur.setter

    def longueur(self, valeur:int) -> None:
        # Defini la longueur du mots de passe , entier > 0
      if not isinstance(valeur, int) or isinstance(valeur, bool):
          raise TypeError("la longuer doit etre un entier")
      if valeur <= 0:
          raise ValueError("la longuer doit etre plus grand que 0")
      self._longueur = valeur

    @property
    def avec_minuscules(self) -> bool:
        """Indique si les minuscules sont inscluses"""
        return self._avec_minuscules
    @avec_minuscules.setter

    def avec_minuscules(self, valeur:bool) -> None:
        if not isinstance(valeur, bool):
            raise TypeError("avec-minuscules doit etre un bool")
        self._avec_minuscules = valeur

    @property
    def avec_majuscules(self) -> bool:
        """Indique si les majuscules sont inscluses"""
        return self._avec_majuscules
    @avec_majuscules.setter

    def avec_majuscules(self, valeur:bool) -> None:
        if not isinstance(valeur, bool):
            raise TypeError("avec-majuscules doit etre un bool")
        self._avec_majuscules = valeur

    @property
    def avec_chiffres(self) -> bool:
        """Indique si les chiffres sont insclus"""
        return self._avec_chiffres
    @avec_chiffres.setter

    def avec_chiffres(self, valeur:bool) -> None:
        if not isinstance(valeur, bool):
            raise TypeError("avec-chiffres doit etre un bool")
        self._avec_chiffres = valeur

    @property
    def avec_symboles(self) -> bool:
        """Indique si les symboles sont insclus"""
        return self._avec_symboles
    @avec_symboles.setter

    def avec_symboles(self, valeur:bool) -> None:
        if not isinstance(valeur, bool):
            raise TypeError("avec-symboles doit etre un bool")
        self._avec_symboles = valeur

    @property
    def valider(self) -> bool:
        """Indique si on force au moins un caractère de chaque type sélectionné."""
        return self._valider
    @valider.setter

    def valider(self, valeur:bool) -> None:
        if not isinstance(valeur, bool):
            raise TypeError("valider doit etre un bool")
        self._valider = valeur

    def _ensemble_caractere(self) -> list[str]:
        """retourne la liste des ensembles de caractères sélectionnés."""
        ensemble_caractere = []
        if self.avec_minuscules:
            ensemble_caractere.append(self.MINUSCULES)
        if self.avec_majuscules:
            ensemble_caractere.append(self.MAJUSCULES)
        if self.avec_chiffres:
            ensemble_caractere.append(self.CHIFFRES)
        if self.avec_symboles:
            ensemble_caractere.append(self.SYMBOLES)
        return ensemble_caractere

    def _prendre_caractere(self, caractere:str) -> str:
        """retourne un caractère au hasard dans la chaîne reçue."""
        return caractere[randint(0,len(caractere)-1)]

    def _faire_mot_de_passe(self, tout_caractere:str) -> str:
        """construit un mot de passe aléatoire en fonction de la longueur"""
        return  "".join([self._prendre_caractere(tout_caractere)for _ in range(self.longueur)])

    def _tous_les_types(self,mot_de_passe:str, ensembles: list[str]) -> bool:
        """vérifie qu'il y a au moins un caractère de chaque ensemble."""
        for ensemble in ensembles:
            trouver = False
            for caractere in mot_de_passe:
                if caractere in ensemble:
                    trouver = True
            if not trouver:
                    return False
        return True

    def generer_mot_de_passe(self) -> str:
        """Génère un mot de passe en fonction des parametre"""
        ensembles = self._ensemble_caractere()
        if len(ensembles) == 0:
            raise ValueError("Au moins un type de caractere doit etre selectionne")
        if self.valider and self.longueur < len(ensembles) :
            raise ValueError(f"La longueur ({self.longueur}) est trop courte pour avoir un caractere de chaque type.")
        tout_caractere = "".join(ensembles)
        mot_de_passe = self._faire_mot_de_passe(tout_caractere)
        while self.valider and not self._tous_les_types(mot_de_passe, ensembles):
            mot_de_passe = self._faire_mot_de_passe(tout_caractere)
        return mot_de_passe

    def __repr__(self) -> str:
        return ( f"PasswordGenerator(longueur={self.longueur},"
                 f"avec_minuscules={self.avec_minuscules},"
                 f"avec_majuscules={self.avec_majuscules},"
                 f"avec_chiffres={self.avec_chiffres},"
                 f"avec_symboles={self.avec_symboles}, valider={self.valider})")