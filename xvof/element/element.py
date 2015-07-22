#!/usr/bin/env python2.7
# -*- coding: iso-8859-1 -*-
"""
Classe de base d�finissant un �l�ment
"""

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# ########### IMPORTATIONS DIVERSES  ####################
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
from abc import abstractmethod
import numpy as np


class Element(object):
    """
    Une classe pour les �l�ments
    """
    @classmethod
    def getCoordinates(cls, noeuds):
        """
        Position du centre de l'�l�ment au temps t
        """
        vec_coord = np.zeros(noeuds[0].dimension)
        for nod in noeuds:
            vec_coord += nod.coordt
        return vec_coord / len(noeuds)

    def __init__(self, proprietes):
        self._index = -1
        self._dt = 0.
        self._size_t = 0.
        self._size_t_plus_dt = 0.
        self._properties = proprietes
        self._rho_t = proprietes.material.rho_init
        self._rho_t_plus_dt = proprietes.material.rho_init
        self._pression_t = proprietes.material.pression_init
        self._pression_t_plus_dt = proprietes.material.pression_init
        self._pseudo_plus_un_demi = 0.
        self._cson_t = 0.
        self._cson_t_plus_dt = 0.
        self._nrj_t = proprietes.material.energie_init
        self._nrj_t_plus_dt = proprietes.material.energie_init

    ##############################################################
    # DEFINITIONS DES PROPRIETES
    ##############################################################
    #
    @property
    def index(self):
        """
        Indice global de l'�l�ment
        """
        return self._index

    @index.setter
    def index(self, index):
        """
        Setter de l'indice global de l'�l�ment
        """
        self._index = index

    @property
    def delta_t(self):
        '''
        Pas de temps critique de la maille
        '''
        return self._dt

    @property
    def taille_t(self):
        """
        Taille (longueur, aire, volume) de l'�l�ment � l'instant t
        """
        return self._size_t

    @property
    def taille_t_plus_dt(self):
        """
        Taille (longueur, aire, volume) de l'�l�ment � l'instant t + dt
        """
        return self._size_t_plus_dt

    @property
    def proprietes(self):
        """
        Proprietes de l'�l�ment
        """
        return self._properties

    @property
    def rho_t(self):
        """
        Masse volumique de l'�l�ment au temps t
        """
        return self._rho_t

    @property
    def rho_t_plus_dt(self):
        """
        Masse volumique de l'�l�ment au temps t + dt
        """
        return self._rho_t_plus_dt

    @property
    def pression_t(self):
        """
        Pression dans l'�l�ment au temps t
        """
        return self._pression_t

    @property
    def pression_t_plus_dt(self):
        """
        Pression dans l'�l�ment au temps t + dt
        """
        return self._pression_t_plus_dt

    @property
    def cson_t(self):
        """
        Vitesse du son dans l'�l�ment au temps t
        """
        return self._cson_t

    @property
    def cson_t_plus_dt(self):
        """
        Vitesse du son dans l'�l�ment au temps t + dt
        """
        return self._cson_t_plus_dt

    @property
    def nrj_t(self):
        """
        Energie interne de l'�l�ment au temps t
        """
        return self._nrj_t

    @property
    def nrj_t_plus_dt(self):
        """
        Energie interne dans l'�l�ment au temps t + dt
        """
        return self._nrj_t_plus_dt

    @property
    def pseudo(self):
        """
        Pseudo viscosit� dans l'�l�ment
        """
        return self._pseudo_plus_un_demi

    # ------------------------------------------------------------
    # DEFINITIONS DES METHODES
    # ------------------------------------------------------------
    def __str__(self):
        message = "ELEMENT {:4d} ".format(self._index)
        return message

    def printInfos(self):
        """
        Affichage des informations concernant l'�l�ment
        """
        message = "{} {:4d}\n".format(self.__class__, self._index)
        message += "==> taille � t = {}\n".format(self.taille_t)
        message += "==> taille � t+dt = {}\n".format(self.taille_t_plus_dt)
        message += "==> masse volumique � t = {}\n".format(self.rho_t)
        message += "==> masse volumique � t+dt = {}\n".\
            format(self.rho_t_plus_dt)
        message += "==> pression � t = {}\n".format(self.pression_t)
        message += "==> pression � t+dt = {}\n".\
            format(self.pression_t_plus_dt)
        message += "==> �nergie interne � t = {}\n".format(self.nrj_t)
        message += "==> �nergie interne � t+dt = {}\n".\
            format(self.nrj_t_plus_dt)
        message += "==> vitesse du son � t = {}\n".format(self.cson_t)
        message += "==> vitesse du son � t+dt = {}\n".\
            format(self.cson_t_plus_dt)
        print message

    def incrementVariables(self):
        """
        Incr�mentation des variables
        """
        self._pression_t = self._pression_t_plus_dt
        self._rho_t = self._rho_t_plus_dt
        self._cson_t = self._cson_t_plus_dt
        self._nrj_t = self._nrj_t_plus_dt
        self._size_t = self._size_t_plus_dt
    #############################################################
    # DEFINITIONS DES METHODES VIRTUELLES
    #############################################################

    @abstractmethod
    def computeNewPressure(self):
        """
        Algorithme de Newton-Raphson pour d�terminer le couple
        energie/pression au pas de temps suivant
        Formulation v-e
        """

    @abstractmethod
    def computeSize(self, nodes):
        """
        Calcul de la taille (longueur, aire, volume) au temps t de l'�l�ment
        """

    @abstractmethod
    def computeNewSize(self, nodes, time_step=None):
        """
        Calcul de la nouvelle taille (longueur, aire, volume) de l'�l�ment
        """

    @abstractmethod
    def computeNewDensity(self):
        """
        Calcul de la densit� � l'instant t+dt bas� sur
        la conservation de la masse
        """

    @abstractmethod
    def computeNewPseudo(self, time_step):
        """
        Calcul de la nouvelle pseudo
        """

    @abstractmethod
    def computeNewTimeStep(self):
        """
        Calcul du nouveau pas de temps
        """

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# ######          PROGRAMME PRINCIPAL        ###############
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
if __name__ == "__main__":
    import doctest
    TESTRES = doctest.testmod(verbose=0)
    if TESTRES[0] == 0:
        print "TESTS UNITAIRES : OK"
