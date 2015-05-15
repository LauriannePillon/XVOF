#!/usr/bin/env python2.7
# -*- coding: iso-8859-1 -*-
"""
Classe d�finissant un traitement de la rupture en enrichissant l'�l�ment concern�
"""
from xvof.element.element1dupgraded import Element1dUpgraded
from xvof.rupturetreatment.rupturetreatment import RuptureTreatment


class EnrichElement(RuptureTreatment):
    """
    Un traitement de rupture qui enrichit l'�l�ment rompu
    """
    def __init__(self, position_rupture):
        RuptureTreatment.__init__(self)
        self.__position_rupture = position_rupture

    def applyTreatment(self, cell, *args, **kwargs):
        if (not isinstance(cell, Element1dUpgraded)):
            enrich_element = Element1dUpgraded(cell, self.__position_rupture)
            indice = kwargs["MAILLES"].index(cell)
            kwargs["MAILLES"][indice] = enrich_element
            kwargs["MAILLES_ROMPUES"].remove(cell)
