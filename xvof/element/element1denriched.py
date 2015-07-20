#!/usr/bin/env python2.7
# -*- coding: iso-8859-1 -*-
"""
Classe d�finissant un �l�ment enrichi en 1d
"""
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# ########### IMPORTATIONS DIVERSES  ####################
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
import numpy as np
from xvof.element import Element1d
from xvof.solver.newtonraphson import NewtonRaphson
from xvof.solver.functionstosolve.vnrenergyevolutionforveformulation import VnrEnergyEvolutionForVolumeEnergyFormulation


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# ###### DEFINITION DES CLASSES & FONCTIONS  ###############
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
class Element1dEnriched(Element1d):
    """
    Une classe pour les �l�ments enrichis dans le cas 1d
    """
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

    def __init__(self, element_origin, pos_discontin):
        Element1d.__init__(self, element_origin.proprietes)
        self._function_to_vanish = VnrEnergyEvolutionForVolumeEnergyFormulation()
        self._solver = NewtonRaphson(self._function_to_vanish, self.nrj_t)
        #
        if(pos_discontin < 0.) or (pos_discontin > 1.):
            message = "La position de la discontinuit� dans"
            message += " l'�l�ment enrichi doit �tre comprise entre 0 et 1!"
            raise SystemExit(message)
        #
        self.index = element_origin.index
        self._size_t = element_origin.taille_t
        self._size_t_plus_dt = element_origin.taille_t_plus_dt
        self._pression_t = element_origin.pression_t
        self._pression_t_plus_dt = element_origin.pression_t_plus_dt
        self._rho_t = element_origin.rho_t
        self._rho_t_plus_dt = element_origin.rho_t_plus_dt
        self._nrj_t = element_origin.nrj_t
        self._nrj_t_plus_dt = element_origin.nrj_t_plus_dt
        self._pseudo_plus_un_demi = element_origin.pseudo
        self._cson_t = element_origin.cson_t
        self._cson_t_plus_dt = element_origin.cson_t_plus_dt
        #
        self._pression_t_enrichi = 0.
        self._pression_t_plus_dt_enrichi = 0.
        self._rho_t_enrichi = 0.
        self._rho_t_plus_dt_enrichi = 0.
        self._nrj_t_enrichi = 0.
        self._nrj_t_plus_dt_enrichi = 0.
        self._pseudo_plus_un_demi_enrichi = 0.
        self._cson_t_enrichi = 0.
        self._cson_t_plus_dt_enrichi = 0.
        #
        self._taille_gauche_t = element_origin.taille_t * pos_discontin
        self._taille_gauche_t_plus_dt = \
            element_origin.taille_t_plus_dt * pos_discontin
        self._taille_droite_t = element_origin.taille_t * (1. - pos_discontin)
        self._taille_droite_t_plus_dt = \
            element_origin.taille_t_plus_dt * (1. - pos_discontin)
        #
        self._to_gauche = Element1dEnriched.fromEnrichToLeftPartField
        self._to_droite = Element1dEnriched.fromEnrichToRightPartField
        self._to_classic = Element1dEnriched.fromGeometryToClassicField
        self._to_enrich = Element1dEnriched.fromGeometryToEnrichField

    @property
    def taille_t_gauche(self):
        """
        Taille de la partie gauche de l'�l�ment au temps t
        """
        return self._taille_gauche_t

    @property
    def taille_t_droite(self):
        """
        Taille de la partie droite de l'�l�ment au temps t
        """
        return self._taille_droite_t

    @property
    def taille_t_plus_dt_gauche(self):
        """
        Taille de la partie gauche de l'�l�ment au temps t+dt
        """
        return self._taille_gauche_t_plus_dt

    @property
    def taille_t_plus_dt_droite(self):
        """
        Taille de la partie droite de l'�l�ment au temps t+dt
        """
        return self._taille_droite_t_plus_dt

    def getLeftPartCoordinates(self, noeuds):
        """
        Position du centre de l'�l�ment au temps t
        """
        vec_coord = np.zeros(noeuds[0].dimension)
        vec_coord = noeuds[0].coordt[:] + self.taille_t_gauche / 2.0
        return vec_coord

    def getRightPartCoordinates(self, noeuds):
        """
        Position du centre de l'�l�ment au temps t
        """
        vec_coord = np.zeros(noeuds[0].dimension)
        vec_coord = noeuds[1].coordt[:] - self.taille_t_droite / 2.0
        return vec_coord

    @property
    def pression_t_gauche(self):
        """
        Pression dans la partie gauche de l'�l�ment au temps t
        """
        return self._to_gauche(self._pression_t, self._pression_t_enrichi)

    @property
    def pression_t_droite(self):
        """
        Pression dans la partie droite de l'�l�ment au temps t
        """
        return self._to_droite(self._pression_t,
                               self._pression_t_enrichi)

    @property
    def pression_t_plus_dt_gauche(self):
        """
        Pression dans la partie gauche de l'�l�ment au temps t+dt
        """
        return self._to_gauche(self._pression_t_plus_dt,
                               self._pression_t_plus_dt_enrichi)

    @property
    def pression_t_plus_dt_droite(self):
        """
        Pression dans la partie droite de l'�l�ment au temps t+dt
        """
        return self._to_droite(self._pression_t_plus_dt,
                               self._pression_t_plus_dt_enrichi)

    @property
    def rho_t_gauche(self):
        """
        Densit� dans la partie gauche de l'�l�ment au temps t
        """
        return self._to_gauche(self._rho_t, self._rho_t_enrichi)

    @property
    def rho_t_droite(self):
        """
        Densit� dans la partie droite de l'�l�ment au temps t
        """
        return self._to_droite(self._rho_t, self._rho_t_enrichi)

    @property
    def rho_t_plus_dt_gauche(self):
        """
        Densit� dans la partie gauche de l'�l�ment au temps t+dt
        """
        return self._to_gauche(self._rho_t_plus_dt,
                               self._rho_t_plus_dt_enrichi)

    @property
    def rho_t_plus_dt_droite(self):
        """
        Densit� dans la partie droite de l'�l�ment au temps t+dt
        """
        return self._to_droite(self._rho_t_plus_dt,
                               self._rho_t_plus_dt_enrichi)

    @property
    def nrj_t_gauche(self):
        """
        Densit� dans la partie gauche de l'�l�ment au temps t
        """
        return self._to_gauche(self._nrj_t, self._nrj_t_enrichi)

    @property
    def nrj_t_droite(self):
        """
        Energie dans la partie droite de l'�l�ment au temps t
        """
        return self._to_droite(self._nrj_t, self._nrj_t_enrichi)

    @property
    def nrj_t_plus_dt_gauche(self):
        """
        Energie dans la partie gauche de l'�l�ment au temps t+dt
        """
        return self._to_gauche(self._nrj_t_plus_dt,
                               self._nrj_t_plus_dt_enrichi)

    @property
    def nrj_t_plus_dt_droite(self):
        """
        Energie dans la partie droite de l'�l�ment au temps t+dt
        """
        return self._to_droite(self._nrj_t_plus_dt,
                               self._nrj_t_plus_dt_enrichi)

    @property
    def cson_t_gauche(self):
        """
        Vitesse du son dans la partie gauche de l'�l�ment au temps t
        """
        return self._to_gauche(self._cson_t, self._cson_t_enrichi)

    @property
    def cson_t_droite(self):
        """
        Vitesse du son dans la partie droite de l'�l�ment au temps t
        """
        return self._to_droite(self._cson_t, self._cson_t_enrichi)

    @property
    def cson_t_plus_dt_gauche(self):
        """
        Vitesse du son dans la partie gauche de l'�l�ment au temps t+dt
        """
        return self._to_gauche(self._cson_t_plus_dt,
                               self._cson_t_plus_dt_enrichi)

    @property
    def cson_t_plus_dt_droite(self):
        """
        Vitesse du son dans la partie droite de l'�l�ment au temps t+dt
        """
        return self._to_droite(self._cson_t_plus_dt,
                               self._cson_t_plus_dt_enrichi)

    @property
    def pseudo_gauche(self):
        """
        Pseudo viscosit� dans la partie gauche de l'�l�ment
        """
        return self._to_gauche(self._pseudo_plus_un_demi,
                               self._pseudo_plus_un_demi_enrichi)

    @property
    def pseudo_droite(self):
        """
        Pseudo viscosit� dans la partie droite de l'�l�ment
        """
        return self._to_droite(self._pseudo_plus_un_demi,
                               self._pseudo_plus_un_demi_enrichi)

    # --------------------------------------------------------
    #        DEFINITION DES METHODES                         #
    # --------------------------------------------------------
    def __str__(self):
        message = "ELEMENT ENRICHI {:4d} ".format(self.index)
        return message

    def printInfos(self):
        """
        Affichage des informations concernant l'�l�ment
        """
        Element1d.printInfos(self)
        message = "==> masse volumique � gauche � t = {}\n".\
            format(self.rho_t_gauche)
        message += "==> masse volumique � droite � t = {}\n".\
            format(self.rho_t_droite)
        message += "==> masse volumique � gauche � t+dt = {}\n".\
            format(self.rho_t_plus_dt_gauche)
        message += "==> masse volumique � droite � t+dt = {}\n".\
            format(self.rho_t_plus_dt_droite)
        message += "==> taille � gauche � t = {}\n".\
            format(self.taille_t_gauche)
        message += "==> taille � droite � t = {}\n".\
            format(self.taille_t_droite)
        message += "==> taille � gauche � t+dt = {}\n".\
            format(self.taille_t_plus_dt_gauche)
        message += "==> taille � droite � t+dt = {}\n".\
            format(self.taille_t_plus_dt_droite)
        message += "==> pression � gauche � t = {}\n".\
            format(self.pression_t_gauche)
        message += "==> pression � droite � t = {}\n".\
            format(self.pression_t_droite)
        message += "==> pression � gauche � t+dt = {}\n".\
            format(self.pression_t_plus_dt_gauche)
        message += "==> pression � droite � t+dt = {}\n".\
            format(self.pression_t_plus_dt_droite)
        message += "==> vitesse du son � gauche � t = {}\n".\
            format(self.cson_t_gauche)
        message += "==> vitesse du son � droite � t = {}\n".\
            format(self.cson_t_droite)
        message += "==> vitesse du son � gauche � t+dt = {}\n".\
            format(self.cson_t_plus_dt_gauche)
        message += "==> vitesse du son � droite � t+dt = {}\n".\
            format(self.cson_t_plus_dt_droite)
        message += "==> �nergie � gauche � t = {}\n".\
            format(self.nrj_t_gauche)
        message += "==> �nergie � droite � t = {}\n".\
            format(self.nrj_t_droite)
        message += "==> �nergie � gauche � t+dt = {}\n".\
            format(self.nrj_t_plus_dt_gauche)
        message += "==> �nergie � droite � t+dt = {}\n".\
            format(self.nrj_t_plus_dt_droite)
        message += "==> pseudo � gauche = {}\n".\
            format(self.pseudo_gauche)
        message += "==> pseudo � droite = {}\n".\
            format(self.pseudo_droite)
        print message

    def computeNewPressure(self):
        """
        Calcul du triplet energie, pression, vitesse du son
        au pas de temps suivant
        Formulation v-e
        """
        # Traitement partie gauche
        my_variables = {'EquationOfState': self.proprietes.material.eos,
                        'OldDensity': self.rho_t_gauche,
                        'NewDensity': self.rho_t_plus_dt_gauche,
                        'Pressure': self.pression_t_gauche + 2. * self.pseudo_gauche,
                        'OldEnergy': self.nrj_t_gauche}
        self._function_to_vanish.setVariables(my_variables)
        nrj_t_plus_dt_g = self._solver.computeSolution()
        pression_t_plus_dt_g, _, cson_t_plus_dt_g = \
            self.proprietes.material.eos.solveVolumeEnergy(1. / self.rho_t_plus_dt_gauche, nrj_t_plus_dt_g)
        self._function_to_vanish.eraseVariables()
        # Traitement partie droite
        my_variables = {'EquationOfState': self.proprietes.material.eos,
                        'OldDensity': self.rho_t_droite,
                        'NewDensity': self.rho_t_plus_dt_droite,
                        'Pressure': self.pression_t_droite + 2. * self.pseudo_droite,
                        'OldEnergy': self.nrj_t_droite}
        self._function_to_vanish.setVariables(my_variables)
        nrj_t_plus_dt_d = self._solver.computeSolution()
        pression_t_plus_dt_d, _, cson_t_plus_dt_d = \
            self.proprietes.material.eos.solveVolumeEnergy(1. / self.rho_t_plus_dt_droite, nrj_t_plus_dt_d)
        self._function_to_vanish.eraseVariables()
        #
        self._pression_t_plus_dt = \
            self._to_classic(pression_t_plus_dt_g, pression_t_plus_dt_d)
        self._pression_t_plus_dt_enrichi = \
            self._to_enrich(pression_t_plus_dt_g, pression_t_plus_dt_d)
        #
        self._nrj_t_plus_dt = \
            self._to_classic(nrj_t_plus_dt_g, nrj_t_plus_dt_d)
        self._nrj_t_plus_dt_enrichi = \
            self._to_enrich(nrj_t_plus_dt_g, nrj_t_plus_dt_d)
        #
        self._cson_t_plus_dt = \
            self._to_classic(cson_t_plus_dt_g, cson_t_plus_dt_d)
        self._cson_t_plus_dt_enrichi = \
            self._to_enrich(cson_t_plus_dt_g, cson_t_plus_dt_d)

    def computeNewSize(self, noeuds, time_step=None):
        """
        Calcul des nouvelles longueurs de l'�l�ment
        """
        # Les noeuds sont class�s par coord croissante
        nod_g = noeuds[0]
        nod_d = noeuds[1]
        self._taille_gauche_t_plus_dt = self.taille_t_gauche + \
            (0.5 * (nod_d.upundemi_classique - nod_g.upundemi_enrichi) -
             0.5 * (nod_g.upundemi_classique - nod_g.upundemi_enrichi)) \
            * time_step
        self._taille_droite_t_plus_dt = self.taille_t_droite + \
            (0.5 * (nod_d.upundemi_classique + nod_d.upundemi_enrichi) -
             0.5 * (nod_g.upundemi_classique + nod_d.upundemi_enrichi)) \
            * time_step

    def computeNewDensity(self):
        """
        Calcul des nouvelles densit�s
        """
        densite_gauche_t_plus_dt = self.rho_t_gauche * self.taille_t_gauche \
            / self.taille_t_plus_dt_gauche
        densite_droite_t_plus_dt = self.rho_t_droite * self.taille_t_droite \
            / self.taille_t_plus_dt_droite
        self._rho_t_plus_dt = \
            self._to_classic(densite_gauche_t_plus_dt, densite_droite_t_plus_dt)
        self._rho_t_plus_dt_enrichi = \
            self._to_enrich(densite_gauche_t_plus_dt, densite_droite_t_plus_dt)

    def computeNewPseudo(self, delta_t):
        """
        Calcul de la nouvelle pseudo
        """
        pseudo_gauche = \
            Element1d.computePseudo(delta_t, self.rho_t_gauche,
                                    self.rho_t_plus_dt_gauche,
                                    self.taille_t_plus_dt_gauche,
                                    self.cson_t_gauche,
                                    self.proprietes.numeric.a_pseudo, self.proprietes.numeric.b_pseudo)

        pseudo_droite = \
            Element1d.computePseudo(delta_t, self.rho_t_droite,
                                    self.rho_t_plus_dt_droite,
                                    self.taille_t_plus_dt_droite,
                                    self.cson_t_droite,
                                    self.proprietes.numeric.a_pseudo, self.proprietes.numeric.b_pseudo)

        self._pseudo_plus_un_demi = \
            self._to_classic(pseudo_gauche, pseudo_droite)
        self._pseudo_plus_un_demi_enrichi = \
            self._to_enrich(pseudo_gauche, pseudo_droite)

    def computeNewTimeStep(self):
        """
        Calcul du pas de temps
        """
        cfl = self.proprietes.numeric.cfl
        dt_g = \
            Element1d.computeTimeStep(cfl, self.rho_t_gauche,
                                      self.rho_t_plus_dt_gauche,
                                      self.taille_t_plus_dt_gauche,
                                      self.cson_t_plus_dt_gauche,
                                      self.pseudo_gauche)

        dt_d = \
            Element1d.computeTimeStep(cfl, self.rho_t_droite,
                                      self.rho_t_plus_dt_droite,
                                      self.taille_t_plus_dt_droite,
                                      self.cson_t_plus_dt_droite,
                                      self.pseudo_droite)

        self._dt = dt_g + dt_d  # Bizarre --> A v�rifier

    def incrementVariables(self):
        """
        Incr�mentation des variables
        """
        Element1d.incrementVariables(self)
        self._pression_t_enrichi = self._pression_t_plus_dt_enrichi
        self._rho_t_enrichi = self._rho_t_plus_dt_enrichi
        self._cson_t_enrichi = self._cson_t_plus_dt_enrichi
        self._nrj_t_enrichi = self._nrj_t_plus_dt_enrichi
        self._taille_gauche_t = self._taille_gauche_t_plus_dt
        self._taille_droite_t = self._taille_droite_t_plus_dt
