#!/usr/bin/env python2.7
# -*- coding: iso-8859-1 -*-
"""
Classe d�finissant un champ enrichi comme
composition de deux champs classiques
"""
from xvof.fields.field import Field


class EnrichedField(object):
    '''
    Champ physique = champ physique classique + enrichi
    '''
    @classmethod
    def fromGeometryToEnrichField(cls, champ_gauche, champ_droite):
        """
        Renvoi le champ enrichi � partir des champs gauche et droite
        """
        return (champ_droite - champ_gauche) * 0.5

    @classmethod
    def fromGeometryToClassicField(cls, champ_gauche, champ_droite):
        """
        Renvoi le champ classique � partir des champs gauche et droite
        """
        return (champ_droite + champ_gauche) * 0.5

    @classmethod
    def fromEnrichToLeftPartField(cls, champ_classic, champ_enrich):
        """
        Renvoi le champ � gauche d'apr�s les champs classsique et enrichis
        """
        return champ_classic - champ_enrich

    @classmethod
    def fromEnrichToRightPartField(cls, champ_classic, champ_enrich):
        """
        Renvoi le champ � droite d'apr�s les champs classsique et enrichis
        """
        return champ_classic + champ_enrich

    def __init__(self, current, new):

        self.__classical = Field(current, new)
        self.__enriched = Field(0., 0.)

    def incrementValues(self):
        '''
        Incr�mente les valeurs du champ
        '''
        self.__classical.incrementValues()
        self.__enriched.incrementValues()

    @property
    def current_left_value(self):
        '''
        Renvoie la valeur courante du champ � gauche dans l'�l�ment enrichi
        '''
        return EnrichedField.fromEnrichToLeftPartField(self.__classical.current_value, self.__enriched.current_value)

    @property
    def current_right_value(self):
        '''
        Renvoie la valeur courante du champ � droite dans l'�l�ment enrichi
        '''
        return EnrichedField.fromEnrichToRightPartField(self.__classical.current_value, self.__enriched.current_value)

    @property
    def new_left_value(self):
        '''
        Renvoie la nouvelle valeur du champ � gauche dans l'�l�ment enrichi
        '''
        return EnrichedField.fromEnrichToLeftPartField(self.__classical.new_value, self.__enriched.new_value)

    @property
    def new_right_value(self):
        '''
        Renvoie la nouvelle valeur du  champ � droite dans l'�l�ment enrichi
        '''
        return EnrichedField.fromEnrichToRightPartField(self.__classical.new_value, self.__enriched.new_value)

    @property
    def classical_part(self):
        '''
        Renvoie le champ classique
        '''
        return self.__classical

    @property
    def enriched_part(self):
        '''
        Renvoie le champ enrichi
        '''
        return self.__enriched
