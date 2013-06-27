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
