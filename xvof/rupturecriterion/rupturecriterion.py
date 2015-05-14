#!/usr/bin/env python2.7
# -*- coding: iso-8859-1 -*-
"""
Classe de base abstraite (interface) d�finissant un crit�re de rupture
"""
from abc import ABCMeta, abstractmethod


class RuptureCriterion():
    """
    Une interface pour les crit�res de rupture
    """
    # N�cessaire pour sp�cifier l'interface
    __metaclass__ = ABCMeta
    #

    def __init__(self):
        pass

    @abstractmethod
    def checkCriterion(self, cell, *args, **kwargs):
        """
        V�rification du crit�re de rupture sur la maille
        pass�e en argument
        """
        pass
