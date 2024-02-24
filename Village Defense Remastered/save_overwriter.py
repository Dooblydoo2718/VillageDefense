import pickle, time
from os import path
from vdtoolkit import *
text = Save(time.time())
f2 = open(r'E:\Village Defense Remastered\GameData\Data\save.dat', 'wb')
pickle.dump(text, f2)
f2.close()
