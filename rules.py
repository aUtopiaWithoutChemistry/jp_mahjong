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


def regular_win(tiles):
    if contains_double(tiles)
    return False


def contains_double(tiles):
    for i in range(12):
        if tiles[i] == tiles[i + 1]:
            return True
        