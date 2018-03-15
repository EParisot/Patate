import sys
import srcs.color as c
from srcs.photos import Photos

# python3 label.py photos_srcs photos_label trash 1

if not len(sys.argv) in (3, 4, 5):
    print('Usage: python3 label.py <photos> <labelised photos> [trash=\'trash\'] [auto_next=[01]]')
    exit(0)

if len(sys.argv) == 3:
    p = Photos(sys.argv[1] + '/', sys.argv[2] + '/')
elif len(sys.argv) == 4:
    p = Photos(sys.argv[1] + '/', sys.argv[2] + '/', sys.argv[3] + '/')
else:
    p = Photos(sys.argv[1] + '/', sys.argv[2] + '/', sys.argv[3] + '/', True if sys.argv[4] == '1' else False)

p.load()
p.init_win()
