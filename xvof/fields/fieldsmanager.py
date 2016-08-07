# -*- coding: iso-8859-1 -*-
"""
Implementing field manager class

:todo: Use Singleton metaclass
"""
import os
from collections import OrderedDict

from xvof.fields.enrichedfield import EnrichedField
from xvof.utilities.singleton import Singleton


class FieldManager(OrderedDict):
    """
    Field manager class
    """
    __metaclass__ = Singleton

    def __init__(self):
        super(FieldManager, self).__init__()

    def __setitem__(self, key, value):
        """
        Set a field in the manager if the field doesn't yey exist or if it is an enriched field

        :param key: name of the field
        :param value: Field object
        """
        if key not in self.keys() or isinstance(value, EnrichedField) and not isinstance(self[key], EnrichedField):
            super(FieldManager, self).__setitem__(key, value)
        else:
            raise KeyError("Le champ {:s} existe d�j� dans le gestionnaire!".format(key))

    def __str__(self):
        """
        :return: informations about the contents of the manager
        """
        msg = "FieldManager contents :" + os.linesep
        msg += os.linesep.join(("{:s} <-> {:s}".format(name, field) for name, field in self.items()))
        return msg

    def moveClassicalToEnrichedFields(self, size):
        """
        Turn all classical fields into enriched ones
        """
        for name, field in self.items():
            self[name] = EnrichedField(size, field.current_value, field.new_value)

    def incrementFields(self):
        """
        Increment all the fields registered in the manager
        """
        for field in self.values():
            field.incrementValues()
