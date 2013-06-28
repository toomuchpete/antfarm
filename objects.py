import libtcodpy as libtcod

class Ant:
    def __init__(self, x, y, char, color, name='Ant-nonymous'):
        self.name = name
        self.x = x
        self.y = y
        self.char = char
        self.color = color
 
    def move(self, dx, dy):
        #move by the given amount
        self.x += dx
        self.y += dy

class Food:
    def __init__(self):
        self.char = 5
        self.bg_color = libtcod.Color(204,255,255)
        self.fg_color = libtcod.Color(0,96,0)


class Dirt:
    char_options = [' ', 176, 177, 178]
    def __init__(self, char_selection = 0):
        self.char = self.char_options[abs(int(char_selection))]
        # http://www.colourlovers.com/palette/1254353/Reflections
        self.bg_color = libtcod.Color(120,72,0)
        self.fg_color = libtcod.Color(89,54,12)

class Wall:
    def __init__(self):
        self.char = ' '
        self.bg_color = libtcod.Color(0,168,0)
        self.fg_color = libtcod.white

class Air:
    def __init__(self):
        self.char = ' '
        self.bg_color = libtcod.Color(212,255,255)
        self.fg_color = libtcod.Color(0,0,0)


class Farm:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.console = libtcod.console_new(height, width)

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
                if isinstance(self.tiles[x][y], Air):
                    tile_below = self.tiles[x][y+1]
                    if isinstance(tile_below, Dirt) or isinstance(tile_below, Wall):
                        locations.append((x,y))
        return locations

    def place_entities(self, entity_list):
        for entity in entity_list:
            libtcod.console_put_char_ex(self.console, entity.x, entity.y, entity.char, entity.color, self.tiles[entity.x][entity.y].bg_color)
