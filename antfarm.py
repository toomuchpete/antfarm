import libtcodpy as libtcod
from objects import Ant, Dirt, Wall, Air
from lib import switch
from random import choice
import os

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
FARM_WIDTH = 160
FARM_HEIGHT = 120
TOP_BUFFER = 10
BORDER_SIZE = 1
farm_console = libtcod.console_new(FARM_WIDTH, FARM_HEIGHT)

# Camera Offsets
camera_x = int((FARM_WIDTH/2)-(SCREEN_WIDTH/2))
camera_y = 0

# Farm Data
farm = []
entities = []

# More globals, because I love them
mouse = libtcod.Mouse()
key = libtcod.Key()

# Name generator
for file in os.listdir(b'data/namegen') :
    if file.find(b'.cfg') > 0 :
        libtcod.namegen_parse(os.path.join(b'data',b'namegen',file))

def handle_keys():
    global key, mouse, camera_x, camera_y, farm_console, panel_console, show_panel, entities
 
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
            build_farm()
            draw_farm(farm_console)
            entities = []
            place_ants(3)
            draw_entities(farm_console)
        else:
            key_char = chr(key.c)
            for case in switch(key_char):
                if case('?'):
                    show_panel = not show_panel

    if mouse.lbutton_pressed:
        (x,y) = (mouse.cx + camera_x,mouse.cy + camera_y)
        entity_list = []
        check_count = 0
        # Check for an ant?
        for entity in entities:
            check_count += 1
            if entity.x == x and entity.y == y:
                entity_list.append(str.format("{}\n---------------\nAnt ID: {}\nPosition: ({},{})", entity.name, id(entity), x, y))

        if len(entity_list) == 0:
            entity_list.append(str.format("There are no ants at ({},{}).\n\nChecked {} entities.", x, y, check_count))

        libtcod.console_clear(panel_console)
        libtcod.console_print_rect(panel_console, 2, 2, PANEL_WIDTH-4, 10, "\n\n".join(entity_list))



def build_farm():
    global farm
    noise_2d = libtcod.noise_new(2)
    farm = [[ Dirt(libtcod.noise_get(noise_2d,[x,y])*3) for y in range(FARM_HEIGHT) ] for x in range(FARM_WIDTH) ]
    for x in range(len(farm)):
        for y in range(len(farm[x])):
            if x < BORDER_SIZE or y < BORDER_SIZE or  x > ((FARM_WIDTH - 1) - BORDER_SIZE) or y > ((FARM_HEIGHT - 1) - BORDER_SIZE):
                farm[x][y] = Wall()
            elif y < BORDER_SIZE + TOP_BUFFER:
                farm[x][y] = Air()

def draw_farm(con):
    global farm
    for x in range(len(farm)):
        for y in range(len(farm[x])):
            tile = farm[x][y]
            libtcod.console_put_char_ex(con, x, y, tile.char, tile.fg_color, tile.bg_color)

def place_ants(number):
    global farm, entities
    spots = []
    for x in range(len(farm)):
        for y in range(len(farm[x])):
            if isinstance(farm[x][y], Air):
                tile_below = farm[x][y+1]
                if isinstance(tile_below, Dirt) or isinstance(tile_below, Wall):
                    spots.append((x,y))
    
    if len(spots) > 0:
        for i in range(number):
            (x, y) = choice(spots)
            entities.append(Ant(x, y, '@', libtcod.black, libtcod.namegen_generate(choice(libtcod.namegen_get_sets()))))

def draw_entities(con):
    global farm, entities
    for entity in entities:
        libtcod.console_put_char_ex(con, entity.x, entity.y, entity.char, entity.color, farm[entity.x][entity.y].bg_color)


libtcod.console_set_custom_font('data/fonts/lord_dullard_12x12.png', libtcod.FONT_LAYOUT_ASCII_INROW)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Pete\'s Ant Farm', False)
libtcod.console_set_default_background(0, libtcod.Color(204,255,255))
build_farm()
place_ants(3)
draw_farm(farm_console)

# draw_panel(panel_console)
libtcod.console_clear(panel_console)
draw_entities(farm_console)

while not libtcod.console_is_window_closed():
    libtcod.console_clear(0)
    libtcod.console_blit(farm_console, camera_x, camera_y, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
    if show_panel:
        libtcod.console_blit(panel_console, 0, 0, PANEL_WIDTH, PANEL_HEIGHT, 0, SCREEN_WIDTH - PANEL_WIDTH, 0, 1, .9)
    libtcod.console_flush()

    #handle keys and exit game if needed
    libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE,key,mouse)
    exit = handle_keys()
    if exit:
        break