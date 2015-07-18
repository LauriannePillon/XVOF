#!/usr/bin/env python2.7
# -*- coding: iso-8859-1 -*-
"""
Classe de base abstraite (interface) d�finissant une �quation d'�tat
"""
from abc import ABCMeta, abstractmethod


class EquationOfStateBase(object):
    """
    Une interface pour les �quations d'�tat
    """
    # N�cessaire pour sp�cifier l'interface
    __metaclass__ = ABCMeta
    #

    def __init__(self):
        pass

    @abstractmethod
    def solveVolumeEnergy(self, specific_volume, internal_energy):
        """
        R�solution en formulation V-E
        """
        pass

    @abstractmethod
    def solveVolumeTemperature(self, specific_volume, temperature):
        """
        R�solution en formulation V-T
        """
        pass

    @abstractmethod
    def solveVolumePressure(self, specific_volume, pressure):
        """
        R�solution en formulation V-P
        """
        pass
