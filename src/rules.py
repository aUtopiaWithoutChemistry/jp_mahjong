from const import *


def tiles_to_value(original_tiles: list[tuple]) -> list:
    """ transfer tuple tiles to single value
        >>> ruler = Rule()
        >>> tiles_to_value([(41, 0), (41, 0), (41, 0), (42, 0), (42, 0)])
        [41, 41, 41, 42, 42]
    """
    values = []
    for tile in original_tiles:
        values.append(tile[0])
    return values


def man(tile):
    return True if 0 < tile < 10 else False


def ping(tile):
    return True if 10 < tile < 20 else False


def suo(tile):
    return True if 20 < tile < 30 else False


def feng(tile):
    return True if 30 < tile < 35 else False


def sanyuan(tile):
    return True if 40 < tile < 44 else False


def split_tiles(cond):
    """ to split all tiles in to five type of tiles, ease the following judgement
        >>> tiles = [(5,19), (5,16), (8,28), (8,29), (8,30), (41,124), (41,125), (41,126), (42,128), (42,129), \
                     (42,130), (43,132), (43,133), (43,134)]
        >>> man_tiles = split_tiles(man)(tiles)
        >>> man_tiles
        [(5, 19), (5, 16), (8, 28), (8, 29), (8, 30)]
        >>> feng_tiles = split_tiles(feng)(tiles)
        >>> feng_tiles
        []
        >>> sanyuan_tiles = split_tiles(sanyuan)(tiles)
        >>> sanyuan_tiles
        [(41, 124), (41, 125), (41, 126), (42, 128), (42, 129), (42, 130), (43, 132), (43, 133), (43, 134)]
    """

    def func(tiles):
        sub_list = [tile for tile in tiles if cond(tile[0])]
        return sub_list

    return func


def shun_zi(tiles):
    """ shun_zi is three adjacent tiles have the relationship of [n, n + 1, n + 2]
        since all the number tiles are separated(1~9, 11~19, 21~29)
        helper function, so take tiles as input
        :param tiles: list[tuple]
        :return: bool
        >>> tiles = [(4,14), (5,19), (6,23)]
        >>> shun_zi(tiles)
        True
        >>> tiles = [(41,124), (42,128), (43,132)]
        >>> shun_zi(tiles)
        False
    """
    tiles.sort()
    for tile in tiles:
        if tile[0] > 30:
            return False

    return True if tiles[0][0] + 1 == tiles[1][0] and tiles[1][0] + 1 == tiles[2][0] else False


def ke_zi(tiles):
    """ ke_zi is three adjacent tiles have the same value
        helper function, so take tiles as input
        :param tiles: list[tuple]
        :return: bool
        >>> tiles = [(15,55), (15,53), (15,54)]
        >>> ke_zi(tiles)
        True
        >>> tiles = [(41,125), (42,128), (43,134)]
        >>> ke_zi(tiles)
        False
    """
    return True if tiles[0][0] == tiles[1][0] and tiles[1][0] == tiles[2][0] else False


def double(tiles):
    """ double is nesscery for win in jp mahjong
        helper function, so take tiles as input
        :param tiles: list[tuple]
        :return: bool
        >>> tiles = [(5,16), (5,19)]
        >>> double(tiles)
        True
        >>> tiles = [(42,128), (41,125)]
        >>> double(tiles)
        False
    """
    return True if tiles[0][0] == tiles[1][0] else False


def same_shunzi(tiles):
    """ test for yi_bei_kou, which means there are two exact same shunzi in my_tiles
        helper function, so take tiles as input
        :param tiles: list[tuple]
        :return: bool
        >>> tiles = [(1,0), (1,1), (2,4), (2,5), (3,8), (3,9)]
        >>> same_shunzi(tiles)
        True
    """
    tiles.sort()
    for tile in tiles:
        if tile[0] > 30:
            return False

    return all(tiles[i][0] == tiles[i + 1][0] for i in range(0, 5, 2)) and tiles[4][0] == tiles[2][0] + 1 == \
        tiles[0][
            0] + 2


def overlapping_same_shunzi(tiles):
    """ check if there is overlapping shun_zi
        :param tiles: list[tuple]
        :return: bool
    """
    tiles.sort()
    for tile in tiles:
        if tile[0] > 30:
            return False

    test_tiles = tiles_to_value(tiles)
    for i in range(10):
        if (test_tiles == [i, i, i, i, i + 1, i + 1, i + 1, i + 1, i + 2, i + 2, i + 2, i + 2] or
                test_tiles == [i, i, i + 1, i + 1, i + 1, i + 1, i + 2, i + 2, i + 2, i + 2, i + 3, i + 3]):
            return True
    return False


def overlapping(tiles):
    """ sometimes there will be overlapping in tiles, which makes shun_zi cannot detect
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
    """
    tiles.sort()
    for tile in tiles:
        if tile[0] > 30:
            return False

    return True if shun_zi([tiles[0], tiles[1], tiles[3]]) and shun_zi(
        [tiles[2], tiles[4], tiles[5]]) else False


class Rule:
    """ all check work should be done in the rule object"""

    def __init__(self, game=None, player=None):
        """ Constructor for Rule class
            :param game: Game object
            :param player: Player object
        """
        self.game = None
        self.all_behaviors = None
        self.cur_chang = None
        self.this_game = None
        self.dora = None

        self.player = None
        self.my_tiles = None
        self.chi_peng_gang_tiles = None
        self.waste_tiles = None
        self.my_position = None
        self.number = None

        if game is not None:
            self.set_game(game)
        if player is not None:
            self.set_player(player)

    def set_game(self, game):
        self.game = game
        self.all_behaviors = game.get_all_behaviors()
        self.cur_chang = game.get_cur_chang()
        self.this_game = game.get_this_game()
        self.dora = game.get_dora()

    def set_player(self, player):
        self.player = player
        self.get_information()

    def get_player_tiles(self):
        self.my_tiles, self.chi_peng_gang_tiles, self.waste_tiles = self.player.get_my_tiles()
        self.my_tiles, self.chi_peng_gang_tiles = self.transfer()

    def get_information(self):
        self.get_player_tiles()
        self.number = self.player.get_my_number()
        self.my_position = self.player.get_my_position()

    def check_possible_moves(self):
        pass

    # rules for winning
    def win(self):
        return True if self.clear_win() or self.chi_peng_gang_win() else False

    def check_points(self):
        pass

    def transfer(self):
        """ transfer current tile representation to previous version to make sure all code works
            from class to tuple
            :return: my_tiles, chi_peng_gang_tiles
        """
        new_my_tiles = []
        new_chi_peng_gang_tiles = []
        for tile in self.my_tiles:
            new_tile = tile.get_value_id()
            new_my_tiles.append(new_tile)
        for group in self.chi_peng_gang_tiles:
            new_group = []
            for tile in group[1]:
                new_tile = tile.get_value_id()
                new_group.append(new_tile)
            new_chi_peng_gang_tiles.append([group[0], new_group])
        return new_my_tiles, new_chi_peng_gang_tiles

    def chi_peng_gang_win(self):
        """ have chi_peng_gang
            >>> ruler = Rule()
            >>> ruler.my_tiles = [(41,0), (41,0), (41,0), (42,0), (42,0)]
            >>> ruler.chi_peng_gang_tiles = [[0, [(1,0), (2,0), (3,0)]], [0, [(4,0), \
                (5,0), (6,0)]], [0, [(7,0), (8,0), (9,0)]]]
            >>> ruler.chi_peng_gang_win()
            True
        """
        return True if self.chi_peng_gang_tiles != [] and self.composition() else False

    def clear_win(self):
        """ 门前清
        """
        return True if self.special_clear_win() or \
                       self.regular_clear_win() else False

    def special_clear_win(self):
        """ check if 七对子 or 国士无双
        """
        return True if self.seven_double() == 7 or self.guo_shi() else False

    def regular_clear_win(self):
        """ if the composition return True, then the player wins
            >>> ruler = Rule()
            >>> ruler.my_tiles = [(41,0), (41,0), (41,0), (42,0), (42,0), (42,0), (43,0), \
                (43,0), (43,0), (5,0), (5,0), (15,0), (15,0), (15,0)]
            >>> ruler.chi_peng_gang_tiles = []
            >>> ruler.regular_clear_win()
            True
        """
        return True if (self.chi_peng_gang_tiles == [] and self.composition()) else False

    def basic_point_cal(self):
        fan = self.check_fan()
        fu = self.check_fu()
        basic_point = self.bp(fan, fu)
        return basic_point

    def check_fan(self):

        all_yi = {self.duan_yao_jiu, self.yi_tiles, self.he_di_mo_yu, self.ling_shang_kai_hua,
                  self.qiang_gang, self.hai_di_lao_yue, self.riichi, self.yi_fa, self.clear_zimo,
                  self.ping_hu, self.yi_bei_kou, self.dui_dui_hu, self.san_an_ke, self.san_gang_zi,
                  self.san_gang_zi, self.hun_lao_tou, self.xiao_san_yuan, self.san_se_tong_shun,
                  self.yi_qi_guan_tong, self.hun_quan_dai_yao_jiu, self.two_riichi, self.er_bei_kou,
                  self.hun_yi_se, self.chun_quan_dai_yao_jiu, self.liu_ju_man_guan, self.qing_yi_se,
                  self.da_san_yuan, self.xiao_si_xi, self.da_si_xi, self.zi_yi_se, self.lv_yi_se,
                  self.qing_lao_tou, self.si_an_ke, self.jiu_lian_bao_deng,
                  self.si_gang_zi, self.tian_hu, self.di_hu, self.guo_shi}

        if self.seven_double() == 7:
            fan = 2
        else:
            fan = 0
            for check in all_yi:
                fan += check()

        player_tiles = self.my_tiles
        if self.chi_peng_gang_tiles:
            player_tiles += [group[1] for group in self.chi_peng_gang_tiles]

        red_dora = [(5, 19), (15, 55), (25, 91)]
        for tile in player_tiles:
            # red dora
            if tile in red_dora:
                fan += 1
            # game dora
            if tile[0] in self.dora:
                fan += 1

        return fan

    def check_fu(self):
        fu = 0
        ZI_FENG = self.my_position + 31
        CHANG_FENG = self.cur_chang + 31
        KE_FENG = [tile for tile in FENG if tile != ZI_FENG and tile != CHANG_FENG]

        if self.seven_double() == 7:
            return 25
        if self.clear_zimo() and self.ping_hu():
            return 20
        if self.ping_hu() and self.chi_peng_gang_tiles != []:
            return 30

        groups = self.composition()
        for group in groups:
            tile = group[1][0][0]

            if group[0] == QUE_TOU:
                if tile in ZI_FENG + CHANG_FENG + SAN_YUAN:
                    fu += 2
                elif tile in LAO_TOU + ZHONG_ZHANG + KE_FENG:
                    fu += 0

            if group[0] == MING_KE:
                if tile in ZHONG_ZHANG:
                    fu += 2
                elif tile in YAO_JIU:
                    fu += 4

            if group[0] == AN_KE:
                if tile in ZHONG_ZHANG:
                    fu += 4
                elif tile in YAO_JIU:
                    fu += 8

            if group[0] == MING_GANG:
                if tile in ZHONG_ZHANG:
                    fu += 8
                elif tile in YAO_JIU:
                    fu += 16

            if group[0] == AN_GANG:
                if tile in ZHONG_ZHANG:
                    fu += 16
                elif tile in YAO_JIU:
                    fu += 32

            if fu % 10 != 0:
                fu = 10 * ((fu // 10) + 1)

        return fu

    @staticmethod
    def bp(fan, fu):
        basic_point = fu * 2 ** (fan + 2)
        if basic_point > 2000:
            if fan <= 5:  # 满贯
                basic_point = 2000
            elif 6 <= fan <= 7:  # 跳满
                basic_point = 3000
            elif 8 <= fan <= 10:  # 倍满
                basic_point = 4000
            elif 11 <= fan <= 12:  # 三倍满
                basic_point = 6000
            elif fan >= 13:  # 役满
                basic_point = 8000
        return basic_point

    # 一番役 ################################################################################################
    def duan_yao_jiu(self):
        """ 断幺九 without yao jiu tiles when win
            yao jiu tiles: 1, 9, 11, 19, 21, 29, 31, 32, 33, 34, 41, 42, 43
            >>> ruler = Rule()
            >>> ruler.my_tiles = [(2,4), (3,9), (4,15), (5,16), (5,18), (5, 19), (6,20), \
                (6,21), (6,22), (7,24), (7,25), (7,26), (8,28), (8,30)]
            >>> ruler.chi_peng_gang_tiles = []
            >>> ruler.duan_yao_jiu()
            1
            >>> ruler.my_tiles = [(2,4), (3,9), (4,15), (5,16), (5,18), (5, 19), (6,20), \
                (6,21), (6,22), (7,24), (7,25), (7,26), (9,32), (9,33)]
            >>> ruler.chi_peng_gang_tiles = []
            >>> ruler.duan_yao_jiu()
            0
            >>> ruler.my_tiles = [(18,66), (18,67)]
            >>> ruler.chi_peng_gang_tiles = [(11, [(2,4), (2,5), (2,6)]),(11, [(3,9), (3,10), \
                (3,11)]),(11, [(4,12), (4,13), (4,14)]),(11, [(5,16), (5,17), (5,19)])]
            >>> ruler.duan_yao_jiu()
            1
        """
        tiles = self.my_tiles
        chi_peng_gang_tiles = [group[1] for group in self.chi_peng_gang_tiles]
        for group in chi_peng_gang_tiles:
            tiles += group
        yao_jiu = [tile[0] for tile in tiles if tile[0] in [1, 9, 11, 19, 21, 29, 31, 32, 33, 34, 41, 42, 43]]
        return 1 if len(yao_jiu) == 0 else 0

    def yi_tiles(self):
        """ 役牌刻子或杠子，如场风、自风、三元牌 contains (dong, xi, nan, bei) one kezi of corresponding my position
            or chang_feng, bai, fa, zhong, which is 41, 42, 43 and 31 + cur_chang or 31 + cur_position
            >>> ruler = Rule()
            >>> ruler.my_tiles = [(1,0),(1,0),(2,0),(2,0),(2,0),(3,0),(3,0),(3,0),(4,0),(4,0),(4,0)]
            >>> ruler.chi_peng_gang_tiles = [(11, [(31,0), (31,0), (31,0)])]
            >>> ruler.cur_chang = 0
            >>> ruler.my_position = 0
            >>> ruler.yi_tiles()
            1
        """
        valid_yi = [self.cur_chang + 31, self.my_position + 31, 41, 42, 43]
        all_tiles_groups = self.composition()
        for group in all_tiles_groups:
            if group[0] in [1, 11, 12, 13] and group[1][0][0] in valid_yi:
                return 1
        return 0

    def he_di_mo_yu(self):
        """ 河底摸鱼 use the last tile to win the game
        """
        return 1 if self.this_game == [] and self.all_behaviors[-1][2] == 'rong_hu' else 0

    def ling_shang_kai_hua(self):
        """ 岭上开花 use the ling shang tile to win the game
        """
        return 1 if (self.all_behaviors[-1][2] == 'zimo' and
                     self.all_behaviors[-3][2] in ['hidden_gang', 'add_gang', 'gang']) else 0

    def qiang_gang(self):
        """ 抢杠 use other player's add_gang tile to win
        """
        return 1 if self.all_behaviors[-1][2] == 'rong_hu' and self.all_behaviors[-2][2] == 'add_gang' else 0

    def hai_di_lao_yue(self):
        """ 海底捞月 zimo the last tile
        """
        return 1 if self.this_game == [] and self.all_behaviors[-1][2] == 'zimo' else 0

    def riichi(self):
        """ リーチ 立直
        """
        for behavior in self.all_behaviors:
            if behavior[2] == 'riichi' and behavior[1] == self.number:
                return 1
        return 0

    def yi_fa(self):
        """ 一发 yifa means after riichi, win the game inside one circle, and during this time
            should no one chi, peng, or gang, if this player can win by other's add_gang, then
            add_gang invalid, this player still can yifa
        """
        riichi_turn = -1
        for behavior in self.all_behaviors:
            if behavior[2] == 'riichi' and behavior[1] == self.number:
                riichi_turn = behavior[0]
            else:
                return 0

        if self.all_behaviors[-1][0] - riichi_turn <= 8:
            for behavior in self.all_behaviors[riichi_turn:]:
                if behavior[2] not in ['chi', 'peng', 'gang', 'hidden_gang']:
                    return 1
        return 0

    def clear_zimo(self):
        """ 门前清自摸和 clear win + zimo
        """
        return 1 if self.regular_clear_win() and self.all_behaviors[-1][2] == 'zimo' else 0

    def ping_hu(self):
        """ 平和 don't have extra fu except from zimo, which means only have shunzi and
            double can't be zifeng, changfeng, and sanyuan tiles, and should ting pai for two tiles
        """
        groups = self.composition()
        for group in groups:
            if group[0] not in [-1, 0]:
                return 0
            if group[0][0][0] in [self.my_position + 31, self.cur_chang + 31, 41, 42, 43]:
                return 0
        return 1

    def yi_bei_kou(self):
        """ 一杯口 have two exact same shunzi, can't fulu
        """
        cnt = 0
        groups = self.composition()
        for group in groups:
            if group[0] == 2:
                cnt += 1
        if cnt == 1 and self.chi_peng_gang_tiles == []:
            return 1
        return 0

    # 二番役 ################################################################
    def dui_dui_hu(self):
        groups = self.composition()
        for group in groups:
            if group[0] not in QUE_TOU + GANG_ZI + KE_ZI:
                return 0
        return 2

    def san_an_ke(self):
        cnt = 0
        groups = self.composition()
        for group in groups:
            if group[0] in [1, 13]:
                cnt += 1
        if cnt == 3:
            return 2
        else:
            return 0

    def san_gang_zi(self):
        cnt = 0
        groups = self.composition()
        for group in groups:
            if group[0] in GANG_ZI:
                cnt += 1
        if cnt == 3:
            return 2
        else:
            return 0

    def san_se_tong_ke(self):
        kezi = []
        groups = self.composition()
        for group in groups:
            if group[0] in KE_ZI + GANG_ZI:
                kezi += [group[1][0][0]]
        if len(kezi) == 3 and kezi[0] == kezi[1] == kezi[2]:
            return 2
        else:
            return 0

    def hun_lao_tou(self):
        if self.seven_double() or self.dui_dui_hu():
            zi, lao_tou = False, False
            groups = self.composition()
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

    def xiao_san_yuan(self):
        cnt = 0
        groups = self.composition()
        for group in groups:
            if group[0] == QUE_TOU and group[1][0][0] in SAN_YUAN:
                cnt += 1
            if group[0] in KE_ZI + GANG_ZI and group[1][0][0] in SAN_YUAN:
                cnt += 10
        if cnt == 21:
            return 2
        return 0

    # 二番役 副露减一番 ###########################################################
    def san_se_tong_shun(self):
        groups = self.composition()
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

    def yi_qi_guan_tong(self):
        groups = self.composition()
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
                    third = True

        if first and second and third:
            for cond in FU_LU:
                if cond in group_type:
                    return 1
            return 2
        return 0

    def hun_quan_dai_yao_jiu(self):
        groups = self.composition()
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
                    for cond2 in FU_LU:
                        if cond2 in group_type:
                            return 1
                    return 2
        return 0

    def two_riichi(self):
        behaviors = []
        for i in range(len(self.all_behaviors[5:])):
            behaviors.append(self.all_behaviors[5 + i][2])
            if self.all_behaviors[5 + i][1] == self.number:
                behaviors.append(self.all_behaviors[6 + i][2])
                break

        if not self.chi_peng_gang_tiles:
            if behaviors[-1] == 'riichi':
                for cond in ['chi', 'peng', 'gang', 'hidden_gang']:
                    if cond not in behaviors:
                        return 2
        return 0

    # 三番役 #####################################################################
    def er_bei_kou(self):
        groups = self.composition()
        for group in groups:
            if group[0] == 3:
                return 3
        return 0

    # 三番役 副露减一番 ###########################################################
    def hun_yi_se(self):
        groups = self.composition()
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

        if len(nums) == len(all_tiles):
            return 0
        for n in range(3):
            if all(num // 10 == n for num in nums):
                for cond in FU_LU:
                    if cond in group_type:
                        return 2
                return 3
        return 0

    def chun_quan_dai_yao_jiu(self):
        groups = self.composition()
        group_type = []
        for group in groups:
            group_type.append(group[0])
            tiles = tiles_to_value(group[1])
            contains = False
            for tile in tiles:
                if tile in YAO_JIU:
                    contains = True
            if not contains:
                return 0

        for cond in SHUN_ZI:
            if cond in group_type:
                for cond2 in FU_LU:
                    if cond2 in group_type:
                        return 2
                return 3
        return 0

    # 满贯役 #####################################################################
    def liu_ju_man_guan(self):
        cond = True
        if self.all_behaviors[-1] == 'liuju':
            for behavior in self.all_behaviors:
                if behavior[1] == self.number and behavior[2] == 'discard':
                    if behavior[3][0] not in YAO_JIU:
                        cond = False

            for i in range(len(self.all_behaviors)):
                behavior = self.all_behaviors[i]
                next_behavior = self.all_behaviors[i + 1]
                if behavior[1] == self.number and behavior[2] == 'discard':
                    if next_behavior[2] in ['chi', 'peng', 'gang']:
                        cond = False

        if cond:
            return 5
        else:
            return 0

    # 六番役 副露减一番 #####################################################################
    def qing_yi_se(self):
        groups = self.composition()
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

    # 役满役 #####################################################################
    def da_san_yuan(self):
        cnt = 0
        groups = self.composition()
        for group in groups:
            if group[0] in KE_ZI + GANG_ZI and group[1][0][0] in SAN_YUAN:
                cnt += 1
        if cnt == 3:
            return 13
        return 0

    def xiao_si_xi(self):
        cnt = 0
        groups = self.composition()
        for group in groups:
            if group[0] in QUE_TOU and group[1][0][0] in FENG:
                cnt += 1
            elif group[0] in KE_ZI + GANG_ZI and group[1][0][0] in FENG:
                cnt += 10
        if cnt == 31:
            return 13
        return 0

    def da_si_xi(self):
        cnt = 0
        groups = self.composition()
        for group in groups:
            if group[0] in KE_ZI + GANG_ZI and group[1][0][0] in FENG:
                cnt += 10
        if cnt == 40:
            return 13
        return 0

    def zi_yi_se(self):
        if self.seven_double() != 0 or self.dui_dui_hu() != 0:
            tiles = self.my_tiles
            for i in range(len(self.chi_peng_gang_tiles)):
                tiles += self.chi_peng_gang_tiles[i][1]
            for tile in tiles:
                if tile[0] not in ZI:
                    return 0
            return 13
        return 0

    def lv_yi_se(self):
        tiles = self.my_tiles
        for i in range(len(self.chi_peng_gang_tiles)):
            tiles += self.chi_peng_gang_tiles[i][1]
        for tile in tiles:
            if tile[0] not in [22, 23, 24, 26, 28, 42]:
                return 0
        return 13

    def qing_lao_tou(self):
        if self.dui_dui_hu() != 0:
            tiles = self.my_tiles
            for i in range(len(self.chi_peng_gang_tiles)):
                tiles += self.chi_peng_gang_tiles[i][1]
            for tile in tiles:
                if tile[0] not in YAO_JIU:
                    return 0
            return 13

    # 役满役 门前清 ##############################################################
    def si_an_ke(self):
        groups = self.composition()
        cnt = 0
        for group in groups:
            if group[0] in [1, 13]:
                cnt += 1

        if cnt == 4:
            if self.all_behaviors[-1][2] == 'ronghu':
                return self.san_an_ke() + self.dui_dui_hu()
            return 13
        return 0

    def jiu_lian_bao_deng(self):
        if self.qing_yi_se() != 0:
            tile_type = self.my_tiles[0][0] // 10
            groups = self.composition()
            cnt = 0
            for group in groups:
                if group[0] == 1:
                    if group[1][0][0] == tile_type * 10 + 1 or group[1][0][0] == tile_type * 10 + 9:
                        cnt += 1

            contains_all = True
            all_tiles = tiles_to_value(self.my_tiles)
            for i in range(1, 10):
                if i not in all_tiles:
                    contains_all = False

            if cnt > 0 and contains_all:
                return 13
            return 0

    def si_gang_zi(self):
        groups = self.composition()
        cnt = 0
        for group in groups:
            if group[0] in GANG_ZI:
                cnt += 1
        if cnt == 4:
            return 13
        return 0

    def tian_hu(self):
        if self.my_position == 0:
            for i in self.all_behaviors[5:]:
                if self.all_behaviors[i][1] == self.number and self.all_behaviors[i][2] == 'mopai':
                    if self.all_behaviors[i + 1][2] != 'zimo':
                        return 0
                    else:
                        return 13

    def di_hu(self):
        for i in self.all_behaviors[5:]:
            if self.all_behaviors[i][2] in ['chi', 'peng', 'gang', 'hidden_gang']:
                return 0
            if self.all_behaviors[i][1] == self.number and self.all_behaviors[i][2] == 'mopai':
                if self.all_behaviors[i + 1][2] != 'zimo':
                    return 0
                else:
                    return 13

    # special yi ####################################################################################################
    def seven_double(self):
        """ check if the player's tiles fit the seven double
            >>> ruler = Rule()
            >>> ruler.my_tiles = [(1,0),(1,1),(3,9),(3,11),(5,16),(5,17),(21,72),(21,73),(32,113),(32,114),(33,116),\
                                  (33,117),(42,128),(42,129)]
            >>> ruler.seven_double()
            2
        """
        tiles = self.my_tiles
        if all(tiles[i][0] == tiles[i + 1][0] for i in range(0, 13, 2)):
            return 2
        return 0

    def guo_shi(self):
        """ check for if the player's tiles fit the requsite of guo_shi
            helper function, so take tiles as input
            >>> ruler = Rule()
            >>> ruler.my_tiles = [(1,1), (9,32), (11,36), (19,69), (21,75), (29,104), (31,110), (32,113), (33,119), \
                                  (34,123), (41,124), (42,128), (43,132), (43,135)]
            >>> ruler.guo_shi()
            13
        """
        tiles = tiles_to_value(self.my_tiles)
        standard_guo_shi = {1, 9, 11, 19, 21, 29, 31, 32, 33, 34, 41, 42, 43}
        for tile in standard_guo_shi:
            if tile not in tiles:
                return 0

        for tile in tiles:
            if tile not in standard_guo_shi:
                return 0
        return 13

    ###################################################################################################################

    def composition_mianzi(self, tiles: list[tuple]):
        """ check how many mianzi are there in tiles, this often apply on tiles that
            removed double, which can avoid some errors

            helper function, so take tiles as input

            the return value should be a clasified list, which contains two to four group
            of tiles, and should mark its type

            for example, the input is [(1,0), (1,1), (2,4), (2,6), (3,8), (3,9), (5,16),
                                        (5,18), (5,19), (14,49), (16,58), (15,55)]
            the output should be [(2, [(1,0), (1,1), (2,4), (2,6), (3,8), (3,9)]), (1, [(5,16), (5,18), (5,19)]),
                                  (0, [(14,49), (16,58), (15,55)])]
                                 [(type, [tile_list]), (), ()]
                                 for type, 0 means shunzi, 1 means kezi, 2 means yibeiko
            >>> ruler = Rule()
            >>> tiles = [(1,0), (1,1), (2,4), (2,6), (3,8), (3,9), (5,16), (5,18), (5,19), (14,49), (16,58), (15,55)]
            >>> ruler.composition_mianzi(tiles)
            [(2, [(1, 0), (1, 1), (2, 4), (2, 6), (3, 8), (3, 9)]), (1, [(5, 16), (5, 18), (5, 19)]), (0, [(14, 49), (16, 58), (15, 55)])]
        """
        if not tiles:
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
            tmp = [item for item in new_list]
            for item in original_list:
                if item in new_list:
                    original_list.pop(original_list.index(item))
                    tmp.pop(tmp.index(item))

            return_value += [(1, original_list)]
            remain = tiles[6:]
        elif len(tiles) == 12 and overlapping_same_shunzi(tiles):
            return_value, remain = [(3, tiles)], []
        else:
            return self.composition_mianzi(tiles[1:])
        return return_value + self.composition_mianzi(remain)

    def composition(self):
        """ take player as input, orgnaize my_tiles into group
            the return value are in the form of [(-1, []), (0, []), (), (), ()]
            -1 means double, 0 means shunzi, 1 means kezi
            >>> ruler = Rule()
            >>> ruler.my_tiles = [(1,0),(1,1),(1,2),(2,4),(3,8),(4,12),(5,16),(5,18),\
                                  (6,23),(7,24),(8,31),(9,32),(9,33),(9,34)]
            >>> ruler.chi_peng_gang_tiles = []
            >>> ruler.composition()
            [(-1, [(5, 16), (5, 18)]), (1, [(1, 0), (1, 1), (1, 2)]), (0, [(2, 4), (3, 8), (4, 12)]), (0, [(6, 23), (7, 24), (8, 31)]), (1, [(9, 32), (9, 33), (9, 34)])]
            >>> ruler.my_tiles = [(1,0), (1,0), (1,0), (2,0), (2,0), (2,0), (3,0), (3,0), (42,0), (42,0), (5,0), \
                                  (5,0), (6,0), (6,0)]
            >>> ruler.chi_peng_gang_tiles = []
            >>> ruler.composition()
            False
            >>> ruler.my_tiles = [(1,0), (1,1)]
            >>> ruler.chi_peng_gang_tiles = [(10, [(2,4), (2,5), (2,6)]), (10, [(3,8), (3,9), (3,10)]), (10, [(4,12), \
                                                        (4,13), (4,14)]), (10, [(5,16), (5,17), (5,19)])]
            >>> ruler.composition()
            [(-1, [(1, 0), (1, 1)]), (10, [(2, 4), (2, 5), (2, 6)]), (10, [(3, 8), (3, 9), (3, 10)]), (10, [(4, 12), (4, 13), (4, 14)]), (10, [(5, 16), (5, 17), (5, 19)])]
        """
        organized_tiles = self.chi_peng_gang_tiles
        for i in range(len(self.my_tiles) - 1):
            if double([self.my_tiles[i], self.my_tiles[i + 1]]):
                test_tiles = [tile for tile in self.my_tiles]
                double_tiles = [(-1, [test_tiles.pop(i), test_tiles.pop(i)])]
                tiles_comp = double_tiles
                test_tiles.sort()
                tiles_comp += self.composition_mianzi(test_tiles)
                tiles_comp += organized_tiles
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


if __name__ == '__main__':
    import doctest

    doctest.testmod()
