#!/usr/bin/env python2.7
# -*- coding: iso-8859-15 -*-
from math import pi

import lxml.etree as et
import matplotlib.pyplot as plt
import numpy as np
from xvof.equationsofstate.miegruneisen import MieGruneisen
from xvof.figure_manager.figure_manager import FigureManager
from xvof.mesh.mesh1d import Mesh1d
from xvof.miscellaneous import geometrical_props, material_props
from xvof.miscellaneous import numerical_props, properties
from xvof.pressurelaw.constantpressure import ConstantPressure
from xvof.pressurelaw.twostepspressure import TwoStepsPressure
from xvof.rupturecriterion.minimumpressure import MinimumPressureCriterion
from xvof.rupturetreatment.imposepressure import ImposePressure


#  =================================================
#  SIMULATION PARAMETERS                           =
#  =================================================
FinalTime = 15.0e-06
InitialTimeStep = 2.0e-09
InitialPressure = 100006.2096
InitialInternalEnergy = 7.689
InitialDensity = 8129.
Section = pi * 0.01 ** 2
EquationOfState = MieGruneisen()
LeftBoundaryPressure = TwoStepsPressure(15e+09, InitialPressure, 2.0e-06)
RightBoundaryPressure = ConstantPressure(InitialPressure)
RuptureCriterion = MinimumPressureCriterion(-7.0e+09)
RuptureTreatment = ImposePressure(0.)
Length = 25.0e-03
NumberOfElements = 1001
QuadraticPseudoParameter = 1.5
LinearPseudoParameter = 0.2
CFL = 0.95

ImagesNumber = 150
#  =================================================

if __name__ == '__main__':
    np.set_printoptions(formatter={'float': '{: 25.23g}'.format})
    #
    time = 0.
    step = 0
    dt = InitialTimeStep
    dt_crit = 2 * dt
    # ---------------------------------------------#
    #         PROPERTIES CREATION                  #
    # ---------------------------------------------#
    num_props = numerical_props(QuadraticPseudoParameter, LinearPseudoParameter, CFL)
    mat_props = material_props(InitialPressure, InitialInternalEnergy, InitialDensity, EquationOfState)
    geom_props = geometrical_props(Section)
    props = properties(num_props, mat_props, geom_props)
    # ---------------------------------------------#
    #         MESH CREATION                        #
    # ---------------------------------------------#
    coord_init = np.zeros([NumberOfElements + 1, 1], dtype=np.float64, order='C')
    coord_init[:, 0] = np.linspace(0, Length, NumberOfElements + 1)
    vit_init = np.zeros([NumberOfElements + 1, 1], dtype=np.float64, order='C')
    my_mesh = Mesh1d(props, initial_coordinates=coord_init, initial_velocities=vit_init)
    # ---------------------------------------------#
    #  FIGURES MANAGER SETUP                       #
    # ---------------------------------------------#
    if (ImagesNumber != 0):
        delta_t_images = FinalTime / ImagesNumber
        my_fig_manager = FigureManager(my_mesh, dump=True, show=True)
        my_fig_manager.populate_figs()
    else:
        delta_t_images = FinalTime * 2.0
    t_next_image = delta_t_images
    # ---------------------------------------------#
    #         NODAL MASS COMPUTATION               #
    # ---------------------------------------------#
    my_mesh.computeCellsSizes()
    my_mesh.computeNodesMasses()
    print "CALCULUS LAUNCHED!"
    while (time < FinalTime):
        if step % 1000 == 0:
            msg = ("""Iteration {:<4d} -- Time : {:15.9g} seconds with"""
                   """ a time step of {:15.9g} seconds\n""").format(step, time, dt)
            print msg
        # ---------------------------------------------#
        #         NODES VELOCITIES COMPUTATION         #
        # ---------------------------------------------#
        my_mesh.computeNewNodesVelocities(dt)
        # ---------------------------------------------#
        #         NODES COORDINATES COMPUTATION        #
        # ---------------------------------------------#
        my_mesh.computeNewNodesCoordinates(dt)
        # ---------------------------------------------#
        #         CELLS VOLUMES COMPUTATION            #
        # ---------------------------------------------#
        my_mesh.computeNewCellsSizes(dt)
        # ---------------------------------------------#
        #         CELLS DENSITIES COMPUTATION          #
        # ---------------------------------------------#
        my_mesh.computeNewCellsDensities()
        # ---------------------------------------------#
        #         CELLS PRESSURES COMPUTATION          #
        # ---------------------------------------------#
        my_mesh.computeNewCellsPressures()
        # ---------------------------------------------#
        #              RUPTURE                         #
        # ---------------------------------------------#
        my_mesh.getRupturedCells(RuptureCriterion)
        my_mesh.applyRuptureTreatment(RuptureTreatment)
        # ---------------------------------------------#
        #         NODES FORCES COMPUTATION             #
        # ---------------------------------------------#
        my_mesh.computeNewNodesForces()
        # ---------------------------------------------#
        #         LOADING                              #
        # ---------------------------------------------#
        my_mesh.applyPressure('left', LeftBoundaryPressure.evaluate(time))
        my_mesh.applyPressure('right', RightBoundaryPressure.evaluate(time))
        # ---------------------------------------------#
        #         TIME STEP COMPUTATION                #
        # ---------------------------------------------#
        dt_crit = my_mesh.computeNewTimeStep()
        # ---------------------------------------------#
        #         PSEUDOVISCOSITY COMPUTATION          #
        # ---------------------------------------------#
        my_mesh.computeNewCellsPseudoViscosities(dt)
        # ---------------------------------------------#
        #                INCREMENTATION                #
        # ---------------------------------------------#
        my_mesh.increment()
#         dt = dt_crit
        time += dt
        step += 1
        # ---------------------------------------------#
        #                OUTPUT MANAGEMENT             #
        # ---------------------------------------------#
        if (time > t_next_image):
            my_fig_manager.update_figs("t={:5.4g} us".format(time / 1.e-06))
            t_next_image += delta_t_images

    plt.show()
