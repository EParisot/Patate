from os import listdir, rename

directory = './D/'
for name in listdir(directory):
    filename = './D/' + name
    new = './' + 'D' + name
    rename(filename, new)
