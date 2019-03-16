import sys
import os

if len(sys.argv) > 1:
    
    for elem in os.listdir(sys.argv[1]):
        elem_tab = elem.split("_")
        if len(elem_tab) == 3:
            if float(elem_tab[0]) > 0.8:
                os.rename(os.path.join(sys.argv[1], elem), os.path.join(sys.argv[1], "1_"+elem_tab[1]+"_"+elem_tab[2]))
            else:
                os.rename(os.path.join(sys.argv[1], elem), os.path.join(sys.argv[1], "0_"+elem_tab[1]+"_"+elem_tab[2]))

    for elem in os.listdir(sys.argv[1]):
        elem_tab = elem.split("_")
        if len(elem_tab) == 3:
            if float(elem_tab[1]) < -0.8:
                os.rename(os.path.join(sys.argv[1], elem), os.path.join(sys.argv[1], elem_tab[0]+"_0_"+elem_tab[2]))
            elif float(elem_tab[1]) <= -0.001:
                os.rename(os.path.join(sys.argv[1], elem), os.path.join(sys.argv[1], elem_tab[0]+"_1_"+elem_tab[2]))
            elif float(elem_tab[1]) > -0.001 and float(elem_tab[1]) < 0.001:
                os.rename(os.path.join(sys.argv[1], elem), os.path.join(sys.argv[1], elem_tab[0]+"_2_"+elem_tab[2]))
            elif float(elem_tab[1]) >= 0.001 and float(elem_tab[1]) < 0.8:
                os.rename(os.path.join(sys.argv[1], elem), os.path.join(sys.argv[1], elem_tab[0]+"_3_"+elem_tab[2]))
            elif float(elem_tab[1]) > 0.8 and float(elem_tab[1]) <= 1.0:
                os.rename(os.path.join(sys.argv[1], elem), os.path.join(sys.argv[1], elem_tab[0]+"_4_"+elem_tab[2]))
