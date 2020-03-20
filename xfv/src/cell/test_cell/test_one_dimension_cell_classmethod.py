#!/usr/bin/env python2.7
# -*- coding: iso-8859-1 -*-
"""
one_dimension_cell module unit tests
"""
import numpy as np
import unittest
import os
from xfv.src.cell.one_dimension_cell import OneDimensionCell
from xfv.src.data.data_container import DataContainer


class OneDimensionCellTest(unittest.TestCase):

    def setUp(self):
        data_file_path = os.path.join(os.path.dirname(__file__), "../../../tests/0_UNITTEST/XDATA_elasto.xml")
        self.test_datacontainer = DataContainer(data_file_path)

        self.nbr_cells = 4
        self.my_cells = OneDimensionCell(self.nbr_cells)
        self.my_cells.cell_in_target = np.ones(self.nbr_cells, dtype='bool')

    def tearDown(self):
        DataContainer.clear()
        pass

    def test_apply_equation_of_state(self):
        """
        Test of apply_equation_of_state class method
        """
        density_current = np.ones(self.nbr_cells) * 8930.
        pressure_current = np.ones(self.nbr_cells) * 1.e+05
        energy_current = np.ones(self.nbr_cells) * 6.719465

        density_new = np.array([9000., 8900., 8915., 8920.])
        cson_new = np.zeros([self.nbr_cells])
        pressure_new = np.zeros([self.nbr_cells])
        energy_new = np.zeros([self.nbr_cells])
        pseudo = np.zeros([self.nbr_cells])

        eos = DataContainer().material_target.constitutive_model.eos

        energy_new_value, pressure_new_value, sound_velocity_new_value = \
            OneDimensionCell.apply_equation_of_state(self.my_cells, eos, density_current, density_new,
                                         pressure_current, pressure_new,
                                         energy_current, energy_new, pseudo, cson_new)

        expected_energy = np.array([487.425148, 94.274747, 28.598207, 16.438778])
        expected_pressure = np.array([1.103738e+09,  -4.640087e+08,  -2.323383e+08,  -1.549395e+08])
        expected_sound_speed = np.array([4000.877516, 3926.583447, 3933.306654, 3935.541937])
        np.testing.assert_allclose(energy_new_value, expected_energy, rtol=1.e-5)
        np.testing.assert_allclose(pressure_new_value, expected_pressure, rtol=1.e-5)
        np.testing.assert_allclose(sound_velocity_new_value, expected_sound_speed)

    def test_add_elastic_energy_method(self):
        """
        Test de la m�thode add_elastic_energy_method
        """
        dt = 1.
        density_current = np.ones(self.nbr_cells) * 8930.
        density_new = np.ones(self.nbr_cells) * 8950.
        stress_dev_current = np.array([[2, -1, -1],
                                      [4,-2, -2],
                                      [10., -5., -5.],
                                      [40., -20., -20.]])
        stress_dev_new = np.array([[20., -10, -10.],
                                   [5., -2.5, -2.5],
                                   [10., -5., -5.],
                                   [40., -20., -20.]])
        strain_rate_dev = np.array([[1., -0.5, -0.5],
                                   [2., -1, -1],
                                   [3., -1.5, -1.5],
                                   [4., -2., -2.]])
        energy_new = OneDimensionCell.add_elastic_energy_method(dt, density_current, density_new,
                                                                stress_dev_current, stress_dev_new, strain_rate_dev)
        expected_energy = np.array([ 0.001846,  0.00151 ,  0.005034,  0.026846])
        np.testing.assert_allclose(energy_new, expected_energy, rtol=1.e-3)

    def test_general_method_deviator_strain_rate(self):
        """
        Test of general_method_deviator_strain_rate
        """
        mask = np.ones([self.nbr_cells], dtype=np.bool)
        mask[0] = False
        mask[1] = False
        dt = 1.
        x_new = np.array([[-0.5, ], [0.1, ], [0.2, ], [0.35, ], [0.65, ]])
        u_new = np.array([[0.1, ], [-0.05, ], [0., ], [0.2, ], [0.3, ]])
        # Reconstruction des array donn�s par la topologie
        position_new = np.array([[x_new[0], x_new[1]],
                                 [x_new[1], x_new[2]],
                                 [x_new[2], x_new[3]],
                                 [x_new[3], x_new[4]]]).reshape((4,2))
        vitesse_new = np.array([[u_new[0], u_new[1]],
                                [u_new[1], u_new[2]],
                                [u_new[2], u_new[3]],
                                [u_new[3], u_new[4]]]).reshape((4,2))
        expected_result = np.array([0., 0., 2.666667, -1.333333])
        dev_strain_rate = np.zeros(self.nbr_cells)
        dev_strain_rate[mask] = OneDimensionCell.general_method_deviator_strain_rate(mask, dt, position_new, vitesse_new)
        np.testing.assert_allclose(dev_strain_rate, expected_result, rtol=1.e-05)

    def test_compute_pseudo(self):
        """
        Test of compute_pseudo class method
        """
        rho_new = np.array([8500., 3500, 2175])
        rho_old = np.array([8700., 3200, 2171])
        new_size = np.array([0.025, 0.01, 0.005])
        sound_speed = np.array([4400, 3200, 1140])
        dt = 1.2e-08
        pseudo_a, pseudo_b = 1.2, 0.25
        result = OneDimensionCell.compute_pseudo(dt, rho_old, rho_new, new_size, sound_speed, pseudo_a, pseudo_b)
        np.testing.assert_allclose(result, [0.00000000e+00, 2.25427729e+13, 2.00897590e+09])

    def test_compute_time_step(self):
        """
        Test of compute_time_step class method
        """
        cfl, cfl_pseudo = 0.25, 0.1
        rho_new = np.array([8500., 2175., 3500.])
        rho_old = np.array([8700., 2174.9, 3200])
        new_size = np.array([0.025, 0.01, 0.005])
        sound_speed = np.array([4400., 3200., 1140.])
        pseudo_old = np.array([1.0e+09, 0.5e+08, 0.3e+08])
        pseudo_new = np.array([1.5e+09, 1.5e+08, 0.])
        result = OneDimensionCell.compute_time_step(cfl, cfl_pseudo, rho_old, rho_new, new_size, sound_speed, pseudo_old, pseudo_new)
        np.testing.assert_allclose(result, [1.41137110e-06, 7.81250000e-07, 1.09649123e-06])

if __name__ == "__main__":
    unittest.main()