#!/usr/bin/env python2.7
# -*- coding: iso-8859-1 -*-
"""
Module impl�mentant la classe Element
"""

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# ########### IMPORTATIONS DIVERSES  ####################
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
from abc import abstractmethod
from copy import deepcopy

import numpy as np
from xvof.fields.fieldsmanager import FieldManager


class Element(object):
    """
    Un objet Element repr�sente l'ensemble des �l�ments du maillage.
    Ses diff�rents membres sont essentiellement des vecteurs de nbr_of_cells lignes.

    L'organisation en m�moire est comme en C/C++ c'est � dire 'row wise'. C'est pour cette raison
    que les lignes de chacun des vecteurs repr�sentent les mailles. Ce faisant on a par exemple
    toutes les pressions des mailles contigues en m�moire. (vectorisation, localisation spatiale)
    """
    @classmethod
    def getCoordinates(cls, nbr_cells, topologie, vecteur_x_node, vecteur_y_node=None, vecteur_z_node=None):
        """
        D�termine le vecteur position du centre de l'�l�ment au temps t

        :param topologie: topologie du calcul
        :param vecteur_x_node: vecteur des coordonn�es x des noeuds
        :param vecteur_y_node: vecteur des coordonn�es y des noeuds
        :param vecteur_z_node: vecteur des coordonn�es z des noeuds

        :type topologie: Topology
        :type vecteur_x_node: numpy.array([nbr_of_nodes, 1], dtype=np.float64, order='C')
        :type vecteur_y_node: numpy.array([nbr_of_nodes, 1], dtype=np.float64, order='C')
        :type vecteur_z_node: numpy.array([nbr_of_nodes, 1], dtype=np.float64, order='C')
        :return: les vecteurs des coordonn�es du centre de chaque �l�ment au temps t
        :rtype:
        """
        vec_coord = np.zeros([nbr_cells, topologie.dimension])
        for ielem in xrange(nbr_cells):
            nodes_index = topologie.getNodesBelongingToCell(ielem)
            vec_coord[ielem][0] = vecteur_x_node[nodes_index].mean()
            if topologie.dimension == 2:
                vec_coord[ielem][1] = vecteur_y_node[nodes_index].mean()
            if topologie.dimension == 3:
                vec_coord[ielem][2] = vecteur_z_node[nodes.index].mean()
        return vec_coord

    def __init__(self, number_of_elements, proprietes, pressure_offset=0):
        self._shape = [number_of_elements, ]
        self._dt = np.zeros(self._shape, dtype=np.float64, order='C')
        self._size_t = np.zeros(self._shape, dtype=np.float64, order='C')
        self._size_t_plus_dt = np.zeros(self._shape, dtype=np.float64, order='C')
        self._properties = proprietes
        self._fields_manager = FieldManager()
        self._fields_manager.addClassicalField('Density', self._shape[0],
                                               proprietes.material.rho_init,
                                               proprietes.material.rho_init)
        self._fields_manager.addClassicalField('Pressure', self._shape[0] + pressure_offset,
                                               proprietes.material.pression_init,
                                               proprietes.material.pression_init)
        self._fields_manager.addClassicalField('Pseudo', self._shape[0])
        self._fields_manager.addClassicalField('SoundVelocity', self._shape[0])
        self._fields_manager.addClassicalField('Energy', self._shape[0],
                                               proprietes.material.energie_init,
                                               proprietes.material.energie_init)
    ##############################################################
    # DEFINITIONS DES PROPRIETES
    ##############################################################
    #
    @property
    def dt(self):
        '''
        Pas de temps critique de la maille
        '''
        return self._dt

    @property
    def size_t(self):
        """
        Taille (longueur, aire, volume) de l'�l�ment � l'instant t
        """
        return self._size_t

    @property
    def size_t_plus_dt(self):
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
    def density(self):
        """
        Champ masse volumique de l'�l�ment
        """
        return self._fields_manager.getField('Density')

    @property
    def pressure(self):
        """
        Champ pression dans l'�l�ment
        """
        return self._fields_manager.getField('Pressure')

    @property
    def sound_velocity(self):
        """
        Champ vitesse du son dans l'�l�ment
        """
        return self._fields_manager.getField('SoundVelocity')

    @property
    def energy(self):
        """
        Champ �nergie interne de l'�l�ment
        """
        return self._fields_manager.getField('Energy')

    @property
    def pseudo(self):
        """
        Champ pseudoviscosit� dans l'�l�ment
        """
        return self._fields_manager.getField('Pseudo')

    @property
    def fields_manager(self):
        '''
        Renvoi une copie du gestionnaire de champs
        '''
        return deepcopy(self._fields_manager)

    @property
    def number_of_cells(self):
        return self._shape[0]
    # ------------------------------------------------------------
    # DEFINITIONS DES METHODES
    # ------------------------------------------------------------
    def __str__(self):
        message = "Nombre d'�l�ments : {:d}".format(self._shape[0])
        return message

    def printInfos(self, index):
        """
        Affichage des informations concernant l'�l�ment d'indice index
        """
        message = "{} {:4d}\n".format(self.__class__, index)
        message += "==> taille � t = {}\n".format(self.size_t[index])
        message += "==> taille � t+dt = {}\n".format(self.size_t_plus_dt[index])
        message += "==> masse volumique � t = {}\n".format(self.density.current_value[index])
        message += "==> masse volumique � t+dt = {}\n".\
            format(self.density.new_value[index])
        message += "==> pression � t = {}\n".format(self.pressure.current_value[index])
        message += "==> pression � t+dt = {}\n".\
            format(self.pressure.new_value[index])
        message += "==> �nergie interne � t = {}\n".format(self.energy.current_value[index])
        message += "==> �nergie interne � t+dt = {}\n".\
            format(self.energy.new_value[index])
        message += "==> vitesse du son � t = {}\n".format(self.sound_velocity.current_value[index])
        message += "==> vitesse du son � t+dt = {}\n".\
            format(self.sound_velocity.new_value[index])
        print message

    def incrementVariables(self):
        """
        Incr�mentation des variables
        """
        self._fields_manager.incrementFields()
        self._size_t[:] = self._size_t_plus_dt[:]
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
    def computeSize(self, topologie):
        """
        Calcul de la taille (longueur, aire, volume) au temps t de l'�l�ment
        """

    @abstractmethod
    def computeNewSize(self, topologie, time_step=None):
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
