import pickle, time
from os import path
from vdtoolkit import *
text = {'towns':[Town(0, 'Lake Corent City', (1875, 2372), False, 1),
                 Town(1, 'Emerald Foothills', (1320, 2178), False, 1),
                 Town(2, 'Promised Oasis', (304, 1183), False, 0),
                 Town(3, 'N.E. Outpost', (3283, 77), True, 0),
                 Town(4, 'Port of Delgray', (2191, 2137), True, 0),
                 Town(5, 'Bristlecone', (3463, 2381), False, 2),
                 Town(6, 'Acaciapolis', (2660, 2728), False, 5),
                 Town(7, 'Southern Lumberjacks\'', (2883, 2435), False, 2),
                 Town(8, 'Redstone Flatlands', (3205, 2770), False, 0),
                 Town(9, 'Lagoonville', (2174, 1113), True, 1),
                 Town(10, 'Cobblestown', (2994, 3230), False, 3),
                 Town(11, 'Chiseled County', (760, 1143), False, 3),
                 Town(12, 'Sand Town of Pers', (600, 1685), False, 3),
                 Town(13, 'Frozen Delta', (3491, 728), True, 4),
                 Town(14, 'Base Forbidden', (3511, 1795), False, 4)
                 ],
        'levels':[Level(0, 0, 1, (2050, 2300)),
                  Level(1, 1, 3, (2380, 2336)),
                  Level(2, 2, 2, (2060, 2620)),
                  Level(3, 3, 2, (1560, 2368)),
                  Level(4, 4, 4, (1332, 2613)),
                  Level(5, 5, 3, (2716, 2453)),
                  Level(6, 6, 4, (1650, 2946)),
                  Level(7, 7, 3, (1021, 2150))
                  ],
        'roads':[Road(('town', 0), ('level', 0), 1),
                 Road(('town', 0), ('level', 2), 2),
                 Road(('town', 0), ('level', 3), 2),
                 Road(('town', 1), ('level', 3), 3),
                 Road(('town', 1), ('level', 7), 6),
                 Road(('town', 4), ('level', 0), 1),
                 Road(('town', 4), ('level', 1), 2),
                 Road(('town', 6), ('level', 5), 4),
                 Road(('town', 7), ('level', 5), 2),
                 Road(('level', 1), ('level', 5), 4),
                 Road(('level', 3), ('level', 4), 5),
                 Road(('level', 4), ('level', 6), 4)
                 ]
}
text['towns'].sort(key=lambda x: x.index)
text['levels'].sort(key=lambda x: x.index)
for road in text['roads']:
    text[road.ends[0][0] + 's'][road.ends[0][1]].connections.append(road.ends[1])
    text[road.ends[1][0] + 's'][road.ends[1][1]].connections.append(road.ends[0])
f = open(r'E:\Village Defense Remastered\GameData\Data\map.dat', 'wb')
pickle.dump(text, f)
f.close()
