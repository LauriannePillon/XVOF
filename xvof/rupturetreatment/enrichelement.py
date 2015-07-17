#!/usr/bin/env python2.7
# -*- coding: iso-8859-1 -*-
"""
Classe d�finissant un traitement de la rupture en
enrichissant l'�l�ment et les noeuds concern�s
"""
from xvof.element.element1dupgraded import Element1dUpgraded
from xvof.node.node1dupgraded import Node1dUpgraded
from xvof.rupturetreatment.rupturetreatment import RuptureTreatment


class EnrichElement(RuptureTreatment):
    """
    Un traitement de rupture qui enrichit l'�l�ment rompu
    """
    __never_enriched = True

    def __init__(self, position_rupture):
        RuptureTreatment.__init__(self)
        self.__position_rupture = position_rupture

    def applyTreatment(self, cell, *args, **kwargs):
        if EnrichElement.__never_enriched:
            if (not isinstance(cell, Element1dUpgraded)):
                topologie = kwargs['TOPOLOGIE']
                print "<-- Enrichissement de la maille : {} -->".format(cell)
                print "    |_> Cr�ation de l'�l�ment enrichi"
                enrich_element = Element1dUpgraded(cell, self.__position_rupture)
                print "    |_> Cr�ation des noeuds enrichis"
                enrich_nodes = [Node1dUpgraded(nod) for nod in
                                topologie._getNodesBelongingToCell(enrich_element)]
                enrich_nodes = sorted(enrich_nodes, key=lambda m: m.coordt)
                enrich_nodes[0].position_relative = -1
                enrich_nodes[1].position_relative = +1
                print "    |_> Remplacement de l'�l�ment concern� dans la topologie: {}".format(enrich_element)
                topologie._changeCellType(enrich_element)
                print "    |_> Remplacement des noeuds concern�s dans la topologie: {}".format(enrich_nodes)
                for nod in enrich_nodes:
                    topologie._changeNodeType(nod)
                EnrichElement.__never_enriched = False
        kwargs["MAILLES_ROMPUES"].remove(cell)
