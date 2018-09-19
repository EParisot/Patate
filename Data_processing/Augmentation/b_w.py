from PIL import Image
import os
import sys

if len(sys.argv) == 2:
    for elem in os.listdir(sys.argv[1]):
        col = Image.open(os.path.join(sys.argv[1], elem))
        gray = col.convert('L')
        #bw = gray.point(lambda x: 0 if x<128 else 255, '1')
        gray.save(os.path.join(sys.argv[1], elem))
