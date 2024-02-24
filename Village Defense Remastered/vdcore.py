import pygame
from vdtoolkit import *
from random import randint, randrange, choice, shuffle
pygame.init()
class Game:
    def __init__(self, gamesave, level, settings):
        self.arrow_keys_held = [False, False, False, False]
        self.biome = level.biome
        self.day = getdaynight(gamesave.gametime) == 'day'
        self.defense_ref = [list([None] * 20) for i in range(20)]
        self.defenses = []
        self.difficulty = (gamesave.difficulty, level.difficulty)
        self.field = Field(level.biome)
        self.gui_shown = True
        self.health = 10
        self.unlocked = gamesave.unlocked
        self.mob_ref = [list([None] * 20) for i in range(20)]
        self.mobs = []
        self.mouse_pos = [0, 0]
        self.player = Player(gamesave.skin)
        self.resources = 100
        self.settings = settings
        self.timers = {
            'hurt':0,
            'not_enough':0
            }
        self.weather = gamesave.weather['raining']
        if self.settings['graphics'] != 0:
            self.field.update((0, 0), (19, 19))
    def update(self, events, mouse_pos, fps, eff):
        if self.settings['cheat']:
            self.resources = 100
            self.health = 10
        for event in events:
            if event.type == pygame.QUIT:
                return 255
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.arrow_keys_held[0] = True
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.arrow_keys_held[1] = True
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.arrow_keys_held[2] = True
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.arrow_keys_held[3] = True
                elif pygame.K_1 <= event.key <= pygame.K_9:
                    if self.unlocked[event.key - 49]:
                        self.player.selected = event.key - 49
                elif event.key == pygame.K_0:
                    if self.unlocked[9]:
                        self.player.selected = 9
                elif event.key == pygame.K_F1:
                    self.gui_shown = not self.gui_shown
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.arrow_keys_held[0] = False
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.arrow_keys_held[1] = False
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.arrow_keys_held[2] = False
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.arrow_keys_held[3] = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pass
                elif event.button == 3:
                    if self.checkblock([int(mouse_pos[0] // 32), int(mouse_pos[1] // 32)])[0] == 0:
                        if self.player.selected == 0:
                            if self.resources >= 15:
                                self.resources -= 15
                                new = Cactus([int(mouse_pos[0] // 32), int(mouse_pos[1] // 32)])
                                self.defenses.append(new)
                                self.defense_ref[int(mouse_pos[0] // 32)][int(mouse_pos[1] // 32)] = new
                                eff.place['wood'].play()
                                self.field.elevation[new.block[0]][new.block[1]] += 1
                                if self.settings['graphics'] != 0:
                                    self.field.update((0, 0), (19, 19))
                            else:
                                self.timers['not_enough'] = 1
                                eff.no.play()
                        elif self.player.selected == 3:
                            if self.resources >= 30:
                                self.resources -= 30
                                new = Blast_Furnace([int(mouse_pos[0] // 32), int(mouse_pos[1] // 32)])
                                self.defenses.append(new)
                                self.defense_ref[int(mouse_pos[0] // 32)][int(mouse_pos[1] // 32)] = new
                                eff.place['stone'].play()
                                self.field.elevation[new.block[0]][new.block[1]] += 1
                                if self.settings['graphics'] != 0:
                                    self.field.update((0, 0), (19, 19))
                            else:
                                self.timers['not_enough'] = 1
                                eff.no.play()
                elif event.button == 4:
                    self.player.selected = (self.player.selected + 1) % 10
                    while not self.unlocked[self.player.selected]:
                        self.player.selected = (self.player.selected + 1) % 10
                elif event.button == 5:
                    self.player.selected = (self.player.selected + 9) % 10
                    while not self.unlocked[self.player.selected]:
                        self.player.selected = (self.player.selected + 9) % 10
        self.mouse_pos = mouse_pos
        for timer in self.timers.keys():
            self.timers[timer] -= 1 / fps
            if self.timers[timer] < 0:    self.timers[timer] = 0
        if self.player.passed == 0:
            blocked = -1
            if self.arrow_keys_held[0]:
                self.player.facing = 0
                blocked = self.checkblock([self.player.block[0], self.player.block[1] - 1])[0] in (1, 3, 5, 6)
            elif self.arrow_keys_held[1]:
                self.player.facing = 1
                blocked = self.checkblock([self.player.block[0], self.player.block[1] + 1])[0] in (1, 3, 5, 6)
            elif self.arrow_keys_held[2]:
                self.player.facing = 2
                blocked = self.checkblock([self.player.block[0] - 1, self.player.block[1]])[0] in (1, 3, 5, 6)
            elif self.arrow_keys_held[3]:
                self.player.facing = 3
                blocked = self.checkblock([self.player.block[0] + 1, self.player.block[1]])[0] in (1, 3, 5, 6)
            if not blocked:
                eff.step[self.getwalkingsound(self.player.block)].play()
                self.player.walk(self.getwalkingspeed(self.player.block))
        self.player.update(fps)
        for mob in self.mobs:
            if mob.type == 'zombie':
                mob.decide(difficulty, player, defenses, field)
                mob.update(fps)
        return 0
    def animate(self, screen, img, font):
        self.field.show(screen, img)
        for defense in self.defenses:
            defense.show(screen, img)
        if self.settings['graphics'] != 0:
            self.field.showshadow(screen, img)
        self.player.show(screen, img)
        if self.gui_shown:
            self.show_gui(screen, img, font)
    def show_gui(self, screen, img, font):
        if self.checkblock([int(self.mouse_pos[0] // 32), int(self.mouse_pos[1] // 32)])[0]:
            pygame.draw.rect(screen, [255, 0, 0], [self.mouse_pos[0] // 32 * 32 - 2, self.mouse_pos[1] // 32 * 32 - 2, 36, 36], 2)
        else:
            pygame.draw.rect(screen, [0, 255, 0], [self.mouse_pos[0] // 32 * 32 - 2, self.mouse_pos[1] // 32 * 32 - 2, 36, 36], 2)
        screen.blit(img.gui.inventory, [236, 0])
        for i in range(10):
            screen.blit(img.block.display[i], [242 + 40 * i, 6])
        for i in range(10):
            if not self.unlocked[i]:
                screen.blit(img.gui.locked, [241 + 40 * i, 5])
        screen.blit(img.gui.inventory_selected, [234 + 40 * self.player.selected, -2])
        for i in range(10):
            screen.blit(img.gui.hearts[self.difficulty[0] == 3][self.timers['hurt'] > 0], [8 + i * 20, 8])
        for i in range(int(self.health)):
            screen.blit(img.gui.hearts[self.difficulty[0] == 3][2], [8 + i * 20, 8])
        if self.health - int(self.health) >= 0.5:
            screen.blit(img.gui.hearts[self.difficulty[0] == 3][3], [8 + int(self.health) * 20, 8])
        screen.blit(img.gui.resources, [8, 32])
        resources_surf = font(24).render('%.1f' % self.resources, False, [255, 0, 0] if self.timers['not_enough'] > 0 else [224, 224, 224])
        screen.blit(resources_surf, [64, 56 - resources_surf.get_height() // 2])
        draw_cursor(self.mouse_pos, screen)
    def checkblock(self, block):
        if block[0] >= 20 or block[0] < 0 or block[1] >= 20 or block[1] < 0:
            return (1, None) # bound
        if block == self.player.block:
            return (2, self.player) # blocked by player
        if self.mob_ref[block[0]][block[1]] != None:
            return (3, self.mob_ref[block[0]][block[1]]) # blocked by mobs
        if self.defense_ref[block[0]][block[1]] != None:
            if self.defense_ref[block[0]][block[1]].category == 'trap':
                return (4, self.defense_ref[block[0]][block[1]]) # blocked by trap defenses
            else:
                return (5, self.defense_ref[block[0]][block[1]]) # blocked by aboveground defenses
        return (0, None) # not blocked
    def getwalkingspeed(self, block):
        if False:
            pass
        else:
            return 137.6
    def getwalkingsound(self, block):
        if not self.checkblock(block)[0] in (4, 5):
            return self.field.surface[self.player.block[0]][self.player.block[1]]
class Field:
    def __init__(self, biome):
        # surface{0:grass, 1:sand, 2:water, 3:stone, 4:snow}
        self.biome = biome
        if biome == 0:
            self.elevation = [list([0] * 20) for i in range(20)]
            self.surface = [list([0] * 20) for i in range(20)]
        self.shadow = [list([0] * 20) for i in range(20)]
        self.treetop_shadow = [list([0] * 20) for i in range(20)]
    def show(self, screen, img):
        for i in range(20):
            for j in range(20):
                if self.surface[i][j] == 0:
                    screen.blit(img.block.grass[self.biome], [i * 32, j * 32])
    def showshadow(self, screen, img):
        for i in range(20):
            for j in range(20):
                for k in range(8):
                    if (self.shadow[i][j] & (1 << k)) > 0:
                        screen.blit(img.effect.shadow[k], [i * 32, j * 32])
    def showtreetopshadow(self, screen, img):
        pass
    def update(self, topleft, bottomright):
        l, u = topleft
        r, d = bottomright
        if l < 0:    l = 0
        if u < 0:    u = 0
        if r > 19:    r = 19
        if d > 19:    d = 19
        for i in range(l, r):
            for j in range(u, d):
                self.shadow[i][j] = 0
        for i in range(l, r):
            for j in range(u, d):
                if j != u and self.elevation[i][j] > self.elevation[i][j - 1]:
                    self.shadow[i][j - 1] += 32
                if j != d and self.elevation[i][j] > self.elevation[i][j + 1]:
                    self.shadow[i][j + 1] += 2
                if i != l and self.elevation[i][j] > self.elevation[i - 1][j]:
                    self.shadow[i - 1][j] += 8
                if i != r and self.elevation[i][j] > self.elevation[i + 1][j]:
                    self.shadow[i + 1][j] += 128
                if i != l and j != u and self.elevation[i][j] > self.elevation[i - 1][j - 1]:
                    self.shadow[i - 1][j - 1] += 16
                if i != r and j != u and self.elevation[i][j] > self.elevation[i + 1][j - 1]:
                    self.shadow[i + 1][j - 1] += 64
                if i != r and j != d and self.elevation[i][j] > self.elevation[i + 1][j + 1]:
                    self.shadow[i + 1][j + 1] += 1
                if i != l and j != d and self.elevation[i][j] > self.elevation[i - 1][j + 1]:
                    self.shadow[i - 1][j + 1] += 4
        for i in range(l, r):
            for j in range(u, d):
                if self.surface[i][j] == 2:
                    self.shadow[i][j] = 0
        for i in range(l, r):
            for j in range(u, d):
                if self.shadow[i][j] & 1 > 0 and (self.shadow[i][j] & 2 > 0 or self.shadow[i][j] & 128 > 0):
                    self.shadow[i][j] -= 1
                if self.shadow[i][j] & 4 > 0 and (self.shadow[i][j] & 2 > 0 or self.shadow[i][j] & 8 > 0):
                    self.shadow[i][j] -= 4
                if self.shadow[i][j] & 16 > 0 and (self.shadow[i][j] & 8 > 0 or self.shadow[i][j] & 32 > 0):
                    self.shadow[i][j] -= 16
                if self.shadow[i][j] & 64 > 0 and (self.shadow[i][j] & 32 > 0 or self.shadow[i][j] & 128 > 0):
                    self.shadow[i][j] -= 64
class Entity:
    def __init__(self, skin, block):
        self.block = block
        self.skin = skin
        self.facing = 0
        self.passed = 0
        self.leg = 0
        self.walking_speed = 0
        self.location = self.locate()
    def locate(self):
        if self.facing == 0 or self.facing == 1:
            location = [self.block[0] * 32, self.block[1] * 32]
        elif self.facing == 2 or self.facing == 3:
            location = [self.block[0] * 32, self.block[1] * 32]
        return location
    def walk(self, walking_speed):
        self.walking_speed = walking_speed
        self.location = self.locate()
        self.leg = 1 - self.leg
        self.passed = 32
        self.block[int(1 - self.facing // 2)] += self.facing % 2 * 2 - 1
    def update(self, fps):
        if self.passed > 0:
            self.passed -= self.walking_speed / fps
            if self.facing == 0:
                self.location[1] -= self.walking_speed / fps
            elif self.facing == 1:
                self.location[1] += self.walking_speed / fps
            elif self.facing == 2:
                self.location[0] -= self.walking_speed / fps
            elif self.facing == 3:
                self.location[0] += self.walking_speed / fps
            if self.passed < 0:
                self.passed = 0
                self.walking_speed = 0
                self.location = self.locate()
class Player(Entity):
    def __init__(self, skin):
        super().__init__(skin, [8, 18])
        self.type = 'player'
        self.selected = 0
    def show(self, screen, img):
        if self.passed == 0:
            screen.blit(img.entity.skin[self.skin][self.facing][2], self.location)
        else:
            screen.blit(img.entity.skin[self.skin][self.facing][((2, 3, 4, 3), (2, 1, 0, 1))[self.leg][int((-self.passed) // 8)]], self.location)
        if self.facing == 0:
            screen.blit(img.block.hand[self.selected], [self.location[0] + 21, self.location[1] + 1])
        elif self.facing == 1:
            screen.blit(pygame.transform.rotate(img.block.hand[self.selected], 180), [self.location[0] + 3, self.location[1] + 23])
        elif self.facing == 2:
            screen.blit(pygame.transform.rotate(img.block.hand[self.selected], 90), [self.location[0] + 1, self.location[1] + 4])
        elif self.facing == 3:
            screen.blit(pygame.transform.rotate(img.block.hand[self.selected], -90), [self.location[0] + 23, self.location[1] + 21])
class Zombie(Entity):
    def __init__(self, skin, block):
        super().__init__(skin, block)
        self.type = 'zombie'
    def show(self, screen, img):
        if self.passed == 0:
            screen.blit(img.entity.zombie[self.skin][self.facing][2], self.location)
        else:
            screen.blit(img.entity.zombie[self.skin][self.facing][((2, 3, 4, 3), (2, 1, 0, 1))[self.leg][int((-self.passed) // 8)]], self.location)
    def decide(self, difficulty, player, defenses, field):
        pass
class Defense:
    def __init__(self, block, type_):
        self.block = block
        self.location = [block[0] * 32, block[1] * 32]
        self.type = type_
        self.category = 'trap' if self.type in ('water', 'trapdoor', 'lava') else 'aboveground'
        self.material = 'stone'
        self.health = 50
        if self.type in ('hay', 'tnt'):
            self.material = 'grass'
            self.health = 10
        elif self.type in ('cactus', 'trapdoor'):
            self.material = 'wood'
            self.health = 30
        elif self.type in ('water', 'lava'):
            self.material = 'liquid'
            self.health = float('inf')
        elif self.type == 'obsidian':
            self.material = 'obsidian'
            self.health = 600
class Cactus(Defense):
    def __init__(self, block):
        super().__init__(block, 'cactus')
    def show(self, screen, img):
        screen.blit(img.block.cactus, self.location)
class Blast_Furnace(Defense):
    def __init__(self, block):
        super().__init__(block, 'Blast_Furnace')
    def show(self, screen, img):
        screen.blit(img.block.blast_furnace, self.location)
