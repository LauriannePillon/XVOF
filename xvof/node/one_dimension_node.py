#!/usr/bin/env python2.7
# -*- coding: iso-8859-1 -*-
"""
Module d�finissant la classe Node1d
"""
from xvof.mass_matrix.mass_matrix_utilities import multiplicationMasse
from xvof.node import Node
import numpy as np


class OneDimensionNode(Node):
    """
    Un objet Node1d repr�sente l'ensemble des noeuds 1d du maillage
    """
    def __init__(self, nbr_of_nodes, poz_init, vit_init,
                 section=1.):

        Node.__init__(self, nbr_of_nodes, position_initiale=poz_init,
                      dim=1, vitesse_initiale=vit_init)
        self._section = section
        self._nbr_of_nodes = nbr_of_nodes
        # Par d�finition, ces noeuds ne sont pas enrichis
        self._classical = np.empty([self.number_of_nodes, ], dtype=np.bool, order='C')
        self._classical[:] = True

    @property
    def classical(self):
        """Noeuds classiques"""
        return self._classical

    @property
    def section(self):
        """
        Surface associ�e au noeud
        """
        return self._section

    def infos(self, index):
        """
        Affichage des informations concernant le noeud d'indice index

        :param index: indice du noeud � afficher
        :type index: int
        """
        Node.infos(self, index)
        message = "==> section = {:5.4g}".format(self.section)
        print message

    def compute_new_force(self, topologie, vecteur_pression_maille, vecteur_pseudo_maille):
        """
        Calcul des forces agissant sur les noeuds

        :param topologie: topologie du calcul
        :param vecteur_pression_maille: vecteur des pressions de chaque �l�ment + 2 pressions nulles � gauche et � droite
        :param vecteur_pseudo_maille: vecteur des pseudoviscosite de chaque �l�ment

        :type topologie: Topology
        :type vecteur_pression_maille: numpy.array([nbr_of_nodes+2, 1], dtype=np.float64, order='C')
        :type vecteur_pseudo_maille: numpy.array([nbr_of_nodes, 1], dtype=np.int64, order='C')
        """
        # Suppose les �l�ments voisins tri�s par position croissante

        connectivity = topologie.cells_in_contact_with_node[1:-1]
        pressure = self.section * (vecteur_pression_maille[connectivity] + vecteur_pseudo_maille[connectivity])
        self._force[1:-1][:, 0] = (pressure[:, 0] - pressure[:, 1])
        ind_node = 0
        elements_voisins = topologie.getCellsInContactWithNode(ind_node)
        pressure = self.section * (vecteur_pression_maille[elements_voisins] + vecteur_pseudo_maille[elements_voisins])
        self._force[ind_node] = -pressure[0]
        ind_node = self.number_of_nodes - 1
        elements_voisins = topologie.getCellsInContactWithNode(ind_node)

        pressure = self.section * (vecteur_pression_maille[elements_voisins] + vecteur_pseudo_maille[elements_voisins])
        self._force[ind_node] = pressure[0]

    def compute_new_velocity(self, delta_t, mask, matrice_masse):
        """
        Calcul de la vitesse au demi pas de temps sup�rieur

        :param delta_t: pas de temps
        :type delta_t: float
        :param mask : noeuds s�lectionn�s pour calculer avec cette m�thode
            (typiquement : OneDimensionEnrichedNode.classical / .enriched )
            s'applique sur les degr�s de libert� classiques des noeuds classiques ou enrichis
            ne prend pas en compte le couplage entre degr�s de libert� enrichis/classiques
        :type mask : tableau de bool�ens
        """
        # Nouveau : ddl classique de noeud classique (sauf 0 1 2 3 quand enrichissement)
        # = noeuds classiques non concern�s par l'enrichissement
        self._upundemi[mask] = self.umundemi[mask] + multiplicationMasse(matrice_masse, self.force[mask]) * delta_t

    def apply_correction_for_complete_mass_matrix_cell_500_ref(self, delta_t, inv_complete_mass_matrix,
                                                               inv_wilkins_mass_matrix, mask):
        """
        Apply a correction on velocity field to compute velocity from exact(non lumped) mass matrix for elements in mask
        """
        self._upundemi[mask] += multiplicationMasse(inv_complete_mass_matrix, self.force[mask]) * delta_t
        self._upundemi[mask] -= multiplicationMasse(inv_wilkins_mass_matrix, self.force[mask]) * delta_t

    def apply_pressure(self, ind_node, pressure):
        """
        Appliquer une pressure sur le noeud d'indice "ind_node"

        :param ind_node: indice du noeud sur lequel appliquer la pressure
        :param pressure: pressure � appliquer

        :type ind_node: int
        :type pressure: float
        """
        self._force[ind_node] += pressure * self.section

