#!/usr/bin/env python2.7
# -*- coding: iso-8859-15 -*-
""" 
Generate a mesh from the data in XDATA.xml
(length of the bar, number of elements)
return : a file (table) containing the node id and its initial position
"""
import numpy as np
import os
import sys


def generate_mesh(path, user_arg):
    """
    Cr�e un fichier de maillage
    :param path: path in with the mesh file has to be created
    :param user_arg : tableau comprenant les longueurs et nb points pour les diff�rentes parties du maillage
    :return:
    """
    meshfile = path + "mesh.txt"
    with open(meshfile, 'w') as f:
        f.write('Maillage : coordonnées initiales des noeuds')
        f.write(os.linesep)
        f.write('Node Number    Coordonnée x [m]     Coordonnée y [m]     Coordonnée z [m]')
        f.write(os.linesep)
        f.write('{}         {:+10.9e}'.format(0, 0.))  # premier noeud qui est toujours situ� � x=0
        f.write(os.linesep)

    total_length = 0
    total_nb_mailles = 0
    for data in enumerate(user_arg):
        length = data[1][0]
        nb_mailles = data[1][1]
        print("length = " + str(length) + " = nb mailles " + str(nb_mailles))
        bloc = np.linspace(total_length, total_length + length, int(nb_mailles) + 1)

        with open(meshfile, 'a') as f:
            for i in range(int(nb_mailles)):
                i += 1  # astuce pour pas �crire le premier noeud (qui est d�j� �crit) pour �viter les doublons
                index_node = total_nb_mailles + i
                x = bloc[i]
                f.write('{}         {:+10.9e}'.format(index_node, x))
                f.write(os.linesep)

        total_length += length
        total_nb_mailles += int(nb_mailles)

    print("Generating mesh with {:} elements in repository {:}".format(total_nb_mailles, path))


if __name__ == '__main__':
    msg = "Script pour cr�er un fichier de maillage 1D. \n"
    msg += "On renseigne les arguments suivants :\n"
    msg += "Une liste de longueur / nombre de points pour les diff�rents blocs de maillage � cr�er\n"
    msg += "Exemple : ./generate_mesh.py base_rep 1/100 0.5/3 va cr�er un maillage dans le dossier base_rep " \
           "contenant un bloc d'1m � 100 mailles et un bloc de 50 cm � 3 mailles"

    if (len(sys.argv) < 2):
        print(msg)
        os._exit(0)

    #  Lecture des donn�es :
    path = str(sys.argv[1] + "/")
    nb_blocs = len(sys.argv) - 2  # 0eme argument = nom de la m�thode, 1er argument et rep, les donn�es commenncent � partir du 2�me argument
    user_data = np.zeros([nb_blocs, 2])

    for i in range(nb_blocs):
        arg = sys.argv[i + 2].split("/")
        user_data[i, 0] = arg[0]
        user_data[i, 1] = arg[1]

    generate_mesh(path, user_data)
    print("Done !")
