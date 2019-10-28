import os
import re

rootdir = '/home/servercentos/Desktop/EstilosDataSet'
counter = 0
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if not re.search('^([^.])+\\.(gif|jpg|jpeg|png|JPG|PNG|JPEG|GIF)$', file):
            counter += 1
            # print(subdir)
            print('             mal archivo', file)
            os.remove(os.path.join(subdir, file))
        else:
            # print(file)
            pass


print(counter)