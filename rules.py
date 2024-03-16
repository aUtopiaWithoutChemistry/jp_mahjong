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
    standard_guo_shi = [1, 9, 11, 19, 21, 29, 30, 31, 32, 33, 40, 41, 42]
    cur_tiles = tiles
    for i in range(len(standard_guo_shi)):
        if standard_guo_shi[i] not in cur_tiles:
            return False
    return True


def split_tiles(cond):
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
    return True if tile > 29 and tile < 34 else False

def sanyuan(tile):
    return True if tile > 39 and tile < 43 else False


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
    return False


def ke_zi(tiles):
    for tile in tiles:
        if x_continously(tiles, 3)(tile):
            return True 
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
        