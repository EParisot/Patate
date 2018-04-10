import os

for img in os.listdir('.'):
    os.rename(img, ('_'.join(img.split('_')[1:])))

# move
# rm -rf photos_label/*; rm -rf  photos_srcs/*; rm -rf trash/*; cp cpy_photos_srcs/* photos_srcs
