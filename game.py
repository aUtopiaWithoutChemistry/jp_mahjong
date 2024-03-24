import random, math
from element import all_tiles
from rules import win, check_point
from player import player

# table class，包含四个玩家和剩余牌
class game:
    
    ''' cur_tile is the tile that every player discard, if no one chi, peng, gang, hu, then this tile
        goes into current player's waste tiles, clear cur_tile, waiting for next player discard
    '''
    cur_tile = ((-1, -1), -1) # the first tuple shows the tile, second shows where it from
    cur_player = -1 # how many players in there
    total_chang = 0
    cur_chang = -1
    cur_ju = -1
    time_stamp = -1
    this_game = []
    players = []
    
    ''' store all players behaviors in a total game 
        in the form of [ [(cur_chang, cur_ju), (0, 0's tiles), (1, 1's tiles), (2, 2's tiles), (3, 3's tiles),
                          (time stamp, player_number, behavior, on which tile)], [], []]
        the cur_chang and cur_ju will be the index 0 for every element in this list, the second to the fifth will
        be the initial tiles for player 0 to 3, from index six there will be every single move on the game,
        they should be in the form of (time_stamp, player, behavior, tile)
        
        time_stamp is an attribute of game, it will renew in each new game, and increament when every movement have been 
        down.
        
        behavior can be 'mopai', 'chi', 'peng', 'gang', 'add_gang', 'hidden_gang', 'discard', 'riichi', 'zimo', 'rong_hu', 'liu_ju'
        
        tile should be in the form of (value, id)
    '''
    all_behaviors = []       
    
    ace = []                # 14 in total, lingshang and dora tiles are in this
    ling_shang_tiles = []   # max 4, only can be access when someone gang
    surface_dora_tiles = [] # max 1, visable from starting
    hidden_dora_tiles = []  # max 4, every riichi from player will show one more
    gang_dora_tiles = []    # max 4, every gang from player will show one more


    def __init__(self, total_chang=2, total_player=4):
        # decide how many chang in total should be played
        self.total_chang = total_chang
        self.total_player = total_player
        self.cur_chang = 0
        self.cur_ju = 0
        self.time_stamp = 0

        # add all mahjong tiles in this game
        for ele in all_tiles:
            self.this_game.append(ele)

        # create n players
        for n in range(total_player):
            self.players.append(player(25000, [], n, False))
    
    
    def time_update(self):
        self.time_stamp += 1
        return self.time_stamp
    

    def shuffle(self):
        random.shuffle(self.this_game)


    def end(self, end_type, cur_players):
        ''' check which type of end is this game, players is a list, shows which player 
            and how many players can win, then call the check point function then transfer
            points to end current game 
        '''
        if end_type == 'liuju':
            ''' when liuju, game() will pass all four players in a list to end method
                we should check which one is in the status of ting_pai, so that they can get
                points from other who didn't in that status
            '''
            ting_pai = []
            for player in cur_players:
                if player.final_check_ting_pai():
                    ting_pai += [player]
            send = [player for player in self.players if player not in ting_pai]
            if len(ting_pai) == 0 or len(ting_pai) == 4:
                return False
            elif len(ting_pai) == 1:
                for i in range(3):
                    self.transfer_point(1000, send[i], ting_pai[0])
            elif len(ting_pai) == 2:
                for i in range(2):
                    self.transfer_point(1000, send[i], ting_pai[i])
            elif len(ting_pai) == 3:
                for i in range(3):
                    self.transfer_point(1000, send[0], ting_pai[i])
                
        elif end_type == 'zimo':
            ''' when zimo, game() will pass a list have single item which is the player
                who finished his tile. Other should give to that player 1/3 of this player's
                final score, if the outcome of multiple by 1/3 is not divisible by 100, then
                make it up to the nearest 100 number
            '''
            send = [player for player in self.players if player not in cur_players]
            total_point = check_point(cur_players[0])
            points_from_other = math.ceil(total_point // 100 / 3) * 100
            for i in range(3):
                if send[i].my_position == self.cur_chang:
                    self.transfer_point(points_from_other, send[i], cur_players[0])
            
        elif end_type == 'ronghu':
            ''' when ronghu, game will pass a list that contains the loser and all other winner,
                loser should pay full score that winner made
            '''
            loser, winners = cur_players[0], cur_players[1:]
            points = []
            for winner in winners:
                points += [check_point(winner)]
            for i in range(len(winner)):
                self.transfer_point(points[i], loser, winner[i])
    

    def transfer_point(send_points, from_who, to_whom):
        from_who.score -= send_points
        to_whom.score += send_points
    

    def next_player(self, player):
        ''' both player and ju should in [0, 3]
            if reach 3, then next should be 0

            >>> game1 = game(1, 4)
            >>> game1.cur_player.index() = 2
            >>> game1.cur_player = game1.next_item(game1.cur_player)
            >>> game1.cur_player.index()
            3
            >>> game1.cur_player = game1.next_item(game1.cur_player)
            >>> game1.cur_player.index()
            0
        '''
        index = self.players.index(player)
        return self.players[index + 1] if index < 3 else self.players[0]
    

    def game(self, cur_player, remain_tiles, storage_place):
        ''' game is a recursive method, it only finished when one
            player wins or run out of tiles
        '''
        
        #   if there are no tiles in remain_tiles, weather there's no tile in
        #   this_game, or there's no tile in 岭上 tiles, which means there are
        #   four gang in a single game, both will lead to 流局    
        if len(remain_tiles) <= 0:
            self.end('liuju', self.players)
            return True

        # read player's tiles
        player_tiles = cur_player.my_tiles
        player_chi_peng_gang_tiles = cur_player.chi_peng_gang_tiles

        # mopai this will change remain_tiles
        cur_player.mopai(remain_tiles)
        self.time_stamp += 1

        # check if zimo
        if win(player_tiles, player_chi_peng_gang_tiles):
            self.end('zimo', [cur_player])
            return True

        # check hidden_gang
        if cur_player.check_hidden_gang():
            cur_player.hidden_gang()
            self.time_stamp += 1
            remain_tiles = self.ling_shang_tiles
            self.game(cur_player, remain_tiles, storage_place)

        # check add_gang
        if cur_player.check_add_gang():
            cur_player.add_gang()
            self.time_stamp += 1
            
            ting_pai_player = [player for player in self.players if player.check_ting_pai()]
            if ting_pai_player != []:
                self.end('ronghu', [cur_player] + ting_pai_player)
                return True

            remain_tiles = self.ling_shang_tiles
            self.game(cur_player, remain_tiles, storage_place)

        # check riichi
        if cur_player.check_riichi():
            cur_player.riichi()
            self.time_stamp += 1
        else: 
            cur_player.discard()
            self.time_stamp += 1

        # check if current discarded tile in th list of other player ting_pai tiles
        self.cur_tile = (cur_player.my_waste[len(cur_player.my_waste) - 1], self.players.index(cur_player))
        ting_pai_player = [player for player in self.players if player.check_ting_pai()]
        if ting_pai_player != []:
            self.end('ronghu', [cur_player] + ting_pai_player)
            return True

        for player in self.players:

            if player.check_gang():
                player.gang()
                self.time_stamp += 1
                remain_tiles = self.ling_shang_tiles
                self.game(player, remain_tiles, storage_place)
            
            if player.check_peng():
                player.peng()
                self.time_stamp += 1
                self.game(player, remain_tiles, storage_place)
            
            if player.check_chi():
                player.chi()
                self.time_stamp += 1
                self.game(player, remain_tiles, storage_place)
        
        cur_player = self.next_player(cur_player)
        self.game(cur_player, remain_tiles, storage_place)
        

    def start_ju(self):
        ''' setup all the stuff for a new ju in this game
        '''
        if self.cur_ju != 3:
            self.cur_ju += 1
        else: 
            self.cur_ju = 0
            self.cur_chang += 1
            if self.cur_chang > self.total_chang:
                print("Game end!")
                return False

        # the index in all_behaviors for this game
        storage_place = self.cur_chang * 4 + self.cur_ju
        
        # add all mahjong tiles in this game
        all_tiles = []
        for ele in all_tiles:
            self.this_game.append(ele)

        # shuffle all the tiles
        self.this_game.shuffle()

        # prepare for ace tiles
        self.ace = []
        self.ling_shang_tiles = [] 
        self.surface_dora_tiles = []
        self.hidden_dora_tiles = [] 
        self.gang_dora_tiles = []

        for i in range(14):
            self.ace.append(self.this_game.pop(i))
        self.surface_dora_tiles.append(self.ace.pop(0))

        for i in range(4):
            self.ling_shang_tiles.append(self.ace.pop(i))

        for i in range(4):
            # clear all players' tiles ready for the new game
            self.players[i].my_tiles = []
            self.players[i].my_waste = []
            self.players[i].chi_peng_gang_tiles = []

            # change the position for every player
            if self.players[i].position != 3:
                self.players[i].position += 1
            else:
                self.players[i].position = 0
        
        self.time_stamp = 0
        self.game(self.players[0], self.this_game, storage_place)


    # TODO
    def store_game():
        return False
    
    
    # TODO 
    def reply():
        return False