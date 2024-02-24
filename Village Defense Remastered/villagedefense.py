# Remember the following:
# Anything about direction follows the order: up, down, left, right
import pygame, sys, math, pickle, time, math
from vdtoolkit import *
from vdcore import *
from vdcollector import *
from os import chdir, getcwd, path
from random import randint, randrange, choice, shuffle
pygame.init()
screen = pygame.display.set_mode([640, 640])
pygame.display.set_caption('Village Defense Remastered - Beta 0.1.0')
pygame.mouse.set_visible(False)
cwd = getcwd()
icon = pygame.image.load(path.join(cwd, 'GameData\\Icon\\icon.png'))
pygame.display.set_icon(icon)
version = (True, 0, 1, 0)
chdir(path.join(cwd, 'GameData\\Data'))
with open('map.dat', 'rb') as f:
    adventure_map = pickle.load(f)
with open('settings.dat', 'rb') as f: # Uploads settings
    settings = pickle.load(f)
with open('save.dat', 'rb') as f: # Uploads save
    save = pickle.load(f)
    save.update_time_now()
chdir(cwd)
font = FontCollector(pygame.font.Font)
_bg = pygame.image.load(path.join(cwd, 'GameData\\Images\\gui\\bg.png'))
_loading_text = font(32).render('Loading...', False, [255, 255, 255])
screen.blit(_bg, [0, 0])
screen.blit(_loading_text, [320 - _loading_text.get_width() // 2, 320 - _loading_text.get_height() // 2])
pygame.display.flip()
img = ImageMetaCollector(pygame.image.load)
eff = SoundCollector(pygame.mixer.Sound)
eff.update_volume(settings)
txt = TextCollector(pickle.load)
def restart_progress(): # Replaces the game files containing the player's progress with empty(default) ones
    global settings, save
    settings['gameplay_set'] = False
    chdir(path.join(cwd, 'GameData\\Data'))
    save = Save(time.time())
    chdir(cwd)
def menu_loop(): # The loop for the main menu(not including other specific pages, just the main page)
    global mouse_pos, fps, music
    if music != 'menu':
        eff.music[music].stop()
        music = 'menu'
        eff.music[music].play(-1)
    title_surf = font(36).render(txt.menu['title'], False, [255, 255, 255])
    subtitle_surf = pygame.transform.rotate(font(18).render(txt.menu['subtitle'], False, [255, 0, 0]), 20)
    ver_surf = font(16).render(txt.menu['version'].format(*(version[1:])) + ' Beta' if version[0] else '', False, [255, 255, 255])
    letter_surf = font(16).render(txt.menu['letter_title'], False, [255, 255, 255])
    about_surf = font(16).render(txt.menu['about_title'], False, [255, 255, 255])
    achievements_surf = font(16).render(txt.menu['achievements_title'], False, [255, 255, 255])
    start_surf = font(16).render(txt.menu['start_title'], False, [255, 255, 255])
    wizardry_surf = font(16).render(txt.menu['wizardry_title'], False, [255, 255, 255])
    research_surf = font(16).render(txt.menu['research_title'], False, [255, 255, 255])
    settings_surf = font(16).render(txt.menu['settings_title'], False, [255, 255, 255])
    statistics_surf = font(16).render(txt.menu['statistics_title'], False, [255, 255, 255])
    letter_surf_active = font(16).render(txt.menu['letter_title'], False, [0, 255, 0])
    about_surf_active = font(16).render(txt.menu['about_title'], False, [0, 255, 0])
    achievements_surf_active = font(16).render(txt.menu['achievements_title'], False, [0, 255, 0])
    start_surf_active = font(16).render(txt.menu['start_title'], False, [0, 255, 0])
    wizardry_surf_active = font(16).render(txt.menu['wizardry_title'], False, [0, 255, 0])
    research_surf_active = font(16).render(txt.menu['research_title'], False, [0, 255, 0])
    settings_surf_active = font(16).render(txt.menu['settings_title'], False, [0, 255, 0])
    statistics_surf_active = font(16).render(txt.menu['statistics_title'], False, [0, 255, 0]) # Renders the text surfs
    return_value = -1
    running = True
    about_rect = pygame.Rect([(640 - about_surf.get_width()) // 2 - 150, 250], [about_surf.get_width(), about_surf.get_height()])
    start_rect = pygame.Rect([(640 - start_surf.get_width()) // 2 + 150, 250], [start_surf.get_width(), start_surf.get_height()])
    letter_rect = pygame.Rect([(640 - letter_surf.get_width()) // 2 - 150, 300], [letter_surf.get_width(), letter_surf.get_height()])
    achievements_rect = pygame.Rect([(640 - achievements_surf.get_width()) // 2 + 150, 300], [achievements_surf.get_width(), achievements_surf.get_height()])
    research_rect = pygame.Rect([(640 - research_surf.get_width()) // 2 - 150, 350], [research_surf.get_width(), research_surf.get_height()])
    wizardry_rect = pygame.Rect([(640 - wizardry_surf.get_width()) // 2 + 150, 350], [wizardry_surf.get_width(), wizardry_surf.get_height()])
    statistics_rect = pygame.Rect([(640 - statistics_surf.get_width()) // 2 - 150, 400], [statistics_surf.get_width(), statistics_surf.get_height()])
    settings_rect = pygame.Rect([(640 - settings_surf.get_width()) // 2 + 150, 400], [settings_surf.get_width(), settings_surf.get_height()]) # Saves the rects for each button
    about_active = achievements_active = start_active = wizardry_active = research_active = settings_active = letter_active = statistics_active = False # Stores the status of each button(hovering or not)
    while running:
        clock.tick(settings['max_framerate'])
        fps = clock.get_fps() if clock.get_fps() > 0 else 1
        fps_surf = font(16).render(txt.menu['fps'] % fps, False, [255, 255, 255]) # Gets the FPS value and updates the fps surf
        save.update_time()
        clock_surf = font(16).render(txt.menu['time'] % numtotime(save.gametime), False, [255, 255, 255])
        mouse_surf = font(16).render(txt.menu['mouse_pos'] % tuple(mouse_pos), False, [255, 255, 255])
        weather_surf = font(16).render(txt.menu['weather'][save.weather['raining']], False, [255, 255, 255])
        est_weather_surf = font(16).render(txt.menu['est_weather'] %
                                           (txt.menu['weather'][0] if save.weather['raining'] else txt.menu['weather'][1],
                                           (save.weather['next'] - save.gametime['time']) // 7200,
                                           (save.weather['next'] - save.gametime['time']) % 7200 / 300),
                                           False, [255, 255, 255])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return_value = 255
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if about_active:
                    eff.click.play()
                    return_value = 1
                    running = False
                elif start_active:
                    eff.click.play()
                    return_value = 2
                    running = False
                elif letter_active:
                    eff.click.play()
                    return_value = 3
                    running = False
                elif achievements_active:
                    eff.click.play()
                    return_value = 4
                    running = False
                elif research_active:
                    eff.click.play()
                    return_value = 5
                    running = False
                elif wizardry_active:
                    eff.click.play()
                    return_value = 6
                    running = False
                elif statistics_active:
                    eff.click.play()
                    return_value = 7
                    running = False
                elif settings_active:
                    eff.click.play()
                    return_value = 8
                    running = False # Ends the loop and returns the corresponding value for each page. See more in the main loop
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(img.gui.bg, [0, 0])
        screen.blit(title_surf, [180, 100])
        screen.blit(subtitle_surf, [450, 110])
        screen.blit(ver_surf, [630 - ver_surf.get_width(), 610])
        screen.blit(fps_surf, [630 - fps_surf.get_width(), 30])
        screen.blit(img.gui.clock[numtoclock(save.gametime)], [10, 10])
        screen.blit(clock_surf, [30, 10])
        screen.blit(getweather(save, img.gui.weather), [10, 30])
        screen.blit(weather_surf, [30, 30])
        screen.blit(est_weather_surf, [100, 30])
        screen.blit(mouse_surf, [630 - mouse_surf.get_width(), 10])
        screen.blit(img.gui.about_icon, [about_rect.left - 25, about_rect.top])
        screen.blit(about_surf_active if about_active else about_surf, about_rect.topleft)
        screen.blit(img.gui.achievements_icon, [achievements_rect.left - 25, achievements_rect.top])
        screen.blit(achievements_surf_active if achievements_active else achievements_surf, achievements_rect.topleft)
        screen.blit(img.gui.start_icon, [start_rect.left - 25, start_rect.top])
        screen.blit(start_surf_active if start_active else start_surf, start_rect.topleft)
        screen.blit(img.gui.wizardry_icon, [wizardry_rect.left - 25, wizardry_rect.top])
        screen.blit(wizardry_surf_active if wizardry_active else wizardry_surf, wizardry_rect.topleft)
        screen.blit(img.gui.research_icon, [research_rect.left - 25, research_rect.top])
        screen.blit(research_surf_active if research_active else research_surf, research_rect.topleft)
        screen.blit(img.gui.settings_icon, [settings_rect.left - 25, settings_rect.top])
        screen.blit(settings_surf_active if settings_active else settings_surf, settings_rect.topleft)
        screen.blit(img.gui.letter_icon, [letter_rect.left - 25, letter_rect.top])
        screen.blit(letter_surf_active if letter_active else letter_surf, letter_rect.topleft)
        screen.blit(img.gui.statistics_icon, [statistics_rect.left - 25, statistics_rect.top])
        screen.blit(statistics_surf_active if statistics_active else statistics_surf, statistics_rect.topleft)
        draw_cursor(mouse_pos, screen) # Renders the page
        about_active = about_rect.collidepoint(mouse_pos)
        achievements_active = achievements_rect.collidepoint(mouse_pos)
        start_active = start_rect.collidepoint(mouse_pos)
        wizardry_active = wizardry_rect.collidepoint(mouse_pos)
        research_active = research_rect.collidepoint(mouse_pos)
        settings_active = settings_rect.collidepoint(mouse_pos)
        letter_active = letter_rect.collidepoint(mouse_pos)
        statistics_active = statistics_rect.collidepoint(mouse_pos) # Test if the buttons are hovered
        pygame.display.flip()
    return return_value
def about_page(): # The page containing some information about the game
    global mouse_pos, fps, music
    if music != 'menu':
        eff.music[music].stop()
        music = 'menu'
        eff.music[music].play(-1)
    title_surf = font(36).render(txt.menu['about_title'], False, [0, 0, 0])
    ver_surf = font(24).render(txt.menu['version'].format(*(version[1:])) + ' Beta' if version[0] else '', False, [0, 0, 0])
    text_surfs = addnewline(txt.about['text'], font(16), 525, False, [0, 0, 0]) # The 'addnewline' function splits a long piece of text into lines and renders them. Usage in 'vdtoolkit.py'
    back_surf = font(24).render(txt.menu['back'], False, [0, 0, 0])
    back_surf_active = font(24).render(txt.menu['back'], False, [0, 255, 0])
    back_rect = pygame.Rect([75, 75], [back_surf.get_width(), back_surf.get_height()])
    back_active = False
    return_value = -1
    running = True
    while running:
        clock.tick(settings['max_framerate'])
        fps = clock.get_fps() if clock.get_fps() > 0 else 1
        fps_surf = font(16).render(txt.menu['fps'] % fps, False, [255, 255, 255])
        save.update_time()
        clock_surf = font(16).render(txt.menu['time'] % numtotime(save.gametime), False, [255, 255, 255])
        mouse_surf = font(16).render(txt.menu['mouse_pos'] % tuple(mouse_pos), False, [255, 255, 255])
        weather_surf = font(16).render(txt.menu['weather'][save.weather['raining']], False, [255, 255, 255])
        est_weather_surf = font(16).render(txt.menu['est_weather'] %
                                           (txt.menu['weather'][0] if save.weather['raining'] else txt.menu['weather'][1],
                                           (save.weather['next'] - save.gametime['time']) // 7200,
                                           (save.weather['next'] - save.gametime['time']) % 7200 / 300),
                                           False, [255, 255, 255])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return_value = 255
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_active:
                    eff.click.play()
                    return_value = 0
                    running = False
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(img.gui.bg, [0, 0])
        screen.blit(img.gui.paper_background, [32, 32])
        screen.blit(fps_surf, [630 - fps_surf.get_width(), 30])
        screen.blit(img.gui.clock[numtoclock(save.gametime)], [10, 10])
        screen.blit(clock_surf, [30, 10])
        screen.blit(getweather(save, img.gui.weather), [10, 30])
        screen.blit(weather_surf, [30, 30])
        screen.blit(est_weather_surf, [100, 30])
        screen.blit(mouse_surf, [630 - mouse_surf.get_width(), 10])
        screen.blit(title_surf, [(640 - title_surf.get_width()) // 2, 75])
        screen.blit(ver_surf, [(640 - ver_surf.get_width()) // 2, 120])
        screen.blit(back_surf_active if back_active else back_surf, back_rect.topleft)
        for i in range(len(text_surfs)):
            screen.blit(text_surfs[i], [75, 150 + i * 30])
        draw_cursor(mouse_pos, screen)
        back_active = back_rect.collidepoint(mouse_pos)
        pygame.display.flip()
    return return_value
def letter_from_doge(): # The page containing Doge's(my) letter
    global mouse_pos, fps, music
    if music != 'menu':
        eff.music[music].stop()
        music = 'menu'
        eff.music[music].play(-1)
    title_surf = font(36).render(txt.menu['letter_title'], False, [0, 0, 0])
    signature_surf = font(16).render(txt.letter['signature'], False, [0, 0, 0])
    text_surfs = addnewline(txt.letter['text'], font(16), 525, False, [0, 0, 0]) # The 'addnewline' function splits a long piece of text into lines and renders them. Usage in 'vdtoolkit.py'
    back_surf = font(24).render(txt.menu['back'], False, [0, 0, 0])
    back_surf_active = font(24).render(txt.menu['back'], False, [0, 255, 0])
    back_rect = pygame.Rect([75, 75], [back_surf.get_width(), back_surf.get_height()])
    back_active = False
    return_value = -1
    running = True
    while running:
        clock.tick(settings['max_framerate'])
        fps = clock.get_fps() if clock.get_fps() > 0 else 1
        fps_surf = font(16).render(txt.menu['fps'] % fps, False, [255, 255, 255])
        save.update_time()
        clock_surf = font(16).render(txt.menu['time'] % numtotime(save.gametime), False, [255, 255, 255])
        mouse_surf = font(16).render(txt.menu['mouse_pos'] % tuple(mouse_pos), False, [255, 255, 255])
        weather_surf = font(16).render(txt.menu['weather'][save.weather['raining']], False, [255, 255, 255])
        est_weather_surf = font(16).render(txt.menu['est_weather'] %
                                           (txt.menu['weather'][0] if save.weather['raining'] else txt.menu['weather'][1],
                                           (save.weather['next'] - save.gametime['time']) // 7200,
                                           (save.weather['next'] - save.gametime['time']) % 7200 / 300),
                                           False, [255, 255, 255])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return_value = 255
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_active:
                    eff.click.play()
                    return_value = 0
                    running = False
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(img.gui.bg, [0, 0])
        screen.blit(img.gui.paper_background, [32, 32])
        screen.blit(fps_surf, [630 - fps_surf.get_width(), 30])
        screen.blit(img.gui.clock[numtoclock(save.gametime)], [10, 10])
        screen.blit(clock_surf, [30, 10])
        screen.blit(getweather(save, img.gui.weather), [10, 30])
        screen.blit(weather_surf, [30, 30])
        screen.blit(est_weather_surf, [100, 30])
        screen.blit(mouse_surf, [630 - mouse_surf.get_width(), 10])
        screen.blit(title_surf, [(640 - title_surf.get_width()) // 2, 125])
        screen.blit(back_surf_active if back_active else back_surf, back_rect.topleft)
        for i in range(len(text_surfs)):
            screen.blit(text_surfs[i], [75, 200 + i * 24])
        screen.blit(signature_surf, [540 - signature_surf.get_width(), 200 + len(text_surfs) * 24])
        draw_cursor(mouse_pos, screen)
        back_active = back_rect.collidepoint(mouse_pos)
        pygame.display.flip()
    return return_value
def wip_page(default_return): # The page taking the page of (maybe) future features
    global mouse_pos, fps, music
    if music != 'menu':
        eff.music[music].stop()
        music = 'menu'
        eff.music[music].play(-1)
    title_surf = font(36).render(txt.wip['title'], False, [255, 255, 0])
    subtitle_surf = font(24).render(txt.wip['subtitle'], False, [255, 255, 0])
    text_surfs = addnewline(txt.wip['text'], font(16), 550, False, [255, 255, 0])
    fps_surf = font(16).render(txt.menu['fps'] % fps, False, [255, 255, 255])
    back_surf = font(24).render(txt.menu['back'], False, [0, 0, 0])
    back_surf_active = font(24).render(txt.menu['back'], False, [0, 255, 0])
    back_rect = pygame.Rect([75, 75], [back_surf.get_width(), back_surf.get_height()])
    back_active = False
    return_value = -1
    running = True
    while running:
        clock.tick(settings['max_framerate'])
        fps = clock.get_fps() if clock.get_fps() > 0 else 1
        fps_surf = font(16).render(txt.menu['fps'] % fps, False, [255, 255, 255])
        mouse_surf = font(16).render(txt.menu['mouse_pos'] % tuple(mouse_pos), False, [255, 255, 255])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return_value = 255
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_active:
                    eff.click.play()
                    return_value = default_return
                    running = False
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(img.gui.wip_bg, [0, 0])
        screen.blit(title_surf, [(640 - title_surf.get_width()) // 2, 100])
        screen.blit(subtitle_surf, [(640 - subtitle_surf.get_width()) // 2, 150])
        screen.blit(fps_surf, [630 - fps_surf.get_width(), 30])
        screen.blit(mouse_surf, [630 - mouse_surf.get_width(), 10])
        screen.blit(back_surf_active if back_active else back_surf, back_rect.topleft)
        for i in range(len(text_surfs)):
            screen.blit(text_surfs[i], [75, 200 + i * 24])
        draw_cursor(mouse_pos, screen)
        back_active = back_rect.collidepoint(mouse_pos)
        pygame.display.flip()
    return return_value
def choose_game_mode(): # The page for choosing which mode you're going to play on
    global mouse_pos, settings, fps, music
    if music != 'menu':
        eff.music[music].stop()
        music = 'menu'
        eff.music[music].play(-1)
    back_surf = font(24).render(txt.menu['back'], False, [255, 255, 255])
    back_surf_active = font(24).render(txt.menu['back'], False, [0, 255, 0])
    back_rect = pygame.Rect([75, 75], [back_surf.get_width(), back_surf.get_height()])
    title_surf = font(36).render(txt.choose_mode['title'], False, [255, 255, 255])
    adventure_title = font(24).render(txt.choose_mode['adventure'], False, [255, 255, 255])
    survival_title = font(24).render(txt.choose_mode['survival'], False, [255, 255, 255])
    adventure_desc = [font(16).render(tmp, False, [255, 255, 255]) for tmp in txt.choose_mode['adventure_desc']] # Iterates and renders the lines of text for decription
    survival_desc = [font(16).render(tmp, False, [255, 255, 255]) for tmp in txt.choose_mode['survival_desc']]
    adventure_title_shade = font(24).render(txt.choose_mode['adventure'], False, [0, 0, 0])
    survival_title_shade = font(24).render(txt.choose_mode['survival'], False, [0, 0, 0])
    adventure_desc_shade = [font(16).render(tmp, False, [0, 0, 0]) for tmp in txt.choose_mode['adventure_desc']]
    survival_desc_shade = [font(16).render(tmp, False, [0, 0, 0]) for tmp in txt.choose_mode['survival_desc']] # The '_shade' surfs act like a shade on the lower-right of test surfs
    adventure_rect = pygame.Rect([30, 180, 600, 190])
    survival_rect = pygame.Rect([30, 380, 600, 190])
    back_active = False
    adventure_active = False
    survival_active = False
    running = True
    return_value = -1
    while running:
        clock.tick(settings['max_framerate'])
        fps = clock.get_fps() if clock.get_fps() > 0 else 1
        fps_surf = font(16).render(txt.menu['fps'] % fps, False, [255, 255, 255])
        save.update_time()
        clock_surf = font(16).render(txt.menu['time'] % numtotime(save.gametime), False, [255, 255, 255])
        mouse_surf = font(16).render(txt.menu['mouse_pos'] % tuple(mouse_pos), False, [255, 255, 255])
        weather_surf = font(16).render(txt.menu['weather'][save.weather['raining']], False, [255, 255, 255])
        est_weather_surf = font(16).render(txt.menu['est_weather'] %
                                           (txt.menu['weather'][0] if save.weather['raining'] else txt.menu['weather'][1],
                                           (save.weather['next'] - save.gametime['time']) // 7200,
                                           (save.weather['next'] - save.gametime['time']) % 7200 / 300),
                                           False, [255, 255, 255])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return_value = 255
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_active:
                    eff.click.play()
                    return_value = 0
                    running = False
                elif adventure_active:
                    eff.click.play()
                    return_value = 16 # Adventure page
                    running = False
                elif survival_active:
                    eff.click.play()
                    return_value = 17 # Survival page (currently a WIP page)
                    running = False
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(img.gui.bg, [0, 0])
        screen.blit(title_surf, [(640 - title_surf.get_width()) // 2, 120])
        screen.blit(fps_surf, [630 - fps_surf.get_width(), 30])
        screen.blit(img.gui.clock[numtoclock(save.gametime)], [10, 10])
        screen.blit(clock_surf, [30, 10])
        screen.blit(getweather(save, img.gui.weather), [10, 30])
        screen.blit(weather_surf, [30, 30])
        screen.blit(est_weather_surf, [100, 30])
        screen.blit(mouse_surf, [630 - mouse_surf.get_width(), 10])
        screen.blit(img.gui.adventure_icon, [50, 200])
        screen.blit(adventure_title_shade, [251, 201])
        screen.blit(adventure_title, [250, 200])
        for i in range(len(adventure_desc)):
            screen.blit(adventure_desc_shade[i], [251, 251 + i * 30])
            screen.blit(adventure_desc[i], [250, 250 + i * 30])
        if adventure_active:    pygame.draw.rect(screen, [255, 255, 255], adventure_rect, 2)
        screen.blit(img.gui.survival_icon, [50, 400])
        screen.blit(survival_title_shade, [251, 401])
        screen.blit(survival_title, [250, 400])
        for i in range(len(survival_desc)):
            screen.blit(survival_desc_shade[i], [251, 451 + i * 30])
            screen.blit(survival_desc[i], [250, 450 + i * 30])
        if survival_active:    pygame.draw.rect(screen, [255, 255, 255], survival_rect, 2)
        screen.blit(back_surf_active if back_active else back_surf, back_rect.topleft)
        draw_cursor(mouse_pos, screen)
        back_active = back_rect.collidepoint(mouse_pos)
        adventure_active = adventure_rect.collidepoint(mouse_pos)
        survival_active = survival_rect.collidepoint(mouse_pos)
        pygame.display.flip()
    return return_value
def settings_page(): # The settings page! Took me a ton of time :(
    global mouse_pos, settings, fps, music
    if music != 'menu':
        eff.music[music].stop()
        music = 'menu'
        eff.music[music].play(-1)
    title_surf = font(36).render(txt.menu['settings_title'], False, [255, 255, 255])
    fps_surf = font(16).render(txt.menu['fps'] % fps, False, [255, 255, 255])
    back_surf = font(24).render(txt.menu['back'], False, [255, 255, 255])
    back_surf_active = font(24).render(txt.menu['back'], False, [0, 255, 0])
    back_rect = pygame.Rect([75, 75], [back_surf.get_width(), back_surf.get_height()])
    ma_vol_surf = font(16).render(txt.settings['master_volume'] % int(settings['master_volume'] * 100), False, [255, 255, 255])
    gu_vol_surf = font(16).render(txt.settings['gui_volume'] % int(settings['gui_volume'] * 100), False, [255, 255, 255])
    ga_vol_surf = font(16).render(txt.settings['game_volume'] % int(settings['game_volume'] * 100), False, [255, 255, 255])
    mu_vol_surf = font(16).render(txt.settings['music_volume'] % int(settings['music_volume'] * 100), False, [255, 255, 255])
    framerate_surf = font(16).render(txt.settings['max_framerate'] % settings['max_framerate'], False, [255, 255, 255])
    graphics_surf = font(16).render(txt.settings['graphics'][settings['graphics']], False, [255, 255, 255])
    difficulty_surf = font(16).render(txt.settings['difficulty'][settings['difficulty']], False, [255, 255, 255])
    difficulty_desc_surf = font(12).render(txt.settings['difficulty_desc'][settings['difficulty']], False, [255, 255, 255])
    difficulty_desc_shade_surf = font(12).render(txt.settings['difficulty_desc'][settings['difficulty']], False, [63, 63, 63])
    cheat_surf = font(16).render(txt.settings['cheat'][settings['cheat']], False, [255, 255, 255])
    cheat_desc_surf = font(12).render(txt.settings['cheat_desc'][settings['cheat']], False, [255, 255, 255])
    cheat_desc_shade_surf = font(12).render(txt.settings['cheat_desc'][settings['cheat']], False, [63, 63, 63])
    sound_section_surf = font(16).render(txt.settings['sound_section'], False, [255, 255, 255])
    video_section_surf = font(16).render(txt.settings['video_section'], False, [255, 255, 255])
    gameplay_section_surf = font(16).render(txt.settings['gameplay_section'], False, [255, 255, 255])
    sound_section_shade_surf = font(16).render(txt.settings['sound_section'], False, [63, 63, 63])
    video_section_shade_surf = font(16).render(txt.settings['video_section'], False, [63, 63, 63])
    gameplay_section_shade_surf = font(16).render(txt.settings['gameplay_section'], False, [63, 63, 63])
    gameplay_warning_surfs = addnewline(txt.settings['gameplay_warning'], font(12), 400, False, [255, 0, 0])
    restart_surf = font(16).render(txt.settings['restart'], False, [255, 255, 255])
    restart_slider_surf = font(16).render(txt.settings['restart_hint'], False, [255, 255, 255])
    apply_surf = font(16).render(txt.settings['apply'], False, [255, 255, 255])
    volume_slider_rail = getbutton(250, 0, img.gui.buttons, pygame.Surface)
    volume_slider = getbutton(15, 1, img.gui.buttons, pygame.Surface)
    volume_slider_active = getbutton(15, 2, img.gui.buttons, pygame.Surface)
    apply_button_pressed = getbutton(100, 0, img.gui.buttons, pygame.Surface)
    apply_button = getbutton(100, 1,  img.gui.buttons, pygame.Surface)
    apply_button_active = getbutton(100, 2, img.gui.buttons, pygame.Surface)
    button_inactive = getbutton(250, 0, img.gui.buttons, pygame.Surface)
    button = getbutton(250, 1, img.gui.buttons, pygame.Surface)
    button_active = getbutton(250, 2, img.gui.buttons, pygame.Surface)
    settings_modified = dict(settings)
    ma_vol_slider_rect = pygame.Rect([35 + settings_modified['master_volume'] * 235, 150], [volume_slider.get_width(), volume_slider.get_height()])
    gu_vol_slider_rect = pygame.Rect([35 + settings_modified['gui_volume'] * 235, 200], [volume_slider.get_width(), volume_slider.get_height()])
    ga_vol_slider_rect = pygame.Rect([355 + settings_modified['game_volume'] * 235, 150], [volume_slider.get_width(), volume_slider.get_height()])
    mu_vol_slider_rect = pygame.Rect([355 + settings_modified['music_volume'] * 235, 200], [volume_slider.get_width(), volume_slider.get_height()])
    framerate_slider_rect = pygame.Rect([35 + int((settings_modified['max_framerate'] - 20) / 100 * 235 + 0.5), 300], [volume_slider.get_width(), volume_slider.get_height()])
    graphics_slider_rect = pygame.Rect([355 + int(settings_modified['graphics'] * 117.5), 300], [volume_slider.get_width(), volume_slider.get_height()])
    restart_slider_rect = pygame.Rect([195, 500], [volume_slider.get_width(), volume_slider.get_height()])
    ma_vol_rect = pygame.Rect([35, 150], [volume_slider_rail.get_width(), volume_slider_rail.get_height()])
    gu_vol_rect = pygame.Rect([35, 200], [volume_slider_rail.get_width(), volume_slider_rail.get_height()])
    ga_vol_rect = pygame.Rect([355, 150], [volume_slider_rail.get_width(), volume_slider_rail.get_height()])
    mu_vol_rect = pygame.Rect([355, 200], [volume_slider_rail.get_width(), volume_slider_rail.get_height()])
    framerate_rect = pygame.Rect([35, 300], [volume_slider_rail.get_width(), volume_slider_rail.get_height()])
    graphics_rect = pygame.Rect([355, 300], [volume_slider_rail.get_width(), volume_slider_rail.get_height()])
    difficulty_rect = pygame.Rect([35, 400], [volume_slider_rail.get_width(), volume_slider_rail.get_height()])
    cheat_rect = pygame.Rect([355, 400], [volume_slider_rail.get_width(), volume_slider_rail.get_height()])
    restart_rect = pygame.Rect([195, 500], [volume_slider_rail.get_width(), volume_slider_rail.get_height()])
    apply_rect = pygame.Rect([270, 590], [apply_button.get_width(), apply_button.get_height()])
    back_active = False
    ma_vol_active = False
    gu_vol_active = False
    ga_vol_active = False
    mu_vol_active = False
    framerate_active = False
    graphics_active = False
    difficulty_active = False
    cheat_active = False
    apply_active = False
    restart_active = False # The restart button will turn into a slider if pressed. This stores whether the button is hovered
    restart_slider_active = False  # The restart button will turn into a slider if pressed. This stores whether the slider is active
    apply_pressed = False
    restart_pressed = False # The restart button will turn into a slider if pressed. This stores whether it has turned into a slider
    held = False
    dragging = -1 # Stores which slider the user is dragging. If one slider is being dragged, it will continue to be selected until mouse button released, regardless of the position of the mouse pointer
    return_value = -1
    running = True
    while running:
        clock.tick(settings['max_framerate'])
        fps = clock.get_fps() if clock.get_fps() > 0 else 1
        fps_surf = font(16).render(txt.menu['fps'] % fps, False, [255, 255, 255])
        save.update_time()
        clock_surf = font(16).render(txt.menu['time'] % numtotime(save.gametime), False, [255, 255, 255])
        mouse_surf = font(16).render(txt.menu['mouse_pos'] % tuple(mouse_pos), False, [255, 255, 255])
        weather_surf = font(16).render(txt.menu['weather'][save.weather['raining']], False, [255, 255, 255])
        est_weather_surf = font(16).render(txt.menu['est_weather'] %
                                           (txt.menu['weather'][0] if save.weather['raining'] else txt.menu['weather'][1],
                                           (save.weather['next'] - save.gametime['time']) // 7200,
                                           (save.weather['next'] - save.gametime['time']) % 7200 / 300),
                                           False, [255, 255, 255])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return_value = 255
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                held = True
                if ma_vol_active or gu_vol_active or ga_vol_active or mu_vol_active or framerate_active or graphics_active:
                    eff.click.play()
                if back_active:
                    eff.click.play()
                    return_value = 0
                    running = False
                elif apply_active:
                    apply_pressed = True
                    settings = dict(settings_modified) # Copies the modified settings to replace 'settings'
                    eff.update_volume(settings) # Updates the volume
                    eff.click.play()
                elif difficulty_active:
                    settings_modified['difficulty'] = (settings_modified['difficulty'] + 1) % 4 # Loops from Easy to Hardcore
                    difficulty_surf = font(16).render(txt.settings['difficulty'][settings_modified['difficulty']], False, [255, 255, 255])
                    difficulty_desc_surf = font(12).render(txt.settings['difficulty_desc'][settings_modified['difficulty']], False, [255, 255, 255])
                    difficulty_desc_shade_surf = font(12).render(txt.settings['difficulty_desc'][settings_modified['difficulty']], False, [63, 63, 63])
                    eff.click.play()
                elif cheat_active:
                    settings_modified['cheat'] = (settings_modified['cheat'] + 1) % 2 # Loops from ON to OFF
                    cheat_surf = font(16).render(txt.settings['cheat'][settings_modified['cheat']], False, [255, 255, 255])
                    cheat_desc_surf = font(12).render(txt.settings['cheat_desc'][settings_modified['cheat']], False, [255, 255, 255])
                    cheat_desc_shade_surf = font(12).render(txt.settings['cheat_desc'][settings_modified['cheat']],False, [63, 63, 63])
                    eff.click.play()
                elif restart_active:
                    restart_pressed = True # It turns into a slider
                    eff.click.play()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                held = False
                apply_pressed = False
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(img.gui.bg, [0, 0])
        screen.blit(title_surf, [(640 - title_surf.get_width()) // 2, 50])
        screen.blit(fps_surf, [630 - fps_surf.get_width(), 30])
        screen.blit(img.gui.clock[numtoclock(save.gametime)], [10, 10])
        screen.blit(clock_surf, [30, 10])
        screen.blit(getweather(save, img.gui.weather), [10, 30])
        screen.blit(weather_surf, [30, 30])
        screen.blit(est_weather_surf, [100, 30])
        screen.blit(mouse_surf, [630 - mouse_surf.get_width(), 10])
        screen.blit(back_surf_active if back_active else back_surf, back_rect.topleft)
        screen.blit(sound_section_shade_surf, [36, 126])
        screen.blit(video_section_shade_surf, [36, 276])
        screen.blit(gameplay_section_shade_surf, [36, 376])
        screen.blit(sound_section_surf, [35, 125])
        screen.blit(video_section_surf, [35, 275])
        screen.blit(gameplay_section_surf, [35, 375])
        screen.blit(gameplay_warning_surfs[0], [150, 370])
        screen.blit(gameplay_warning_surfs[1], [150, 385])
        screen.blit(volume_slider_rail, ma_vol_rect.topleft)
        screen.blit(volume_slider_active if ma_vol_active else volume_slider, ma_vol_slider_rect.topleft)
        screen.blit(ma_vol_surf, [ma_vol_rect.centerx - ma_vol_surf.get_width() // 2, ma_vol_rect.centery - ma_vol_surf.get_height() // 2])
        screen.blit(volume_slider_rail, gu_vol_rect.topleft)
        screen.blit(volume_slider_active if gu_vol_active else volume_slider, gu_vol_slider_rect.topleft)
        screen.blit(gu_vol_surf, [gu_vol_rect.centerx - gu_vol_surf.get_width() // 2, gu_vol_rect.centery - gu_vol_surf.get_height() // 2])
        screen.blit(volume_slider_rail, ga_vol_rect.topleft)
        screen.blit(volume_slider_active if ga_vol_active else volume_slider, ga_vol_slider_rect.topleft)
        screen.blit(ga_vol_surf, [ga_vol_rect.centerx - ga_vol_surf.get_width() // 2, ga_vol_rect.centery - ga_vol_surf.get_height() // 2])
        screen.blit(volume_slider_rail, mu_vol_rect.topleft)
        screen.blit(volume_slider_active if mu_vol_active else volume_slider, mu_vol_slider_rect.topleft)
        screen.blit(mu_vol_surf, [mu_vol_rect.centerx - mu_vol_surf.get_width() // 2, mu_vol_rect.centery - mu_vol_surf.get_height() // 2])
        screen.blit(volume_slider_rail, framerate_rect.topleft)
        screen.blit(volume_slider_active if framerate_active else volume_slider, framerate_slider_rect.topleft)
        screen.blit(framerate_surf, [framerate_rect.centerx - framerate_surf.get_width() // 2, framerate_rect.centery - framerate_surf.get_height() // 2])
        screen.blit(volume_slider_rail, graphics_rect.topleft)
        screen.blit(volume_slider_active if graphics_active else volume_slider, graphics_slider_rect.topleft)
        screen.blit(graphics_surf, [graphics_rect.centerx - graphics_surf.get_width() // 2, graphics_rect.centery - graphics_surf.get_height() // 2])
        screen.blit(button_inactive if settings['gameplay_set'] else (button_active if difficulty_active else button), difficulty_rect.topleft) # The gameplay settings will become locked once the user start a game
        screen.blit(difficulty_surf, [difficulty_rect.centerx - difficulty_surf.get_width() // 2, difficulty_rect.centery - difficulty_surf.get_height() // 2])
        screen.blit(difficulty_desc_shade_surf, [difficulty_rect.left + 1, difficulty_rect.top + 51])
        screen.blit(difficulty_desc_surf, [difficulty_rect.left, difficulty_rect.top + 50])
        screen.blit(button_inactive if settings['gameplay_set'] else (button_active if cheat_active else button), cheat_rect.topleft) # Same as the last one
        screen.blit(cheat_surf, [cheat_rect.centerx - cheat_surf.get_width() // 2, cheat_rect.centery - cheat_surf.get_height() // 2])
        screen.blit(cheat_desc_shade_surf, [cheat_rect.left + 1, cheat_rect.top + 51])
        screen.blit(cheat_desc_surf, [cheat_rect.left, cheat_rect.top + 50])
        screen.blit(volume_slider_rail if restart_pressed else (button, button_active)[restart_active], restart_rect.topleft)
        if restart_pressed:
            screen.blit(volume_slider_active if restart_slider_active else volume_slider, restart_slider_rect.topleft)
        if restart_pressed:    screen.blit(restart_slider_surf, [restart_rect.centerx - restart_slider_surf.get_width() // 2, restart_rect.centery - restart_slider_surf.get_height() // 2])
        else:    screen.blit(restart_surf, [restart_rect.centerx - restart_surf.get_width() // 2, restart_rect.centery - restart_surf.get_height() // 2])
        screen.blit((apply_button, apply_button_pressed, apply_button_active)[-apply_pressed + apply_active * 2], apply_rect.topleft)
        screen.blit(apply_surf, [apply_rect.centerx - apply_surf.get_width() // 2, apply_rect.centery - apply_surf.get_height() // 2])
        draw_cursor(mouse_pos, screen)
        back_active = back_rect.collidepoint(mouse_pos)
        apply_active = apply_rect.collidepoint(mouse_pos)
        ma_vol_active = ma_vol_rect.collidepoint(mouse_pos) if dragging == -1 else dragging == 0 # If the user is dragging the corresponding slider, it will remain active regardless of position of pointer
        gu_vol_active = gu_vol_rect.collidepoint(mouse_pos) if dragging == -1 else dragging == 1
        ga_vol_active = ga_vol_rect.collidepoint(mouse_pos) if dragging == -1 else dragging == 2
        mu_vol_active = mu_vol_rect.collidepoint(mouse_pos) if dragging == -1 else dragging == 3
        framerate_active = framerate_rect.collidepoint(mouse_pos) if dragging == -1 else dragging == 4
        graphics_active = graphics_rect.collidepoint(mouse_pos) if dragging == -1 else dragging == 5
        difficulty_active = not settings['gameplay_set'] and difficulty_rect.collidepoint(mouse_pos)
        cheat_active = not settings['gameplay_set'] and cheat_rect.collidepoint(mouse_pos)
        restart_active = restart_rect.collidepoint(mouse_pos)
        restart_slider_active = restart_pressed and restart_slider_rect.collidepoint(mouse_pos)
        if (ma_vol_active and held) or dragging == 0:
            dragging = 0 if held else -1
            ma_vol_slider_rect.centerx = mouse_pos[0]
            if ma_vol_slider_rect.left < 35:    ma_vol_slider_rect.left = 35
            if ma_vol_slider_rect.right > 285:    ma_vol_slider_rect.right = 285
            settings_modified['master_volume'] = (ma_vol_slider_rect.left - 35) / 235
            ma_vol_surf = font(16).render(txt.settings['master_volume'] % int(settings_modified['master_volume'] * 100), False, [255, 255, 255])
        elif (gu_vol_active and held) or dragging == 1:
            dragging = 1 if held else -1
            gu_vol_slider_rect.centerx = mouse_pos[0]
            if gu_vol_slider_rect.left < 35:    gu_vol_slider_rect.left = 35
            if gu_vol_slider_rect.right > 285:    gu_vol_slider_rect.right = 285
            settings_modified['gui_volume'] = (gu_vol_slider_rect.left - 35) / 235
            gu_vol_surf = font(16).render(txt.settings['gui_volume'] % int(settings_modified['gui_volume'] * 100), False, [255, 255, 255])
        elif (ga_vol_active and held) or dragging == 2:
            dragging = 2 if held else -1
            ga_vol_slider_rect.centerx = mouse_pos[0]
            if ga_vol_slider_rect.left < 355:    ga_vol_slider_rect.left = 355
            if ga_vol_slider_rect.right > 605:    ga_vol_slider_rect.right = 605
            settings_modified['game_volume'] = (ga_vol_slider_rect.left - 355) / 235
            ga_vol_surf = font(16).render(txt.settings['game_volume'] % int(settings_modified['game_volume'] * 100), False, [255, 255, 255])
        elif (mu_vol_active and held) or dragging == 3:
            dragging = 3 if held else -1
            mu_vol_slider_rect.centerx = mouse_pos[0]
            if mu_vol_slider_rect.left < 355:    mu_vol_slider_rect.left = 355
            if mu_vol_slider_rect.right > 605:    mu_vol_slider_rect.right = 605
            settings_modified['music_volume'] = (mu_vol_slider_rect.left - 355) / 235
            mu_vol_surf = font(16).render(txt.settings['music_volume'] % int(settings_modified['music_volume'] * 100), False, [255, 255, 255])
        elif (framerate_active and held) or dragging == 4:
            dragging = 4 if held else -1
            framerate_slider_rect.centerx = mouse_pos[0]
            if framerate_slider_rect.left < 35:    framerate_slider_rect.left = 35
            if framerate_slider_rect.right > 285:   framerate_slider_rect.right = 285
            settings_modified['max_framerate'] = 20 + (framerate_slider_rect.left - 35) * 100 // 235
            framerate_surf = font(16).render(txt.settings['max_framerate'] % settings_modified['max_framerate'], False, [255, 255, 255])
        elif (graphics_active and held) or dragging == 5:
            dragging = 5 if held else -1
            graphics_slider_rect.centerx = mouse_pos[0]
            if graphics_slider_rect.left < 355:    graphics_slider_rect.left = 355
            if graphics_slider_rect.right > 605:   graphics_slider_rect.right = 605
            settings_modified['graphics'] = (graphics_slider_rect.left - 355 + 39) // 117
            graphics_surf = font(16).render(txt.settings['graphics'][settings_modified['graphics']], False, [255, 255, 255]) # Changes the modified settings according to the sliders
        elif restart_slider_active and held:
            dragging = 6 if held else -1
            restart_slider_rect.centerx = mouse_pos[0]
            if restart_slider_rect.left < 195:    restart_slider_rect.left = 195
            if restart_slider_rect.right > 445:
                dragging = -1
                restart_slider_rect.left = 195
                restart_slider_active = False
                restart_active = False
                restart_pressed = False
                settings_modified['gameplay_set'] = False
                restart_progress() # Restarts the progress and unlocks the gameplay settings
        pygame.display.flip()
    save.difficulty = settings['difficulty']
    save.cheat = settings['cheat']
    return return_value
def choose_adventure_map(): # The adventure level selection map
    global mouse_pos, settings, fps, music
    if music != 'map':
        eff.music[music].stop()
        music = 'map'
        eff.music[music].play(-1)
    back_surf = font(24).render(txt.menu['back'], False, [0, 0, 0])
    back_surf_active = font(24).render(txt.menu['back'], False, [0, 255, 0])
    back_rect = pygame.Rect([75, 75], [back_surf.get_width(), back_surf.get_height()])
    back_active = False
    running = True
    return_value = -1
    drag = False
    drag_start = mouse_pos[:]
    camera = [2048, 1792]
    scale = 2 # determines how many pixels on the map 1 pixel shows [1, 4]
    map_page = 0
    key_held = [False, False, False, False]
    selected_item = None
    top_bar_rect = pygame.Rect([0, -40, 640, img.gui.top_bar.get_height()])
    info_pad_rect = pygame.Rect([320 - img.gui.gui_background.get_width() // 2, 500, img.gui.gui_background.get_width(), img.gui.gui_background.get_height()])
    while running:
        clock.tick(settings['max_framerate'])
        fps = clock.get_fps() if clock.get_fps() > 0 else 1
        fps_surf = font(16).render(txt.menu['fps'] % fps, False, [0, 0, 0])
        save.update_time()
        clock_surf = font(16).render(txt.menu['time'] % numtotime(save.gametime), False, [0, 0, 0])
        mouse_surf = font(16).render(txt.menu['mouse_pos'] % tuple(mouse_pos), False, [0, 0, 0])
        weather_surf = font(16).render(txt.menu['weather'][save.weather['raining']], False, [0, 0, 0])
        est_weather_surf = font(16).render(txt.menu['est_weather'] %
                                           (txt.menu['weather'][0] if save.weather['raining'] else txt.menu['weather'][1],
                                           (save.weather['next'] - save.gametime['time']) // 7200,
                                           (save.weather['next'] - save.gametime['time']) % 7200 / 300),
                                           False, [0, 0, 0])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return_value = 255
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if back_active:
                        eff.click.play()
                        return_value = 2
                        running = False
                    elif scale < 3:
                        flag = False
                        for town in adventure_map['towns']:
                            screen_pos = getscreenpos(camera, town.coords, scale)
                            if -img.map.large_town.get_width() // 2 <= screen_pos[0] - mouse_pos[0] <= img.map.large_town.get_width() // 2 and \
                               -img.map.large_town.get_height() // 2 <= screen_pos[1] - mouse_pos[1] <= img.map.large_town.get_height() // 2:
                                eff.click.play()
                                selected_item = town
                                flag = True
                        for level in adventure_map['levels']:
                            screen_pos = getscreenpos(camera, level.coords, scale)
                            if -img.map.banners[0].get_width() // 2 <= screen_pos[0] - mouse_pos[0] <= img.map.banners[0].get_width() // 2 and \
                               0 <= screen_pos[1] - mouse_pos[1] <= img.map.banners[1].get_height():
                                eff.click.play()
                                selected_item = level
                                flag = True
                        if not flag and not top_bar_rect.collidepoint(mouse_pos) and (selected_item == None or not info_pad_rect.collidepoint(mouse_pos)):
                            drag = True
                            drag_start = mouse_pos[:]
                            camera_start = camera[:]
                    elif not top_bar_rect.collidepoint(mouse_pos) and (selected_item == None or not info_pad_rect.collidepoint(mouse_pos)):
                        selected_item = None
                        drag = True
                        drag_start = mouse_pos[:]
                        camera_start = camera[:]
                elif event.button == 4:
                    if scale > 1:
                        scale -= 0.1
                elif event.button == 5:
                    if scale < 4:
                        scale += 0.1
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drag = False
                    if abs(sum(drag_start) - sum(mouse_pos)) < 3:
                        selected_item = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    key_held[0] = True
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    key_held[1] = True
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    key_held[2] = True
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    key_held[3] = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    key_held[0] = False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    key_held[1] = False
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    key_held[2] = False
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    key_held[3] = False
        if drag:
            camera[0] = camera_start[0] + (drag_start[0] - mouse_pos[0]) * scale
            camera[1] = camera_start[1] + (drag_start[1] - mouse_pos[1]) * scale
        if key_held[0]:    camera[0] -= 200 * scale / fps
        if key_held[1]:    camera[0] += 200 * scale / fps
        if key_held[2]:    camera[1] -= 200 * scale / fps
        if key_held[3]:    camera[1] += 200 * scale / fps
        if camera[0] < 320 * scale:    camera[0] = 320 * scale
        if camera[0] > 4095 - 320 * scale:    camera[0] = 4095 - 320 * scale
        if camera[1] < 320 * scale:    camera[1] = 320 * scale
        if camera[1] > 3583 - 320 * scale:    camera[1] = 3583 - 320 * scale
        mouse_pos = pygame.mouse.get_pos()
        map_topleft = [camera[0] - 320 * scale, camera[1] - 320 * scale]
        map_bottomright = [camera[0] + 320 * scale, camera[1] + 320 * scale]
        topleft_map = [int(map_topleft[0] // 512), int(map_topleft[1] // 512)]
        bottomright_map = [int(map_bottomright[0] // 512), int(map_bottomright[1] // 512)]
        for i in range(topleft_map[0], bottomright_map[0] + 1):
            for j in range(topleft_map[1], bottomright_map[1] + 1):
                scaled_map = pygame.transform.scale(img.map.maps[i][j], [512 // scale + 1, 512 // scale + 1])
                screen_pos = [320 + (i * 512 - camera[0]) // scale, 320 + (j * 512 - camera[1]) // scale]
                screen.blit(scaled_map, screen_pos)
        if scale <= 3: # Render roads
            for road in adventure_map['roads']:
                object0 = getmapobject(adventure_map, road.ends[0])
                object1 = getmapobject(adventure_map, road.ends[1])
                coords0 = object0.coords
                coords1 = object1.coords
                screen_pos0 = getscreenpos(camera, coords0, scale)
                screen_pos1 = getscreenpos(camera, coords1, scale)
                explored = (object0.type == 'town' or (object0.type == 'level' and save.levels[object0.index].completed)) and \
                           (object1.type == 'town' or (object1.type == 'level' and save.levels[object1.index].completed))
                if explored:
                    pygame.draw.line(screen, [0, 0, 0] if object0 != selected_item and object1 != selected_item else [255, 255, 0],
                                     screen_pos0, screen_pos1, int(5 / scale + 0.5) if object0 != selected_item and object1 != selected_item else int(8 / scale + 0.5))
                else:
                    draw_dashed_line(pygame.draw.line, screen, [0, 0, 0] if object0 != selected_item and object1 != selected_item else [255, 255, 0],
                                     screen_pos0, screen_pos1, int(5 / scale + 0.5) if object0 != selected_item and object1 != selected_item else int(8 / scale + 0.5), 30 / scale)
        elif selected_item != None:
            for connection in selected_item.connections:
                connected = getmapobject(adventure_map, connection)
                coords0 = selected_item.coords
                coords1 = connected.coords
                screen_pos0 = getscreenpos(camera, coords0, scale)
                screen_pos1 = getscreenpos(camera, coords1, scale)
                draw_dashed_line(pygame.draw.line, screen, [255, 255, 0],    screen_pos0, screen_pos1, int(8 / scale + 0.5), 30 / scale)
        if scale <= 3: # Icons for levels
            for level in adventure_map['levels']:
                screen_pos = getscreenpos(camera, level.coords, scale)
                banner = img.map.banners[save.levels[level.index].completed * 3]
                if not (-320 <= screen_pos[0] <= 960 and -320 <= screen_pos[1] <= 960):
                    continue
                screen.blit(banner, [screen_pos[0] - banner.get_width() // 2,
                                     screen_pos[1] - banner.get_height()])
                if selected_item == level:
                    screen.blit(img.map.pointer, [screen_pos[0] - img.map.pointer.get_width() // 2,
                                                  screen_pos[1] - img.map.pointer.get_height() - img.map.banners[0].get_height() - 4])
        elif selected_item != None:
            if selected_item.type == 'level' and (-320 <= screen_pos[0] <= 960 and -320 <= screen_pos[1] <= 960):
                screen_pos = getscreenpos(camera, selected_item.coords, scale)
                banner = img.map.banners[save.levels[selected_item.index].completed * 3]
                screen.blit(banner, [screen_pos[0] - banner.get_width() // 2,
                                     screen_pos[1] - banner.get_height()])
                screen.blit(img.map.pointer, [screen_pos[0] - img.map.pointer.get_width() // 2,
                                              screen_pos[1] - img.map.pointer.get_height() - img.map.banners[0].get_height() - 4])
            for connection in selected_item.connections:
                if connection[0] == 'town':    continue
                connected = getmapobject(adventure_map, connection)
                screen_pos = getscreenpos(camera, connected.coords, scale)
                banner = img.map.banners[save.levels[connected.index].completed * 3]
                screen.blit(banner, [screen_pos[0] - banner.get_width() // 2,
                                     screen_pos[1] - banner.get_height()])
        for town in adventure_map['towns']: # Icons for towns
            screen_pos = getscreenpos(camera, town.coords, scale)
            if not (-320 <= screen_pos[0] <= 960 and -320 <= screen_pos[1] <= 960):
                continue
            if scale > 3:
                screen.blit(img.map.small_town, [screen_pos[0] - img.map.small_town.get_width() // 2,
                                                 screen_pos[1] - img.map.small_town.get_height() // 2])
            else:
                screen.blit(img.map.large_town, [screen_pos[0] - img.map.large_town.get_width() // 2,
                                                 screen_pos[1] - img.map.large_town.get_height() // 2])
            if scale <= 3:
                name_surf = None
                if selected_item == town:
                    name_surf = font(16).render(txt.map['town_name'][town.index], False, [255, 255, 0])
                elif save.player_loc == town.index:
                    name_surf = font(16).render(txt.map['town_name'][town.index], False, [0, 255, 0])
                elif scale <= 2:
                    name_surf = font(16).render(txt.map['town_name'][town.index], False, [0, 0, 0])
                if name_surf != None:
                    screen.blit(name_surf, [screen_pos[0] + 16,
                                            screen_pos[1] + 8])
            if selected_item == town:
                screen.blit(img.map.pointer, [screen_pos[0] - img.map.pointer.get_width() // 2, screen_pos[1] - img.map.pointer.get_height() - img.map.large_town.get_height() // 2])
            if save.player_loc == town.index:
                screen.blit(img.map.player, [screen_pos[0] - img.map.player.get_width() // 2, screen_pos[1] - img.map.player.get_height() // 2])
        if selected_item != None: # Info pad
            screen.blit(img.gui.gui_background, info_pad_rect.topleft)
            if selected_item.type == 'town':
                name_surf = font(16).render(txt.map['town_name'][selected_item.index], False, [0, 0, 0])
                screen.blit(name_surf, [330 - img.gui.gui_background.get_width() // 2, 510])
                screen.blit(img.env.town_scene[getdaynight(save.gametime)]['rain' if save.weather['raining'] else 'clear'][selected_item.scenery],
                            [330 - img.gui.gui_background.get_width() // 2, 530])
            elif selected_item.type == 'level':
                name_surf = font(16).render(txt.map['biome_name'][selected_item.biome], False, [0, 0, 0])
                screen.blit(name_surf, [330 - img.gui.gui_background.get_width() // 2, 510])
                screen.blit(img.env.biome_scene[getdaynight(save.gametime)]['rain' if save.weather['raining'] else 'clear'][selected_item.biome],
                            [330 - img.gui.gui_background.get_width() // 2, 530])
        screen.blit(img.gui.top_bar, top_bar_rect.topleft)
        pos_home = [320 + (adventure_map['towns'][save.player_loc].coords[0] - camera[0]) // scale,
                    320 + (adventure_map['towns'][save.player_loc].coords[1] - camera[1]) // scale]
        x_diff = pos_home[0] - 320
        y_diff = pos_home[1] - img.gui.compass[0].get_width() // 2
        if x_diff != 0:
            deg = math.degrees(math.atan(y_diff / x_diff))
            if y_diff > 0:
                if deg < 0:    deg += 180
            elif y_diff == 0:
                if x_diff < 0:    deg += 180
            elif y_diff < 0:
                if deg >= 0:    deg += 180
                else:    deg += 360
        else:
            if y_diff > 0:
                deg = 90
            elif y_diff == 0:
                deg = 0
            elif y_diff < 0:
                deg = 270
        deg = (deg + 270) % 360
        compassi = int(deg / 360 * 32 + 0.5) % 32
        screen.blit(img.gui.compass[compassi], [320 - img.gui.compass[0].get_width() // 2, 0])
        screen.blit(fps_surf, [630 - fps_surf.get_width(), 30])
        screen.blit(img.gui.clock[numtoclock(save.gametime)], [10, 10])
        screen.blit(clock_surf, [30, 10])
        screen.blit(getweather(save, img.gui.weather), [10, 30])
        screen.blit(weather_surf, [30, 30])
        screen.blit(est_weather_surf, [100, 30])
        screen.blit(mouse_surf, [630 - mouse_surf.get_width(), 10])
        screen.blit(back_surf_active if back_active else back_surf, back_rect.topleft)
        draw_cursor(mouse_pos, screen)
        back_active = back_rect.collidepoint(mouse_pos)
        pygame.display.flip()
    return return_value
def start_game(gamesave, level):
    global mouse_pos, music
    settings['gameplay_set'] = True
    game = Game(gamesave, level, settings)
    eff.music[music].stop()
    if level.biome == 1 or level.biome == 2 or level.biome == 5 or level.biome == 6:
        music = 'woods'
    elif level.biome == 3 or level.biome == 7:
        music = 'cold'
    elif level.biome == 4 or level.biome == 8:
        music = 'water'
    else:
        music = 'default'
    eff.music[music].play(-1)
    response = 0
    while response == 0:
        clock.tick(settings['max_framerate'])
        fps = clock.get_fps() if clock.get_fps() > 0 else 1
        save.update_time()
        mouse_pos = pygame.mouse.get_pos()
        response = game.update(pygame.event.get(), mouse_pos, fps, eff)
        game.animate(screen, img, font)
        pygame.display.flip()
    if response == 255:
        return 255
    return 0
clock = pygame.time.Clock()
bg_music_playing = True # Whether the background music is still playing. Some pages will have different background music from Wet Hands
mouse_pos = [0, 0]
fps = 1
return_value = 0
music = 'menu'
eff.music['menu'].play()
# This is the main loop for the WHOLE game
# Way of numbering a sub-page: n(main-page) * 8 + (0~7)
while return_value != 255: # Return value = 255: Game quit
    if return_value == 0:
        return_value = menu_loop()
    elif return_value == 1:
        return_value = about_page()
    elif return_value == 2:
        return_value = choose_game_mode()
    elif return_value == 3:
        return_value = letter_from_doge()
    elif return_value == 4:
        return_value = wip_page(0) # Planned: achievements
    elif return_value == 5:
        return_value = wip_page(0) # Planned: research
    elif return_value == 6:
        return_value = wip_page(0) # Planned: wizardry
    elif return_value == 7:
        return_value = wip_page(0) # Planned: statistics
    elif return_value == 8:
        return_value = settings_page()
    elif return_value == 16:
        return_value = choose_adventure_map()
    elif return_value == 17:
        # Currenty altered for game tests
        return_value = start_game(save, adventure_map['levels'][0])
        #return_value = wip_page(2) # Planned: choose_survival_map
for item in eff.music.values():
    item.stop()
chdir(path.join(cwd, 'GameData\\Data'))
with open('settings.dat', 'wb') as f:
    pickle.dump(settings, f) # Saves the settings
with open('save.dat', 'wb') as f:
    pickle.dump(save, f) # Saves the game
chdir(cwd)
pygame.quit()
sys.exit()
