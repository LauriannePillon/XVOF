#!/usr/bin/env python2.7
# -*- coding: iso-8859-1 -*-
"""
Interface d�finissant le contrat � remplir pur qu'ne fonction sont r�solue par le solveur
non lin�aire de tpye Newton Raphson
"""
from abc import ABCMeta, abstractmethod


class FunctionToSolveBase(object):
    """
    Interface d�finissant le contrat � remplir pur qu'ne fonction sont r�solue par le solveur
    non lin�aire de tpye Newton Raphson
    """
    # pylint: disable=abstract-class-not-used
    # N�cessaire pour sp�cifier l'interface
    __metaclass__ = ABCMeta

    def __init__(self):
        self._variables = None

    def setVariables(self, variables):
        '''
        Fixation de la valeur des variables
        '''
        if self._variables is None:
            self._variables = variables
        else:
            raise ValueError("Impossible de fixer deux fois les variables de la fonction � annuler!")

    def eraseVariables(self):
        '''
        Remise � None de _variables
        '''
        self._variables = None

    @abstractmethod
    def computeFunctionAndDerivative(self, variable_value):
        '''
        Renvoie la valeur de la fonction et sa d�riv�e
        '''
        raise NotImplementedError
