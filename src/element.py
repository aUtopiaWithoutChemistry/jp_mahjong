''' all_tiles are all tiles that can appear on the table, 
        every single tile in tiles are in the form of (value, id)
        since have red dora tile, they are evaluated as regular tile during win checking,
        but have different score in score_counting.
        So I identify tiles with id 16, 52, 88 are red dora for man, ping, and suo

    mahjong_tile_elements is a dict show every tile's value's meaning in human's word.
        it might useful when human player playing game, but it will lose meaning when I added
        graphic user interface. Anyway, it can notice me now about how this number represent
        mahjong tiles.

    find_num_using_tile is a reversed dict for mahjong_tile_elements, which means people can
        type in the tile they want to find and get the number of this tile in my representation
        system. This only useful before I implement the GUI, but I hardly think so that I would 
        play this game without GUI

    key_list is a helper list for generate all tiles in following for loop, this list contains
        all the key of mahjong_tile_elements, so every item in this list is the value of four 
        same tiles.

    using the following for loop, I generated a list of tuples, the list's length is 136 which
        is the number of all the mahjong tiles, I use the id which is also iterable part in the
        for loop to // 4 which means I want to let every tiles in key_list generate four tiles 
        which have the same value but different id. This can help me to identify all red dora
        tiles without change their value to match other rules, which is a extremly hard problem
        for jp_mahjong ver -1.1
'''
import pygame
from const import TILE_RATIO

mahjong_tile_elements = {
    1: '1m', 2: '2m', 3: '3m', 4: '4m', 5: '5m', 6: '6m', 7: '7m', 8: '8m', 9: '9m',
    11: '1p', 12: '2p', 13: '3p', 14: '4p', 15: '5p', 16: '6p', 17: '7p', 18: '8p', 19: '9p',
    21: '1s', 22: '2s', 23: '3s', 24: '4s', 25: '5s', 26: '6s', 27: '7s', 28: '8s', 29: '9s',
    31: '1z', 32: '2z', 33: '3z', 34: '4z',
    41: '5z', 42: '6z', 43: '7z'
}

find_num_using_tile = {v: k for k, v in mahjong_tile_elements.items()}

key_list = list(mahjong_tile_elements.keys())

red_dora_id = [19, 55, 91]
red_dora_ele = {19: '0m', 55: '0p', 91: '0s'}


class tile:
    value = -1
    id = -1
    img = None
    
    def __init__(self, value, id, SCREEN_HEIGHT):
        self.value = value
        self.id = id
        if id not in red_dora_id:
            self.img = pygame.image.load(f'../img/tiles/{mahjong_tile_elements[value]}.png')
        else:
            self.img = pygame.image.load(f'../img/tiles/{red_dora_ele[id]}.png')
        
        # resize the tile
        self.size = (0.7 * SCREEN_HEIGHT / TILE_RATIO, SCREEN_HEIGHT / TILE_RATIO)
        self.img = pygame.transform.smoothscale(surface=self.img, size=self.size)
        self.hover = False
        self.selected = False
        self.last_click = 0
        
        
    def select_by_id(self, id):
        if id == self.id:
            return self
            
            
    def get_value_id(self):
        return (self.value, self.id)
        
    
    def get_effect(self):
        return (self.hover, self.selected)
    
    
    def set_effect(self, hover, selected):
        self.hover = hover
        self.selected = selected


def generate_tiles(SCREEN_HEIGHT):
    all_tiles = []
    for id in range(136):
        value = key_list[id // 4]
        all_tiles.append(tile(value, id, SCREEN_HEIGHT))
    return all_tiles

