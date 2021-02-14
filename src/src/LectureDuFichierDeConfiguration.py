"""
    Module qui contient la classe LectureDuFichierDeConfiguration pour l'application des comptes
"""

__all__ = ["LectureDuFichierDeConfiguration"]

# ======================================================================================================================
# Import des librairies
# ======================================================================================================================

import os
import json
from typing import Optional, Dict


# ======================================================================================================================
# Définitions des classes
# ======================================================================================================================

class LectureDuFichierDeConfiguration(object):
    """
        Classe de lecture du contenu du fichier de configuration de l'application des comptes
    """
    
    def __init__(self, emplacement_absolu_du_fichier_de_configuration):
        """
            Constructeur de la classe
        """

        self._emplacement_absolu_du_fichier_de_configuration = emplacement_absolu_du_fichier_de_configuration
        self._contenu_du_fichier_de_configuration: Optional[Dict] = None

    # Accesseurs et mutateurs

    def get_emplacement_absolu_du_fichier_de_configuration(self):
        """
            Accesseur de l'attribut _emplacement_absolu_du_fichier_de_configuration
        """

        return self._emplacement_absolu_du_fichier_de_configuration

    def set_emplacement_absolu_du_fichier_de_configuration(self, valeur):
        """
            Accesseur de l'attribut _emplacement_absolu_du_fichier_de_configuration
        """

        self._emplacement_absolu_du_fichier_de_configuration = valeur

    def get_contenu_du_fichier_de_configuration(self):
        """
            Accesseur de l'attribut _contenu_du_fichier_de_configuration
        """

        return self._contenu_du_fichier_de_configuration

    def set_contenu_du_fichier_de_configuration(self, valeur):
        """
            Accesseur de l'attribut _contenu_du_fichier_de_configuration
        """

        self._contenu_du_fichier_de_configuration = valeur

    def lecture_du_fichier(self):
        """
            Méthode qui permet de récupérer les informations de configuration de l'appli
            Ces informations se trouvent dans le fichier Controleur.json
            Ce fichier doit se trouver au même emplacement que l'application
        """

        # On vérifie si le fichier de configuration existe dans le répertoire contenant l'application
        if not os.path.isfile(self._emplacement_absolu_du_fichier_de_configuration):
            fichier = os.path.basename(self._emplacement_absolu_du_fichier_de_configuration)
            dossier = os.path.dirname(self._emplacement_absolu_du_fichier_de_configuration)
            raise OSError(f"Le fichier de configuration '{fichier}' n'existe pas das le dossier '{dossier}'")

        # Lecture du fichier de configuration
        with open(self._emplacement_absolu_du_fichier_de_configuration, 'r') as fichier_de_configuration:
            # ATTENTION : il faut que le fichier JSON soit encodé en ANSI sinon impossible de le lire !
            # ==> vérifier si ce n'est pas plutôt un problème de conf
            self._contenu_du_fichier_de_configuration: Dict = json.load(fichier_de_configuration)
