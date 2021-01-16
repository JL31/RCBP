"""
    Module qui permet de lancer l'application des comptes
"""

# ======================================================================================================================
# Import des librairies
# ======================================================================================================================

from PyQt5 import QtWidgets
import sys
from src.src.controleur import Controleur


# ======================================================================================================================
# Utilisation
# ======================================================================================================================

if __name__ == "__main__":

    # définition de l'application
    app = QtWidgets.QApplication(sys.argv)

    # instanciation du controlleur
    controleur = Controleur(app)
    controleur.main()

    # lancement de l'application
    app.exec_()
