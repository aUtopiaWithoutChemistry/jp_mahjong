import random
from element import all_tiles, mahjong_tile_elements, find_num_using_tile
from rules import x_continously, win, deal_red

# player class，包含属性：点数、手牌、自风、弃牌，
# 函数：摸牌✅、弃牌✅、吃、碰、杠、暗杠、立直、加杠
#               check:吃、碰、杠、暗杠、立直、加杠
class player:
    score = 0 # should start with 25000
    my_tiles = [] # store all tiles of a player
    my_position = -1
    my_waste = []
    chi_pong_gang_tiles = []


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


    def check_hidden_gang(self):
        ''' check if have hidden gang using my tiles

            >>> player1 = player(25000, [], 0)
            >>> player1.my_tiles = [1, 1, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 30, 30]
            >>> player1.check_hidden_gang()
            True
            >>> player1.my_tiles = [1, 1, 1, 2, 3, 4, 5, 5, 6, 7, 8, 9, 9, 9]
            >>> player1.check_hidden_gang()
            False
        '''
        for tile in self.my_tiles:
            four_con = x_continously(self.my_tiles, 4)
            if four_con(tile):
                return True
        return False


    def check_gang(self, current_tile):
        ''' check if could gang using other's waste tile

            >>> player1 = player(25000, [], 0)
            >>> player1.my_tiles = [1, 1, 1, 2, 3, 4, 5, 5, 6, 7, 8, 9, 9]
            >>> current_tile = (1, 3)
            >>> player1.check_gang(current_tile)
            True
            >>> player1.my_tiles = [1, 1, 2, 2, 3, 4, 5, 5, 6, 7, 8, 9, 9]
            >>> player1.check_gang(current_tile)
            False
        '''
        test_tiles = [tile for tile in self.my_tiles]
        test_tiles.append(current_tile[0])
        test_tiles = deal_red(test_tiles)
        test_tiles.sort()
        four_con = x_continously(test_tiles, 4)
        return True if four_con(current_tile[0]) else False
    

    def check_add_gang(self, current_tile):
        return False


    def check_peng(self, current_tile):
        ''' check if could peng using other's waste tile

            >>> player1 = player(25000, [], 0)
            >>> player1.my_tiles = [1, 1, 2, 2, 3, 4, 5, 5, 6, 7, 8, 9, 9]
            >>> current_tile = (0, 3)
            >>> player1.check_peng(current_tile)
            True
            >>> player1.my_tiles = [1, 2, 2, 2, 3, 4, 4, 5, 6, 7, 8, 9, 9]
            >>> player1.check_peng(current_tile)
            False
        '''
        test_tiles = [tile for tile in self.my_tiles]
        test_tiles.append(current_tile[0])
        test_tiles = deal_red(test_tiles)
        test_tiles.sort()
        three_con = x_continously(test_tiles, 3)
        if current_tile[0] // 10 == 0:
            return True if three_con(current_tile[0] + 5) else False
        else:
            return True if three_con(current_tile[0]) else False


    def check_richi(self, this_game):
        ''' richi means player needs only one tile to win the game, after the player 
            richi, then this player must automatically drop the new tile if he can't win
            with this tile

            >>> player1 = player(25000, [], 0)
            >>> player1.my_tiles = [1, 1, 1, 2, 3, 4, 0, 6, 7, 8, 9, 9, 9, 41]
            >>> for ele in player1.my_tiles:
            ...     all_tiles.remove(ele)
            >>> this_game = all_tiles
            >>> player1.check_richi(this_game)
            True
        '''
        test_tiles = [tile for tile in self.my_tiles]
        test_tiles = deal_red(test_tiles)
        for tile in range(len(test_tiles)):
            for ele in this_game:
                test_tiles.pop(tile)
                test_tiles.append(ele)
                if win(test_tiles):
                    return True
        return False


    def check_chi(self, current_tile):
        ''' check_chi returns a boolean value to represent if current player can chi the tile 
            from last player's waste tile which is current_tile

            >>> player1 = player(25000, [], 1)
            >>> current_tile = (4, 0)
            >>> player1.my_tiles = [2, 3, 0, 6, 7]
            >>> player1.check_chi(current_tile)
            True
        '''
        if current_tile[1] == (self.my_position - 1) or current_tile[1] == (self.my_position + 3):
            tile_type = current_tile[0] // 10
            valid_chi_list = [tile for tile in self.my_tiles if tile // 10 == tile_type]
            valid_chi_list = deal_red(valid_chi_list)
            valid_chi_list.sort()
            if current_tile[0] > 30:
                return False
            elif (((current_tile[0] - 2) in valid_chi_list) and ((current_tile[0] - 1) in valid_chi_list) or
                  ((current_tile[0] - 1) in valid_chi_list) and ((current_tile[0] + 1) in valid_chi_list) or
                  ((current_tile[0] + 1) in valid_chi_list) and ((current_tile[0] + 2) in valid_chi_list)):
                return True
            else:
                return False
        else:
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
            self.players.append(player(25000, [], n))


    def next_round(self):
        random.shuffle(self.this_game)

