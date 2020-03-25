#!/usr/bin/env python2.7
# -*- coding: iso-8859-15 -*-
""" 
Compare the time evolution of nodes and cell for xfem simulation with reference
Parameters :
    USER INPUT :
    id_item : id of the item to be studied (int)
        For 'max_diff_vs_space' : possibility to consider a list of ids : id_item = -1
            -> takes into account a list entered in the source code
    case_list : list of cases to be considered.
            case : tuple qui contient : nom du cas, simulation associ�e,
                    r�pertoire de stockage des r�sultats, label et couleur pour les graphiques
            entrer cette liste entre guillemet et sans espace. s�parateur = ','.
            case default : pour prendre les r�sultats situ�s dasn "0_XFEM"

    OTHER PARAMETERS
    save_fig, show_fig : bool�ens pour sauver et afficher les r�sultats
    id_item_list : cf id_item
    ref_case : default : mass_wilkins
"""

import os
import sys
import matplotlib.pyplot as plt

import xfv.src.figure_manager.time_figure_tools as fig_tools_path
from xfv.src.utilities.case_definition import CaseManager
from xfv.src.figure_manager.time_figure_manager import TimeFigureManager
from xfv.src.figure_manager.time_figure_tools import TimeFigureTools
from xfv.src.output_figure.profile_tools import A3_list, plot_field_from_txt_file, get_field_from_txt_file

# -----------------------------------------
# Initialize treatment and legend
# -----------------------------------------
save_fig = True
show_fig = True
file_name = "all_fields.hdf5"
extension = '.hdf5'

project_dir = os.path.split(os.path.dirname(os.path.abspath(os.path.curdir)))[0]
base_dir = os.path.split(project_dir)[0]

# -----------------------------------------
# Read user instructions
# -----------------------------------------
msg = "Mini programme pour tracer l'�volution temporelle d'un champ en un point de la barre\n" \
      "Ce script attend comme arguments  : \n"
msg += "- le type de simulation (single|compare|diff) \n"
msg += "- les champs � tracer ([X]Field, ...)\n"
msg += "- les ids des items (int, s�par�s par une virgule et sans espace) \n"
msg += "- une liste des cas � traiter (s�par�s par une virgule, sans espace | None par d�faut) \n"
msg += "- -h ou --help pour afficher l'aide\n"
msg += " Si analysis = diff : " \
    "\n \t - Le premier cas rensign� sert de r�f�rence" \
    "\n \t - On demandera une option pour savoir comment calculer l'erreur (absolue, adimensionn�e, relative)"

analysis = None

if len(sys.argv) not in [2, 5]:
    print(msg)
    exit(0)

if sys.argv[1] in ["-h", "--help"]:
    print(msg)
    exit(0)

# on lit lest arguments donn�es par l'utilisateur
try:
    analysis = sys.argv[1]
    if analysis not in ['single', 'compare', 'diff']:
        print(msg)
        print(("Type d'analysis {:s} inconnu!".format(analysis)))
        os._exit(0)

    field_list = sys.argv[2].split(',')
    field_list = [getattr(fig_tools_path, t_f) for t_f in field_list]

    id_item_list = sys.argv[3].split(',')
    id_item_list = [int(id_item) for id_item in id_item_list]

except:
    print(msg)
    raise

case_list = sys.argv[4].split(',')
case_list = [CaseManager().find_case(case) for case in case_list]
case_ref_choice = case_list[0]  # pas utile pour une comparaison single mais on a beosin d'en d�finir un quand m�me

if analysis in ['diff']:
    # Pour une courbe d'erreur, la r�f�rence est donn�e par le premier cas renseign�
    if len(case_list) < 2:
        print("Impossible de faire une analyse en erreur (diff) si il n'y a pas au moins 2 cas renseign�s")
        exit(0)
    case_ref_choice = case_list[0]
    case_list = case_list[1:]
    # On demande quel calcul d'erreur faire
    option = 1
    # option = None
    # while option not in range(3):
    #     option = input("Quelle m�thode de calcul pour l'erreur ? (0 = absolue, 1 = adimensionn�e, 2 = relative) ")



# -----------------------------------------
# Run user instruction (analysis)
# -----------------------------------------
for case in case_list:
    print("-------------------------------")
    print(case.case_name)
    item = field_list[0].application

    for field in field_list:
        print(field.title)

        for id_item in id_item_list:
            print("item : {:}".format(id_item))

            fig_manager = TimeFigureManager(case, item, id_item, data_file_name=file_name, case_ref=case_ref_choice)
            fig_tools = TimeFigureTools(case, item, id_item, data_file_name=file_name)

            if analysis == 'single':
                fig_manager.plot_single_time_figure(field)
                plt.legend(loc="best")

            elif analysis == 'diff':
                print("Reference case is {}".format(case_ref_choice.case_name))
                print("Post treating data for case : {:}".format(case.label))
                fig_manager.plot_error_vs_time(field, compute_error_index=option)
                # set_acceptance_criterion(item, id_item, 0., 5., 1.e-4)
                plt.legend(loc=4)

if show_fig:
    plt.show()




