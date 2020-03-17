# -*- coding: iso-8859-1 -*-
"""
Implementing the Element1dEnriched class
"""
import numpy as np
import os
from xvof.src.cell import OneDimensionCell
from xvof.src.discontinuity.discontinuity import Discontinuity


class OneDimensionEnrichedCell(OneDimensionCell):
    """
    A collection of 1d enriched elements. Treatment for all enrichment type
    """

    def __init__(self, number_of_elements):
        super(OneDimensionEnrichedCell, self).__init__(number_of_elements)
        #
        self._fields_manager.moveClassicalToEnrichedFields(number_of_elements)
        print self._fields_manager
        self._classical = np.empty(self.number_of_cells, dtype=np.bool, order='C')
        self._classical[:] = True
        self._initial_additional_dof = {}

    @property
    def classical(self):
        """
        :return: a mask where True indicate a classical cell
        """
        return self._classical

    @property
    def enriched(self):
        """
        :return: a mask where True indicates an enrich cell
        """
        return ~self.classical

    def __str__(self):
        message = "<--ENRICHED CELLS COLLECTION-->" + os.linesep
        message += "Classical elements are:"
        message += str(self.classical) + os.linesep
        message += "Enriched elements are:"
        message += str(self.enriched)
        return message

    def print_infos(self):
        """
        Printing informations about Elements
            A REECRIRE AU PROPRE; NOTATIONS ONT CHANGE
        """
        message = "{}\n".format(self.__class__)
        for disc in Discontinuity.discontinuity_list():
            message += "---- Discontinuity {:} ----".format(disc.label)
            message += "==> masse volumique classique � t = {}\n". \
                        format(self.density.current_value[disc.ruptured_cell_id])
            message += "==> masse volumique enrichie � t = {}\n". \
                        format(disc.additional_dof_density.current_value)
            message += "==> masse volumique classique � t+dt = {}\n". \
                        format(self.density.new_left_value[disc.ruptured_cell_id])
            message += "==> masse volumique enrichie � t+dt = {}\n". \
                        format(disc.additional_dof_density.new_value)
            message += "==> taille � gauche � t = {}\n". \
                format(disc.left_size.current_value)
            message += "==> taille � droite � t = {}\n". \
                format(disc.right_size.current_value)
            message += "==> taille � gauche � t+dt = {}\n". \
                format(disc.left_size.new_value)
            message += "==> taille � droite � t+dt = {}\n". \
                format(disc.right_size.new_value)

            message += "==> pression � gauche � t = {}\n". \
                format(self.pressure.current_value[disc.ruptured_cell_id])
            message += "==> pression � droite � t = {}\n". \
                format(disc.additional_dof_pressure.current_value)
            message += "==> vitesse du son � gauche � t = {}\n". \
                format(self.sound_velocity.current_value[disc.ruptured_cell_id])
            message += "==> vitesse du son � droite � t = {}\n". \
                format(disc.additional_dof_sound_velocity.current_value)
            message += "==> vitesse du son � gauche � t+dt = {}\n". \
                format(self.sound_velocity.new_value[disc.ruptured_cell_id])
            message += "==> vitesse du son � droite � t+dt = {}\n". \
                format(disc.additional_dof_sound_velocity.new_value)
            message += "==> �nergie � gauche � t = {}\n". \
                format(self.energy.current_value[disc.ruptured_cell_id])
            message += "==> �nergie � droite � t = {}\n". \
                format(disc.additional_dof_energy.current_value)
            message += "==> �nergie � gauche � t+dt = {}\n". \
                format(self.energy.new_value[disc.ruptured_cell_id])
            message += "==> �nergie � droite � t+dt = {}\n". \
                format(disc.additional_dof_energy.new_value)
            message += "==> pseudo � gauche = {}\n". \
                format(self.pseudo.current_value[disc.ruptured_cell_id])
            message += "==> pseudo � droite = {}\n". \
                format(disc.additional_dof_artificial_viscosity.current_value)
        print message

    @classmethod
    def compute_new_left_right_size(cls, time_step, disc, u1h, u2h, ug, ud):
        """
        Calcule les nouvelles longueurs des parties gauche et droite des �l�ments enrichis
        puis transformation classique /enrichi
        :param time_step: time step
        :param disc :discontinuity to be considered
        :param u1h : vitesse vraie du noeud 1
        :param u2h : vitesse vraie du noeud 2
        :param ug : vitesse vraie de la fronti�re gauche de la discontinuit�
        :param ud : vitesse vraie de la fronti�re droite de la discontinuit�
        """
        disc.left_part_size.new_value = disc.left_part_size.current_value + (ug - u1h) * time_step
        disc.right_part_size.new_value = disc.right_part_size.current_value + (u2h - ud) * time_step

    @classmethod
    def compute_new_left_right_density(cls, density_left, density_right, disc):
        """
        Calcule les nouvelles densit�s gauche et droite pour les �l�ments enrichis
        � partir de la conservation de la masse
        """
        density_left_new = (density_left * disc.left_part_size.current_value / disc.left_part_size.new_value)
        density_right_new = (density_right * disc.right_part_size.current_value / disc.right_part_size.new_value)
        return density_left_new, density_right_new
