''' all_tiles are all tiles that can appear on the table, 
        every single tile in tiles are in the form of (value, id)
        since have red dora tile, they are evaluated as regular tile during win checking,
        but have different score in score_counting.
        So I identify tiles with id 16, 52, 88 are red dora for man, ping, and suo

    mahjong_tile_elements is a dict show every tile's value's meaning in human's word.
        it might useful when human player playing game, but it will lose meaning when I added
        graphic user interface. Anyway, it can notice me now about how this number represent
        mahjong tiles.

    find_num_using_tile is a reversed dict for mahjong_tile_elements, which means people can
        type in the tile they want to find and get the number of this tile in my representation
        system. This only useful before I implement the GUI, but I hardly think so that I would 
        play this game without GUI

    key_list is a helper list for generate all tiles in following for loop, this list contains
        all the key of mahjong_tile_elements, so every item in this list is the value of four 
        same tiles.

    using the following for loop, I generated a list of tuples, the list's length is 136 which
        is the number of all the mahjong tiles, I use the id which is also iterable part in the
        for loop to // 4 which means I want to let every tiles in key_list generate four tiles 
        which have the same value but different id. This can help me to identify all red dora
        tiles without change their value to match other rules, which is a extremly hard problem
        for jp_mahjong ver -1.1
'''

mahjong_tile_elements = {
    1: '1m', 2: '2m', 3: '3m', 4: '4m', 5: '5m', 6: '6m', 7: '7m', 8: '8m', 9: '9m',
    11: '1p', 12: '2p', 13: '3p', 14: '4p', 15: '5p', 16: '6p', 17: '7p', 18: '8p', 19: '9p',
    21: '1s', 22: '2s', 23: '3s', 24: '4s', 25: '5s', 26: '6s', 27: '7s', 28: '8s', 29: '9s',
    31: '1z', 32: '2z', 33: '3z', 34: '4z',
    41: '5z', 42: '6z', 43: '7z'
}

find_num_using_tile = {v: k for k, v in mahjong_tile_elements.items()}

key_list = list(mahjong_tile_elements.keys())


def generate_tiles():
    all_tiles = []
    for id in range(136):
        value = key_list[id // 4]
        all_tiles.append((value ,id))
    return all_tiles

red_dora_id = [19, 55, 91]


def tiles_to_value(tiles):
    ''' This helper function can help previous written methods that based on ver -1.0's tiles
        representation smoothly transit to current version.
        from [(5, 16), (5, 19), (5, 17), (15, 55), (25, 91)]
        to   [5, 5, 5, 10, 20]
        >>> tiles = [(5, 16), (5, 19), (5, 17), (15, 55), (25, 91)]
        >>> value = tiles_to_value(tiles)
        >>> value
        [5, 5, 5, 10, 20]
    '''
    cur_tiles1 = [tile[0] for tile in tiles if tile[1] not in red_dora_id]
    # cur_tiles2 = [tile[0] - 5 for tile in tiles if tile[1] in red_dora_id]
    cur_tiles = cur_tiles1 # + cur_tiles2
    cur_tiles.sort()
    return cur_tiles


def value_to_tiles(simple_tiles):
    ''' This helper function can make previous single value into new tiles
        this function will generate tiles in repeated id, only for test, it might generate 
        unpredictable error in real game
        from [0, 5, 5, 10, 20]
        to   [(5, 16), (5, 16), (5, 19), (15, 55), (25, 91)]
        >>> value = [0, 5, 5, 10, 20]
        >>> new_tiles = value_to_tiles(value)
        >>> new_tiles
        [(5, 16), (5, 16), (5, 19), (15, 55), (25, 91)]
    '''
    new_tiles = []
    for tile in simple_tiles:
        if tile == 0:
            new_tiles.append((5, 19))
        elif tile == 10:
            new_tiles.append((15, 55))
        elif tile == 20:
            new_tiles.append((25, 91))
        else:
            for ele in all_tiles:
                if ele[0] == tile:
                    new_tiles.append(ele)
                    break
    new_tiles.sort()
    return new_tiles
                