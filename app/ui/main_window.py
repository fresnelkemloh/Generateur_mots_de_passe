#Fresnel foguimgang kemloh, 2440103, fresnelkemloh

import sys

from PySide6 import QtWidgets
from PySide6.QtCore import Signal

from app.core.storage import Coffre, Entree, FichierCoffreInvalideError

from app.ui.generator_ui import FenetreGenerator

"""Fenêtre du coffre-fort"""

class LigneListe(QtWidgets.QWidget):
    """"Une ligne de la liste ou l'e-mail est à gauche et le mot de passe à droite."""
    clic = Signal(int)
    THEME_COLOR = "background-color:#8cd98c"

    def __init__(self, index: int, entree: Entree, parent=None):
        """Crée la ligne pour une entrée du coffre."""
        super().__init__(parent)
        self._index = index
        self._entree = entree
        self._visible = False

        layout = QtWidgets.QHBoxLayout()
        self.label_email = QtWidgets.QLabel(entree.email)
        self.label_mot_de_passe = QtWidgets.QLabel()
        layout.addWidget(self.label_email)
        layout.addWidget(self.label_mot_de_passe)
        self.setLayout(layout)
        self.mettre_a_jour_affichage()

    @property
    def index(self) -> int:
        """Retourne la position de l'entrée dans le coffre."""
        return self._index

    def mettre_a_jour_affichage(self) -> None:
        """Affiche le mot de passe de facon lisible ou en astérisques selon l'état actuel."""
        if self._visible:
            self.label_mot_de_passe.setText(self._entree.password)
        else:
            self.label_mot_de_passe.setText("*" * len(self._entree.password))

    def marquer_selection(self, selectionnee: bool) -> None:
        """Colore la ligne si elle est sélectionnée sinon retire la couleur."""
        if selectionnee:
            theme = self.THEME_COLOR
        else:
            theme = ""
        self.label_email.setStyleSheet(theme)
        self.label_mot_de_passe.setStyleSheet(theme)

    def mousePressEvent(self, event):
        """Emet le signal du clic pour sélectionner la ligne avec un clic."""
        self.clic.emit(self._index)
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        """affiche ou masque le mot de passe de cette ligne avec un double clic."""
        self._visible = not self._visible
        self.mettre_a_jour_affichage()
        super().mouseDoubleClickEvent(event)

    @property
    def email(self) -> str:
        """Retourne l'e-mail de la ligne"""
        return self._entree.email

class FenetreSetUpEntree(QtWidgets.QDialog):
    """Fenetre pour ajouter une entrée ou modifier une entrée existante"""
    entree_validee = Signal(object)

    def __init__(self, parent=None, entree: Entree | None = None):
        """Creer la fenetre"""
        super().__init__(parent)
        if entree is not None:
            self.setWindowTitle("Modifier l'entrée")
        else:
            self.setWindowTitle("Ajouter une entrée")
        self.setGeometry(250, 250, 420, 160)

        layout = QtWidgets.QVBoxLayout()

        formulaire = QtWidgets.QFormLayout()
        self.champ_email = QtWidgets.QLineEdit()
        self.champ_mot_de_passe = QtWidgets.QLineEdit()
        formulaire.addRow("E-mail :", self.champ_email)
        formulaire.addRow("Mot de passe :", self.champ_mot_de_passe)

        generer_layout = QtWidgets.QHBoxLayout()
        self.bouton_generer = QtWidgets.QPushButton("Générer")
        generer_layout.addStretch()
        generer_layout.addWidget(self.bouton_generer)
        formulaire.addRow(generer_layout)
        layout.addLayout(formulaire)

        self.label_indicateur_force= QtWidgets.QLabel("")
        layout.addWidget(self.label_indicateur_force)
        self.champ_mot_de_passe.textChanged.connect(self.mettre_a_jour_force)

        if entree is not None:
            self.champ_email.setText(entree.email)
            self.champ_mot_de_passe.setText(entree.password)

        self.label_erreur = QtWidgets.QLabel("")
        self.label_erreur.setStyleSheet("color: red")
        layout.addWidget(self.label_erreur)

        boutons_layout = QtWidgets.QHBoxLayout()
        self.bouton_ok = QtWidgets.QPushButton("OK")
        self.bouton_annuler = QtWidgets.QPushButton("Annuler")
        boutons_layout.addWidget(self.bouton_ok)
        boutons_layout.addWidget(self.bouton_annuler)
        layout.addLayout(boutons_layout)

        self.setLayout(layout)

        self.bouton_generer.clicked.connect(self.ouvrir_generateur)
        self.bouton_ok.clicked.connect(self.valider)
        self.bouton_annuler.clicked.connect(self.reject)

    def ouvrir_generateur(self) -> None:
        """ouvre le générateur"""
        dialogue = FenetreGenerator(self)
        dialogue.mot_de_passe_choisi.connect(self.champ_mot_de_passe.setText)
        dialogue.exec()

    def valider(self) -> None:
        """crée l'entrée, l'envoie puis ferme la fenetre"""
        try:
            entree = Entree(self.champ_email.text(), self.champ_mot_de_passe.text())
        except (TypeError, ValueError) as erreur:
            self.label_erreur.setText(str(erreur))
            return
        self.entree_validee.emit(entree)
        self.accept()

    def mettre_a_jour_force(self, texte: str) -> None:
        """Affiche la force du mot de passe en couleur, selon sa longueur."""
        if len(texte) == 0:
            self.label_indicateur_force.setText("")
        elif len(texte) < 8:
            self.label_indicateur_force.setText("Le mot de passe est faible")
            self.label_indicateur_force.setStyleSheet("color: red")
        elif len(texte) < 12:
            self.label_indicateur_force.setText("Le mot de passe est moyen")
            self.label_indicateur_force.setStyleSheet("color: orange")
        else:
            self.label_indicateur_force.setText("Le mot de passe est fort")
            self.label_indicateur_force.setStyleSheet("color: green")

class MainFenetre(QtWidgets.QMainWindow):
    """Fenêtre principale du coffre-fort."""
    def __init__(self, coffre: Coffre):
        """Crée la fenêtre et charge le coffre depuis son fichier JSON"""
        super().__init__()
        self._coffre = coffre
        self._lignes = []
        self._index_selectionne = -1
        self._fichier_corrompu = False

        self.setWindowTitle(f"Coffre-fort")
        self.setGeometry(500, 150, 480, 500)

        self.init_ui()
        self.charger_coffre()

    def init_ui(self) -> None:
        """Construit les widgets, les layouts et les connexions des signaux."""
        widget_central = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        haut_layout = QtWidgets.QHBoxLayout()
        self.bouton_trier = QtWidgets.QPushButton("Trier par e-mail")
        self.champ_filtrage = QtWidgets.QLineEdit()
        self.champ_filtrage.setPlaceholderText("Filtrer par e-mail")
        haut_layout.addWidget(self.bouton_trier)
        haut_layout.addWidget(self.champ_filtrage)
        haut_layout.addStretch()
        layout.addLayout(haut_layout)

        self.label_resultats = QtWidgets.QLabel("")
        layout.addWidget(self.label_resultats)

        layout.addWidget(QtWidgets.QLabel())

        self.zone_defilante = QtWidgets.QScrollArea()
        self.zone_defilante.setWidgetResizable(True)
        layout.addWidget(self.zone_defilante)

        boutons_layout = QtWidgets.QHBoxLayout()
        self.bouton_ajouter = QtWidgets.QPushButton("Ajouter")
        self.bouton_modifier = QtWidgets.QPushButton("Modifier")
        self.bouton_supprimer = QtWidgets.QPushButton("Supprimer")
        self.bouton_supprimer.setStyleSheet("background-color: #ffe6e6")
        boutons_layout.addWidget(self.bouton_ajouter)
        boutons_layout.addWidget(self.bouton_modifier)
        boutons_layout.addWidget(self.bouton_supprimer)
        layout.addLayout(boutons_layout)

        widget_central.setLayout(layout)
        self.setCentralWidget(widget_central)

        self.bouton_trier.clicked.connect(self.trier)
        self.bouton_ajouter.clicked.connect(self.ajouter)
        self.bouton_modifier.clicked.connect(self.modifier)
        self.bouton_supprimer.clicked.connect(self.supprimer)
        self.champ_filtrage.textChanged.connect(self.filtrer)

    def charger_coffre(self) -> None:
        """Charge le fichier JSON ; affiche une erreur s'il est corrompu."""
        try:
            self._coffre.charger()
        except FichierCoffreInvalideError as erreur:
            self._fichier_corrompu = True
            QtWidgets.QMessageBox.critical(self,
                "Fichier corrompu",
                f"{erreur}\n\nLe coffre démarre vide. Le fichier ne sera pas remplacé sans votre confirmation à la fermeture.")
        self.rafraichir_liste()

    def rafraichir_liste(self) -> None:
        """Reconstruit la liste défilante à partir des entrées du coffre, puis applique le filtre."""
        conteneur = QtWidgets.QWidget()
        liste_layout = QtWidgets.QVBoxLayout()
        self._lignes = []

        entrees = self._coffre.entrees
        if len(entrees) == 0:
            liste_layout.addWidget(QtWidgets.QLabel("Aucune entrée. Cliquez sur Ajouter."))

        for index in range(len(entrees)):
            ligne = LigneListe(index, entrees[index])
            ligne.clic.connect(self.selectionner)
            ligne.marquer_selection(index == self._index_selectionne)
            liste_layout.addWidget(ligne)
            self._lignes.append(ligne)

        liste_layout.addStretch()
        conteneur.setLayout(liste_layout)
        self.zone_defilante.setWidget(conteneur)

        self.mettre_a_jour_boutons()
        self.filtrer()


    def mettre_a_jour_boutons(self) -> None:
        """Active Modifier et Supprimer seulement si une ligne est sélectionnée."""
        une_selection = self._index_selectionne != -1
        self.bouton_modifier.setEnabled(une_selection)
        self.bouton_supprimer.setEnabled(une_selection)

    def selectionner(self, index: int) -> None:
        """Mémorise la ligne cliquée et met à jour les couleurs."""
        self._index_selectionne = index
        for ligne in self._lignes:
            ligne.marquer_selection(ligne.index == index)
        self.mettre_a_jour_boutons()

    def trier(self) -> None:
        """trie le coffre par e-mail en ordre alphabetique"""
        self._coffre.trier_par_mail()
        self._index_selectionne = -1
        self.rafraichir_liste()

    def ajouter(self) -> None:
        """ouvre le dialogue d'ajout."""
        dialogue = FenetreSetUpEntree(self)
        dialogue.entree_validee.connect(self.ajouter_entree)
        dialogue.exec()

    def ajouter_entree(self, entree: Entree) -> None:
        """Reçoit la nouvelle entrée du dialogue et l'ajoute au coffre"""
        self._coffre.add_entree(entree)
        self._index_selectionne = len(self._coffre.entrees) - 1
        self.rafraichir_liste()

    def modifier(self) -> None:
        """ ouvre le dialogue pré-rempli avec l'entrée sélectionnée."""
        if self._index_selectionne == -1:
            return
        entree = self._coffre.entrees[self._index_selectionne]
        dialogue = FenetreSetUpEntree(self, entree)
        dialogue.entree_validee.connect(self.modifier_entree)
        dialogue.exec()

    def modifier_entree(self, entree: Entree) -> None:
        """Reçoit l'entrée modifiée et remplace l'ancienne dans le coffre."""
        self._coffre.set_entree(self._index_selectionne, entree)
        self.rafraichir_liste()

    def supprimer(self) -> None:
        """Supprime l'entrée sélectionnée après confirmation."""
        if self._index_selectionne == -1:
            return
        entree = self._coffre.entrees[self._index_selectionne]
        reponse = QtWidgets.QMessageBox.question(self,
            "Supprimer l'entrée",
            f"Voulez-vous vraiment supprimer l'entrée ( {entree.email} ) ?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,QtWidgets.QMessageBox.StandardButton.No)
        if reponse == QtWidgets.QMessageBox.StandardButton.Yes:
            self._coffre.remove_entree(self._index_selectionne)
            self._index_selectionne = -1
            self.rafraichir_liste()

    def closeEvent(self, event):
        """sauvegarde le coffre dans le fichier JSON a la fermeture."""
        if self._fichier_corrompu:
            reponse = QtWidgets.QMessageBox.question(self,
                "Remplacer le fichier ?",
                "Le fichier du coffre était corrompu au démarrage.\n"
                "Voulez-vous le remplacer par les entrées actuelles ?",
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
                QtWidgets.QMessageBox.StandardButton.No
            )
            if reponse == QtWidgets.QMessageBox.StandardButton.No:
                event.accept()
                return
        try:
            self._coffre.sauvegarder()
            event.accept()
        except Exception as erreur:
            reponse = QtWidgets.QMessageBox.question(
                self,
                "Erreur de sauvegarde",
                f"Impossible d'enregistrer le coffre :\n{erreur}\n\nQuitter quand même ?",
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
                QtWidgets.QMessageBox.StandardButton.No
            )
            if reponse == QtWidgets.QMessageBox.StandardButton.Yes:
                event.accept()
            else:
                event.ignore()
    def filtrer(self) -> None:
        """Masque les lignes dont l'e-mail ne contient pas le texte du filtre"""
        texte = self.champ_filtrage.text().strip().lower()
        nombre_visibles = 0
        for ligne in self._lignes:
            visible = texte in ligne.email.lower()
            ligne.setHidden(not visible)
            if visible:
                nombre_visibles += 1
        if texte == "":
            self.label_resultats.setText("")
        else:
            self.label_resultats.setText(f"{nombre_visibles} résultats pour {texte}")

        if self._index_selectionne != -1:
            email_selectionne = self._lignes[self._index_selectionne].email.lower()
            if texte not in email_selectionne:
                self.selectionner(-1)

if __name__ == "__main__":
    #test de la fenetre
    app = QtWidgets.QApplication(sys.argv)
    fenetre = MainFenetre(Coffre("vault.json"))
    fenetre.show()
    sys.exit(app.exec())