import pickle
with open(r'E:\Village Defense Remastered\GameData\Text\menu.txt', 'rb') as f:
    d = pickle.load(f)
# insert strange stuff here
d['weather'] = ('Clear', 'Rainy')
# */
with open(r'E:\Village Defense Remastered\GameData\Text\menu.txt', 'wb') as f:
    pickle.dump(d, f)
    
