#!/usr/bin/env python2.7
# -*- coding: iso-8859-15 -*-
""" 
Generate a mesh from the data in XDATA.xml or XDATA_REFERENCE.xml
(length of the bar, number of elements)
return : a file (table) containing the node id and its initial position
"""
import numpy as np
import lxml.etree as et
import os

path = "0_XFEM/"
# path = "0_REFERENCE/"

# Initialization of files names
meshfile = path + "mesh.txt"
datafile_name = path + "XDATA.xml"


# Read XDATA file 
src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
datafile_path = os.path.normpath(os.path.join(src_dir, datafile_name))
print "Opening data file : {:s}".format(datafile_path)
__datadoc = et.parse(datafile_path)

# Length = float(__datadoc.find('geometry/length').text)
# NumberOfElements = int(__datadoc.find('numeric-parameters/number-of-elements').text)

Length = 25e-03
NumberOfElements = 1001

# Generate Nodes coordinates 
if path =="0_REFERENCE/" :
    # # g�n�ration des �l�ments sur la demi barre
    # Length_equiv = Length / (1-1/(2*NumberOfElements))
    # coord_init[:, 0] = np.linspace(0, Length_equiv, NumberOfElements + 1)
    # # D�calage du noeud de droite pour avoir le premier �l�ment de longueur 1/2
    # coord_init[NumberOfElements,0] += -(coord_init[NumberOfElements ,0]-coord_init[NumberOfElements-1,0])/2
    linspce = np.linspace(0, Length, NumberOfElements + 1)
    linspce = linspce[linspce < 12.5e-03]
    coord_init = np.copy(linspce)
    coord_init = np.resize(coord_init, linspce.shape[0] + 1)
    coord_init[-1] = 12.5e-03
else :
    coord_init = np.linspace(0, Length, NumberOfElements + 1)

# V�rification
print coord_init[-1] - coord_init[-2]
print coord_init[-2] - coord_init[-3]

# Write the initial coordinates in the mesh file with node identification (node number)
with open(meshfile,'w') as f :
   f.write('Maillage : coordonnées initiales des noeuds')
   f.write(os.linesep)
   f.write('Node Number    Coordonnée x [m]     Coordonnée y [m]     Coordonnée z [m]')
   f.write(os.linesep)
   for i, x in enumerate(coord_init):
      f.write('{}         {:+10.9e}'.format(i, x))
      f.write(os.linesep)

print "Done !"




