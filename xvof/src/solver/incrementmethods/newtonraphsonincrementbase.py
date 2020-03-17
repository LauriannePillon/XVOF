#!/usr/bin/env python2.7
# -*- coding: iso-8859-1 -*-
"""
Classe de base d�finissant une m�thode d'incr�mentation
"""
from abc import ABCMeta, abstractmethod


class NewtonRaphsonIncrementBase(object):
    """
    Classe base d�finissant une m�thode d'incr�mentation
    """
    # pylint: disable=abstract-class-not-used
    # N�cessaire pour sp�cifier l'interface
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def computeIncrement(self, function_value, derivative_function_value):
        """
        Calcul de l'incr�ment
        """
        raise NotImplementedError
