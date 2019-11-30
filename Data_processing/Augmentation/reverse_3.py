import os
import sys
from PIL import Image

if len(sys.argv) > 1:
    for elem in os.listdir(sys.argv[1]):
        elem_tab = elem.split("_")
        if len(elem_tab) == 2:
            img = Image.open(os.path.join(sys.argv[1], elem))
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
            if elem_tab[0] == "0":
                elem_tab[0] = "2"
            elif elem_tab[0] == "1":
                elem_tab[0] = "1"
            elif elem_tab[0] == "2":
                elem_tab[0] = "0"
            img.save(os.path.join(sys.argv[1], elem_tab[0] + "_r" + elem_tab[1]))
            
    
