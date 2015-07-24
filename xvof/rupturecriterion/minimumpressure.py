#!/usr/bin/env python2.7
# -*- coding: iso-8859-1 -*-
"""
Classe d�finissant un crit�re de rupture bas� sur la pression minimum
"""
from xvof.rupturecriterion.rupturecriterion import RuptureCriterion
from xvof.element.element1denriched import Element1dEnriched


class MinimumPressureCriterion(RuptureCriterion):
    """
    Un crit�re de rupture bas� sur la pression minimale
    """
    def __init__(self, pmin):
        super(MinimumPressureCriterion, self).__init__()
        self.__minimum_pressure = pmin

    def checkCriterion(self, cell, *args, **kwargs):
        if not isinstance(cell, Element1dEnriched) and (cell.pressure.new_value < self.__minimum_pressure):
            return True
        else:
            return False
