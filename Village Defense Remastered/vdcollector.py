from os import chdir, getcwd, path
from random import choice
cwd = getcwd()
class FontCollector: # Collects fonts
    def __init__(self, Font):
        chdir(path.join(cwd, 'GameData\\Font'))
        self.font = [None]
        for i in range(1, 64):
            self.font.append(Font('minecraft.ttf', i))
        chdir(cwd)
    def __call__(self, size):
        return self.font[int(size)]
class ImageCollectorBlock: # Collects images of a certain collection
    def __init__(self, load):
        chdir(path.join(cwd, 'GameData\\Images\\block'))
        self.beacon = load('beacon.png')
        self.blast_furnace = load('blast_furnace.png')
        self.cactus = load('cactus.png')
        self.dispenser = load('dispenser.png')
        self.display = [load('cactus_display.png'),
                        load('water_display.png'),
                        load('hay_display.png'),
                        load('blast_furnace_display.png'),
                        load('dispenser_display.png'),
                        load('obsidian_display.png'),
                        load('trapdoor_display.png'),
                        load('lava_display.png'),
                        load('tnt_display.png'),
                        load('beacon_display.png')]
        self.grass = [load('grass_%d.png' % i) for i in range(9)]
        self.hay = load('hay.png')
        self.hand = [load('cactus_hand.png'),
                     load('water_hand.png'),
                     load('hay_hand.png'),
                     load('blast_furnace_hand.png'),
                     load('dispenser_hand.png'),
                     load('obsidian_hand.png'),
                     load('trapdoor_hand.png'),
                     load('lava_hand.png'),
                     load('tnt_hand.png'),
                     load('beacon_hand.png')]
        lava_raw = load('lava.png')
        self.lava = [lava_raw.subsurface([0, 32 * i, 32, 32]) for i in range(20)]
        self.obsidian = load('obsidian.png')
        self.tnt = [load('tnt.png'), load('tnt_active.png')]
        self.trapdoor = [load('trapdoor_closed.png'), load('trapdoor_open.png')]
        water_raw = load('water.png')
        self.water = [water_raw.subsurface([0, 32 * i, 32, 32]) for i in range(32)]
class ImageCollectorEffect:
    def __init__(self, load):
        chdir(path.join(cwd, 'GameData\\Images\\effect'))
        self.beam = load('beam.png')
        self.cdshade = load('cdshade.png')
        self.explosion = [load('explosion_0.png'),
                          load('explosion_1.png'),
                          load('explosion_2.png'),
                          load('explosion_3.png'),
                          load('explosion_4.png'),
                          load('explosion_5.png'),
                          load('explosion_6.png'),
                          load('explosion_7.png'),
                          load('explosion_8.png'),
                          load('explosion_9.png'),
                          load('explosion_10.png'),
                          load('explosion_11.png'),
                          load('explosion_12.png'),
                          load('explosion_13.png'),
                          load('explosion_14.png'),
                          load('explosion_15.png')]
        self.shadow = [load('shadow_0.png'),
                       load('shadow_1.png'),
                       load('shadow_2.png'),
                       load('shadow_3.png'),
                       load('shadow_4.png'),
                       load('shadow_5.png'),
                       load('shadow_6.png'),
                       load('shadow_7.png')]
class ImageCollectorEntity:
    def __init__(self, load):
        chdir(path.join(cwd, 'GameData\\Images\\entity'))
        self.skin = [((load('steve_u_0.png'),
                       load('steve_u_1.png'),
                       load('steve_u_2.png'),
                       load('steve_u_3.png'),
                       load('steve_u_4.png')),
                      (load('steve_d_0.png'),
                       load('steve_d_1.png'),
                       load('steve_d_2.png'),
                       load('steve_d_3.png'),
                       load('steve_d_4.png')),
                      (load('steve_l_0.png'),
                       load('steve_l_1.png'),
                       load('steve_l_2.png'),
                       load('steve_l_3.png'),
                       load('steve_l_4.png')),
                      (load('steve_r_0.png'),
                       load('steve_r_1.png'),
                       load('steve_r_2.png'),
                       load('steve_r_3.png'),
                       load('steve_r_4.png')),
                      )]
class ImageCollectorGui:
    def __init__(self, load):
        chdir(path.join(cwd, 'GameData\\Images\\gui'))
        self.about_icon = load('about_icon.png')
        self.achievements_icon = load('achievements_icon.png')
        self.adventure_icon = load('adventure_icon.png')
        self.bars = load('bars.png')
        self.bg = load('bg.PNG')
        self.bucket = load('bucket.png')
        self.buttons = (load('button_inactive.png'),
                        load('button_active.png'),
                        load('button_hovering.png'))
        self.clock = list(map(lambda x: load('clock_%02d.png' % x), range(64)))
        self.compass = list(map(lambda x: load('compass_%02d.png' % x), range(32)))
        self.gui_background = load('gui_background.png')
        hearts_raw = load('hearts.png')
        self.hearts = [[hearts_raw.subsurface([j * 18, i * 18, 18, 18]) for j in range(4)] for i in range(2)]
        self.inventory = load('inventory.png')
        self.inventory_selected = load('inventory_selected.png')
        self.letter_icon = load('letter_icon.png')
        self.locked = load('locked.png')
        self.menu = load('menu.png')
        self.moon = load('moon.png')
        self.paper_background = load('paper_background.png')
        self.pickaxe = load('pickaxe.png')
        self.research_icon = load('research_icon.png')
        self.resources = load('resources.png')
        self.settings_icon = load('settings_icon.png')
        self.sign = load('sign.png')
        self.statistics_icon = load('statistics_icon.png')
        self.start_icon = load('start_icon.png')
        self.sun = load('sun.png')
        self.survival_icon = load('survival_icon.png')
        self.top_bar = load('top_bar.png')
        self.weather = {
            'day':{
                'clear':load('weather_day_clear.png'),
                'rain':load('weather_day_rain.png')
            },
            'night':{
                'clear':load('weather_night_clear.png'),
                'rain':load('weather_night_rain.png')
            }
        }
        self.wip_bg = load('wip_bg.png')
        self.wizardry_icon = load('wizardry_icon.png')
class ImageCollectorMap:
    def __init__(self, load):
        chdir(path.join(cwd, 'GameData\\Images\\map'))
        self.adventure_map = load('adventure_map.png')
        self.banners = [load('banner_0.png'),
                       load('banner_1.png'),
                       load('banner_2.png'),
                       load('banner_3.png'),
                       load('banner_4.png')]
        self.cross = load('cross.png')
        self.large_town = load('large_town.png')
        self.maps = []
        for i in range(8):
            self.maps.append(list())
            for j in range(7):
                self.maps[i].append(load('map_%d_%d.png' % (i, j)))
        self.player = load('player.png')
        self.pointer = load('pointer.png')
        self.port = load('port.png')
        self.small_town = load('small_town.png')
class ImageCollectorEnv:
    def __init__(self, load):
        chdir(path.join(cwd, 'GameData\\Images\\environment'))
        self.biome_scene = {
            'day':{
                'clear':[],
                'rain':[]
            },
            'night':{
                'clear':[],
                'rain':[]
            }
        }
        for t in ('day', 'night'):
            for w in ('clear', 'rain'):
                for i in range(8):
                    self.biome_scene[t][w].append(load('biome_scene_%s_%s_%d.png' % (t, w, i)))
        self.town_scene = {
            'day':{
                'clear':[],
                'rain':[]
            },
            'night':{
                'clear':[],
                'rain':[]
            }
        }
        for t in ('day', 'night'):
            for w in ('clear', 'rain'):
                for i in range(6):
                    self.town_scene[t][w].append(load('town_scene_%s_%s_%d.png' % (t, w, i)))
class ImageMetaCollector: # Collects image collectors
    def __init__(self, load):
        self.block = ImageCollectorBlock(load)
        self.effect = ImageCollectorEffect(load)
        self.entity = ImageCollectorEntity(load)
        self.gui = ImageCollectorGui(load)
        self.map = ImageCollectorMap(load)
        self.env = ImageCollectorEnv(load)
        chdir(cwd)
class SoundGroup: # This class replaces sound groups with a single object. It has 'play' and 'set_volume' realized to work like a Sound object
    def __init__(self, *items):
        self.items = items
    def play(self):
        choice(self.items).play()
    def set_volume(self, vol):
        for item in self.items:
            item.set_volume(vol)
class SoundCollector: # Collects all sound effects or music
    def __init__(self, Sound):
        chdir(path.join(cwd, 'GameData\\Sounds'))
        self.click = Sound('click.ogg')
        self.step = [SoundGroup(*[Sound('step_0_%d.ogg' % i) for i in range(6)]),
                     ]
        self.music = {'cold':Sound('music_cold.ogg'),
                      'default':Sound('music_default.ogg'),
                      'map':Sound('music_map.ogg'),
                      'menu':Sound('music_menu.ogg'),
                      'water':Sound('music_water.ogg'),
                      'woods':Sound('music_woods.ogg')}
        self.no = SoundGroup(*[Sound('no_%d.ogg' % i) for i in range(3)])
        self.place = {
            'grass':SoundGroup(*[Sound('place_grass_%d.ogg' % i) for i in range(4)]),
            'liquid':SoundGroup(*[Sound('place_liquid_%d.ogg' % i) for i in range(3)]),
            'stone':SoundGroup(*[Sound('place_stone_%d.ogg' % i) for i in range(4)]),
            'wood':SoundGroup(*[Sound('place_wood_%d.ogg' % i) for i in range(4)])
        }
        chdir(cwd)
    def update_volume(self, settings): # Updates the volume according to the settings
        self.click.set_volume(settings['master_volume'] * settings['gui_volume'])
        for item in self.step:
            item.set_volume(settings['master_volume'] * settings['game_volume'])
        for item in self.music.values():
            item.set_volume(settings['master_volume'] * settings['music_volume'])
        self.no.set_volume(settings['master_volume'] * settings['game_volume'])
        for item in self.place.values():
            item.set_volume(settings['master_volume'] * settings['game_volume'])
class TextCollector: # Collects text files. In the future, perhaps there will be many objects of this kind, each for a certain language
    def __init__(self, load):
        chdir(path.join(cwd, 'GameData\\Text'))
        with open('menu.txt', 'rb') as f:
            self.menu = load(f)
        with open('about.txt', 'rb') as f:
            self.about = load(f)
        with open('letter.txt', 'rb') as f:
            self.letter = load(f)
        with open('map.txt', 'rb') as f:
            self.map = load(f)
        with open('choose_mode.txt', 'rb') as f:
            self.choose_mode = load(f)
        with open('wip.txt', 'rb') as f:
            self.wip = load(f)
        with open('settings.txt', 'rb') as f:
            self.settings = load(f)
        chdir(cwd)
