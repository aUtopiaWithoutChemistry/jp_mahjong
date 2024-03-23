from element import tiles_to_value
from player import player

''' TODO change the original function fit the new tile, the input tile should be in the form of
    (value, id) all functions can only take player and game as parameters
'''


# rules for winning
def win(player):
    return True if clear_win(player) or chi_peng_gang_win(player) else False


def chi_peng_gang_win(player):
    ''' have chi_peng_gang
        >>> tiles = [41, 41, 41, 42, 42]
        >>> chi_peng_gang_tiles = [[0, [1, 2, 3]], [0, [4, 5, 6]], [0, [7, 8, 9]]]
        >>> chi_peng_gang_win(tiles, chi_peng_gang_tiles)
        True
    '''
    n = len(chi_peng_gang_tiles)
    return True if composition(tiles, n) else False


def clear_win(tiles):
    ''' 门前清 '''
    return True if special_win(tiles) or regular_win(tiles) else False


def special_win(tiles):
    return True if seven_double(tiles) == 7 or guo_shi(tiles) else False


def regular_win(tiles):
    ''' if the composition return True, then the player wins

        >>> tiles = [41, 41, 41, 42, 42, 42, 43, 43, 43, 0, 5, 10, 15, 15]
        >>> regular_win(tiles)
        True
    '''
    return True if composition(tiles, 0) else False


# TODO
def check_point(player):
    fan = check_fan(player)
    fu = check_fu(player)
    basic_point = bp(fan, fu, player)
    return False


def check_fan(player):
    if seven_double(player.my_tiles) == 7:
        fan = 2
    return fan


def check_fu(player):
    if seven_double(player.my_tiles) == 7:
        fu = 25
    return fu


def bp(fan, fu):
    basic_point = fu * 2 ** (fan + 2)
    if basic_point > 2000:
        if fan <= 5:
            basic_point = 2000
        elif fan >= 6 and fan <= 7:
            basic_point = 3000
        elif fan >= 8 and fan <= 10:
            basic_point = 4000
        elif fan >= 11 and fan <= 12:
            basic_point = 6000
        elif fan >= 13:
            basic_point = 8000
    return basic_point


# TODO 各种役
# 一番役
def duan_yao_jiu(player):
    ''' 断幺九 without yao jiu tiles when win
        yao jiu tiles: 1, 9, 11, 19, 21, 29, 31, 32, 33, 34, 41, 42, 43
        
        >>> player1 = player()
        >>> player1.my_tiles = [(2,4), (3,9), (4,15), (5,16), (5,18), (5, 19), (6,20), (6,21), (6,22), (7,24), (7,25), (7,26), (8,28), (8,30)]
        >>> duan_yao_jiu(player1)
        1
        >>> player1.my_tiles = [(2,4), (3,9), (4,15), (5,16), (5,18), (5, 19), (6,20), (6,21), (6,22), (7,24), (7,25), (7,26), (9,32), (9,33)]
        >>> duan_yao_jiu(player1)
        0
        >>> player1.my_tiles = [(18,66), (18,67)]
        >>> player1.chi_peng_gang_tiles = [(11, [(2,4), (2,5), (2,6)]),(11, [(3,9), (3,10), (3,11)]),(11, [(4,12), (4,13), (4,14)]),(11, [(5,16), (5,17), (5,19)])]
        >>> duan_yao_jiu(player1)
        1
    '''
    tiles = player.my_tiles
    chi_peng_gang_tiles = [group[1] for group in player.chi_peng_gang_tiles]
    for group in chi_peng_gang_tiles:
        tiles += group
    yao_jiu = [tile[0] for tile in tiles if tile[0] in [1, 9, 11, 19, 21, 29, 31, 32, 33, 34, 41, 42, 43]]
    return 1 if len(yao_jiu) == 0 else 0


def yi_tiles(game, player, tiles):
    ''' 役牌刻子或杠子，如场风、自风、三元牌 contains (dong, xi, nan, bei) one kezi of corresponding my position 
        or chang_feng, bai, fa, zhong, which is 41, 42, 43 and 31 + cur_chang or 31 + cur_position
        
        >>> tiles1 = [(32,112), (32,112), (32,112)]
        >>> player1 = player(0, 25000, [], 1, False)
        >>> game1 = game()
        >>> game1.cur_chang = 0
        
    '''
    valid_yi = [game.cur_chang + 31, player.cur_position + 31, 41, 42, 43]
    return 1 if tiles in valid_yi else 0
    
    
def he_di_mo_yu(game):
    ''' 河底摸鱼 use the last tile to win the game
        tiles = [(), (), (), (), (), (), (), (), (), (), (), (), (), ()]
    '''
    return 1 if game.this_game == [] else 0


def ling_shang_kai_hua(player):
    ''' 岭上开花 use the ling shang tile to win the game
        tiles = [(), (), (), (), (), (), (), (), (), (), (), (), (), ()]
    '''
    return 1 if (player.all_behavior[- 1][1] == 'mopai' and 
                 player.all_behavior[- 2][1] in ['hidden_gang', 'add_gang', 'gang']) else 0


def qiang_gang(players, time_stamp):
    ''' 抢杠 use other player's add_gang tile to win
        tiles = [(), (), (), (), (), (), (), (), (), (), (), (), (), ()]
    '''
    for player in players:
        if player.all_behavior[-1][0] == time_stamp and player.all_behavior[-1][1] == 'add_gang':
            return 1 
    return 0
    
    
def hai_di_lao_yue(game, player):
    ''' 海底捞月 zimo the last tile
        tiles = [(), (), (), (), (), (), (), (), (), (), (), (), (), ()]
    '''
    return 1 if game.this_game == [] and player.all_behavior[-1][1] == 'mopai' else 0
    
    
def riichi(player):
    ''' リーチ 立直 
        tiles = [(), (), (), (), (), (), (), (), (), (), (), (), (), ()]
    '''
    for behavior in player.all_behavior:
        if behavior[1] == 'riichi':
            return 1 
    return 0


def yi_fa(winner, players):
    ''' 一发 yifa means after riichi, win the game inside one circle, and during this time 
        should no one chi, peng, or gang, if this player can win by other's add_gang, then 
        add_gang invalid, this player still can yifa
        tiles = [(), (), (), (), (), (), (), (), (), (), (), (), (), ()]
    '''
    all_behavior_after_riichi = []
    for behavior in winner.all_behavior:
        if behavior[1] == 'riichi':
            riichi_turn = behavior[0]
    for player in players:
        for behavior in player.all_bahavior:
            if behavior[0] > riichi_turn:
                all_behavior_after_riichi += behavior
    
    
def clear_zimo(game):
    ''' 门前清自摸和 clear win + zimo
        tiles = [(), (), (), (), (), (), (), (), (), (), (), (), (), ()]
    '''
    cur_ju = game.cur_chang * 4 + game.cur_ju
    player = game.all_behavior[cur_ju][-1][1]
    behavior = game.all_behavior[cur_ju][-1][2]
    return 1 if regular_win(player.my_tiles) and behavior == 'zimo' else 0


def ping_hu(game):
    ''' 平和 don't have extra fu except from zimo, which means only have shunzi and 
        double can't be zifeng, changfeng, and sanyuan tiles, and should ting pai for two tiles
        tiles = [(), (), (), (), (), (), (), (), (), (), (), (), (), ()]
    '''
    cur_ju = game.cur_chang * 4 + game.cur_ju
    player = game.all_behavior[cur_ju][-1][1]
    all_tiles = player.my_tiles + [tile[1] for tile in player.chi_peng_gang_tiles]
    return 1
    
    
def seven_double(tiles):
    if len(tiles) == 0:
        return 1
    elif tiles[1][0] != tiles[0][0]:
        return 0
    else:
        return 1 + seven_double(tiles[2:])


def guo_shi(tiles):
    tiles = tiles_to_value(tiles)
    standard_guo_shi = [1, 9, 11, 19, 21, 29, 31, 32, 33, 34, 41, 42, 43]
    for i in range(len(standard_guo_shi)):
        if standard_guo_shi[i] not in tiles:
            return False
    return True


def split_tiles(cond):
    ''' to split all tiles in to five type of tiles, ease the following judgement

        >>> tiles = [0, 5, 8, 8, 8, 41, 41, 41, 42, 42, 42, 43, 43, 43]
        >>> split_man = split_tiles(man)
        >>> new_tiles = split_man(tiles)
        >>> new_tiles
        [0, 5, 8, 8, 8]
        >>> split_feng = split_tiles(feng)
        >>> new_tiles = split_feng(tiles)
        >>> new_tiles
        []
        >>> split_man = split_tiles(sanyuan)
        >>> new_tiles = split_man(tiles)
        >>> new_tiles
        [41, 41, 41, 42, 42, 42, 43, 43, 43]
    '''
    def func(tiles):
        sub_list = [tile for tile in tiles if cond(tile)]
        return sub_list
    return func


# condition statement for split_tiles
def man(tile): 
    return True if tile > -1 and tile < 10 else False

def ping(tile):
    return True if tile > 9 and tile < 20 else False

def suo(tile):
    return True if tile > 19 and tile < 30 else False

def feng(tile):
    return True if tile > 30 and tile < 35 else False

def sanyuan(tile):
    return True if tile > 40 and tile < 44 else False


# return a function that judge if there are x same tiles in a list
def x_continously(my_tiles, x):
    ''' return a function to test are there x continously tiles in
        a players tiles, if there have x tiles ,then the return 
        function will return True, vice versa
        >>> my_tiles = [1, 1, 1, 1, 2, 3, 4]
        >>> three_con = x_continously(my_tiles, 3)
        >>> three_con(1)
        False
        >>> four_con = x_continously(my_tiles, 4)
        >>> four_con(1)
        True
    '''
    test_tiles = [x for x in my_tiles]
    def func(tile):
        cnt = 1
        cnt_max = 1
        for n in range(len(test_tiles) - 1):
            if test_tiles[n] == test_tiles[n + 1] and test_tiles[n] == tile:
                cnt += 1
                if cnt > cnt_max:
                    cnt_max = cnt
            else:
                cnt = 1
        if cnt_max == x:
            return True
        return False
    return func


def shun_zi(tiles):
    ''' shun_zi is three adjacent tiles have the relationship of [n, n + 1, n + 2]
        since all the number tiles are separated(1~9, 11~19, 21~29)

        >>> tiles = [(4,14), (5,19), (6,23)]
        >>> shun_zi(tiles)
        True
        >>> tiles = [(41,124), (42,128), (43,132)]
        >>> shun_zi(tiles)
        False
        >>> tiles = [(), (), ()]
    '''
    tiles.sort()
    for tile in tiles:
        if tile[0] > 30:
            return False

    return True if tiles[0][0] + 1 == tiles[1][0] and tiles[1][0] + 1 == tiles[2][0] else False


def ke_zi(tiles):
    ''' ke_zi is three adjacent tiles have the same value

        >>> tiles = [10, 15, 15]
        >>> ke_zi(tiles)
        True
        >>> tiles = [41, 41, 41]
        >>> ke_zi(tiles)
        True
        >>> tiles = [41, 42, 43]
        >>> ke_zi(tiles)
        False
    '''
    return True if tiles[0][0] == tiles[1][0] and tiles[1][0] == tiles[2][0] else False


def double(tiles):
    ''' double is nesscery for win in jp mahjong

        >>> tiles = [0, 5]
        >>> double(tiles)
        True
        >>> tiles = [43, 43]
        >>> double(tiles)
        True
        >>> tiles = [42, 41]
        >>> double(tiles)
        False
    '''
    return True if tiles[0] == tiles[1] else False


def yi_bei_kou(tiles):
    ''' test for yi_bei_kou  Thanks for copilot to help me write this light version
    '''
    return all(tiles[i][0] == tiles[i + 1][0] for i in range(0, 5, 2)) and tiles[4][0] == tiles[2][0] + 1 == tiles[0][0] + 2


def overlapping(tiles):
    ''' sometimes there will be overlapping in tiles, which makes shun_zi cannot detect
        them, but ther are still valid, like [1, 2, 2, 3, 3, 4]
        
        This funciton will take a list as argument, and there are only 6 items inside

        >>> tiles = [(1,0), (1,1), (2,5), (2,6), (3,9), (3,10)]
        >>> overlapping(tiles)
        True
        >>> tiles = [(3,10), (4,13), (4,14), (5,18), (5,19), (6,22)]
        >>> overlapping(tiles)
        True
        >>> tiles = [(41,124), (41,125), (42,128), (42,129), (43,132), (43,133)]
        >>> overlapping (tiles)
        False
    '''
    tiles.sort()
    for tile in tiles:
        if tile[0] > 30:
            return False
    
    return True if shun_zi([tiles[0], tiles[1], tiles[3]]) and shun_zi([tiles[2], tiles[4], tiles[5]]) else False


def composition_mianzi(tiles):
    ''' check how many mianzi are there in tiles, this often apply on tiles that
        removed double, which can avoid some errors
        
        the return value should be a clasified list, which contains two to four group
        of tiles, and should marked it's type
        
        for example, the input is [(1,0), (1,1), (2,4), (2,6), (3,8), (3,9), (5,16), (5,18), (5,19), (14,49), (16,58), (15,55)]
        the output should be [(2, [(1,0), (1,1), (2,4), (2,6), (3,8), (3,9)]), (1, [(5,16), (5,18), (5,19)]), (0, [(14,49), (16,58), (15,55)])]
                             [(type, [tile_list]), (), ()]   
                             for type, 0 means shunzi, 1 means kezi, 2 means yibeiko
                             
        >>> tiles = [(1,0), (1,1), (2,4), (2,6), (3,8), (3,9), (5,16), (5,18), (5,19), (14,49), (16,58), (15,55)]
        >>> composition_mianzi(tiles)
        [(2, [(1, 0), (1, 1), (2, 4), (2, 6), (3, 8), (3, 9)]), (1, [(5, 16), (5, 18), (5, 19)]), (0, [(14, 49), (16, 58), (15, 55)])]
    '''
    if tiles == []:
        return []
    elif len(tiles) > 2 and shun_zi(tiles[:3]):
        return_value, remain = [(0, tiles[:3])], tiles[3:]
    elif len(tiles) > 2 and ke_zi(tiles[:3]):
        return_value, remain = [(1, tiles[:3])], tiles[3:]
    elif len(tiles) > 5 and yi_bei_kou(tiles[:6]):
        return_value, remain = [(2, tiles[:6])], tiles[6:]
    elif len(tiles) > 5 and overlapping(tiles[:6]):
        original_list = tiles[:6]
        new_set = set(original_list)
        new_list = list(new_set)[:3]
        return_value = [(1, new_list)]
        
        tmp = [item for item in new_list]
        for item in original_list:
            if item in new_list:
                original_list.pop(original_list.index(item))
                tmp.pop(tmp.index(item))
                
        return_value += [(1, original_list)]
        remain = tiles[6:]
    else:
        return composition_mianzi(tiles[1:])
    return return_value + composition_mianzi(remain)


def composition(player):
    ''' take player as input, orgnaize my_tiles into group
        the return value are in the form of [(-1, []), (0, []), (), (), ()]
        -1 means double, 0 means shunzi, 1 means kezi

        >>> player1 = player()
        >>> player1.my_tiles = [(1,0), (1,1), (1,2), (2,4), (3,8), (4,12), (5,16), (5,18), (6,23), (7,24), (8,31), (9,32), (9,33), (9,34)]
        >>> composition(player1)
        [(-1, [(5,16), (5,18)])), (0, [(2,4), (3,8), (4,12)]), (0, [(6,23), (7,24), (8,31)]), (1, [(1,0), (1,1), (1,2)], (1, [(9,32), (9,33), (9,34)])]
        >>> player1.my_tiles = [1, 1, 1, 2, 2, 2, 3, 3, 42, 42, 5, 5, 6, 6]
        >>> composition(player1)
        False
        >>> player1.my_tiles = [(1,0), (1,1)]
        >>> player1.chi_peng_gang_tiles = [(10, [(2,4), (2,5), (2,6)]), (10, [(3,8), (3,9), (3,10)]), (10, [(4,12), (4,13), (4,14)]), (10, [(5,16), (5,17), (5,19)])]
        >>> composition(player1)
        [(-1, [(1, 1), (1, 0)]), (10, [(2, 4), (2, 5), (2, 6)]), (10, [(3, 8), (3, 9), (3, 10)]), (10, [(4, 12), (4, 13), (4, 14)]), (10, [(5, 16), (5, 17), (5, 19)])]
    '''
    my_tiles = player.my_tiles
    organized_tiles = player.chi_peng_gang_tiles
    for i in range(len(my_tiles) - 1):
        if double([my_tiles[i][0], my_tiles[i + 1][0]]):
            test_tiles = [tile for tile in my_tiles]
            double_tiles = [(-1, [test_tiles.pop(i + 1), test_tiles.pop(i)])]
            tiles_comp = double_tiles
            tiles_comp += composition_mianzi(test_tiles)
            tiles_comp += organized_tiles
            tiles_comp.sort()
            if len(tiles_comp) == 5:
                return tiles_comp
            elif len(tiles_comp) == 4:
                for group in tiles_comp:
                    if group[0] == 2:
                        return tiles_comp 
            elif len(tiles_comp) == 3:
                if tiles_comp[0][0] == 2 and tiles_comp[1][0] == 2:
                    return tiles_comp
    return False
