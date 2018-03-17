import os

for file in os.listdir("."):
    os.rename(file, "1_" + file)
