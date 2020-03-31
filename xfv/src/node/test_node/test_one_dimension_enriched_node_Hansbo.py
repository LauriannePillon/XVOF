# -*- coding: utf-8 -*-
"""
Classe de test du module OneDimensionEnrichedNode
"""
import unittest
import os
import unittest.mock as mock
import numpy as np

from xfv.src.discontinuity.discontinuity import Discontinuity
from xfv.src.node.one_dimension_enriched_node_Hansbo import OneDimensionHansboEnrichedNode
from xfv.src.data.data_container import DataContainer


class OneDimensionEnrichedNodeHansboTest(unittest.TestCase):
    """
    Test case utilis� pour test les fonctions du module 'OneDimensionHansboEnrichedNode'
    """
    def setUp(self):
        """
        Pr�paration des tests unitaires
        """
        data_file_path = os.path.join(os.path.dirname(__file__),
                                      "../../../tests/0_UNITTEST/XDATA_hydro.xml")
        self.test_datacontainer = DataContainer(data_file_path)

        self.vit_init = np.zeros([2, 1], dtype='float')
        self.vit_init[:, 0] = [1.2e+03, 0.0]
        self.poz_init = np.zeros([2, 1], dtype='float')
        self.poz_init[:, 0] = [1., 2.]
        self.my_nodes = OneDimensionHansboEnrichedNode(2, self.poz_init, self.vit_init,
                                                       section=1.0e-06)
        self.my_nodes._classical = np.array([False, False])

        # configuration d'un mock 'discontinuity'
        config = {'mask_in_nodes': np.array([True, False]),
                  'mask_out_nodes': np.array([False, True]),
                  'label': 1,
                  'position_in_ruptured_element':
                      DataContainer().material_target.failure_model.failure_treatment_value,
                  'mask_ruptured_cell': np.array([True]),
                  'ruptured_cell_id': np.array([0]),
                  'plastic_cells': False,
                  'left_part_size.current_value': np.array([0.2]),
                  'right_part_size.current_value': np.array([0.3]),
                  'left_part_size.new_value': np.array([0.4]),
                  'right_part_size.new_value': np.array([0.6]),
                  'additional_dof_force': np.array([[1., ], [2., ]]),
                  'additional_dof_density.current_value':np.array([4000.]),
                  'additional_dof_density.new_value': np.array([4020.]),
                  'additional_dof_pressure.current_value': np.array([1.1e+09]),
                  'additional_dof_pressure.new_value': np.array([1.3e+09]),
                  'additional_dof_energy.current_value': np.array([1.e+06]),
                  'additional_dof_energy.new_value': np.array([0.8e+06]),
                  'additional_dof_artificial_viscosity.current_value': np.array([1.e+08]),
                  'additional_dof_artificial_viscosity.new_value': np.array([1.e+08]),
                  'additional_dof_sound_velocity.current_value': np.array([300.]),
                  'additional_dof_sound_velocity.new_value': np.array([302.]),
                  'additional_dof_deviatoric_stress_current': np.array([[3., 2., 1.],]),
                  'additional_dof_deviatoric_stress_new': np.array([[5., 12., 7.],]),
                  'additional_dof_velocity_new': np.array([[1., ], [3., ]]),
                  'additional_dof_deviatoric_strain_rate': np.array([[4., 3., 8.],]),
                  'additional_dof_yield_stress.current_value': np.array([10.]),
                  'additional_dof_stress': np.array([[2., 0., 0.]]),
                  '_additional_dof_equivalent_plastic_strain_rate': np.array([0.]),
                  '_additional_dof_deviatoric_stress_new': np.array([[5., 12., 7.], ]),
                  '_additional_dof_velocity_new': np.zeros([2, 1])
                  # 'cohesive_force.current_value': 0.,
                  # 'cohesive_force.new_value': 0.,
                  # 'discontinuity_opening.current_value': 0.5,
                  # 'discontinuity_opening.new_value': 0.5
                  }
        patcher = mock.patch('xfv.src.discontinuity.discontinuity.Discontinuity',
                             spec=Discontinuity, **config)
        self.mock_discontinuity = patcher.start()

    def tearDown(self):
        """
        Operations to be done after completing all the tests in the class
        """
        DataContainer.clear()

    def test_classical(self):
        """
        Test de la propri�t� classical du module OneDimensionEnrichedNode
        """
        np.testing.assert_array_equal(self.my_nodes.classical, np.array([False, False]))

    def test_enriched(self):
        """
        Test de la propri�t� enriched du module OneDimensionEnrichedNode
        """
        np.testing.assert_array_equal(self.my_nodes.enriched, np.array([True, True]))

    def test_enrichment_concerned(self):
        """
        Test de la propri�t� enrichment_concerned du module
        """
        np.testing.assert_array_equal(self.my_nodes.enrichment_concerned, np.array([True, True]))

    def test_enrichment_not_concerned(self):
        """
        Test de la propri�t� enrichment_not_concerned du module
        """
        np.testing.assert_array_equal(self.my_nodes.enrichment_not_concerned,
                                      np.array([False, False]))

    def test_compute_complete_velocity_field(self):
        """
        Test de la m�thode compute_complete_velocity_field de la classe
        OneDimensionHansboEnrichedNodes
        """
        self.my_nodes._upundemi = np.array([1., 1.])
        self.my_nodes.compute_complete_velocity_field()
        np.testing.assert_array_almost_equal(self.my_nodes.velocity_field, np.array([1., 1.]))

    @mock.patch.object(Discontinuity, "discontinuity_list", new_callable=mock.PropertyMock)
    def test_enriched_nodes_compute_new_coordinates(self, mock_disc_list):
        """
        Test de la méthode enriched_nodes_compute_new_coordinates de la classe
        """
        Discontinuity.discontinuity_list.return_value = [self.mock_discontinuity]
        self.mock_discontinuity.additional_dof_coordinates_current = np.array([[1., ], [3., ]])
        self.mock_discontinuity.additional_dof_coordinates_new = np.array([[-1., ], [-3., ]])
        self.mock_discontinuity.additional_dof_velocity_new = np.array([[-3., ], [4., ]])
        self.my_nodes.enriched_nodes_compute_new_coordinates(1.)
        np.testing.assert_array_equal(self.mock_discontinuity.additional_dof_coordinates_new,
                                      np.array([[-2., ], [7., ]]))

    def test_reinitialize_kinematics_after_contact(self):
        """
        Test of the method reinitialize_kinematics_after_contact
        """
        self.mock_discontinuity.mask_disc_nodes = np.ones([2], dtype=bool)
        self.my_nodes._umundemi = np.array([[-0.5, ], [1.5, ]])
        self.my_nodes._xt = np.array([[0., ], [1., ]])
        self.my_nodes._upundemi = np.array([[-1.5, ], [2.5, ]])
        self.my_nodes._xtpdt = np.array([[2., ], [3., ]])
        self.my_nodes.reinitialize_kinematics_after_contact(self.mock_discontinuity)
        np.testing.assert_array_equal(self.my_nodes._upundemi, np.array([[-0.5, ], [1.5, ]]))
        np.testing.assert_array_equal(self.my_nodes._xtpdt, np.array([[0., ], [1., ]]))

    @mock.patch.object(Discontinuity, "discontinuity_list", new_callable=mock.PropertyMock)
    def test_enriched_nodes_new_force(self, mock_disc_list):
        """
        Test de la m�thode enriched_nodes_compute_new_force
        """
        Discontinuity.discontinuity_list.return_value = [self.mock_discontinuity]
        self.mock_discontinuity.position_in_ruptured_element = 0.25
        vecteur_contrainte_classique = np.array([2.])
        self.my_nodes._force = np.array([[4., ], [2., ]])
        self.my_nodes._section = 1.
        self.my_nodes.compute_enriched_nodes_new_force(vecteur_contrainte_classique)

        np.testing.assert_array_almost_equal(
            self.mock_discontinuity.additional_dof_force, np.array([[-0.5, ], [1.5, ]]))
        np.testing.assert_almost_equal(self.my_nodes._force, np.array([[5.5, ], [1.5, ]]))

    @unittest.skip("Mod�le coh�sif pas revu")
    @mock.patch.object(Discontinuity, "discontinuity_list", new_callable=mock.PropertyMock)
    def test_compute_enriched_nodes_cohesive_forces(self, mock_disc_list):
        """
        Test de la m�thode compute_enriched_nodes_cohesive_forces
        """
        # Test des autres cas : la discontinuit� est en train de s'ouvrir
        Discontinuity.discontinuity_list.return_value = [self.mock_discontinuity]
        self.my_nodes._force = np.array([[0., ], [0., ]])
        self.mock_discontinuity.position_in_ruptured_element = 0.25
        self.mock_discontinuity.additional_dof_force = np.array([[0., ], [0., ]])
        self.mock_discontinuity.discontinuity_opening = 0.5
        self.mock_discontinuity.cohesive_force.new_value = [0.]

        exact_force_classic = np.array([[7.5, ], [-2.5, ]])
        exact_force_enriched = np.array([[2.5, ], [-7.5, ]])

        # d�finition de ouverture old
        self.my_nodes._xt = np.array([[0., ], [1., ]])
        self.mock_discontinuity.right_part_size.current_value = np.array([0.4])
        self.mock_discontinuity.left_part_size.current_value = np.array([0.4])
        xd_old = self.my_nodes.xt[self.mock_discontinuity.mask_out_nodes] \
                 - self.mock_discontinuity.right_part_size.current_value
        xg_old = self.my_nodes.xt[self.mock_discontinuity.mask_in_nodes] + \
                 self.mock_discontinuity.left_part_size.current_value
        ouverture_ecaille_old = (xd_old - xg_old)[0][0]
        np.testing.assert_allclose(ouverture_ecaille_old, np.array([0.2]))

        # definition de ouverture new
        self.my_nodes._xtpdt = np.array([[0., ], [1., ]])
        self.mock_discontinuity.right_part_size.new_value = np.array([0.3])
        self.mock_discontinuity.left_part_size.new_value = np.array([0.3])
        xd_old = self.my_nodes.xtpdt[self.mock_discontinuity.mask_out_nodes] - \
                 self.mock_discontinuity.right_part_size.new_value
        xg_old = self.my_nodes.xtpdt[self.mock_discontinuity.mask_in_nodes] + \
                 self.mock_discontinuity.left_part_size.new_value
        ouverture_ecaille_new = (xd_old - xg_old)[0][0]
        np.testing.assert_allclose(ouverture_ecaille_new, np.array([0.4]))

        self.my_nodes.compute_enriched_nodes_cohesive_forces()

        np.testing.assert_allclose(self.my_nodes.force, exact_force_classic)
        np.testing.assert_allclose(self.mock_discontinuity.additional_dof_force,
                                   exact_force_enriched)

if __name__ == '__main__':
    unittest.main()