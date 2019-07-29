import os
import zipfile
mypath = "C:/Users/lucas/Downloads/Programacao/python/Pokemon/Pokemon Pictures"
import shutil

folders = []
for r,d,f in os.walk(mypath):
    for folder in d:
        folders.append(folder)

for folder in folders:

        shutil.make_archive(folder, 'zip', folder)


