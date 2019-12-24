#!/usr/bin/env python2.7
# -*- coding: iso-8859-1 -*-
"""
Classe d�finissant une condition limite g�n�rique
"""
from abc import abstractmethod


class BoundaryCondition(object):
    """
    Une condition limite g�n�rique
    """
    def __init__(self):
        self._type = None

    def type(self):
        """
        Accesseur sur le type de condition limite (pressure ou velocity)
        :return:
        """
        return self._type

    @abstractmethod
    def evaluate(self, time, *args, **kwargs):
        pass
