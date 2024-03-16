# rules during the game


# rules for winning
def special_win(tiles):
    #if tiles
    if seven_double(tiles) or guo_shi(tiles):
        return True
    return False


def seven_double(tiles):
    if len(tiles) == 0:
        return True
    elif tiles[1] != tiles[0]:
        return False
    else:
        return seven_double(tiles[2:])  


def guo_shi(tiles):
    standard_guo_shi = [1, 9, 11, 19, 21, 29, 31, 32, 33, 34, 41, 42, 43]
    cur_tiles = tiles
    for i in range(len(standard_guo_shi)):
        if standard_guo_shi[i] not in cur_tiles:
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
    return False



def regular_win(tiles):
    mian_zi = 0
    que_tou = 0
    man_check = split_tiles(man)
    ping_check = split_tiles(ping)
    suo_check = split_tiles(suo)
    man_list = man_check(tiles)
    ping_list = ping_check(tiles)
    suo_list = suo_check(tiles)
    
    return False


def contains_double(tiles):
    for i in range(12):
        if tiles[i] == tiles[i + 1]:
            return True
        