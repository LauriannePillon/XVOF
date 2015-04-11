#!/usr/bin/env python2.7
# -*- coding: iso-8859-1 -*-
"""
Classe de base d�finissant un noeud
"""

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
############ IMPORTATIONS DIVERSES  ####################
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
from abc import abstractmethod
import numpy as np

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
####### DEFINITION DES CLASSES & FONCTIONS  ###############
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# @Todo : Cr�er un set (variable de classe) qui contient l'ensemble
# des indices de tous les noeuds pour �viter les doublons

class Node(object):
    """
    Une classe pour les noeuds
    """
    # pylint: disable-msg=R0902
    # 10 attributs : cela semble raisonnable pour ce cas
    def __init__(self, dim=1, index=-1,
                 position_initiale=None,
                 vitesse_initiale=None):
        # __dimension doit rester priv� m�me pour les classes filles
        # un noeud consacr� aux simulations 1d ne peut pas changer sa dimension
        self.__dimension = dim
        # _elements_voisins est rendu public par le property.setter
        # mais avec un contr�le sur les acc�s. Cette property est a surcharger
        # dans les classes filles
        self._elements_voisins = None
        # Les autres attributs ne sont pas publics mais restent accessibles et
        # modifiables par les classes filles
        if (not isinstance(index, int)):
            raise TypeError("L'indice du noeud doit �tre un entier!")
        self._index = index
        #
        if (position_initiale is None):
            position_initiale = np.zeros(self.__dimension, dtype=float)
        elif (np.shape(position_initiale) != (self.__dimension,)):
            message = "La dimension du vecteur position_initiale "
            message += "est incorrecte!"
            raise SystemExit(message)
        if (vitesse_initiale is None):
            vitesse_initiale = np.zeros(self.__dimension, dtype=float)
        elif (np.shape(vitesse_initiale) != (self.__dimension,)):
            message = "La dimension du vecteur position_initiale "
            message += "est incorrecte!"
            raise SystemExit(message)
        #
        self._xt = np.array(position_initiale)
        self._umundemi = np.array(vitesse_initiale)
        self._xtpdt = np.zeros(self.__dimension, dtype=float)
        self._upundemi = np.array(vitesse_initiale)
        self._masse = 0.
        self._force = np.zeros(self.__dimension, dtype=float)

    #------------------------------------------------------------
    # DEFINITIONS DES PROPRIETES
    #------------------------------------------------------------
    #
    # Seules les modifications de _elements_voisins sont permises
    # Les autres attributs sont accessibles en lecture seule
    #
    @property
    def elements_voisins(self):
        """
        Liste des �l�ments voisins du noeud
        """
        return self._elements_voisins

    @elements_voisins.setter
    def elements_voisins(self, elems):
        """
        Setter des elements voisins
        """
        self._elements_voisins = elems[:]

    @property
    def index(self):
        """
        Indice global du noeud
        """
        return self._index

    @property
    def coordt(self):
        """
        Position du noeud au temps t
        """
        return self._xt

    @property
    def coordtpdt(self):
        """
        Position du noeud au temps t + dt
        """
        return self._xtpdt

    @property
    def umundemi(self):
        """
        Vitesse au demi pas de temps pr�c�dent
        """
        return self._umundemi

    @property
    def upundemi(self):
        """
        Vitesse au demi pas de temps suivant
        """
        return self._upundemi

    @property
    def masse(self):
        """
        Masse nodale
        """
        return self._masse

    @property
    def force(self):
        """
        Force nodale
        """
        return self._force

    @property
    def dimension(self):
        """
        Dimension associ�e
        """
        return self.__dimension

    #------------------------------------------------------------
    # DEFINITIONS DES METHODES
    #------------------------------------------------------------
    def __str__(self):
        message = "NOEUD {:4d} ".format(self.index)
        message += "(dimension : {:1d})".format(self.__dimension)
        return message

    def infos(self):
        """
        Affichage des informations concernant le noeud
        """
        message = "{} {:4d}\n".format(self.__class__, self.index)
        message += "==> elements_voisins = {}\n".format(self.elements_voisins)
        message += "==> coordonn�es � t = {}\n".format(self.coordt)
        message += "==> coordonn�es � t+dt = {}\n".format(self.coordtpdt)
        message += "==> vitesse � t-1/2 = {}\n".format(self.umundemi)
        message += "==> vitesse � t+1/2 = {}\n".format(self.upundemi)
        message += "==> masse = {:5.4g}\n".format(self.masse)
        message += "==> force = {}".format(self.force)
        print message

    def calculer_masse_wilkins(self):
        """
        Calcule la masse associ�e au noeud par moyenne arithm�tique de la
        masse des �l�ments voisins (m�thode Wilkins)
        """
        for elem in self.elements_voisins:
            self._masse += elem.masse
        self._masse /= len(self.elements_voisins)

    def calculer_nouvo_coord(self, delta_t=1.0):
        """
        Calcul de la coordonn�e au temps t+dt

        @param delta_t : pas de temps
        """
        self._xtpdt = self.coordt + self.upundemi * delta_t

    def incrementer(self):
        """
        Mise � jour de la vitesse et de la coordonn�e du noeud
        pour passer au pas de temps suivant.
        """
        self._umundemi[:] = self.upundemi[:]
        self._xt[:] = self.coordtpdt[:]

    #------------------------------------------------------------
    # DEFINITIONS DES METHODES VIRTUELLES
    #------------------------------------------------------------
    @abstractmethod
    def calculer_nouvo_force(self):
        """
        Calcul de la force agissant sur le noeud
        """

    @abstractmethod
    def calculer_nouvo_vitesse(self, delta_t):
        """
        Calcul de la vitesse au demi pas de temps sup�rieur
        """

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#######          PROGRAMME PRINCIPAL        ###############
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
if __name__ == "__main__":
    import doctest
    testres = doctest.testmod(verbose=0)
    if(testres[0] == 0):
        print "TESTS UNITAIRES : OK"