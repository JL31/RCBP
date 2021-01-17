"""
    Module qui contient les classes de sous-classement pour les QValidator pour l'application des comptes
"""

__all__ = ["SCQDoubleValidation",
           "SCItemDelegateTVComptes",
           "SCItemDelegateTVBalance"]

# ======================================================================================================================
# Import des librairies
# ======================================================================================================================

# Import des librairies graphiques
from PyQt5 import QtGui, QtCore, QtWidgets


# ======================================================================================================================
# Définitions des classes
# ======================================================================================================================

class SCQRegExpValidator(QtGui.QRegExpValidator):
    """
        Classe qui permet de sous-classer la classe QRegExpValidator
    """

    def __init__(self, parent=None):
        """
            Constructeur de la classe
        """

        super(SCQRegExpValidator, self).__init__(parent)

    def validate(self, ch, pos):
        """
            Méthode qui retourne la validation à chaque nouveau caractère
        """

        # on vérifie que la chaîne de caractère n'est pas vide
        if ch not in ['']:

            # on vérifie le jour indiqué
            if pos == 2:

                # si le jour indiqué est supérieur à 31 on retourne une entrée invalide
                # (le format doit être tel que spécifié ici)
                if int(ch) > 31:

                    return QtGui.QValidator.Invalid, pos

            # on vérifie le mois indiqué
            elif pos == 5:

                # on extrait de la chaîne de caractère actuelle la partie qui correspond au mois
                ch_extrait = ch.split("/")[1]

                # si le mois indiqué est supérieur à 12 on retourne une entrée invalide
                # (le format doit être tel que spécifié ici)
                if int(ch_extrait) > 12:

                    return QtGui.QValidator.Invalid, pos

        return QtGui.QRegExpValidator.validate(self, ch, pos)
        

class SCQDoubleValidation(QtGui.QDoubleValidator):
    """
        Classe qui permet de sous-classer la classe QDoubleValidator
    """

    def __init__(self, borne_inferieure, borne_superieure, parent=None):
        """
            Constructeur de la classe
        """

        super(SCQDoubleValidation, self).__init__(parent)
        self._borne_inferieure = borne_inferieure
        self._borne_superieure = borne_superieure

    def validate(self, ch, pos):
        """
            Méthode qui retourne la validation à chaque nouveau caractère
        """

        # on vérifie que la chaîne de caractère n'est pas vide
        if ch not in ['']:

            # # on vérifie que le premier caractère tapé n'est pas le point ('.')
            # # si c'est le cas alors on retourne une entrée invalide
            # # (le format de retour doit être tel que spécifié ici)
            # if pos == 1 and ch in ['.']:
            #
            #     return QtGui.QValidator.Invalid, pos

            # on vérifie que le premier caractère tapé n'est pas le signe moins ('-') si la borne inférieur est positive
            # si c'est le cas alors on retourne une entrée invalide
            # (le format de retour doit être tel que spécifié ici)
            if pos == 1 and ch in ['-'] and self._borne_inferieure >= 0.0:

                return QtGui.QValidator.Invalid, pos

            # on vérifie qu'il n'y ait pas les caractères 'e' et 'E' dans la chaîne
            # si c'est le cas alors on retourne une entrée invalide
            # (le format de retour doit être tel que spécifié ici)
            if str(ch).find('e') != -1 or str(ch).find('E') != -1:

                return QtGui.QValidator.Invalid, pos

            # on essaie de convertir la chaîne de caractères en float
            try:

                float(ch)

            # on ne fait rien juste pour éviter d'avoir une exception ValueError levée
            except ValueError:

                pass

            # on vérifie si l'on se trouve dans la plage de valeurs spécifiée
            else:

                # si ce n'est pas le cas alors on retourne une entrée invalide
                # (le format doit être tel que spécifié ici)
                if float(ch) < self._borne_inferieure or float(ch) > self._borne_superieure:

                    return QtGui.QValidator.Invalid, pos

        return QtGui.QDoubleValidator.validate(self, ch, pos)


class SCItemDelegateTVComptes(QtWidgets.QStyledItemDelegate):
    """
        Classe qui permet de sous-classer la classe QStyledItemDelegate pour le TV Comptes
    """
    
    def __init__(self, parent=None):
        """
            Constructeur de la classe
        """
        
        super(SCItemDelegateTVComptes, self).__init__(parent)
        
        self._borne_inf = -10000.0
        self._borne_sup = 10000.0
        self._nombre_de_decimales = 3
        
        self._liste_des_colonnes_concernees = [2, 3]

    def createEditor(self, widget, option, index):
        """
            Méthode qui permet d'affecter un Qvalidator à certaines cellules du TableView
        """
        
        # Vérification de la validité de l'index
        if not index.isValid():
            
            return 0
            
        
        # Récupération du numéro de la colonne active
        colonne = index.column()
        
        # Affectation du Validator si la colonne active se trouve dans la liste des colonnes concernées
        if colonne in self._liste_des_colonnes_concernees:
            
            editeur = QtWidgets.QLineEdit(widget)
            validateur = SCQDoubleValidation(self._borne_inf, self._borne_sup)
            validateur.setDecimals(self._nombre_de_decimales)
            editeur.setValidator(validateur)
            
            return editeur
            
        return super(SCItemDelegateTVComptes, self).createEditor(widget, option, index)
        

class SCItemDelegateTVBalance(QtWidgets.QStyledItemDelegate):
    """
        Classe qui permet de sous-classer la classe QStyledItemDelegate pour le TV Balance
    """

    def __init__(self, parent=None):
        """
            Constructeur de la classe
        """

        super(SCItemDelegateTVBalance, self).__init__(parent)

        self._borne_inf = -1000.0
        self._borne_sup = 1000.0
        self._nombre_de_decimales = 2

    def createEditor(self, widget, option, index):
        """
            Méthode qui permet d'affecter un Qvalidator à certaines cellules du TableView
        """

        # Vérification de la validité de l'index

        if not index.isValid():

            return 0

        # Récupération du numéro de la colonne active

        colonne = index.column()

        # Affectation des QValidators selon la colonne active

        # colonne contenant les dates
        if colonne in [0]:

            editeur = QtWidgets.QLineEdit(widget)
            # reg_exp = QtCore.QRegExp("[0-3][0-9]\/[0-1][0-9]\/20[0-9]{2}")
            reg_exp = QtCore.QRegExp("(0[1-9]|[1-2]\d|3[0-1])\/(0[1-9]|1[0-2])\/20\d{2}")
            validateur = SCQRegExpValidator()
            validateur.setRegExp(reg_exp)
            editeur.setValidator(validateur)

            return editeur

        # colonnes contenant les montants pour lui et elle
        elif colonne in [2, 3]:

            editeur = QtWidgets.QLineEdit(widget)
            validateur = SCQDoubleValidation(self._borne_inf, self._borne_sup)
            validateur.setDecimals(self._nombre_de_decimales)
            editeur.setValidator(validateur)

            return editeur

        return super(SCItemDelegateTVBalance, self).createEditor(widget, option, index)
