# -*- coding: iso-8859-1 -*-
"""
Definition of CohesiveZoneModelBase interface
"""
from abc import abstractmethod


class CohesiveZoneModelBase(object):
    """
    An interface for all cohesive zone models
    """
    def __init__(self, cohesive_law_points, unloading_model):
        """
        Construction d'un mod�le coh�sif
        :param cohesive_law_points: array describing the stress - opening curve of the
        cohesive model
        # TODO : mettre � jour data container pour construire les mod�les coh�sifs
        :param unloading_model:
        """
        self.cohesive_strength = cohesive_strength
        self.critical_separation = critical_separation
        self.unloading_model = unloading_model

    def compute_cohesive_stress(self, disc):
        """
        Compute the cohesive force for the current opening of discontinuity according to the
        current discontinuity opening
        :param disc :discontinuity
        :type disc: Discontinuity
        """
        cohesive_force = 0.
        new_opening = disc.discontinuity_opening.new_value[0]

        if disc.damage_variable.current_value[0] < 1:

            if new_opening < disc.history_max_opening:
                cohesive_force = self.compute_unloading_reloading_condition(disc, new_opening)

            elif disc.history_max_opening <= new_opening < self.critical_separation:
                cohesive_force = self.compute_cohesive_force_in_model(new_opening)
                disc.history_max_opening = max(disc.history_max_opening, new_opening)
                disc.history_min_cohesive_force = self.compute_cohesive_force_in_model(disc.history_max_opening)
                disc.damage_variable.new_value = new_opening / self.critical_separation

            if new_opening >= self.critical_separation:
                # print "Discontinuity " + str(disc.label) + "is completely open"
                disc.damage_variable.new_value = 1.
                cohesive_force = 0.
                disc.history_max_opening = max(disc.history_max_opening, new_opening)
                disc.history_min_cohesive_force = 0.

        return cohesive_force

    @abstractmethod
    def compute_cohesive_force_in_model(self, opening):
        """
        Le calcul est d�l�gu� � la loi coh�sive choisie
        :param opening:
        :return:
        """
        return 0.

    # def apply_penalty_condition(self,  disc, new_opening):
    #     """
    #     Condition de p�nalit� pour �viter que l'ouverture devienne n�gative
    #     :param disc:
    #     :return:
    #     """
    #     # ancien_opening = disc.discontinuity_opening.current_value[0]
    #     # ancien_force = disc.cohesive_force.current_value[0]
    #     ancien_opening = 0
    #     ancien_force = self.cohesive_strength
    #     return self.unloading_model.apply_penalty_condition(disc, new_opening, ancien_opening,
    #                                                                       ancien_force)
    #     # return 0.

    def compute_unloading_reloading_condition(self, disc, new_opening):
        """
        Charge / D�charge de la zone coh�sive quand on est en dessous de l'ouverture max atteinte
        :param opening: ouverture courante
        :param disc:
        :return:
        """
        # ancien_opening = disc.discontinuity_opening.current_value[0]
        # ancien_force = disc.cohesive_force.current_value[0]
        return self.unloading_model.compute_unloading_reloading_condition(disc, new_opening)