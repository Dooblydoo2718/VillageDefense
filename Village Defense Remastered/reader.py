import pickle
with open(r'E:\Village Defense Remastered\GameData\Text\menu.txt', 'rb') as f:
    d = pickle.load(f)
print(d)
