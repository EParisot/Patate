import sys
import srcs.color as c
from srcs.photos import Photos

# python3 label.py photos_srcs photos_label trash 1

if not len(sys.argv) in (2, 3):
    print('Usage: python3 label.py <photos> [auto_next=[01]]')
    exit(0)

if len(sys.argv) == 2:
    p = Photos(sys.argv[1] + '/')
else:
    p = Photos(sys.argv[1] + '/', False if sys.argv[2] == '0' else True)

p.load()
p.init_win()
