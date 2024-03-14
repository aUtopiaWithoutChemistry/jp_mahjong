import random
from element import all_tiles, mahjong_tile_elements

# player class，包含属性：点数、手牌、自风、弃牌，
# 函数：摸牌✅、弃牌✅、吃、碰、杠、和、立直、加杠
class player:
    score = 0 # should start with 25000
    my_tiles = [] # store all tiles of a player
    my_position = -1
    my_waste = []

    def __init__(self, score, tiles, position):
        self.score = score
        self.my_tiles = tiles
        self.my_position = position

    def mopai(self):
        self.my_tiles.append(this_game.pop(0))
        self.my_tiles.sort()

    def discard(self):
        print("Here is all your tiles: ")
        for tile in self.my_tiles:
            print(mahjong_tile_elements[self.my_tiles[tile]], end = " ")
        discard_tile = input("Please select which tiles to discard: ")
        tile_num = mahjong_tile_elements[discard_tile]
        self.my_tiles.pop(tile_num)

    def chi(self, current_tile):
        if current_tile[1] == (self.my_position - 1) or current_tile[1] == (self.my_position + 3):
            if current_tile < 30 and current_tileself.my_tiles:
                

# table class，包含四个玩家和剩余牌
class table:
    current_tile = (-1, -1) # the first number shows the tile, second shows where it from
    current_player = -1
    total_chang = 0
    cur_chang = 0
    cur_ju = 0

    def __init__(self, total_chang):
        self.total_chang = total_chang


# generate the shuffled tiles for this game
this_game = []

for ele in all_tiles:
    this_game.append(ele)
random.shuffle(this_game)

