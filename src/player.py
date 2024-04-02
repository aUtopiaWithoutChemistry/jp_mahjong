import pygame
import gc
from element import tile, generate_tiles, mahjong_tile_elements, find_num_using_tile

all_tiles = generate_tiles()

# player class，包含属性：点数、手牌、自风、弃牌堆、是否为AI、吃碰杠堆
# 函数：摸牌✅、弃牌✅、吃、碰、加杠、杠、暗杠、立直
# all check:吃、碰、加杠、杠、暗杠、立直 will be move into rules
class player:
    number = 0
    is_ai = False
    score = 0 # should start with 25000
    my_tiles = [] # store all tiles of a player
    my_position = -1
    my_waste = []
    
    ''' tiles in chi_peng_gang_tiles will store in group, like
            [(10, [(1,0), (2,0), (3,0)]), (11, [(5,0), (5,), (5,0)]), (12, [(41,0), (41,0), (41,0), (41,0)]), (13, [(42,0), (42,0), (42,0), (42,0)])]
        each group contains two elements, the first represent it's type, 10 is chi, 11 is peng, 
        12 is gang, 13 is hidden_gang. the second element is a list shows all the tiles in this group.
    '''
    chi_peng_gang_tiles = []
    

    def __init__(self, number=0, score=25000, tiles=[], position=0, is_ai=True, chi_peng_gang_tiles=[],
                 my_waste=[]):
        self.number = number
        self.score = score
        self.my_tiles = tiles
        self.my_position = position
        self.is_ai = is_ai
        self.chi_peng_gang_tiles = chi_peng_gang_tiles
        self.my_waste = my_waste

    # sort all tiles
    def sort_tiles(self):
        cur_list = []
        for tile in self.my_tiles:
            cur_list.append(tile.get_value_id())
        cur_list.sort()
        new_tiles = []
        for value,id in cur_list:
            for tile in self.my_tiles:
                if tile.select_by_id(id) is not None:
                    new_tiles.append(tile.select_by_id(id))
        self.my_tiles = new_tiles
        
    
    # display all my tiles
    def display_my_tiles(self, surface):
        x = 100
        for i in range(len(self.my_tiles)):
            tile_rect = self.my_tiles[i].img.get_rect(bottomleft=(25 + x, 900 - 25))
            tile_rect = self.effects(self.my_tiles[i], tile_rect)
            surface.blit(self.my_tiles[i].img, tile_rect)
            x += 49
            
            
    def effects(self, tile, tile_rect):
        is_hover, is_selected = tile.get_effect()
        if tile_rect[1] == 900 - 25 - 70:
            is_hover = False
        else:
            is_hover = True
        
        # set a last_click to prevent quick double click
        if tile_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and \
            tile.last_click <= 0:
            is_selected = not is_selected
            tile.last_click = 5
        tile.last_click -= 1
        
        # add hover and selected effect
        if (tile_rect.collidepoint(pygame.mouse.get_pos()) and not is_hover) or is_selected:
            tile_rect = tile_rect.move(0, -20)
            
        tile.set_effect(is_hover, is_selected)
        return tile_rect
    
            
    def display(self, surface):
        pass

    # all the movement can be done by players integraded both
    # human and AI
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
        cur_tile = this_game.pop(0)
        self.my_tiles.append(cur_tile)
        
    
    def sort(self):
        pass
    
    
    # all movement
    def discard(self):
        if self.is_ai:
            selected_tile = self.ai_discard()
        else:
            selected_tile = self.human_discard()
        
        # put selected tile into waste section
        self.my_tiles.remove(selected_tile)
        self.my_waste.append(selected_tile)
            

    def chi(self):
        if self.is_ai:
            self.ai_chi()
        else:
            self.human_chi()
            

    def peng(self):
        if self.is_ai:
            self.ai_peng()
        else:
            self.human_peng()
            

    def gang(self):
        if self.is_ai:
            self.ai_gang()
        else:
            self.human_gang()
            

    def add_gang(self):
        if self.is_ai:
            self.ai_add_gang()
        else:
            self.human_add_gang()


    def hidden_gang(self):
        if self.is_ai:
            self.ai_hidden_gang()
        else:
            self.human_hidden_gang()
            

    def riichi(self):
        if self.is_ai:
            self.ai_riichi()
        else:
            self.human_riichi()
  
        
    # human movements
    def human_discard(self):
        ''' remove the selected item from player's tiles and move it 
            into waste tiles
        '''
        print("Here is all your tiles: ")
        for tile in range(len(self.my_tiles)):
            print(mahjong_tile_elements[self.my_tiles[tile]], end = " ")
        print('')
        discard_tile = input("Please select which tiles to discard: ")
        tile_num = find_num_using_tile[discard_tile]
        self.my_waste.append(self.my_tiles.pop(self.my_tiles.index(tile_num)))
        return True

    def human_chi(self, current_tile):
        ''' if player on your left side discard a tile that can used by you to build a shun_zi
            then you can chi, and move the shun_zi in to your chi_peng_gang_tiles
        '''
        combination = self.check_chi(current_tile)
        if combination != 0:
            decision = input("Chi or not?(Y/N) ").upper()
            if decision == 'Y':
                combo = []
                type = current_tile[0] // 10
                test_tiles = [tile for tile in self.my_tiles if (tile // 10) == type]
                test_tiles.sort()
                test_tile = current_tile[0] if (current_tile[0] % 10) != 0 else current_tile[0] + 5
                if (test_tile - 2 in test_tiles) and (test_tile - 1 in test_tiles):
                    combo += [[test_tile - 2, test_tile - 1, test_tile]]
                if (test_tile - 1 in test_tiles) and (test_tile + 1 in test_tiles):
                    combo += [[test_tile - 1, test_tile, test_tile + 1]]
                if (test_tile + 1 in test_tiles) and (test_tile + 2 in test_tiles):
                    combo += [[test_tile, test_tile + 1, test_tile + 2]]
                which = input("Which combo you want to Chi? " + ' '.join(str(item) for item in combo) + ' ')
                self.chi_peng_gang_tiles += [0, combo[int(which)]]
                return True
            else:
                return False


    def human_peng():
        return False
    

    def human_gang():
        return False
    

    def human_add_gang():
        return False


    def human_hidden_gang():
        return False


    def human_riichi():
        return False
    

    # AI movements
    def ai_discard(self):
        return False


    def ai_chi(self):
        return False
    

    def ai_peng(self):
        return False
    

    def ai_gang(self):
        return False
    

    def ai_add_gang(self):
        return False


    def ai_hidden_gang(self):
        return False


    def ai_riichi(self):
        return False


    # check if a movement is valid 
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
        return False
    

    def check_add_gang(self):
        ''' add_gang means player have one ke_zi in chi_pong_gang_tiles, and get the same tile
            as the tiles in ke_zi, then the player can add_gang, put this new tile into his 
            chi_pong_gang_tiles and get a new tile

            >>> player1 = player(25000, [], 0)
            >>> player1.chi_peng_gang_tiles = [[1, [5, 0, 5]]]
            >>> player1.my_tiles = [1, 1, 2, 2, 3, 5, 9]
            >>> player1.check_add_gang()
            True
            >>> player1.chi_peng_gang_tiles = [[1, [4, 4, 4]]]
            >>> player1.check_add_gang()
            False
        '''
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

        return False


    def check_riichi(self, this_game):
        ''' riichi means player needs only one tile to win the game, after the player 
            riichi, then this player must automatically drop the new tile if he can't win
            with this tile

            >>> player1 = player(25000, [], 0)
            >>> player1.my_tiles = [1, 1, 1, 2, 3, 4, 0, 6, 7, 8, 9, 9, 9, 41]
            >>> for ele in player1.my_tiles:
            ...     all_tiles.remove(ele)
            >>> this_game = all_tiles
            >>> player1.check_riichi(this_game)
            True
        '''

        return False
    

    def check_ting_pai(self, cur_tile):
        return False


    def final_check_ting_pai(self):
        ''' ting pai means if get a specific tile, this player can win this game
            >>> player1 = player(25000, [], 1)
            >>> player1.my_tiles, player1.chi_peng_gang_tiles = [1, 1, 1, 2, 2, 2], []
            >>>
        '''

        return False


    def check_chi(self, current_tile):
        ''' check_chi returns a value to represent if current player can chi the tile 
            from last player's waste tile which is current_tile. if can chi, then value 
            is how many ways to chi, if cannot, then return 0

            >>> player1 = player(25000, [], 1)
            >>> current_tile = (4, 0)
            >>> player1.my_tiles = [2, 3, 0, 6, 7]
            >>> player1.check_chi(current_tile)
            3
            >>> player1.my_tiles = [1, 2, 3, 3, 5, 5]
            >>> player1.check_chi(current_tile)
            2
            >>> player1.my_tiles = [3, 3, 6]
            >>> player1.check_chi(current_tile)
            0
        '''
        return 0