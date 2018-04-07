import os

for pic in os.listdir("Tests/G"):
    print(pic)
    os.rename("Tests/G/" + pic, "Tests/1_" + pic)
for pic in os.listdir("Tests/C"):
    print(pic)
    os.rename("Tests/C/" + pic, "Tests/2_" + pic)
for pic in os.listdir("Tests/D"):
    print(pic)
    os.rename("Tests/D/" + pic, "Tests/3_" + pic)

