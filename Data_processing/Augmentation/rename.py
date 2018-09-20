import os
import sys

if len(sys.argv) == 2:
    for elem in os.listdir(sys.argv[1]):
        elem_tab = elem.split("_")
        os.rename(os.path.join(sys.argv[1], elem), os.path.join(sys.argv[1], "0_4_" + elem_tab[2]))
