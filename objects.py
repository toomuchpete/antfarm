import libtcodpy as libtcod
from random import choice
from lib import switch

class Ant:
    def __init__(self, x, y, char, color, farm, name='Ant-nonymous'):
        self.state = 'rest'
        self.state_counter = 0
        self.cooldown = 0

        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.farm = farm
        self.name = name
 
    def move(self, dx, dy):
        #move by the given amount
        if not self.farm.solid(self.x+dx, self.y+dy):
            self.x += dx
            self.y += dy

    def tick(self):
        self.state_counter += 1

        if self.cooldown > 0:
            self.cooldown -= 1
            return
        
        for case in switch(self.state):
            if case('rest'):
                if self.state_counter > 100:
                    self.state_counter = 0
                    self.state = 'wander'
                break
            if case('wander'):
                if self.state_counter > 100:
                    self.state_counter = 0
                    self.state = 'rest'
                    return

                self.move(choice([-1,0,1]),0)

class Food:
    def __init__(self):
        self.char = 5
        self.bg_color = libtcod.Color(204,255,255)
        self.fg_color = libtcod.Color(0,96,0)


class Dirt:
    char_options = [' ', 176, 177, 178]
    solid = True
    def __init__(self, char_selection = 0):
        self.char = self.char_options[abs(int(char_selection))]
        # http://www.colourlovers.com/palette/1254353/Reflections
        self.bg_color = libtcod.Color(120,72,0)
        self.fg_color = libtcod.Color(89,54,12)

class Wall:
    solid = True
    def __init__(self):
        self.char = ' '
        self.bg_color = libtcod.Color(0,168,0)
        self.fg_color = libtcod.white

class Air:
    solid = False
    def __init__(self):
        self.char = ' '
        self.bg_color = libtcod.Color(212,255,255)
        self.fg_color = libtcod.Color(0,0,0)


class Farm:
    class Viewport:
        def __init__(self, x, y, height, width):
            self.x = x
            self.y = y
            self.height = height
            self.width = width

        def move(self, dx, dy):
            self.x += dx
            self.y += dy

        def size(self, height = None, width = None):
            if height != None:
                self.height = height

            if width != None:
                self.width = width

            return (height, width)

        def bounding_box(self):
            return (self.x, self.y, self.x + self.width, self.y + self.height)

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.viewport = Farm.Viewport(0,0,height,width)
        self.console = libtcod.console_new(height, width)

    def solid(self, x, y):
        return self.tiles[x][y].solid

    def generate(self, border_size = 1, air_buffer = 10):
        noise_2d = libtcod.noise_new(2)
        self.tiles = [[ Dirt(libtcod.noise_get(noise_2d,[x,y])*3) for y in range(self.height) ] for x in range(self.width) ]
        for x in range(self.width):
            for y in range(self.height):
                if x < border_size or y < border_size or  x > ((self.width - 1) - border_size) or y > ((self.height - 1) - border_size):
                    self.tiles[x][y] = Wall()
                elif y < border_size + air_buffer:
                    self.tiles[x][y] = Air()
        self.update()    

    def update(self):
        for x in range(self.width):
            for y in range(self.height):
                tile = self.tiles[x][y]
                libtcod.console_put_char_ex(self.console, x, y, tile.char, tile.fg_color, tile.bg_color)

    def standable_locations(self):
        locations = []
        for x in range(self.width):
            for y in range(self.height):
                if not self.solid(x,y) and self.solid(x,y+1):
                    locations.append((x,y))

        return locations

    def place_entities(self, entity_list):
        for entity in entity_list:
            libtcod.console_put_char_ex(self.console, entity.x, entity.y, entity.char, entity.color, self.tiles[entity.x][entity.y].bg_color)