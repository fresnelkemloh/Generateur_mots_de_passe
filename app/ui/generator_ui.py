import sys

from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QSlider, QCheckBox, QLineEdit, \
    QApplication, QDialog

from app.core.generator import PasswordGenerator

class FenetreGenerator(QDialog):
    mot_de_passe_choisi = Signal(str)

    LONGUEUR_MIN = 5
    LONGUEUR_MAX = 32
    LONGUEUR_DEFAUT = 16

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Generateur de mot de passe")
        self.setGeometry(500, 150, 480, 500)

        self._mot_de_passe = ""
        self._visible = False

        self.init_ui()
        self.generer()

    def init_ui(self) -> None:
        layout = QVBoxLayout()

        layout.addChildWidget(QLabel("Longueur"))
        longueur_layout = QHBoxLayout()

        self.bouton_moins = QPushButton("-")
        self.curseur = QSlider(Qt.Orientation.Horizontal)
        self.curseur.setRange(self.LONGUEUR_MIN, self.LONGUEUR_MAX)
        self.curseur.setValue(self.LONGUEUR_DEFAUT)
        self.bouton_plus = QPushButton("+")
        self.label_longueur = QLabel(str(self.LONGUEUR_DEFAUT))

        longueur_layout.addWidget(self.bouton_moins)
        longueur_layout.addWidget(self.curseur)
        longueur_layout.addWidget(self.bouton_plus)
        longueur_layout.addWidget(self.label_longueur)
        layout.addLayout(longueur_layout)

        layout.addWidget(QLabel("Types de caractères"))
        self.case_minuscules = QCheckBox("Minuscules")
        self.case_majuscules = QCheckBox("Majuscules")
        self.case_chiffres = QCheckBox("Chiffres")
        self.case_symboles = QCheckBox("Symboles")
        self.case_valider = QCheckBox("Valider")

        self.case_minuscules.setChecked(True)
        self.case_majuscules.setChecked(True)
        self.case_chiffres.setChecked(True)
        self.case_symboles.setChecked(True)

        layout.addWidget(self.case_minuscules)
        layout.addWidget(self.case_majuscules)
        layout.addWidget(self.case_chiffres)
        layout.addWidget(self.case_symboles)
        layout.addWidget(self.case_valider)

        layout.addWidget(QLabel("Mot de passe"))
        mot_de_passe_layout = QHBoxLayout()

        self.champ_mot_de_passe = QLineEdit()
        self.champ_mot_de_passe.setReadOnly(True)
        self.champ_mot_de_passe.setStyleSheet("font-size: 19px;")
        self.bouton_afficher = QPushButton("Afficher")

        mot_de_passe_layout.addWidget(self.champ_mot_de_passe)
        mot_de_passe_layout.addWidget(self.bouton_afficher)
        layout.addLayout(mot_de_passe_layout)

        self.label_message = QLabel("")
        layout.addWidget(self.label_message)

        boutons_layout = QHBoxLayout()
        self.bouton_generer = QPushButton("Générer")
        self.bouton_copier = QPushButton("Copier")
        self.bouton_utiliser = QPushButton("Utiliser")
        self.bouton_fermer = QPushButton("Fermer")

        boutons_layout.addWidget(self.bouton_generer)
        boutons_layout.addWidget(self.bouton_copier)
        boutons_layout.addWidget(self.bouton_utiliser)
        boutons_layout.addWidget(self.bouton_fermer)
        layout.addLayout(boutons_layout)

        self.setLayout(layout)

        self.bouton_moins.clicked.connect(self.diminuer_longueur)
        self.bouton_plus.clicked.connect(self.augmenter_longueur)
        self.curseur.valueChanged.connect(self.changer_longueur)

        self.case_minuscules.stateChanged.connect(self.generer)
        self.case_majuscules.stateChanged.connect(self.generer)
        self.case_chiffres.stateChanged.connect(self.generer)
        self.case_symboles.stateChanged.connect(self.generer)
        self.case_valider.stateChanged.connect(self.generer)

        self.bouton_afficher.clicked.connect(self.basculer_affichage)
        self.bouton_generer.clicked.connect(self.generer)
        self.bouton_copier.clicked.connect(self.copier)
        self.bouton_utiliser.clicked.connect(self.utiliser)
        self.bouton_fermer.clicked.connect(self.close)

    @property
    def mot_de_passe(self) -> str:
        return self._mot_de_passe

    def diminuer_longueur(self) -> None:
        self.curseur.setValue(self.curseur.value() - 1)

    def augmenter_longueur(self) -> None:
        self.curseur.setValue(self.curseur.value() + 1)

    def changer_longueur(self, valeur: int) -> None:
        self.label_longueur.setText(str(valeur))
        self.generer()

    def generer(self) -> None:
        try:
            generateur = PasswordGenerator(
                longueur=self.curseur.value(),
                avec_minuscules=self.case_minuscules.isChecked(),
                avec_majuscules=self.case_majuscules.isChecked(),
                avec_chiffres=self.case_chiffres.isChecked(),
                avec_symboles=self.case_symboles.isChecked(),
                valider=self.case_valider.isChecked(),
            )
            self._mot_de_passe = generateur.generer_mot_de_passe()
            self.label_message.setText("")
        except ValueError as erreur:
            self._mot_de_passe = ""
            self.label_message.setText(f"Erreur : {erreur}")

        self.bouton_copier.setEnabled(self._mot_de_passe != "")
        self.bouton_utiliser.setEnabled(self._mot_de_passe != "")
        self.mettre_a_jour_affichage()

    def mettre_a_jour_affichage(self) -> None:
        if self._visible:
            self.champ_mot_de_passe.setText(self._mot_de_passe)
            self.bouton_afficher.setText("Masquer")
        else:
            self.champ_mot_de_passe.setText("*" * len(self._mot_de_passe))
            self.bouton_afficher.setText("Afficher")

    def basculer_affichage(self) -> None:
        self._visible = not self._visible
        self.mettre_a_jour_affichage()

    def copier(self) -> None:
        QApplication.clipboard().setText(self._mot_de_passe)
        self.label_message.setText("Mot de passe copié.")

    def utiliser(self) -> None:
        self.mot_de_passe_choisi.emit(self._mot_de_passe)
        self.accept()

if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = FenetreGenerator()
        window.show()
        sys.exit(app.exec())