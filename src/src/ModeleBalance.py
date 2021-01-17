"""
    Module qui contient la classe ModeleBalance pour l'application des comptes
"""

# ======================================================================================================================
# Import des librairies
# ======================================================================================================================

from PyQt5 import QtGui, QtCore
import numpy as np


# ======================================================================================================================
# Définitions des classes
# ======================================================================================================================

class ModeleBalance(QtCore.QAbstractTableModel):
    """ 
        Classe qui permet de remplir un TableView à partir d'un dataframe pandas
    """ 
    
    def __init__(self, donnees, parent=None):
        """
            Constructeur de la classe
        """
        
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._donnees = donnees

    def set_donnees(self, valeurs):
        """
            Mutateur de l'attribut _donnees
        """
        
        self._donnees = valeurs 

    def rowCount(self, parent=None):
        """
            Méthode qui permet de compter le nombre de lignes
        """
        
        return len(self._donnees.values)
        
    def columnCount(self, parent=None):
        """
            Méthode qui permet de compter le nombre de colonnes
        """
        
        return self._donnees.columns.size

    def data(self, index, role=QtCore.Qt.DisplayRole):
        """
            Méthode qui permet de remplir le TableView
        """

        if index.isValid():

            # On vérifie si les valeurs absolues des montants de lui et de elle sont égales
            # Le résultat sera sous la forme d'un booléen

            montant_lui = self._donnees['Montant lui'][index.row()]
            montant_elle = self._donnees['Montant elle'][index.row()]

            statut_total = abs(montant_lui) == abs(montant_elle)
            
            # On gère l'affichage des données ainsi que la coloration selon les cas

            # Si c'est pour de l'affichage on récupère seulement les données
            if role == QtCore.Qt.DisplayRole:

                # return self._donnees.ix[index.row()][index.column()]
                return str(self._donnees.loc[index.row()][index.column()])

            # Si les valeurs absolues des montants de lui et de elle ne sont pas égales
            # on colorie les cellules des montants de lui et de elle en orange (RGB : 255, 170, 0)
            elif role == QtCore.Qt.BackgroundRole and not statut_total:

                if index.column() in [2, 3]:

                    return QtGui.QBrush(QtGui.QColor(255, 170, 0))

            # Si les valeurs absolues des montants de lui et de elle sont égales
            # on colorie les cellules des montants de lui et de elle en gris
            elif role == QtCore.Qt.BackgroundRole and statut_total:

                if index.column() in [2, 3]:

                    return QtGui.QBrush(QtGui.QColor(90, 90, 90))

        return None

    def headerData(self, col, orientation, role):
        """
            Méthode qui permet de remplir la première ligne du TableView avec les en-tetês du dataframe
        """
        
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            
            return self._donnees.columns[col]
            
        return None
        
    def flags(self, index):
        """
            Méthode qui permet de configurer les opérations possibles sur les cellules (sélection, édition, ...)
        """
        
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable
        
    def setData(self, index, valeur, role):
        """
            Méthode qui permet de modifier les données lorsque l'utilisateur a modifié la valeur d'une cellule
        """

        ### Index invalide
        if not index.isValid():

            return False

        ### Rôle invalide
        if role != QtCore.Qt.EditRole:

            return False

        ### Modification de la donnée

        # on récupère les index de la ligne et de la colonne sélectionnée
        ligne = index.row()
        colonne = index.column()

        # Colonnes contenant les montants pour lui et elle
        if colonne in [2, 3]:

            # valeur est une chaîne de carcatères qu'il faut convertir en numpy.float64
            # pour être cohérent vis-à-vis des données préalablement chargées
            valeur_convertie = np.float64(valeur)

            # on arrondi à trois chiffres après la virgule pour éviter les co....... du style :
            # je tape 2.35 et ça affiche 2.34999958
            col_names = self._donnees.columns.values
            self._donnees[col_names[colonne]] = self._donnees[col_names[colonne]].replace(
                self._donnees.loc[ligne][colonne],
                round(valeur_convertie, 3)
            )

        # Colonnes contenant la date et le Libellé
        else:

            self._donnees.loc[ligne, colonne] = valeur

        self.dataChanged.emit(index, index)

        return True
