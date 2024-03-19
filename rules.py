from element import tiles_to_value

# rules for winning
def win(tiles, chi_peng_gang_tiles):
    return True if clear_win(tiles) or chi_peng_gang_win(tiles, chi_peng_gang_tiles) else False


def clear_win(tiles):
    return True if special_win(tiles) or regular_win(tiles) else False


# TODO
def chi_peng_gang_win(tiles, chi_peng_gang_tiles):
    return False


def special_win(tiles):
    return True if seven_double(tiles) or guo_shi(tiles) else False


def seven_double(tiles):
    if len(tiles) == 0:
        return True
    elif tiles[1][0] != tiles[0][0]:
        return False
    else:
        return seven_double(tiles[2:])  


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


def deal_red(tiles):
    ''' there are three red baopai in mahjong, they are special during counting score,
        but they are just considered as 5 man or ping or suo, we need to convert them
        from 0, 10, 20 to 5, 15, 25 during the judgement of win

        >>> tiles = [0, 5, 5]
        >>> new_tiles = deal_red(tiles)
        >>> new_tiles
        [5, 5, 5]
    '''
    for i in range(len(tiles)):
        if tiles[i] % 10 == 0:
            tiles[i] += 5
    return tiles


def shun_zi(tiles):
    ''' shun_zi is three adjacent tiles have the relationship of [n, n + 1, n + 2]

        >>> tiles = [4, 5, 6]
        >>> shun_zi(tiles)
        True
        >>> tiles = [0, 4, 6]
        >>> shun_zi(tiles)
        True
        >>> tiles = [41, 42, 43]
        >>> shun_zi(tiles)
        False
    '''
    tiles = deal_red(tiles)
    tiles.sort()
    for tile in tiles:
        if tile > 30:
            return False
    return True if tiles[0] + 1 == tiles[1] and tiles[1] + 1 == tiles[2] else False


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
    tiles = deal_red(tiles)
    return True if tiles[0] == tiles[1] and tiles[1] == tiles[2] else False


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
    tiles = deal_red(tiles)
    return True if tiles[0] == tiles[1] else False


def overlapping(tiles):
    ''' sometimes there will be overlapping in tiles, which makes shun_zi cannot detect
        them, but ther are still valid, some overlapping even can get higher score, like
        yibeikou [1, 1, 2, 2, 3, 3]

        >>> tiles = [1, 1, 2, 2, 3, 3]
        >>> overlapping(tiles)
        True
        >>> tiles = [3, 4, 4, 5, 0, 6]
        >>> overlapping(tiles)
        True
        >>> tiles = [41, 41, 42, 42, 43, 43]
        >>> overlapping (tiles)
        False
    '''
    tiles = deal_red(tiles)
    tiles.sort()
    for tile in tiles:
        if tile > 30:
            return False
    tiles_set = list(set(tiles))

    if len(tiles_set) > 2 and shun_zi(tiles_set):
        for i in range(3):
            tiles.remove(tiles_set[i])
    return True if shun_zi(tiles) else False


def composition(tiles):
    ''' return a number represent how the tiles composed, for a regular win, it should
        contains 1 double and 4 mianzi(kezi or shunzi), and the return value of this 
        combination is 14. However, if get a non-14 number, it can also reflect the 
        current composition of tiles. first digit shows how many double, second digit
        shows how many mianzi

        >>> tiles = [1, 1, 1, 2, 3, 4, 5, 5, 6, 7, 8, 9, 9, 9]
        >>> composition(tiles)
        14
        >>> tiles = [1, 1, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 30, 30]
        >>> composition(tiles)
        14
        >>> tiles = [41, 41, 41, 42, 42, 42, 43, 43, 43, 0, 5, 10, 15, 15]
        >>> composition(tiles)
        14
        >>> tiles = [1, 1, 1, 2, 2, 2, 3, 3, 42, 42, 5, 5, 6, 6]
        >>> composition(tiles)
        42
        >>> tiles = [1, 1, 2, 2, 3, 3, 4, 5, 0, 6, 6, 7, 41, 41]
        >>> composition(tiles)
        14
    '''
    if tiles == []:
        return 0
    elif len(tiles) > 2 and (shun_zi(tiles[:3]) or ke_zi(tiles[:3])):
        cnt, tiles = 1, tiles[3:]
    elif len(tiles) > 5 and overlapping(tiles[:6]):
        cnt, tiles = 2, tiles[6:]
    elif len(tiles) > 1 and double(tiles[:2]):
        cnt, tiles = 10, tiles[2:]
    else:
        return composition(tiles[1:])
    return cnt + composition(tiles)


def regular_win(tiles):
    ''' if the composition of tiles conform to 14, then the player wins

        >>> tiles = [41, 41, 41, 42, 42, 42, 43, 43, 43, 0, 5, 10, 15, 15]
        >>> regular_win(tiles)
        True
    '''
    return True if composition(tiles) == 14 else False
