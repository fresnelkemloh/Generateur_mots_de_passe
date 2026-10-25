import sys

from PySide6 import QtWidgets
from PySide6.QtCore import Signal

from app.core.storage import Coffre, Entree, FichierCoffreInvalideError

from app.ui.generator_ui import FenetreGenerator

class LigneListe(QtWidgets.QWidget):
    clic = Signal(int)
    THEME_COLOR = "background-color:#8cd98c"

    def __init__(self, index: int, entree: Entree, parent=None):
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
        return self._index

    def mettre_a_jour_affichage(self) -> None:
        if self._visible:
            self.label_mot_de_passe.setText(self._entree.password)
        else:
            self.label_mot_de_passe.setText("*" * len(self._entree.password))

    def marquer_selection(self, selectionnee: bool) -> None:
        if selectionnee:
            theme = self.THEME_COLOR
        else:
            theme = ""
        self.label_email.setStyleSheet(theme)
        self.label_mot_de_passe.setStyleSheet(theme)

    def mousePressEvent(self, event):
        self.clic.emit(self._index)
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        self._visible = not self._visible
        self.mettre_a_jour_affichage()
        super().mouseDoubleClickEvent(event)

class FenetreSetUpEntree(QtWidgets.QDialog):
    entree_validee = Signal(object)

    def __init__(self, parent=None, entree: Entree | None = None):
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
        dialogue = FenetreGenerator(self)
        dialogue.mot_de_passe_choisi.connect(self.champ_mot_de_passe.setText)
        dialogue.exec()

    def valider(self) -> None:
        try:
            entree = Entree(self.champ_email.text(), self.champ_mot_de_passe.text())
        except (TypeError, ValueError) as erreur:
            self.label_erreur.setText(str(erreur))
            return
        self.entree_validee.emit(entree)
        self.accept()

class MainFenetre(QtWidgets.QMainWindow):
    def __init__(self, coffre: Coffre):
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
        widget_central = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        haut_layout = QtWidgets.QHBoxLayout()
        self.bouton_trier = QtWidgets.QPushButton("Trier par e-mail")
        haut_layout.addWidget(self.bouton_trier)
        haut_layout.addStretch()
        layout.addLayout(haut_layout)

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

    def charger_coffre(self) -> None:
        try:
            self._coffre.charger()
        except FichierCoffreInvalideError as erreur:
            self._fichier_corrompu = True
            QtWidgets.QMessageBox.critical(self,
                "Fichier corrompu",
                f"{erreur}\n\nLe coffre démarre vide. Le fichier ne sera pas remplacé sans votre confirmation à la fermeture.")
        self.rafraichir_liste()

    def rafraichir_liste(self) -> None:
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

    def mettre_a_jour_boutons(self) -> None:
        une_selection = self._index_selectionne != -1
        self.bouton_modifier.setEnabled(une_selection)
        self.bouton_supprimer.setEnabled(une_selection)

    def selectionner(self, index: int) -> None:
        self._index_selectionne = index
        for ligne in self._lignes:
            ligne.marquer_selection(ligne.index == index)
        self.mettre_a_jour_boutons()

    def trier(self) -> None:
        self._coffre.trier_par_mail()
        self._index_selectionne = -1
        self.rafraichir_liste()

    def ajouter(self) -> None:
        dialogue = FenetreSetUpEntree(self)
        dialogue.entree_validee.connect(self.ajouter_entree)
        dialogue.exec()

    def ajouter_entree(self, entree: Entree) -> None:
        self._coffre.add_entree(entree)
        self._index_selectionne = len(self._coffre.entrees) - 1
        self.rafraichir_liste()

    def modifier(self) -> None:
        if self._index_selectionne == -1:
            return
        entree = self._coffre.entrees[self._index_selectionne]
        dialogue = FenetreSetUpEntree(self, entree)
        dialogue.entree_validee.connect(self.modifier_entree)
        dialogue.exec()

    def modifier_entree(self, entree: Entree) -> None:
        self._coffre.set_entree(self._index_selectionne, entree)
        self.rafraichir_liste()

    def supprimer(self) -> None:
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

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    fenetre = MainFenetre(Coffre("vault.json"))
    fenetre.show()
    sys.exit(app.exec())