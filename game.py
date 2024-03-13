import random
from element import all_tiles

# player class，包含属性：点数、手牌、自风、弃牌，函数：摸牌、弃牌、吃、碰、杠、和、立直、加杠
class player:
    score = 0
    my_tile = []
    my_position = None
    my_waste = []

    def __init__(self, score, tile, position):
        self.score = score
        self.my_tile = tile


# table class，包含四个玩家和剩余牌
class table:
    current_tile = -1


# generate the shuffled tiles for this game
this_game = []

for ele in all_tiles:
    this_game.append(ele)
random.shuffle(this_game)

