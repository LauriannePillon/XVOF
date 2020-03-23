#!/usr/bin/env python2.7
# -*- coding: iso-8859-1 -*-
"""
Classe de base d�finissant un solveur non lin�aire 1D de type Newton-Raphson
"""
from abc import ABCMeta, abstractmethod


class NewtonRaphsonBase(object, metaclass=ABCMeta):
    """
    Une classe de base pour les solveurs non lin�aire 1D de type Newton-Raphson
    """
    #

    def __init__(self, function_to_vanish, nb_iterations_max, increment_method):
        self.__function_to_vanish = function_to_vanish
        self.__nb_iterations_max = nb_iterations_max
        self._increment_method = increment_method

    @property
    def function(self):
        """
        Renvoie la fonction � annuler
        """
        return self.__function_to_vanish

    @property
    def nb_iterations_max(self):
        """
        Retourne le nombre maximal d'it�rations autoris�
        """
        return self.__nb_iterations_max

    @abstractmethod
    def computeSolution(self, init_variable):
        """
        R�solution du solveur
        """
        raise NotImplementedError
