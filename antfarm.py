import libtcodpy as libtcod
from objects import Ant, Dirt, Wall, Air, Farm
from lib import switch
from random import choice
import os

LIMIT_FPS = 20
libtcod.sys_set_fps(LIMIT_FPS)

# size of the window
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

# size of info panel
PANEL_WIDTH = 20
PANEL_HEIGHT = SCREEN_HEIGHT
panel_console = libtcod.console_new(PANEL_WIDTH, PANEL_HEIGHT)
libtcod.console_set_default_foreground(panel_console, libtcod.black)
libtcod.console_set_default_background(panel_console, libtcod.Color(244,237,159))
show_panel = False

# Farm dimensions
farm = Farm(160, 120)
entities = []

# Camera Offsets
camera_x = int((farm.width/2)-(SCREEN_WIDTH/2))
camera_y = 0

# More globals, because I love them
mouse = libtcod.Mouse()
key = libtcod.Key()

# Name generator
for file in os.listdir(b'data/namegen') :
    if file.find(b'.cfg') > 0 :
        libtcod.namegen_parse(os.path.join(b'data',b'namegen',file))

def handle_keys():
    global farm, key, mouse, camera_x, camera_y, panel_console, show_panel, entities
 
    if key.vk != libtcod.KEY_NONE:
        # vertical movement
        for case in switch(key.vk):
            if case(libtcod.KEY_UP): pass
            if case(libtcod.KEY_KP8): pass
            if case(libtcod.KEY_HOME): pass
            if case(libtcod.KEY_KP7): pass
            if case(libtcod.KEY_PAGEUP): pass
            if case(libtcod.KEY_KP9):
                camera_y -= 1
                break
            if case(libtcod.KEY_DOWN): pass
            if case(libtcod.KEY_KP2): pass
            if case(libtcod.KEY_END): pass
            if case(libtcod.KEY_KP1): pass
            if case(libtcod.KEY_PAGEDOWN): pass
            if case(libtcod.KEY_KP3):
                camera_y += 1
                break

        # horizontal movement
        for case in switch(key.vk):
            if case(libtcod.KEY_LEFT): pass
            if case(libtcod.KEY_KP4): pass
            if case(libtcod.KEY_HOME): pass
            if case(libtcod.KEY_KP7): pass
            if case(libtcod.KEY_END): pass
            if case(libtcod.KEY_KP1):
                camera_x -= 1
                break
            if case(libtcod.KEY_RIGHT): pass
            if case(libtcod.KEY_KP6): pass
            if case(libtcod.KEY_PAGEUP): pass
            if case(libtcod.KEY_KP9): pass
            if case(libtcod.KEY_PAGEDOWN): pass
            if case(libtcod.KEY_KP3):
                camera_x += 1
                break

        if key.vk == libtcod.KEY_ESCAPE:
            return True  #exit game
        elif key.vk == libtcod.KEY_BACKSPACE and (key.lctrl or key.rctrl):
            farm.generate()
            entities = []
            place_ants(3)
            farm.place_entities(entities)
        else:
            key_char = chr(key.c)
            for case in switch(key_char):
                if case('?'):
                    show_panel = not show_panel

    if mouse.lbutton_pressed:
        (x,y) = (mouse.cx + camera_x,mouse.cy + camera_y)
        entity_list = []

        # Check for an ant?
        for entity in entities:
            if entity.x == x and entity.y == y:
                entity_list.append(str.format("{}\n---------------\nAnt ID: {}\nPosition: ({},{})", entity.name, id(entity), x, y))

        if len(entity_list) == 0:
            entity_list.append(str.format("There are no ants at ({},{}).\n", x, y))

        libtcod.console_clear(panel_console)
        libtcod.console_print_rect(panel_console, 2, 2, PANEL_WIDTH-4, 10, "\n\n".join(entity_list))

def place_ants(number):
    global farm, entities
    spots = farm.standable_locations()
   
    if len(spots) > 0:
        for i in range(number):
            (x, y) = choice(spots)
            entities.append(Ant(x, y, '@', libtcod.black, libtcod.namegen_generate(choice(libtcod.namegen_get_sets()))))


libtcod.console_set_custom_font('data/fonts/lord_dullard_12x12.png', libtcod.FONT_LAYOUT_ASCII_INROW)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Pete\'s Ant Farm', False)
libtcod.console_set_default_background(0, libtcod.Color(204,255,255))
farm.generate()
farm.update()
place_ants(3)
farm.place_entities(entities)

# draw_panel(panel_console)
libtcod.console_clear(panel_console)

while not libtcod.console_is_window_closed():
    libtcod.console_clear(0)
    libtcod.console_blit(farm.console, camera_x, camera_y, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
    if show_panel:
        libtcod.console_blit(panel_console, 0, 0, PANEL_WIDTH, PANEL_HEIGHT, 0, SCREEN_WIDTH - PANEL_WIDTH, 0, 1, .9)
    libtcod.console_flush()

    #handle keys and exit game if needed
    libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE,key,mouse)
    exit = handle_keys()
    if exit:
        break