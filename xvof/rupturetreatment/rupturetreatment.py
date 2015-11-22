#!/usr/bin/env python2.7
# -*- coding: iso-8859-1 -*-
"""
Classe de base abstraite (interface) d�finissant un traitement de rupture
"""
from abc import ABCMeta, abstractmethod


class RuptureTreatment(object):
    """
    Une interface pour les traitements de la rupture
    """
    # N�cessaire pour sp�cifier l'interface
    __metaclass__ = ABCMeta
    #

    def __init__(self):
        pass

    @abstractmethod
    def applyTreatment(self, cells, *args, **kwargs):
        """
        Application du traitement de rupture sur les mailles
        pass�es en argument
        """
        pass
