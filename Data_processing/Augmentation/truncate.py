import os

file_list = os.listdir("Auto")

for idx, elem in enumerate(file_list):
    os.rename("Auto/" + elem, "Auto/" + elem[2:])
