import random
from element import all_tiles, mahjong_tile_elements, find_num_using_tile

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

    def mopai(self, this_game):
        ''' remove the first item in this_game and add into my_tiles

        >>> player1 = player(0, [], 0)
        >>> this_game = [19, 8, 9, 6, 4]
        >>> player1.mopai(this_game)
        >>> player1.my_tiles
        [19]
        >>> this_game
        [8, 9, 6, 4]
        '''
        self.my_tiles.append(this_game.pop(0))
        self.my_tiles.sort()

    def discard(self):
        ''' remove the selected item from player's tiles and move it 
            into waste tiles

            >>> player1 = player(25000, [], 0)
            >>> player1.my_tiles = [1, 2, 3, 4, 5]
            >>> player1.discard()
            Here is all your tiles: 
            1m 2m 3m 4m 5m 
            >>> player1.my_tiles
            [2, 3, 4, 5]
            >>> player1.my_waste
            [1]
        '''
        print("Here is all your tiles: ")
        for tile in range(len(self.my_tiles)):
            print(mahjong_tile_elements[self.my_tiles[tile]], end = " ")
        print('')
        # this is original 
        # discard_tile = input("Please select which tiles to discard: ")
        discard_tile = '1m'
        tile_num = find_num_using_tile[discard_tile]
        self.my_waste.append(self.my_tiles.pop(self.my_tiles.index(tile_num)))

    def chi(self, current_tile):
        if current_tile[1] == (self.my_position - 1) or current_tile[1] == (self.my_position + 3):
            if current_tile < 30 and current_tile == self.my_tiles:
                return False

# table class，包含四个玩家和剩余牌
class game:
    current_tile = (-1, -1) # the first number shows the tile, second shows where it from
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

        # create n players
        for n in range(total_player):
            self.players.append(player)

    def next_round(self):
        random.shuffle(self.this_game)

