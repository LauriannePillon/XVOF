#!/usr/bin/env python2.7
# -*- coding: iso-8859-1 -*-
"""
Module d�finissant la classe Node
"""

from abc import abstractmethod
import numpy as np

class Node(object):
    """
    Un objet Node repr�sente l'ensemble des noeuds du maillages. Ses diff�rents membres sont
    essentiellement des vecteurs de nbr_of_nodes lignes. Plusieurs colonnes peuvent �tre
    pr�sentes selon la dimension du probl�me � traiter. 

    L'organisation en m�moire est comme en C/C++ c'est � dire 'row wise'. C'est pour cette raison
    que les lignes de chacun des vecteurs repr�sentent les noeuds. Ce faisant on a par exemple
    tous les X des noeuds contigus en m�moire. (vectorisation, localisation spatiale)
    """
    # pylint: disable-msg=R0902
    # 10 attributs : cela semble raisonnable pour ce cas
    def __init__(self, nbr_of_nodes, position_initiale, dim=1, vitesse_initiale=None):
	"""
	:param dim: dimension du probl�me � traiter (par d�faut 1)
	:param nbr_of_nodes: nombre de noeuds du probl�me
	:param position_initiale: vecteur des positions initiales
	:param vitesse_initiale: vecteur des vitesses initiales

	:type dim: int
	:type nbr_of_nodes: int
	:type position_initiale: numpy.array([nbr_of_nodes, dim], dtype=np.float64, order='C')
	:type vitesse_initiale: numpy.array([nbr_of_nodes, dim], dtype=np.float64, order='C')
	"""
	# Le vecteur est un vecteur dont les lignes sont les noeuds et les colonnes les coordon�es selon
	# les diff�rentes dimensions
	self.__shape = [nbr_of_nodes, dim]
        # Les autres attributs ne sont pas publics mais restent accessibles et
        # modifiables par les classes filles
        if np.shape(position_initiale) != self.__shape:
            message = "Node() : La dimension ({}) du vecteur position_initiale "\
                .format(np.shape(position_initiale))
            message += "est incorrecte!"
            raise SystemExit(message)
        if vitesse_initiale is None:
            vitesse_initiale = np.zeros(self.__shape, dtype=np.float64, order='C')
        elif np.shape(vitesse_initiale) != self.__shape:
            message = "Node() : La dimension ({}) du vecteur vitesse_initiale "\
                .format(np.shape(vitesse_initiale))
            message += "est incorrecte!"
            raise SystemExit(message)
        #
        self._xt = np.array(position_initiale)
        self._umundemi = np.array(vitesse_initiale)
        self._xtpdt = np.zeros(self.__shape, dtype=np.float64, order='C')
        self._upundemi = np.array(vitesse_initiale)
        self._masse = np.zeros([self.__shape[0], 1], dtype=np.float64, order='C')
        self._invmasse = np.zeros([self.__shape[0], 1], dtype=np.float64, order='C')
        self._force = np.zeros([self.__shape[0], 1], dtype=np.float64, order='C')

    property
    def xt(self):
        """
        Positions des noeuds au temps t

        :return: positions des noeuds au temps t
        :rtype: numpy.array([nbr_of_nodes, dim], dtype=np.float64, order='C')
        """
        return self._xt

    @property
    def xtpdt(self):
        """
        Positions des noeuds au temps t + dt
	
        :return: positions des noeuds au temps t + dt
        :rtype: numpy.array([nbr_of_nodes, dim], dtype=np.float64, order='C')
        """
        return self._xtpdt

    @property
    def umundemi(self):
        """
        Vitesses au demi pas de temps pr�c�dent
	
        :return: vitesses des noeuds au demi pas de temps pr�c�dent
        :rtype: numpy.array([nbr_of_nodes, dim], dtype=np.float64, order='C')
        """
        return self._umundemi

    @property
    def upundemi(self):
        """
        Vitesses au demi pas de temps suivant
	
        :return: vitesses des noeuds au demi pas de temps suivant
        :rtype: numpy.array([nbr_of_nodes, dim], dtype=np.float64, order='C')
        """
        return self._upundemi

    @property
    def masse(self):
        """
        Masses nodales

        :return: vecteur des masses nodales
        :rtype: numpy.array([nbr_of_nodes, 1], dtype=np.float64, order='C')
        """
        return self._masse

    @property
    def invmasse(self):
        """
        Inverse des masses nodales

        :return: vecteur des inverses des masses nodales
        :rtype: numpy.array([nbr_of_nodes, 1], dtype=np.float64, order='C')
        """
        return self._invmasse

    @property
    def force(self):
        """
        Forces nodales

        :return: vecteur des forces nodales
        :rtype: numpy.array([nbr_of_nodes, 1], dtype=np.float64, order='C')
        """
        return self._force

    @property
    def dimension(self):
        """
        Dimension du probl�me
        
        :return: dimension du probl�me
        :rtype: int
        """
        return self.__shape[1]

    @property:
    def number_of_nodes(self):
        """
        Nombre de noeuds du probl�me
        
        :return: dimension du probl�me
        :rtype: int
        """ 
        return self.__shape[0]

    def __str__(self):
        message = "Nombre de noeuds {:8d} ".format(self.__shape[0])
        message += "Dimension du probl�me : {:1d})".format(self.__shape[1])
        return message

    def infos(self, index):
        """
        Affichage des informations concernant le noeud d'indice index

        :param index: indice du noeud � afficher
        :type index: int
        """
        message = "{} {:4d}\n".format(self.__class__, index)
        message += "==> coordonn�es � t = {}\n".format(self.coordt[index])
        message += "==> coordonn�es � t+dt = {}\n".format(self.coordtpdt[index])
        message += "==> vitesse � t-1/2 = {}\n".format(self.umundemi[index])
        message += "==> vitesse � t+1/2 = {}\n".format(self.upundemi[index])
        message += "==> masse = {:5.4g}\n".format(self.masse[index])
        message += "==> force = {}".format(self.force[index])
        print message

    def calculer_masse_wilkins(self, topologie, vecteur_masse_elements, vecteur_nb_noeuds_par_element):
        """
        Calcule les masses associ�es � chaque noeud par moyenne arithm�tique de la
        masse des �l�ments voisins (m�thode Wilkins)

        :param topologie: topologie du calcul
        :param vecteur_masse_elements: vecteur des masses de chaque �l�ment
        :param vecteur_nb_noeuds_par_element: vecteur des nombres de noeuds que poss�de chaque �l�ment

        :type topologie: Topology
        :type vecteur_masse_elements: numpy.array([nbr_of_nodes, 1], dtype=np.float64, order='C')
        :type vecteur_nb_noeuds_par_element: numpy.array([nbr_of_nodes, 1], dtype=np.int64, order='C')
        """
        for ind_node in xrange(self.nbr_noeuds):
            elements_voisins = topologie.getCellsInContactWithNode(ind_node)
            self._masse[ind_node] = np.sum(vecteur_masse_elements[elements_voisins] ./ vecteur_nb_noeuds_par_element[elements_voisins])
            self._invmasse[ind_node] = 1. / self._masse[ind_node]

    def calculer_nouvo_coord(self, delta_t=1.0):
        """
        Calcul de la coordonn�e au temps t+dt

        :param delta_t: pas de temps
        :type delta_t: float
        """
        self._xtpdt = self.xt + self.upundemi * delta_t

    def incrementer(self):
        """
        Mise � jour de la vitesse et de la coordonn�e des noeuds
        pour passer au pas de temps suivant.
        """
        self._umundemi[:] = self.upundemi[:]
        self._xt[:] = self.xpdt[:]

    @abstractmethod
    def calculer_nouvo_force(self, *args, **kwargs):
        """
        Calcul de la force agissant sur le noeud
        """

    @abstractmethod
    def calculer_nouvo_vitesse(self, delta_t):
        """
        Calcul de la vitesse au demi pas de temps sup�rieur
        """

if __name__ == "__main__":
    print "Ceci est uniquement un module!"
