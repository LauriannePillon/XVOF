#!/usr/bin/env python2.7
# -*- coding: iso-8859-1 -*-
"""
Classe définissant le gestionnaire d'images

@todo: H�riter de la classe Figure
@todo: Transformer la classe Field en NamedTuple (cf. properties)
"""
import matplotlib.pyplot as plt
import numpy as np
from collections import namedtuple
from os import makedirs
from os.path import exists

from physic_figure import PhysicFigure
from xvof.utilities.singleton import Singleton

Field = namedtuple("Field", ["label", "titre", "val_min", "val_max", "results_path"])

PressureField = Field("Pression [Pa]", "Champ de pression", -20e+09, 20e+09, "./RESULTATS/PressureField")
DensityField = Field("Masse volumique [kg/m3]", "Champ de densite", 6500.0, 9500.0, "./RESULTATS/DensityField")
InternalEnergyField = Field("Energie interne [J/kg]", "Champ d energie interne", 0, 100000.0, "./RESULTATS/InternalEnergyField")
PseudoViscosityField = Field("Pseudoviscosite [Pa]", "Champ de pseudoviscosite", 0, 1.5e+09, "./RESULTATS/PseudoViscosityField")
CellPositionField = Field("Position [m]", "Champ de position", 0.0, 0.04, "./RESULTATS/CellPositionField")
NodePositionField = Field("Position [m]", "Champ de position", 0.0 , 0.04, "./RESULTATS/NodePositionField")
NodeVelocityField = Field("Vitesse [m/s]", "Champ de vitesse", -1000.0 , 1000.0, "./RESULTATS/NodeVelocityField")

class FigureManager(object):
    """
    Gestionnaire de figures
    """
    __metaclass__ = Singleton

    def __init__(self, mesh_instance, dump=False, show=True):
        self.__mesh_instance = mesh_instance
        self.__figures_mailles = []
        self.__figures_noeuds = []
        self.__champs_mailles = {}
        self.__champs_noeuds = {}
        self.update_fields()
        self._dump = dump
        self._show = show

    def update_fields(self):
        """ MAJ des champs par appel des propri�t�s du maillage"""
        self.__champs_mailles = \
            {CellPositionField: self.__mesh_instance.cells_coordinates[:],
             PressureField: self.__mesh_instance.pressure_field,
             DensityField: self.__mesh_instance.density_field,
             InternalEnergyField: self.__mesh_instance.energy_field,
             PseudoViscosityField: self.__mesh_instance.pseudoviscosity_field
            }
        self.__champs_noeuds = \
            {
             NodePositionField: self.__mesh_instance.nodes_coordinates[:],
             NodeVelocityField: self.__mesh_instance.velocity_field
             }

    def create_figure_for_cell_field(self, field_X, field_Y):
        """
        Cr�ation des figures pour les champs aux mailles
        (l'axe des X est donc l'abscisse des mailles)
        """
        try:
            X = self.__champs_mailles[field_X]
        except ValueError as ve:
            print "Le champ {} est inconnu!".format(field_X)
            raise ve
        try:
            Y = self.__champs_mailles[field_Y]
        except ValueError as ve:
            print "Le champ {} est inconnu!".format(field_Y)
            raise ve
        if self._dump:
            phyfig = PhysicFigure(X, Y, xlabel=field_X.label, ylabel=field_Y.label,
                              titre=field_Y.titre, save_path=field_Y.results_path)
        else:
            phyfig = PhysicFigure(X, Y, xlabel=field_X.label, ylabel=field_Y.label,
                              titre=field_Y.titre)
        phyfig.set_y_limit(field_Y.val_min, field_Y.val_max)
        phyfig.set_x_limit(field_X.val_min, field_X.val_max)
        return phyfig

    def create_figure_for_node_field(self, field_X, field_Y):
        """
        Cr�ation des figures pour les champs aux noeuds
        (l'axe des X est donc l'abscisse des noeuds)
        """
        try:
            X = np.array(self.__champs_noeuds[field_X])
        except ValueError as ve:
            print "Le champ {} est inconnu!".format(field_X)
            raise ve
        try:
            Y = np.array(self.__champs_noeuds[field_Y])
        except ValueError as ve:
            print "Le champ {} est inconnu!".format(field_Y)
            raise ve
        if self._dump:
            phyfig = PhysicFigure(X, Y, xlabel=field_X.label, ylabel=field_Y.label,
                              titre=field_Y.titre, save_path=field_Y.results_path)
        else:
            phyfig = PhysicFigure(X, Y, xlabel=field_X.label, ylabel=field_Y.label,
                              titre=field_Y.titre)
        phyfig.set_y_limit(field_Y.val_min, field_Y.val_max)
        phyfig.set_x_limit(field_X.val_min, field_X.val_max)
        return phyfig

    def populate_figs(self):
        """
        Cr�ation des figures associ�es � chacun des champs et ajout �
        la liste des figures
        """
        champ_X = CellPositionField
        for champ_Y in self.__champs_mailles.keys():
            if champ_Y != champ_X:
                fig = self.create_figure_for_cell_field(champ_X, champ_Y)
                self.__figures_mailles.append((fig, champ_X, champ_Y))
        champ_X = NodePositionField
        for champ_Y in self.__champs_noeuds.keys():
            if champ_Y != champ_X:
                fig = self.create_figure_for_node_field(champ_X, champ_Y)
                self.__figures_noeuds.append((fig, champ_X, champ_Y))
        if self._show:
            plt.show(block=False)
        if self._dump:
            self.create_reps()

    def update_figs(self, title_compl=None):
        """
        MAJ des champs puis des figures correspondantes
        """
        self.update_fields()
        for (fig, champ_x, champ_y) in self.__figures_mailles:
            champ_x_valeurs = self.__champs_mailles[champ_x]
            champ_y_valeurs = self.__champs_mailles[champ_y]
            fig.update(champ_x_valeurs, champ_y_valeurs, title_compl)
        for (fig, champ_x, champ_y) in self.__figures_noeuds:
            champ_x_valeurs = self.__champs_noeuds[champ_x]
            champ_y_valeurs = self.__champs_noeuds[champ_y]
            fig.update(champ_x_valeurs, champ_y_valeurs, title_compl)
        if self._show:
            plt.show(block=False)

    def create_reps(self):
        """
        Cr�ation des r�pertoires o� sont stock�es les figures
        """
        for (_, _, field) in self.__figures_mailles + self.__figures_noeuds:
            path = field.results_path
            if (exists(path)):
                msg = "Le chemin {:s} existe d�j�!"
                msg += "\nAbandon pour �viter d'�craser des donn�es!"
                raise SystemExit(msg)
            else:
                makedirs(path)