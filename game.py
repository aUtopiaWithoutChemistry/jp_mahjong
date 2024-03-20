import random
from element import all_tiles, mahjong_tile_elements, find_num_using_tile
from rules import win
from player import player

# table class，包含四个玩家和剩余牌
class game:
    current_tile = ((-1, -1), -1) # the first tuple shows the tile, second shows where it from
    cur_player = -1 # how many players in there
    total_chang = 0
    cur_chang = -1
    cur_ju = -1
    this_game = []
    players = []
    ling_shang_tiles = []   # max 4, only can be access when someone gang
    surface_dora_tiles = [] # max 1, visable from starting
    hidden_dora_tiles = []  # max 4, every riichi from player will show one more
    gang_dora_tiles = []    # max 4, every gang from player will show one more


    def __init__(self, total_chang, total_player):
        # decide how many chang in total should be played
        self.total_chang = total_chang

        # add all mahjong tiles in this game
        for ele in all_tiles:
            self.this_game.append(ele)

        # shuffle all the tiles
        self.this_game.shuffle()

        # create n players
        for n in range(total_player):
            self.players.append(player(25000, [], n, False))


    def shuffle(self):
        random.shuffle(self.this_game)


    def end(self):
        self.check_point()
        return False
    

    def check_point():
        return False
    

    def next_item(self, item):
        ''' both player and ju should in [0, 3]
            if reach 3, then next should be 0

            >>> game1 = game(1, 4)
            >>> game1.cur_player = 2
            >>> game1.cur_player = game1.next_item(game1.cur_player)
            >>> game1.cur_player
            3
            >>> game1.cur_player = game1.next_item(game1.cur_player)
            >>> game1.cur_player
            0
        '''
        return item + 1 if item != 3 else 0
    

    def game(self, cur_player, remain_tiles):
        '''
        '''

        # tranfer cur_player from a number to the object 
        # load the info from current player
        player_tiles = cur_player.my_tiles
        player_chi_peng_gang_tiles = cur_player.chi_peng_gang_tiles

        cur_player.mopai(remain_tiles)
        if win(player_tiles, player_chi_peng_gang_tiles):
            self.end()
        if cur_player.check_hidden_gang():
            cur_player.hidden_gang()
            remain_tiles = self.ling_shang_tiles.pop(0)
            
            self.game(cur_player, remain_tiles)




        return False
    

    def ju(self):
        while(len(self.this_game != 0)):
            return False