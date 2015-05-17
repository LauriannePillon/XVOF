#!/usr/bin/env python2.7
# -*- coding: iso-8859-1 -*-
"""
Classe de base d�finissant un maillage 1d
"""
from configobj import Section

import numpy as np
from xvof.element.element1d import Element1d
from xvof.node.node1d import Node1d

class Mesh1dEnriched(object):
    """
    Une classe d�finissant un maillage 1d
    """
    def __init__(self, proprietes, initial_coordinates=np.linspace(0, 1, 11),
                 initial_velocities=np.zeros(11)):
        if np.shape(initial_coordinates) != np.shape(initial_velocities):
            message = "Les vecteurs initiaux de vitesse et coordonn�es"
            message += " n'ont pas la m�me taille"
            raise ValueError(message)
        if len(np.shape(initial_coordinates)) != 1:
            message = "Il s'agit d'un maillage 1D � initialiser avec des"
            message += " vecteurs � une dimension!"
            raise ValueError(message)
        self.__nbr_nodes = np.shape(initial_coordinates)[0]
        self.__nbr_cells = self.__nbr_nodes - 1
        self.__nodes = []
        self.__cells = []
        self.__ruptured_cells = []
        # Cr�ation des noeuds
        for n in xrange(self.__nbr_nodes):
            poz = initial_coordinates[n]
            vit = initial_velocities[n]
            nod = Node1d(n, poz_init=np.array([poz]),
                         vit_init=np.array([vit]),
                         section=proprietes.geometric.section)
            self.__nodes.append(nod)
        # Cr�ation des �l�ments
        for m in xrange(self.__nbr_cells):
            elem = Element1d(proprietes, m, [self.__nodes[m], self.__nodes[m + 1]])
            self.__cells.append(elem)
            self.__nodes[m].elements_voisins = [elem]
            self.__nodes[m + 1].elements_voisins = [elem]

    @property
    def nodes(self):
        """ Liste des noeuds """
        return self.__nodes

    @property
    def cells(self):
        """ Liste des �l�ments """
        return self.__cells

    def calculer_masse_des_noeuds(self):
        """ Calcul de la masse de chaque noeud"""
        for noeud in self.nodes:
            noeud.calculer_masse_wilkins()

    def calculer_nouvo_vit_noeuds(self, delta_t):
        """ Calcul de la nouvelle vitesse de chaque noeud � t+dt"""
        for noeud in self.nodes:
            noeud.calculer_nouvo_vitesse(delta_t)

    def calculer_nouvo_coord_noeuds(self, delta_t):
        """ Calcul des nouvelles coordonn�es de chaque noeud � t+dt"""
        for noeud in self.nodes:
            noeud.calculer_nouvo_coord(delta_t)

    def calculer_nouvo_taille_des_elements(self, delta_t):
        """ Calcul de la nouvelle taille de chaque �l�ment � t+dt"""
        for cell in self.cells:
            cell.calculer_nouvo_taille(delta_t)

    def calculer_nouvo_densite_des_elements(self):
        """ Calcul des nouvelles densit�s de chaque �l�ment � t+dt"""
        for cell in self.cells:
            cell.calculer_nouvo_densite()

    def calculer_nouvo_pression_des_elements(self):
        """ Calcul des nouvelles pressions de chaque �l�ment � t+dt"""
        for cell in self.cells:
            if cell not in self.__ruptured_cells:
                cell.calculer_nouvo_pression()

    def calculer_nouvo_pseudo_des_elements(self, delta_t):
        """ Calcul de la nouvelle pseudo � t+dt"""
        for cell in self.cells:
            cell.calculer_nouvo_pseudo(delta_t)

    def calculer_nouvo_force_des_noeuds(self):
        """ Calcul des nouvelles forces de chaque noeud � t+dt"""
        for noeud in self.nodes:
            noeud.calculer_nouvo_force()

    def incrementer(self):
        """ Passage au pas de temps suivant"""
        for noeud in self.nodes:
            noeud.incrementer()
        for cell in self.cells:
            cell.incrementer()

    def calculer_nouvo_pdt_critique(self):
        """ Calcul du pas de temps critique """
        dts = []
        for cell in self.cells:
            cell.calculer_nouvo_dt()
            dts.append(cell.delta_t)
        return min(dts)

    def appliquer_pression(self, surface, pression):
        """
        Appliquer une pression donn�e sur 
        les frontieres gauche ou droite
        """
        if surface.lower() not in ("gauche", "droite"):
            raise(ValueError("Sur la surface <gauche> ou <droite> est possible en 1d!"))
        if (surface.lower() == 'gauche'):
            self.__nodes[0].appliquer_pression(pression)
        else:
            self.__nodes[-1].appliquer_pression(-pression)

    @property
    def velocity_t_minus_half_field(self):
        """ Champ de vitesse � t-1/2"""
        return [node.umundemi for node in self.nodes]

    @property
    def velocity_t_plus_half_field(self):
        """ Champ de vitesse � t+1/2"""
        return [node.upundemi for node in self.nodes]

    @property
    def coord_t_field(self):
        """ Champ de position � t"""
        return [node.coordt for node in self.nodes]

    @property
    def coord_t_plus_dt_field(self):
        """ Champ de position � t+dt"""
        return [node.coordtpdt for node in self.nodes]

    @property
    def coord_elements_field(self):
        """
        Champ de position des �l�ments � t
        (Moyenne des champs de position � t des noeuds)
        """
        return [cell.coord for cell in self.cells]

    @property
    def force_field(self):
        """ Champ de force nodale"""
        return [node.force for node in self.nodes]

    @property
    def size_t_field(self):
        """ Tailles des �l�ments � t"""
        return [elem.taille_t for elem in self.cells]

    @property
    def size_t_plus_dt_field(self):
        """ Tailles des �l�ments � t"""
        return [elem.taille_t_plus_dt for elem in self.cells]

    @property
    def pressure_t_field(self):
        """ Champ de pression � t"""
        return [elem.pression_t for elem in self.cells]

    @property
    def pressure_t_plus_dt_field(self):
        """ Champ de pression � t+dt"""
        return [elem.pression_t_plus_dt for elem in self.cells]

    @property
    def rho_t_field(self):
        """ Champ de densit� � t"""
        return [elem.rho_t for elem in self.cells]

    @property
    def rho_t_plus_dt_field(self):
        """ Champ de densit� � t+dt"""
        return [elem.rho_t_plus_dt for elem in self.cells]

    @property
    def nrj_t_field(self):
        """ Champ d'�nergie interne � t"""
        return [elem.nrj_t for elem in self.cells]

    @property
    def pseudo_field(self):
        """ Champ de pseudo """
        return [elem.pseudo for elem in self.cells]

    def get_ruptured_cells(self, rupture_criterion):
        """ Liste des mailles endommag�es"""
        for elem in self.cells:
            if rupture_criterion.checkCriterion(elem):
                self.__ruptured_cells.append(elem)

    def apply_rupture_treatment(self, treatment):
        """
        Application du traitement de rupture sur la liste
        de cells pass�e en arguments
        """
#         print "Mailles rompues : {}".format(self.__ruptured_cells)
        ruptured_cells = self.__ruptured_cells[:]
        for cell in ruptured_cells:
#             print "-->Traitement de la maille {}".format(cell)
            treatment.applyTreatment(cell, MAILLES=self.__cells,
                                     MAILLES_ROMPUES=self.__ruptured_cells,
                                     NOEUDS=self.__nodes)
#             for cell in self.__cells[cell.indice - 2:cell.indice + 2]:
#                 print cell
#             print "-->self.__ruptured_cells = {}".format(self.__ruptured_cells)
#             raw_input()
