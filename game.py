import random
from element import all_tiles, mahjong_tile_elements, find_num_using_tile
from rules import x_continously, clear_win, deal_red
from player import player

# table class，包含四个玩家和剩余牌
class game:
    current_tile = ((-1, -1), -1) # the first tuple shows the tile, second shows where it from
    current_player = -1 # how many players in there
    total_chang = 0
    cur_chang = 0
    cur_ju = 0
    this_game = []
    players = []


    def __init__(self, total_chang, total_player):
        # decide how many chang in total should be played
        self.total_chang = total_chang

        # add all mahjong tiles in this game
        for ele in all_tiles:
            self.this_game.append(ele)

        # shuffle all the tiles
        self.next_round()

        # create n players
        for n in range(total_player):
            self.players.append(player(25000, [], n, False))


    def next_round(self):
        random.shuffle(self.this_game)

