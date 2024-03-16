# idnetify all the possible tiles in mahjong
mahjong_tile_elements = {
    0: '0m', 1: '1m', 2: '2m', 3: '3m', 4: '4m', 5: '5m', 6: '6m', 7: '7m', 8: '8m', 9: '9m',
    10: '0p', 11: '1p', 12: '2p', 13: '3p', 14: '4p', 15: '5p', 16: '6p', 17: '7p', 18: '8p', 19: '9p',
    20: '0s', 21: '1s', 22: '2s', 23: '3s', 24: '4s', 25: '5s', 26: '6s', 27: '7s', 28: '8s', 29: '9s',
    31: 'dong', 32: 'nan', 33: 'xi', 34: 'bei',
    41: 'bai', 42: 'fa', 43: 'zhong'}
    # using 0, 10, 20 to represent red tile, but when calculating chi, pong, gang,
    # and hu they should be consider as itself + 5

find_num_using_tile = {v: k for k, v in mahjong_tile_elements.items()}


# generate all the tiles appear in a single game from all tile elements
def generate_tiles():
    all_tiles = []
    for ele in mahjong_tile_elements:
        if ele == 0 or ele == 10 or ele == 20:
            all_tiles.append(ele)
        elif ele == 5 or ele == 15 or ele == 25: 
            for i in range(3):
                all_tiles.append(ele)
        else:
            for i in range(4):
                all_tiles.append(ele)
    return all_tiles

all_tiles = generate_tiles()