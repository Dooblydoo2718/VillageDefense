import pickle, random, time
from os import getcwd, path
class Saved_Level:
    def __init__(self, index):
        self.index = index
        self.completed = False
class Save:
    def __init__(self, epoch):
        self.player_loc = 0 # Lake Corent City(0)
        self.difficulty = 1
        self.cheats = False
        self.gameplay_set = False
        self.gametime = {
            'epoch':epoch,
            'time':epoch
        }
        self.weather = {
            'raining':False,
            'next':epoch + random.randint(7200, 14400)
        }
        self.levels = [
            Saved_Level(0),
            Saved_Level(1),
            Saved_Level(2),
            Saved_Level(3),
            Saved_Level(4),
            Saved_Level(5),
            Saved_Level(6),
            Saved_Level(7)
        ]
        self.unlocked = [
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True
            ]
        self.levels.sort(key=lambda x: x.index)
        self.skin = 0
    def __repr__(self):
        return 'Save([player_loc:{}, difficulty:{}, cheats:{}, gameplay_set:{}, gametime:{}, weather:{})'.format(
            self.player_loc, self.difficulty, self.cheats, self.gameplay_set, self.gametime, self.weather)
    def update_time(self):
        self.gametime['time'] = time.time()
        if self.gametime['time'] > self.weather['next']:
            if self.weather['raining']:
                self.weather['next'] = self.gametime['time'] + random.randint(1800, 27000)
            else:
                self.weather['next'] = self.gametime['time'] + random.randint(1800, 3600)
            self.weather['raining'] = not self.weather['raining']
    def update_time_now(self):
        self.gametime['time'] = time.time()
        while self.gametime['time'] > self.weather['next']:
            if self.weather['raining']:
                self.weather['next'] += random.randint(3600, 54000)
            else:
                self.weather['next'] += random.randint(3600, 10800)
            self.weather['raining'] = not self.weather['raining']
class Level:
    def __init__(self, index, biome, difficulty, coords):
        self.index = index
        self.type = 'level'
        self.biome = biome
        # Plains: 0;Forest: 1;Flower Forest: 2;Taiga: 3;Swamp: 4;
        # Roofed Forest: 5;Jungle: 6;Extreme Hills: 7;Beach: 8
        self.difficulty = difficulty
        self.coords = coords
        self.connections = []
class Town:
    def __init__(self, index, name, coords, coastal, scenery):
        self.index = index
        self.type = 'town'
        self.name = name
        self.coords = coords
        self.coastal = coastal
        self.scenery = scenery
        self.connections = []
class Road:
    def __init__(self, start, end, time):
        self.ends = [start, end]
        self.time = time
def draw_cursor(pos, screen):
    for i in range(pos[0] - 8, pos[0] + 9):
        for j in range(pos[1] - 1, pos[1] + 2):
            if not (0 <= i < screen.get_width() and (0 <= j < screen.get_height())):
                continue
            screen.set_at([i, j], [255 - k for k in screen.get_at([i, j])])
    for i in range(pos[0] - 1, pos[0] + 2):
        for j in range(pos[1] - 8, pos[1] + 9):
            if not (0 <= i < screen.get_width() and (0 <= j < screen.get_height())):
                continue
            screen.set_at([i, j], [255 - k for k in screen.get_at([i, j])])
    for i in range(pos[0] - 1, pos[0] + 2):
        for j in range(pos[1] - 1, pos[1] + 2):
            if not (0 <= i < screen.get_width() and (0 <= j < screen.get_height())):
                continue
            screen.set_at([i, j], [255 - k for k in screen.get_at([i, j])])
def draw_dashed_line(line_func, surface, color, start_pos, end_pos, width, interval):
    delta = [end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]]
    x_interval = interval * delta[0] / (delta[0] ** 2 + delta[1] ** 2) ** 0.5
    y_interval = interval * delta[1] / (delta[0] ** 2 + delta[1] ** 2) ** 0.5
    last = start_pos[:]
    for i in range(int(delta[0] / x_interval)):
        if i % 2 == 0:
            line_func(surface, color, last, [last[0] + x_interval, last[1] + y_interval], width)
        last[0] += x_interval
        last[1] += y_interval
    line_func(surface, color, last, end_pos, width)
def addnewline(string, font, length, antialias, color):
    words = string.split(' ')
    lines = []
    temp = ''
    for word in words:
        if font.render(temp + word, antialias, color).get_width() >= length:
            lines.append(font.render(temp, False, color))
            temp = word + ' '
        else:
            temp = temp + word + ' '
    lines.append(font.render(temp, False, color))
    return lines
def getbutton(width, num, buttons, Surface):
    if num >= 3 or num < 0:
        raise ValueError('Button type out of range')
    if width < 5:
        raise ValueError('Button width too small')
    res = Surface([width, buttons[0].get_height()])
    if width <= buttons[0].get_width():
        res.blit(buttons[num].subsurface([0, 0, width, buttons[0].get_height()]), [0, 0])
        res.blit(buttons[num].subsurface([buttons[0].get_width() - 2, 0, 2, buttons[0].get_height()]), [width - 2, 0])
    else:
        for i in range(0, width, 198):
            res.blit(buttons[num], [i * 198, 0])
        res.blit(buttons[num].subsurface([buttons[0].get_width() - 2, 0, 2, buttons[0].get_height()]), [width - 2, 0])
    return res
def numtotime(gametime):
    relative_time = gametime['time'] - gametime['epoch']
    d = relative_time // 7200
    h = (relative_time % 7200 // 300 + 6) % 24
    m = relative_time % 300 // 5
    return (d, h, m)
def timetoclock(d, h, m):
    t = (h * 60 + m) / 1440
    return (int(t * 64) + 32) % 64
def numtoclock(gametime):
    return timetoclock(*numtotime(gametime))
def getdaynight(gametime):
    return 'day' if 6 <= numtotime(gametime)[1] < 18 else 'night'
def getweather(save, weather):
    if save.weather['raining']:
        return weather[getdaynight(save.gametime)]['rain']
    else:
        return weather[getdaynight(save.gametime)]['clear']
def getmapobject(mapx, index):
    return mapx[index[0] + 's'][index[1]]
def getscreenpos(camera, real, scale):
    return [320 + (real[0] - camera[0]) // scale, 320 + (real[1] - camera[1]) // scale]
