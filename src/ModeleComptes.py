﻿# coding: utf-8

""" Module qui contient la classe ModeleComptes pour l'application des comptes """


### Paramètres globaux

__author__ = "Julien LEPAIN"
__version__ = 1.0
__all__ = ["ModeleComptes"]


### Import des librairies

from PyQt4 import QtGui, QtCore
import numpy as np


### Définitions des classes

class ModeleComptes(QtCore.QAbstractTableModel):
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
            Méthode qui permet de remplir le TableVIew
        """
        
        if index.isValid():
            
            # On vérifie si la sommes des montants de lui et de elle est égale au montant total
            # Le résultat sera sous la forme d'un booléen
            
            montant = self._donnees['Montant'][index.row()]
            montant_lui = self._donnees['Montant lui'][index.row()]
            montant_elle = self._donnees['Montant elle'][index.row()]
            
            statut_total = round(montant_lui + montant_elle, 2) == round(montant, 2)
            
            # On gère l'affichage des données ainsi que la coloration selon les cas
            
            if role == QtCore.Qt.DisplayRole:
            # Si c'est pour de l'affichage on récupère seulement les données
                
                return str(self._donnees.ix[index.row()][index.column()])
                
            elif role == QtCore.Qt.BackgroundRole and not statut_total:
            # Si la somme des montants de lui et de elle n'est pas égale au montant total on colorie les cellules des montants de lui et de elle en orange (RGB : 255, 170, 0)
                
                if index.column() in [3, 4]:
                    
                    return QtGui.QBrush(QtGui.QColor(255,170,0))
                    
            elif role == QtCore.Qt.BackgroundRole and statut_total:
            # Si la somme des montants de lui et de elle est égale au montant total on colorie les cellules des montants de lui et de elle en blanc
                
                if index.column() in [3, 4]:
                    
                    return QtGui.QBrush(QtGui.QColor(90,90,90))
                    
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
        
        if index.column() == 0:
        # Cas de la colonne contenant la date : la cellule est active et on autorise la sélection
            
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
            
        elif (index.column() == 3 or index.column() == 4):
        # Cas des colonnes contenant les montants pour lui et elle : la cellule est active et on autorise l'édition mais pas la sélection
            
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable
            
        else:
        # Cas des autre colonnes (l'intitulé) : la cellule est active
            
            return QtCore.Qt.ItemIsEnabled
            
    
    def setData(self, index, valeur, role):
        """
            Méthode qui permet de modifier les données lorsque l'utilisateur a modifié la valeur d'une cellule
        """
        
        # Index invalide
        if not index.isValid():
            
            return False
            
        # Rôle invalide
        if role != QtCore.Qt.EditRole:
            
            return False
            
        # Modification de la donnée
        ligne = index.row()
        colonne = index.column()
        valeur_convertie = np.float64(valeur.toFloat()[0])              # valeur est un objet QVariant qu'il faut convertir en float via la méthode toFloat, méthode qui retourne un tuple contenant la valeur convertie (en position 0) ainsi qu'un booléen (en position 1)
                                                                        # il est ensuite nécessaire de convertir ce float en numpy.float64 pour être cohérent vis-à-vis des données préalablement chargées
        
        self._donnees.ix[ligne, colonne] = round(valeur_convertie, 3)   # on arrondi à trois chiffres après la virgule pour éviter les co....... du style : je tape 2.35 et cela affiche 2.34999958
        self.dataChanged.emit(index, index)
        
        return True
        

### Utilisation

if __name__ == "__main__":
    
    print(u"Ce module n'est pas voué à être exécuté seul")
    
