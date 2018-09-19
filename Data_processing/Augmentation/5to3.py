import os
import sys

if len(sys.argv) == 2:
    for elem in os.listdir(sys.argv[1]):
        elem_tab = elem.split("_")
        if elem_tab[1] == "1":
            os.rename(os.path.join(sys.argv[1], elem), os.path.join(sys.argv[1], elem_tab[0] + "_0_" + elem_tab[2]))

    for elem in os.listdir(sys.argv[1]):
        elem_tab = elem.split("_")
        if elem_tab[1] == "2":
            os.rename(os.path.join(sys.argv[1], elem), os.path.join(sys.argv[1], elem_tab[0] + "_1_" + elem_tab[2]))

    for elem in os.listdir(sys.argv[1]):
        elem_tab = elem.split("_")
        if elem_tab[1] == "3" or elem_tab[1] == "4":
            os.rename(os.path.join(sys.argv[1], elem), os.path.join(sys.argv[1], elem_tab[0] + "_2_" + elem_tab[2]))
