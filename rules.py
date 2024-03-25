from element import tiles_to_value, all_tiles
from player import player
from const import *

''' TODO change the original function fit the new tile, the input tile should be in the form of
    (value, id) all functions can only take player and parametor from game as parameters
'''

# rules for winning
def win(player):
    return True if clear_win(player) or chi_peng_gang_win(player) else False


def chi_peng_gang_win(player):
    ''' have chi_peng_gang
    
        >>> player1 = player()
        >>> player1.my_tiles = [(41,0), (41,0), (41,0), (42,0), (42,0)]
        >>> player1.chi_peng_gang_tiles = [[0, [(1,0), (2,0), (3,0)]], [0, [(4,0), (5,0), (6,0)]], [0, [(7,0), (8,0), (9,0)]]]
        >>> chi_peng_gang_win(player1)
        True
    '''
    return True if player.chi_peng_gang_tiles != [] and composition(player) else False


def clear_win(player):
    ''' 门前清 
    '''
    return True if special_clear_win(player.my_tiles) or regular_clear_win(player) else False


def special_clear_win(player):
    ''' check if 七对子 or 国士无双
    '''
    return True if seven_double(player) == 7 or guo_shi(player) else False


def regular_clear_win(player):
    ''' if the composition return True, then the player wins

        >>> player1 = player()
        >>> player1.my_tiles = [(41,0), (41,0), (41,0), (42,0), (42,0), (42,0), (43,0), (43,0), (43,0), (5,0), (5,0), (15,0), (15,0), (15,0)]
        >>> regular_clear_win(player1)
        True
    '''
    return True if player.chi_peng_gang_tiles == [] and composition(player) else False


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
        if fan <= 5:                    # 满贯
            basic_point = 2000
        elif fan >= 6 and fan <= 7:     # 跳满
            basic_point = 3000
        elif fan >= 8 and fan <= 10:    # 倍满
            basic_point = 4000
        elif fan >= 11 and fan <= 12:   # 三倍满
            basic_point = 6000
        elif fan >= 13:                 # 役满
            basic_point = 8000
    return basic_point


# TODO 各种役
# 一番役 ################################################################################################
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


def yi_tiles(player, cur_chang):
    ''' 役牌刻子或杠子，如场风、自风、三元牌 contains (dong, xi, nan, bei) one kezi of corresponding my position 
        or chang_feng, bai, fa, zhong, which is 41, 42, 43 and 31 + cur_chang or 31 + cur_position
        
        >>> player1 = player()
        >>> player1.my_tiles = [(1,0),(1,0),(2,0),(2,0),(2,0),(3,0),(3,0),(3,0),(4,0),(4,0),(4,0)]
        >>> player1.chi_peng_gang_tiles = [(11, [(31,0), (31,0), (31,0)])]
        >>> cur_chang = 0
        >>> yi_tiles(player1, cur_chang)
        1
    '''
    valid_yi = [cur_chang + 31, player.my_position + 31, 41, 42, 43]
    all_tiles_groups = composition(player)
    for group in all_tiles_groups:
        if group[0] in [1, 11, 12, 13] and group[1][0][0] in valid_yi:
            return 1
    return 0
    
    
def he_di_mo_yu(this_game, all_behavior):
    ''' 河底摸鱼 use the last tile to win the game
    '''
    return 1 if this_game == [] and all_behavior[-1][2] == 'rong_hu' else 0


def ling_shang_kai_hua(all_behavior):
    ''' 岭上开花 use the ling shang tile to win the game
    '''
    return 1 if (all_behavior[-1][2] == 'zimo' and 
                 all_behavior[-3][2] in ['hidden_gang', 'add_gang', 'gang']) else 0


def qiang_gang(all_behavior):
    ''' 抢杠 use other player's add_gang tile to win
    '''
    return 1 if all_behavior[-1][2] == 'rong_hu' and all_behavior[-2][2] == 'add_gang' else 0
    
    
def hai_di_lao_yue(this_game, all_behavior):
    ''' 海底捞月 zimo the last tile
    '''
    return 1 if this_game == [] and all_behavior[-1][2] == 'zimo' else 0
    
    
def riichi(player, all_behavior):
    ''' リーチ 立直 
    '''
    for behavior in all_behavior:
        if behavior[2] == 'riichi' and behavior[1] == player.number:
            return 1 
    return 0


def yi_fa(player, all_behavior):
    ''' 一发 yifa means after riichi, win the game inside one circle, and during this time 
        should no one chi, peng, or gang, if this player can win by other's add_gang, then 
        add_gang invalid, this player still can yifa
    '''
    riichi_turn = -1
    for behavior in all_behavior:
        if behavior[2] == 'riichi' and behavior[1] == player.number:
            riichi_turn = behavior[0]
        else:
            return 0
    
    if all_behavior[-1][0] - riichi_turn <= 8:
        for behavior in all_behavior[riichi_turn:]:
            if behavior[2] not in ['chi', 'peng', 'gang', 'hidden_gang']:
                return 1
    return 0

    
def clear_zimo(player, all_behavior):
    ''' 门前清自摸和 clear win + zimo
    '''
    return 1 if regular_clear_win(player.my_tiles) and all_behavior[-1][2] == 'zimo' else 0


def ping_hu(player, cur_chang):
    ''' 平和 don't have extra fu except from zimo, which means only have shunzi and 
        double can't be zifeng, changfeng, and sanyuan tiles, and should ting pai for two tiles
    '''
    groups = composition(player)
    for group in groups:
        if group[0] not in [-1, 0]:
            return 0
        if group[0][0][0] in [player.my_position + 31, cur_chang + 31, 41, 42, 43]:
            return 0
    return 1
    
    
def yi_bei_kou(player):
    ''' 一杯口 have two exact same shunzi, can't fulu
    '''
    cnt = 0
    groups = composition(player)
    for group in groups:
        if group[0] == 2:
            cnt += 1
    if cnt == 1 and player.chi_peng_gang_tiles == []:
        return 1
    return 0
    
    
# 二番役 ################################################################
def dui_dui_hu(player):
    groups = composition(player)
    for group in groups:
        if group[0] not in QUE_TOU + GANG_ZI + KE_ZI:
            return 0
    return 2


def san_an_ke(player):
    cnt = 0
    groups = composition(player)
    for group in groups:
        if group[0] in [1, 13]:
            cnt += 1
    if cnt == 3:
        return 2
    else:
        return 0


def san_gang_zi(player):
    cnt = 0
    groups = composition(player)
    for group in groups:
        if group[0] in GANG_ZI:
            cnt += 1
    if cnt == 3:
        return 2
    else:
        return 0
    
    
def san_se_tong_ke(player):
    kezi = []
    groups = composition(player)
    for group in groups:
        if group[0] in KE_ZI + GANG_ZI:
            kezi += [group[1][0][0]]
    if len(kezi) == 3 and kezi[0] == kezi[1] == kezi[2]:
        return 2
    else:
        return 0
    
    
def hun_lao_tou(player):
    if seven_double(player) or dui_dui_hu(player):
        zi, lao_tou = False, False
        groups = composition(player)
        for group in groups:
            if group[1][0][0] not in YAO_JIU:
                return 0
            else:
                if group[1][0][0] in ZI:
                    zi = True
                if group[1][0][0] in LAO_TOU:
                    lao_tou = True
        if zi and lao_tou:
            return 2
    else:
        return 0
    

def xiao_san_yuan(player):
    cnt = 0
    groups = composition(player)
    for group in groups:
        if group[0] == QUE_TOU and group[1][0][0] in SAN_YUAN:
            cnt += 1
        if group[0] in KE_ZI + GANG_ZI and group[1][0][0] in SAN_YUAN:
            cnt += 10
    if cnt == 21:
        return 2
    return 0


# 二番役 副露减一番 ###########################################################
def san_se_tong_shun(player):
    groups = composition(player)
    shun_zi_list = []
    group_type = []
    for group in groups:
        group_type.append(group[0])
        if group[0] in SHUN_ZI:
            for tile in group[1]:
                shun_zi_list.append(tile[0])
    shun_zi_set = set(shun_zi_list)
    
    if len(shun_zi_set) == 3:
        for cond in FU_LU:
            if cond in group_type:
                return 1
        return 2
    return 0


def yi_qi_guan_tong(player):
    groups = composition(player)
    group_type = []
    first, second, third = False, False, False
    for group in groups:
        group_type.append(group[0])
        if group[0] in SHUN_ZI:
            tiles = []
            for tile in group[1]:
                tiles += [tile[0]]
            tiles.sort()
            if tiles == [1, 2, 3]:
                first = True
            elif tiles == [4, 5, 6]:
                second = True
            elif tiles == [7, 8, 9]:
                third == True
                
    if first and second and third:
        for cond in FU_LU:
            if cond in group_type:
                return 1
        return 2
    return 0
    

def hun_quan_dai_yao_jiu(player):
    groups = composition(player)
    group_type = []
    zi_tile, lao_tou_tile = False, False
    for group in groups:
        group_type.append(group[0])
        cnt = 0
        for tile in group[1]:
            if tile[0] in YAO_JIU:
                cnt += 1
                if tile[0] in ZI:
                    zi_tile = True
                if tile[0] in LAO_TOU:
                    lao_tou_tile = True
        if cnt == 0:
            return 0
    
    if zi_tile and lao_tou_tile:
        for cond in SHUN_ZI:
            if cond in group_type:
                for cond in FU_LU:
                    if cond in group_type:
                        return 1
                return 2
    return 0


def two_riichi(player, all_behaviors):
    behaviors = []
    for i in range(len(all_behaviors[5:])):
        behaviors.append(all_behaviors[5 + i][2])
        if all_behaviors[5 + i][1] == player.number:
            behaviors.append(all_behaviors[6 + i][2])
            break
    
    if player.chi_peng_gang_tiles == []:
        if behaviors[-1] == 'riichi':
            for cond in ['chi', 'peng', 'gang', 'hidden_gang']:
                if cond not in behaviors:
                    return 2
    return 0        
    
    
# 三番役 #####################################################################
def er_bei_kou(player):
    groups = composition(player)
    for group in groups:
        if group[0] == 3:
            return 3
    return 0

    
# 三番役 副露减一番 ###########################################################
def hun_yi_se(player):
    groups = composition(player)
    all_tiles = []
    group_type = []
    for group in groups:
        group_type.append(group[0])
        all_tiles += group[1]
    all_tiles = tiles_to_value(all_tiles)
    
    nums = []
    for tile in all_tiles:
        if tile not in ZI:
            nums += [tile]
    
    if len(nums) == len(tile):
        return 0
    for n in range(3):
        if all(num // 10 == n for num in nums):
            for cond in FU_LU:
                if cond in group_type:
                    return 2
            return 3
    return 0


def chun_quan_dai_yao_jiu(player):
    groups = composition(player)
    group_type = []
    for group in groups:
        group_type.append(group[0])
        tiles = tiles_to_value(group[1])
        contains = False
        for tile in tiles:
            if tile in YAO_JIU:
                contains = True
        if contains == False:
            return 0
        
    for cond in SHUN_ZI:
        if cond in group_type:
            for cond in FU_LU:
                if cond in group_type:
                    return 2
            return 3
    return 0
            
    
# 满贯役 #####################################################################
def liu_ju_man_guan(all_behaviors, player):
    cond = True
    if all_behaviors[-1] == 'liuju':
        for behavior in all_behaviors:
            if behavior[1] == player.number and behavior[2] == 'discard':
                if behavior[3][0] not in YAO_JIU:
                    cond = False
        
        for i in range(len(all_behaviors)):
            behavior = all_behaviors[i]
            next_behavior = all_behaviors[i + 1]
            if behavior[1] == player.number and behavior[2] == 'discard':
                if next_behavior[2] in ['chi', 'peng', 'gang']:
                    cond = False
                    
    if cond == True:
        return 5
    else:
        return 0


# 六番役 副露减一番 #####################################################################
def qing_yi_se(player):
    groups = composition(player)
    group_type = []
    tiles = []
    for group in groups:
        group_type.append(group[0])
        tiles += group[1]
    
    for i in range(3):
        if all(tile[0] // 10 == i for tile in tiles):
            for cond in FU_LU:
                if cond in group_type:
                    return 5
            return 6
    return 0


# special yi ####################################################################################################
def seven_double(player):
    ''' check if the player's tiles fit the seven double
    
        >>> player1 = player()
        >>> player1.my_tiles = [(1,0),(1,1),(3,9),(3,11),(5,16),(5,17),(21,72),(21,73),(32,113),(32,114),(33,116),(33,117),(42,128),(42,129)]
        >>> seven_double(player1)
        2
    '''
    tiles = player.my_tiles
    if all(tiles[i][0] == tiles[i + 1][0] for i in range(0, 13, 2)):
        return 2
    return 0


def guo_shi(player):
    ''' check for if the player's tiles fit the requsite of guo_shi
    
        helper function, so take tiles as input

        >>> player1 = player()
        >>> player1.my_tiles = [(1,1), (9,32), (11,36), (19,69), (21,75), (29,104), (31,110), (32,113), (33,119), (34,123), (41,124), (42,128), (43,132), (43,135)]
        >>> guo_shi(player1)
        13
    '''
    tiles = tiles_to_value(player.my_tiles)
    standard_guo_shi = [1, 9, 11, 19, 21, 29, 31, 32, 33, 34, 41, 42, 43]
    for tile in standard_guo_shi:
        if tile not in tiles:
            return 0
        
    for tile in tiles:
        if tile not in standard_guo_shi:
            return 0
    return 13


#####################################################################################################################################
def split_tiles(cond):
    ''' to split all tiles in to five type of tiles, ease the following judgement

        >>> tiles = [(5,19), (5,16), (8,28), (8,29), (8,30), (41,124), (41,125), (41,126), (42,128), (42,129), (42,130), (43,132), (43,133), (43,134)]
        >>> man_tiles = split_tiles(man)(tiles)
        >>> man_tiles
        [(5, 19), (5, 16), (8, 28), (8, 29), (8, 30)]
        >>> feng_tiles = split_tiles(feng)(tiles)
        >>> feng_tiles
        []
        >>> sanyuan_tiles = split_tiles(sanyuan)(tiles)
        >>> sanyuan_tiles
        [(41, 124), (41, 125), (41, 126), (42, 128), (42, 129), (42, 130), (43, 132), (43, 133), (43, 134)]
    '''
    def func(tiles):
        sub_list = [tile for tile in tiles if cond(tile[0])]
        return sub_list
    return func


# condition statement for split_tiles
def man(tile): 
    return True if tile > 0 and tile < 10 else False

def ping(tile):
    return True if tile > 10 and tile < 20 else False

def suo(tile):
    return True if tile > 20 and tile < 30 else False

def feng(tile):
    return True if tile > 30 and tile < 35 else False

def sanyuan(tile):
    return True if tile > 40 and tile < 44 else False


# # return a function that judge if there are x same tiles in a list
# def x_continously(my_tiles, x):
#     ''' return a function to test are there x continously tiles in
#         a players tiles, if there have x tiles ,then the return 
#         function will return True, vice versa
#         >>> my_tiles = [1, 1, 1, 1, 2, 3, 4]
#         >>> three_con = x_continously(my_tiles, 3)
#         >>> three_con(1)
#         False
#         >>> four_con = x_continously(my_tiles, 4)
#         >>> four_con(1)
#         True
#     '''
#     test_tiles = [x for x in my_tiles]
#     def func(tile):
#         cnt = 1
#         cnt_max = 1
#         for n in range(len(test_tiles) - 1):
#             if test_tiles[n] == test_tiles[n + 1] and test_tiles[n] == tile:
#                 cnt += 1
#                 if cnt > cnt_max:
#                     cnt_max = cnt
#             else:
#                 cnt = 1
#         if cnt_max == x:
#             return True
#         return False
#     return func


def shun_zi(tiles):
    ''' shun_zi is three adjacent tiles have the relationship of [n, n + 1, n + 2]
        since all the number tiles are separated(1~9, 11~19, 21~29)
        
        helper function, so take tiles as input

        >>> tiles = [(4,14), (5,19), (6,23)]
        >>> shun_zi(tiles)
        True
        >>> tiles = [(41,124), (42,128), (43,132)]
        >>> shun_zi(tiles)
        False
    '''
    tiles.sort()
    for tile in tiles:
        if tile[0] > 30:
            return False

    return True if tiles[0][0] + 1 == tiles[1][0] and tiles[1][0] + 1 == tiles[2][0] else False


def ke_zi(tiles):
    ''' ke_zi is three adjacent tiles have the same value
    
        helper function, so take tiles as input

        >>> tiles = [(15,55), (15,53), (15,54)]
        >>> ke_zi(tiles)
        True
        >>> tiles = [(41,125), (42,128), (43,134)]
        >>> ke_zi(tiles)
        False
    '''
    return True if tiles[0][0] == tiles[1][0] and tiles[1][0] == tiles[2][0] else False


def double(tiles):
    ''' double is nesscery for win in jp mahjong

        helper function, so take tiles as input
        
        >>> tiles = [(5,16), (5,19)]
        >>> double(tiles)
        True
        >>> tiles = [(42,128), (41,125)]
        >>> double(tiles)
        False
    '''
    return True if tiles[0][0] == tiles[1][0] else False


def same_shunzi(tiles):
    ''' test for yi_bei_kou, which means there are two exact same shunzi in my_tiles
    
        helper function, so take tiles as input

        >>> tiles = [(1,0), (1,1), (2,4), (2,5), (3,8), (3,9)]
        >>> same_shunzi(tiles)
        True
    '''
    tiles.sort()
    for tile in tiles:
        if tile[0] > 30:
            return False
        
    return all(tiles[i][0] == tiles[i + 1][0] for i in range(0, 5, 2)) and tiles[4][0] == tiles[2][0] + 1 == tiles[0][0] + 2


def overlapping(tiles):
    ''' sometimes there will be overlapping in tiles, which makes shun_zi cannot detect
        them, but ther are still valid, like [1, 2, 2, 3, 3, 4]
        
        This funciton will take a list as argument, and there are only 6 items inside
        
        helper function, so take tiles as input

        >>> tiles = [(1,0), (1,1), (2,5), (2,6), (3,9), (3,10)]
        >>> overlapping(tiles)
        False
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


def overlapping_same_shunzi(tiles):
    tiles.sort()
    for tile in tiles:
        if tile[0] > 30:
            return False
        
    test_tiles = tiles_to_value(tiles)
    for i in range(10):
        if (test_tiles == [i, i, i, i, i+1, i+1, i+1, i+1, i+2, i+2, i+2, i+2] or
            test_tiles == [i, i, i+1, i+1, i+1, i+1, i+2, i+2, i+2, i+2, i+3, i+3]):
            return True
    return False


def composition_mianzi(tiles):
    ''' check how many mianzi are there in tiles, this often apply on tiles that
        removed double, which can avoid some errors
        
        helper function, so take tiles as input
        
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
    elif len(tiles) > 5 and same_shunzi(tiles[:6]):
        return_value, remain = [(2, tiles[:6])], tiles[6:]
    elif len(tiles) > 5 and overlapping(tiles[:6]):
        original_list = tiles[:6]
        new_set = set(original_list)
        new_list = list(new_set)[:3]
        return_value = [(1, new_list)]
    elif len(tiles) == 12 and overlapping_same_shunzi(tiles):
        return_value, remain = [(3, tiles)], []
        
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
        [(-1, [(5, 18), (5, 16)]), (1, [(1, 0), (1, 1), (1, 2)]), (0, [(2, 4), (3, 8), (4, 12)]), (0, [(6, 23), (7, 24), (8, 31)]), (1, [(9, 32), (9, 33), (9, 34)])]
        >>> player1.my_tiles = [(1,0), (1,0), (1,0), (2,0), (2,0), (2,0), (3,0), (3,0), (42,0), (42,0), (5,0), (5,0), (6,0), (6,0)]
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
        if double([my_tiles[i], my_tiles[i + 1]]):
            test_tiles = [tile for tile in my_tiles]
            double_tiles = [(-1, [test_tiles.pop(i + 1), test_tiles.pop(i)])]
            tiles_comp = double_tiles
            tiles_comp += composition_mianzi(test_tiles)
            tiles_comp += organized_tiles
            #tiles_comp.sort()
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
