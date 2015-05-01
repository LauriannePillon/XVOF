#!/usr/bin/env python2.7
# -*- coding: iso-8859-1 -*-
"""
Classe d�finissant une �quation d'�tat de type Mie-Gruneisen
"""

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
############ IMPORTATIONS DIVERSES  ####################
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
from xvof.equationsofstate import EquationOfState

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
####### DEFINITION DES CLASSES & FONCTIONS  ###############
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# Deactivate pylint warnings due to NotImplementedError
# pylint: disable=R0921


class MieGruneisen(EquationOfState):
    """
    Un objet d�crivant l'�quation d'�tat de type Mie_Gruneisen
    """
    def __init__(self, **kwargs):
        """
        self.czero    : param�tre czero
        self.coeff_s1       : param�tre S1
        self.coeff_s2       : param�tre S2
        self.coeff_s3       : param�tre S3
        self.rhozeo   : param�tre rhozero
        self.grunzero : param�tre grunzero
        self.coeff_b        : param�tre b
        self.ezero    : param�tre ezero
        """
        EquationOfState.__init__(self)
        #
        self.__parameters = {
        'czero': 3980.0,
        'S1': 1.58,
        'S2': 0.,
        'S3': 0.,
        'rhozero': 8129.0,
        'grunzero': 1.6,
        'b': 0.5,
        'ezero': 0.
        }

        for (prop, default) in self.__parameters.iteritems():
            self.__parameters[prop] = kwargs.get(prop, default)

    @property
    def czero(self):
        """
        Vitesse du son standard
        """
        return self.__parameters['czero']

    @property
    def coeff_s1(self):
        """
        Param�tre S1
        """
        return self.__parameters['S1']

    @property
    def coeff_s2(self):
        """
        Param�tre S2
        """
        return self.__parameters['S2']

    @property
    def coeff_s3(self):
        """
        Param�tre S3
        """
        return self.__parameters['S3']

    @property
    def rhozero(self):
        """
        Masse volumique standard
        """
        return self.__parameters['rhozero']

    @property
    def grunzero(self):
        """
        Coefficient de Gruneisen standard
        """
        return self.__parameters['grunzero']

    @property
    def coeff_b(self):
        """
        Param�tre b
        """
        return self.__parameters['b']

    @property
    def ezero(self):
        """
        Energie interne standard
        """
        return self.__parameters['ezero']

    def __str__(self):
        message = "EquationOfState : {}".format(self.__class__)
        message += "\nParameters : "
        for key, val in sorted(self.__parameters.items(), key=lambda m: m[0]):
            message += "\n -- {:>20s} : {:>9.8g}".format(key, val)
        return message

    def __repr__(self):
        return self.__str__()

    def solve_ve(self, specific_volume, internal_energy):
        """
        Fournit le triplet (pression | d�riv�e de la pression en
        fonction de l'�nergie | vitesse du son) � partir du couple
        ( volume massique | �nergie interne )
        """
        #-------------------------------------------------
        # D�finition de variable locales pour eviter de
        # multiples recherche (gain de temps)
        #-------------------------------------------------
        locs1 = self.coeff_s1
        locs2 = self.coeff_s2
        locs3 = self.coeff_s3
        rhozero = self.rhozero
        grunzero = self.grunzero
        ezero = self.ezero
        locb = self.coeff_b
        czero2 = self.czero ** 2
        # D�rivee du coefficient de gruneisen
        dgam = rhozero * (grunzero - locb)
        #
        epsv = 1 - rhozero * specific_volume
        #
        epsv2 = epsv ** 2
        # Coefficient de gruneisen
        gam = grunzero * (1 - epsv) + locb * epsv
        #
        gampervol = gam / specific_volume
        #-------------------------------------------------
        # D�finition de variable locales redondantes
        #-------------------------------------------------
        redond_a = locs1 + 2. * locs2 * epsv + 3. * locs3 * epsv2
        if(epsv > 0):
            # ============================================================
            # si epsv > 0, la pression depend de einth et phi.
            # einth : energie interne specifique sur l hugoniot
            # phi : pression sur l hugoniot
            # denom : racine du denominateur de phi
            # dphi : derivee de ph par rapport a
            # deinth : derivee de einth par rapport a v
            # dpdv : dp/dv
            # ============================================================
            denom = (1. - (locs1 + locs2 * epsv + locs3 * epsv2) * epsv)
            phi = rhozero * czero2 * epsv / denom ** 2
            einth = ezero + phi * epsv / (2. * rhozero)
            #
            dphi = phi * rhozero * (-1. / epsv - 2. * redond_a / denom)
            #
            deinth = phi * (-1. - epsv * redond_a / denom)
            #
            dpdv = dphi + (dgam - gampervol) * \
            (internal_energy - einth) / specific_volume - \
            gampervol * deinth
            #
        elif(epsv <= 0):
            #============================================================
            # traitement en tension : epsv < 0
            # la pression depend d une fonction de v : phi
            # et
            # de e0 appelee einth
            #============================================================
            phi = rhozero * czero2 * epsv / (1. - epsv)
            # einth ---> e0
            einth = ezero
            #
            dphi = -czero2 / specific_volume ** 2
            #
            dpdv = dphi + (dgam - gampervol) * \
            (internal_energy - einth) / specific_volume
        #****************************
        # Pression :
        #****************************
        pressure = phi + (gampervol) * (internal_energy - einth)
        #****************************************
        # Derivee de la pression par rapport a e :
        #****************************************
        dpsurde = gampervol
        #======================================
        # Carre de la vitesse du son :
        #======================================
        vson2 = specific_volume ** 2 * (pressure * dpsurde - dpdv)
        if(vson2 < 0):
            print "Carr� de la vitesse du son < 0"
            print "specific_volume = {:15.9g}".format(specific_volume)
            print "pressure = {:15.9g}".format(pressure)
            print "dpsurde = {:15.9g}".format(dpsurde)
            print "dpdv = {:15.9g}".format(dpdv)
            raise SystemExit
        vson = vson2 ** 0.5
        #
        if(not ((vson > 0.)and(vson < 10000.))):
            vson = 0.
        #
        return pressure, dpsurde, vson

    def solve_vp(self, specific_volume, pressure):
        raise NotImplementedError

    def solve_vt(self, specific_volume, temperatue):
        raise NotImplementedError

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
############ PROGRAMME PRINCIPAL ####################
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\
if __name__ == '__main__':
    #
    # Lancemet du profiling
    #
    from xvof.utilities import timeit_file
    from os import system
    #

    @timeit_file('solve_ve.log')
    def profil_solve_ve(equation_of_state, spec_vol, e_int, it_nb=100):
        """
        Fait it_nb appel(s) � solve_ve � des fins de profiling
        """
        i = 0
        while i < it_nb:
            equation_of_state.solve_ve(spec_vol, e_int)
            i += 1
    #
    MY_EE = MieGruneisen()
    RHO = 9.000001000003e+03
    E_INT = 2.0e+03
    NBR_ITER = 100000
    print "Lancement profiling sur {:6d} it�rations".format(NBR_ITER)
    profil_solve_ve(MY_EE, 1. / RHO, E_INT, NBR_ITER)
    system('cat solve_ve.log')
