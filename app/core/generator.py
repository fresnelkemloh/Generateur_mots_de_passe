class PasswordGenerator:
    MINISCULES= "abcdefghijklmnopqrstuvwxyz"
    MAJUSCULES = MINISCULES.upper()
    CHIFFRES = "0123456789"
    SYMBOLES = "!@#$%^&*()-_=+[]{};:,.?/"

    def __init__(self, longueur:int=16, avec_minuscules:bool = True, avec_majuscules:bool = True,avec_chiffres:bool = True, avec_symboles:bool = True, valider:bool = False):
        self.longueur = None
        self.avec_minuscules = None
        self.avec_majuscules = None
        self.avec_chiffres = None
        self.avec_symboles = None
        self.valider = None

        self.longueur = longueur
        self.avec_minuscules = avec_minuscules
        self.avec_majuscules = avec_majuscules
        self.avec_chiffres = avec_chiffres
        self.avec_symboles = avec_symboles
        self.valider = valider

    @property
    def longueur(self) -> int:
        return self.longueur
    @longueur.setter

    def longueur(self, valeur:int) -> None:
      if not isinstance(valeur, int) or isinstance(valeur, bool):
          raise TypeError("la longuer doit etre un entier")
      if valeur <= 0:
          raise ValueError("la longuer doit etre plus grand que 0")
      self.longueur = valeur

    @property
    def avec_minuscules(self) -> bool:
        return self.avec_minuscules
    @avec_minuscules.setter

    def avec_minuscules(self, valeur:bool) -> None:
        if not isinstance(valeur, bool):
            raise TypeError("avec-minuscules doit etre un bool")
        self.avec_minuscules = valeur

    @property
    def avec_majuscules(self) -> bool:
        return self.avec_majuscules
    @avec_majuscules.setter

    def avec_majuscules(self, valeur:bool) -> None:
        if not isinstance(valeur, bool):
            raise TypeError("avec-majuscules doit etre un bool")
        self.avec_majuscules = valeur

    @property
    def avec_chiffres(self) -> bool:
        return self.avec_chiffres
    @avec_chiffres.setter

    def avec_chiffres(self, valeur:bool) -> None:
        if not isinstance(valeur, bool):
            raise TypeError("avec-chiffres doit etre un bool")
        self.avec_chiffres = valeur

    @property
    def avec_symboles(self) -> bool:
        return self.avec_symboles
    @avec_symboles.setter

    def avec_symboles(self, valeur:bool) -> None:
        if not isinstance(valeur, bool):
            raise TypeError("avec-symboles doit etre un bool")
        self.avec_symboles = valeur

    @property
    def valider(self) -> bool:
        return self.valider
    @valider.setter

    def valider(self, valeur:bool) -> None:
        if not isinstance(valeur, bool):
            raise TypeError("valider doit etre un bool")
        self.valider = valeur