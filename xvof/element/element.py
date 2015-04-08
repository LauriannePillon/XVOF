#!/usr/bin/env python2.7
# -*- coding: iso-8859-1 -*-
"""
Classe de base d�finissant un �l�ment
"""

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
############ IMPORTATIONS DIVERSES  ####################
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
from abc import abstractmethod
import numpy as np
from miscellaneous import *

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
####### DEFINITION DES CLASSES & FONCTIONS  ###############
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


class Element(object):
    """
    Une classe pour les �l�ments
    """
    def __init__(self, proprietes, indice, taille):
        self._index = indice
        self._size = taille
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
        self._noeuds = []

    #------------------------------------------------------------
    # DEFINITIONS DES PROPRIETES
    #------------------------------------------------------------
    #
    # Seules les modifications de _noeuds_voisins sont permises
    # Les autres attributs sont accessibles en lecture seule
    #
    @property
    def indice(self):
        """
        Indice global de l'�l�ment
        """
        return self._index

    @property
    def taille(self):
        """
        Taille (longueur, aire, volume) de l'�l�ment
        """
        return self._size

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

    @property
    def noeuds(self):
        """
        Liste des noeuds de l'�l�ment
        """
        return self._noeuds

    @noeuds.setter
    def noeuds(self, node_list):
        """
        Setter des noeuds de l'�l�ment
        """
        self._noeuds[:] = node_list[:]

    #------------------------------------------------------------
    # DEFINITIONS DES METHODES
    #------------------------------------------------------------
    def __str__(self):
        message = "ELEMENT {:4d} ".format(self.indice)
        return message

    def infos(self):
        """
        Affichage des informations concernant l'�l�ment
        """
        message = "{} {:4d}\n".format(self.__class__, self.index)
        message += "==> noeuds = {}\n".format(self.noeuds)
        message += "==> taille = {}\n".format(self.taille)
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