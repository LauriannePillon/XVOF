#!/usr/bin/env python2.7
# -*- coding: iso-8859-1 -*-
"""
Classe d�finissant la fonction d'�volution de l'�nergie interne � annuler dans le sch�ma VNR
Formulation V-E
"""
import numpy as np
from xvof.solver.functionstosolve.functiontosolvebase import FunctionToSolveBase


class VnrEnergyEvolutionForVolumeEnergyFormulation(FunctionToSolveBase):
    '''
    Classe d�finissant la fonction d'�volution de l'�nergie interne � annuler dans le sch�ma VNR
    Formulation V-E
    '''
    def __init__(self):
        super(VnrEnergyEvolutionForVolumeEnergyFormulation, self).__init__()

    def computeFunctionAndDerivative(self, newton_variable_value):
        nrj = newton_variable_value
        eos = self._variables['EquationOfState']
        old_rho = self._variables['OldDensity']
        new_rho = self._variables['NewDensity']
        pressure = self._variables['Pressure']
        old_nrj = self._variables['OldEnergy']
        p_i = np.zeros(old_rho.shape, dtype=np.float64, order='C')
        dpsurde = np.zeros(old_rho.shape, dtype=np.float64, order='C')
        for icell in xrange(old_rho.shape[0]):
            try:
#                 print 'new_rho[{:d}] = {:25.23g}\n'.format(icell, new_rho[icell])
#                 print 'nrj[{:d}] = {:25.23g}\n'.format(icell, nrj[icell])
                (p_i[icell], dpsurde[icell], dummy) = eos.solveVolumeEnergy(1. / new_rho[icell], nrj[icell])
#                 print 'p_i[{:d}] = {:25.23g}\n'.format(icell, p_i[icell])
#                 print 'dpsuirde[{:d}] = {:25.23g}\n'.format(icell, dpsurde[icell])
            except ValueError as ve:
                print "Pb dans la maille d'indice : {:d}!\n".format(icell)
                raise ve
        # Fonction � annuler
        delta_v = 1. / new_rho - 1. / old_rho
        func = nrj + p_i * delta_v / 2. + pressure * delta_v / 2. - old_nrj
        # D�riv�e de la fonction � annuler
        dfunc = 1 + dpsurde * delta_v / 2.
        return (func, dfunc)
