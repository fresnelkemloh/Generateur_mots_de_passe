#Fresnel foguimgang kemloh, 2440103, fresnelkemloh
import json
"""Gestion du coffre-fort"""

class FichierCoffreInvalideError(ValueError):
    """Exception levée lorsque le fichier du coffre est corrompu"""

    def __init__(self,chemin:str, message:str):
        self.chemin = chemin
        super().__init__(f"fichier {chemin} invalide {message}")

class Entree:
    """Un e-mail et un mot de passe conservé dans le coffre"""

    def __init__(self, email:str, password:str):
        self._email = None
        self._password = None

        self.email = email
        self.password = password

    @property
    def email(self) -> str:
        """Retourne l'adresse e-mail"""
        return self._email

    @email.setter
    def email(self, valeur:str) -> None:
        """Définit l'e-mail"""
        if not isinstance(valeur, str):
            raise TypeError("L'emal doit etre une chaine de caractere")
        veleur = valeur.strip()
        if len(veleur) == 0:
            raise ValueError("L'email ne doit pas etre vide")
        if "@" not in veleur:
            raise ValueError("L'email doit avoir un @")
        self._email = veleur

    @property
    def password(self) -> str:
        """Retourne le mot de passe."""
        return self._password

    @password.setter
    def password(self, valeur:str) -> None:
        """Définit le mot de passe"""
        if not isinstance(valeur, str):
            raise TypeError("Le mots de passe doit etre une chaine de caractere")
        if len(valeur) == 0:
            raise ValueError("Le mots de passe ne doit pas etre vide")
        self._password = valeur

    def to_dict(self) -> dict[str, str]:
        """Convertit l'entrée en dictionnaire"""
        return {"email": self.email, "password": self.password}

    @classmethod
    def from_dict(cls, data:dict[str, str]):
        """Crée une entrée à partir d'un dictionnaire lu dans le fichier JSON"""
        return cls(data["email"], data["password"])

    def __repr__(self) -> str:
        """Représentation de l'entrée"""
        return f"Entree(email='{self.email}', mot_de_passe='****')"

class Coffre:
    """Collection d'entrées, chargée depuis et sauvegardée dans un fichier JSON"""
    def __init__(self, chemin_du_fichier:str = "vault.json"):
        self._chemin_du_fichier = chemin_du_fichier
        self._entrees = []

    @property
    def chemin_du_fichier(self) -> str:
        """Retourne le chemin du fichier JSON utilisé"""
        return self._chemin_du_fichier

    @property
    def entrees(self) -> list[Entree]:
        """Retourne une copie de la liste des entrées."""
        return list(self._entrees)

    def _verifier_index(self, index: int) -> None:
        """vérifie que l'index correspond à une entrée existante"""
        if index < 0 or index >= len(self._entrees):
            raise ValueError(f"pas d'entree a {index}")

    def add_entree(self, entree:Entree) -> None:
        """Ajoute une entrée à la fin du coffre"""
        self._entrees.append(entree)

    def remove_entree(self, index: int) -> None:
        """Retire l'entrée située à la position donnée"""
        self._verifier_index(index)
        self._entrees.remove(self._entrees[index])

    def set_entree(self, index: int,entree:Entree) -> None:
        """Remplace l'entrée située à la position donnée"""
        self._verifier_index(index)
        self._entrees[index] = entree

    def trier_par_mail(self) -> None:
        """Trie les entrées par e-mail, en ordre alphabétique"""
        self._entrees = sorted(self._entrees, key=lambda entree: entree.email.lower())

    def charger(self) -> None:
        """Charge les entrées depuis le fichier JSON."""
        try:
            with open(self._chemin_du_fichier, "r", encoding="utf-8") as fichier:
                data = json.load(fichier)
        except FileNotFoundError:
            self._entrees = []
            return
        except json.JSONDecodeError as erreur:
            raise FichierCoffreInvalideError(self.chemin_du_fichier, f"json non lisible{erreur}")
        if not isinstance(data, list):
            raise FichierCoffreInvalideError(self.chemin_du_fichier, f"une liste d'entree devrai y etre")
        entrees_lu = []
        for entree in data:
            if not isinstance(entree, dict):
                raise FichierCoffreInvalideError(self.chemin_du_fichier, "chaque fichier doit etre un object")
            if "email" not in entree or "password" not in entree:
                raise FichierCoffreInvalideError(self.chemin_du_fichier, "le champs email ou password est vide")
            try:
                entrees_lu.append(Entree.from_dict(entree))
            except (ValueError, TypeError) as erreur:
                raise FichierCoffreInvalideError(self.chemin_du_fichier, str(erreur))
        self._entrees = entrees_lu

    def sauvegarder(self) -> None:
        """Sauvegarde les entrées dans le fichier JSON"""
        data = [entree.to_dict() for entree in self._entrees]
        with open(self._chemin_du_fichier, "w", encoding="utf-8") as fichier:
            json.dump(data, fichier, ensure_ascii=False, indent=4)



