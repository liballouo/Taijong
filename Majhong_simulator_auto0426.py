import random
import pandas as pd

class Mahjong:
    def __init__(self, num_players):
        # 有哪些牌
        self.all_tiles = [  '萬1', '萬2', '萬3', '萬4', '萬5', '萬6', '萬7', '萬8', '萬9',  # 0 ~ 8
                        '條1', '條2', '條3', '條4', '條5', '條6', '條7', '條8', '條9',  # 9 ~ 17
                        '餅1', '餅2', '餅3', '餅4', '餅5', '餅6', '餅7', '餅8', '餅9',  # 18~ 26
                        'E', 'S', 'W', 'N', 'C', 'F', 'P']      # E:東, S:南, W:西, N:北, C:中, F: 發, P:白
        # 牌庫
        self.tiles = [  '萬1', '萬2', '萬3', '萬4', '萬5', '萬6', '萬7', '萬8', '萬9',  # 0 ~ 8
                        '條1', '條2', '條3', '條4', '條5', '條6', '條7', '條8', '條9',  # 9 ~ 17
                        '餅1', '餅2', '餅3', '餅4', '餅5', '餅6', '餅7', '餅8', '餅9',  # 18~ 26
                        'E', 'S', 'W', 'N', 'C', 'F', 'P']      # E:東, S:南, W:西, N:北, C:中, F: 發, P:白
        self.w_tiles = ['萬1', '萬2', '萬3', '萬4', '萬5', '萬6', '萬7', '萬8', '萬9']
        self.t_tiles = ['條1', '條2', '條3', '條4', '條5', '條6', '條7', '條8', '條9']
        self.b_tiles = ['餅1', '餅2', '餅3', '餅4', '餅5', '餅6', '餅7', '餅8', '餅9']
        self.tiles *= 4
        self.players = ['1(East)', '2(South)', '3(West)', '4(North)']
        self.card_river = []    
        self.hands = {player :[self.tiles.pop(random.randint(0, len(self.tiles) - 1)) for i in range(16)] for player in self.players}
        self.open_hands = {player :[] for player in self.players}
        self.discard_hand = {player :[] for player in self.players}
        self.sets = {player :[] for player in self.players}
        self.pairs = {player :[] for player in self.players}
        self.current_player = '1(East)'
        self.fisrt_round = True
        self.Kong_this_round = False
        self.win = False
        self.draw = False

        self.Chow_data = pd.DataFrame({
            "throw":[],"hand":[], 
            "openhand1":[], "openhand2":[], "openhand3":[], "openhand4":[],
            "discard1":[], "discard2":[], "discard3":[], "discard4":[],
            "chow":[],
            "chowtype":[]})
        self.Pong_data = pd.DataFrame({
            "throw":[],"hand":[], 
            "openhand1":[], "openhand2":[], "openhand3":[], "openhand4":[],
            "discard1":[], "discard2":[], "discard3":[], "discard4":[],
            "pong":[]})
        self.Kong_data = pd.DataFrame({
            "throw":[],"hand":[], 
            "openhand1":[], "openhand2":[], "openhand3":[], "openhand4":[],
            "discard1":[], "discard2":[], "discard3":[], "discard4":[],
            "kong":[]})
        self.discard_data = pd.DataFrame({
            "throw":[],"hand":[], 
            "openhand1":[], "openhand2":[], "openhand3":[], "openhand4":[],
            "discard1":[], "discard2":[], "discard3":[], "discard4":[]})


    def display_all_hands(self):
        self.sort_all_hands()
        for player in self.players:
            print('\nPlayer {0} 的手牌: '.format(player))
            index = 1
            for tile in self.hands[player]:
                print('({0}){1:^2}'.format(index, tile), end=' ')
                index += 1
            print('\n')

    def display_hand(self):
        self.sort_all_hands()
        print('\nPlayer', self.current_player + '\'s turn.')
        print('\n玩家{0}的手牌: '.format(self.current_player))
        index = 1
        for tile in self.hands[self.current_player]:
            print('({0}){1:^2}'.format(index, tile), end=' ')
            index += 1
        print('\n')

    def display_open_hand(self):
        
        for player in self.players:
            print('玩家{0:5}: {1}\n'.format(player, self.open_hands[player]))

    def player_change(self):
        for i in range(len(self.players)):  # len(self.players) == 4
                if self.players[i] == self.current_player:
                    self.current_player = self.players[(i+1)%len(self.players)]
                    break

    def current_player_turn(self):
        # The turn starts
        # Draw a tile
        draw_tile = self.draw_tile()

        # Sort player's hand
        self.sort_all_hands()

        # Display player's hand
        # self.display_hand()

        # Check win
        self.win = self.check_win(draw_tile, self.current_player)
        if self.win:
            return

        # Check Kong
        self.check_Kong(draw_tile)

        # Discard a tile
        discard_tile = self.discard_tile()

        return discard_tile

    def check_other_player_move(self, discard_tile):
        status = False # Determine whether continue other players' move

        # Check win
        for player in self.players:
            if player != self.current_player:
                self.win = self.check_win(discard_tile, player, True)

        # Check draw
        self.draw = self.check_draw()

        if self.win or self.draw:
            return

        # Check Pong
        status = self.check_Pong(discard_tile)

        # Check Kong
        if not status:
            status = self.check_Kong(discard_tile, True)

        # Check Chow
        if not status:
            status = self.check_Chow(discard_tile)

        return status

    def check_Kong(self, tile, discard=False):
        hand = self.hands[self.current_player]
        
        count_hand = hand.count(tile)   # Count for the same tile

        tile_index = self.all_tiles.index(tile)
        throw_sl = [0] * 34
        throw_sl[tile_index] = 1
        
        Kong_tile_3 = []
        for i in range(3):
            Kong_tile_3.append(tile)
        Kong_tile_4 = []
        for i in range(4):
            Kong_tile_4.append(tile)
        

        # Check whether there's a set in play's open hand
        if Kong_tile_3 in self.open_hands[self.current_player]:
            is_in_open_hand = True
        else:
            is_in_open_hand = False
        
        # A player draws a tile.
        if not discard:
            # concealed Kong case 1:
            for i in hand: # i is the tile in hand
                if hand.count(i) == 4:
                    decision = print("玩家{0}是否要暗槓({1}): (1)是 (2)否: ".format(self.current_player, i), end='')
                    # random choose action 
                    decision = random.randint(1, 2)
                    print(decision)

                    hand_sl = [0] * 34
                    for j in hand:
                        hand_sl[self.all_tiles.index(j)] += 1
                    open_hand_sl = []
                    discard_hand_sl = []
                    Kong_player_index = self.players.index(self.current_player)
                    for p in range(Kong_player_index, Kong_player_index+4):
                        player_index = p % 4
                        player = self.players[player_index]
                        open_hand = self.open_hands[player]
                        discard_hand = self.discard_hand[player]
                        

                        open_hand_array = [0] * 34
                        for j in open_hand:
                            open_hand_array[self.all_tiles.index(j)] += 1
                        open_hand_sl.append(open_hand_array)
                        discard_hand_array = [0] * 34
                        for j in discard_hand:
                            discard_hand_array[self.all_tiles.index(j)] += 1
                        discard_hand_sl.append(discard_hand_array)

                    open_hand_1_sl = open_hand_sl[0]
                    open_hand_2_sl = open_hand_sl[1]
                    open_hand_3_sl = open_hand_sl[2]
                    open_hand_4_sl = open_hand_sl[3]
                    discard_hand_1_sl = discard_hand_sl[0]
                    discard_hand_2_sl = discard_hand_sl[1]
                    discard_hand_3_sl = discard_hand_sl[2]
                    discard_hand_4_sl = discard_hand_sl[3]
                    self.Kong_data.loc[len(self.Kong_data.index)]=[throw_sl,hand_sl,open_hand_1_sl,open_hand_2_sl,open_hand_3_sl,open_hand_4_sl,
                                                                    discard_hand_1_sl,discard_hand_2_sl,discard_hand_3_sl,discard_hand_4_sl,
                                                                    decision] 
                    if decision == 1:
                        for j in range(4):
                            hand.remove(i)
                        #Kong_tile_4 = []
                        for j in range(4):
                            #Kong_tile_4.append(i)
                            self.open_hands[self.current_player].append(i)  # append Kong tiles to the player's open hand
                        self.Kong_this_round = True
                        return True
                    return False
            # add Kong
            if is_in_open_hand:
                decision = print("玩家{0}是否要加槓: (1)是 (2)否: ".format(self.current_player), end='')
                # random choose action 
                decision = random.randint(1, 2)
                print(decision)

                hand_sl = [0] * 34
                for i in hand:
                    hand_sl[self.all_tiles.index(i)] += 1
                open_hand_sl = []
                discard_hand_sl = []
                Kong_player_index = self.players.index(self.current_player)
                for p in range(Kong_player_index, Kong_player_index+4):
                    player_index = p % 4
                    player = self.players[player_index]
                    open_hand = self.open_hands[player]
                    discard_hand = self.discard_hand[player]
                    
                    open_hand_array = [0] * 34
                    for j in open_hand:
                        open_hand_array[self.all_tiles.index(j)] += 1
                    open_hand_sl.append(open_hand_array)
                    discard_hand_array = [0] * 34
                    for j in discard_hand:
                        discard_hand_array[self.all_tiles.index(j)] += 1
                    discard_hand_sl.append(discard_hand_array)
                
                open_hand_1_sl = open_hand_sl[0]
                open_hand_2_sl = open_hand_sl[1]
                open_hand_3_sl = open_hand_sl[2]
                open_hand_4_sl = open_hand_sl[3]
                discard_hand_1_sl = discard_hand_sl[0]
                discard_hand_2_sl = discard_hand_sl[1]
                discard_hand_3_sl = discard_hand_sl[2]
                discard_hand_4_sl = discard_hand_sl[3]
                self.Kong_data.loc[len(self.Chow_data.index)]=[throw_sl,hand_sl,open_hand_1_sl,open_hand_2_sl,open_hand_3_sl,open_hand_4_sl,
                                                               discard_hand_1_sl,discard_hand_2_sl,discard_hand_3_sl,discard_hand_4_sl,
                                                               decision]
                

                if decision == 1:
                    hand.remove(tile)   # remove the tile from player's hand 
                    # adjust the set in open hand from 3 tiles to 4 tiles
                    
                    #tile_index = self.open_hands[self.current_player].index(Kong_tile_3)
                    self.open_hands[self.current_player].append(tile)
                    self.Kong_this_round = True
                    return True
                return False
            return False

        # A player discards a tile.
        if discard:
            for player in self.players:
                if player != self.current_player:
                    hand = self.hands[player]
                    count_hand = hand.count(tile)   # Count for the same tile
                    # exposed Kong
                    if count_hand == 3:
                        decision = print("玩家{0}是否要明槓: (1)是 (2)否: ".format(player), end='')
                        # random choose action 
                        decision = random.randint(1, 2)
                        print(decision)

                        hand_sl = [0] * 34
                        for i in hand:
                            hand_sl[self.all_tiles.index(i)] += 1
                        open_hand_sl = []
                        discard_hand_sl = []
                        Kong_player_index = self.players.index(player)
                        for p in range(Kong_player_index, Kong_player_index+4):
                            player_index = p % 4
                            player_sl = self.players[player_index]
                            open_hand = self.open_hands[player_sl]
                            discard_hand = self.discard_hand[player_sl]
                            
                            open_hand_array = [0] * 34
                            for i in open_hand:
                                open_hand_array[self.all_tiles.index(i)] += 1
                            open_hand_sl.append(open_hand_array)
                            discard_hand_array = [0] * 34
                            for i in discard_hand:
                                discard_hand_array[self.all_tiles.index(i)] += 1
                            discard_hand_sl.append(discard_hand_array)
                        
                        open_hand_1_sl = open_hand_sl[0]
                        open_hand_2_sl = open_hand_sl[1]
                        open_hand_3_sl = open_hand_sl[2]
                        open_hand_4_sl = open_hand_sl[3]
                        discard_hand_1_sl = discard_hand_sl[0]
                        discard_hand_2_sl = discard_hand_sl[1]
                        discard_hand_3_sl = discard_hand_sl[2]
                        discard_hand_4_sl = discard_hand_sl[3]
                        self.Kong_data.loc[len(self.Chow_data.index)]=[throw_sl,hand_sl,open_hand_1_sl,open_hand_2_sl,open_hand_3_sl,open_hand_4_sl,
                                                                       discard_hand_1_sl,discard_hand_2_sl,discard_hand_3_sl,discard_hand_4_sl,
                                                                       decision]

                        if decision == 1:
                            for i in range(3):
                                hand.remove(tile)   # remove tiles from player's hand
                            for i in range(4):
                                self.open_hands[player].append(tile)  # append Kong tiles to the player's open hand
                            self.Kong_this_round = True
                            # Player change
                            self.current_player = player
                            return True
                        return False
        return False

    def check_Pong(self, tile):
        Pong_tile = []

        tile_index = self.all_tiles.index(tile)
        throw_sl = [0] * 34
        throw_sl[tile_index] = 1

        for i in range(3):
            Pong_tile.append(tile)
        
        for player in self.players:
            if player != self.current_player:
                hand = self.hands[player]
                count_hand = hand.count(tile)   # count for the same tile
                
                # Pong
                if count_hand == 2:
                    decision = print("玩家{0}是否要碰牌: (1)是 (2)否: ".format(player), end='')
                    # random choose action 
                    decision = random.randint(1, 2)
                    print(decision)

                    hand_sl = [0] * 34
                    for i in hand:
                        hand_sl[self.all_tiles.index(i)] += 1
                    open_hand_sl = []
                    discard_hand_sl = []
                    Pong_player_index = self.players.index(player)
                    for p in range(Pong_player_index, Pong_player_index+4):
                        player_index = p % 4
                        player_sl = self.players[player_index]
                        open_hand = self.open_hands[player_sl]
                        discard_hand = self.discard_hand[player_sl]

                        open_hand_array = [0] * 34
                        for i in open_hand:
                            open_hand_array[self.all_tiles.index(i)] += 1
                        open_hand_sl.append(open_hand_array)
                        discard_hand_array = [0] * 34
                        for i in discard_hand:
                            discard_hand_array[self.all_tiles.index(i)] += 1
                        discard_hand_sl.append(discard_hand_array)
                    
                    open_hand_1_sl = open_hand_sl[0]
                    open_hand_2_sl = open_hand_sl[1]
                    open_hand_3_sl = open_hand_sl[2]
                    open_hand_4_sl = open_hand_sl[3]
                    discard_hand_1_sl = discard_hand_sl[0]
                    discard_hand_2_sl = discard_hand_sl[1]
                    discard_hand_3_sl = discard_hand_sl[2]
                    discard_hand_4_sl = discard_hand_sl[3]
                    self.Pong_data.loc[len(self.Pong_data.index)]=[throw_sl,hand_sl,open_hand_1_sl,open_hand_2_sl,open_hand_3_sl,open_hand_4_sl,
                                                                   discard_hand_1_sl,discard_hand_2_sl,discard_hand_3_sl,discard_hand_4_sl,
                                                                   decision]

                    if decision == 1:
                        for i in range(2):
                            hand.remove(tile)   # remove tiles from player's hand
                        for i in range(3):
                            self.open_hands[player].append(tile)  # append Pong tiles to the player's open hand
                        # Player change
                        self.current_player = player
                        
                        return True
        return False

    def check_Chow(self, tile):
        current_player_index = self.players.index(self.current_player)
        next_player_index = (current_player_index + 1) % 4
        next_player = self.players[next_player_index]
        hand = self.hands[next_player]

        hand_sl = [0] * 34
        for i in hand:
            hand_sl[self.all_tiles.index(i)] += 1
        open_hand_sl = []
        discard_hand_sl = []
        for p in range(next_player_index, next_player_index+4):
            player_index = p % 4
            player = self.players[player_index]
            open_hand = self.open_hands[player]
            discard_hand = self.discard_hand[player]
            
            open_hand_array = [0] * 34
            for i in open_hand:
                open_hand_array[self.all_tiles.index(i)] += 1
            open_hand_sl.append(open_hand_array)
            discard_hand_array = [0] * 34
            for i in discard_hand:
                discard_hand_array[self.all_tiles.index(i)] += 1
            discard_hand_sl.append(discard_hand_array)
            
        
        open_hand_1_sl = open_hand_sl[0]
        open_hand_2_sl = open_hand_sl[1]
        open_hand_3_sl = open_hand_sl[2]
        open_hand_4_sl = open_hand_sl[3]
        discard_hand_1_sl = discard_hand_sl[0]
        discard_hand_2_sl = discard_hand_sl[1]
        discard_hand_3_sl = discard_hand_sl[2]
        discard_hand_4_sl = discard_hand_sl[3]

        hand.append(tile)
        
        tile_index = self.all_tiles.index(tile)
        throw_sl = [0] * 34
        throw_sl[tile_index] = 1

        Chow_sets = []  # 紀錄可以吃的組合
        tile_type = []  # 哪種牌(萬or條or餅)
        # 萬
        if tile_index < 9:
            tile_type = self.w_tiles
            tile_index %= 9
        # 條
        elif tile_index < 18:
            tile_type = self.t_tiles
            tile_index %= 9
        # 餅
        elif tile_index < 27:
            tile_type = self.b_tiles
            tile_index %= 9

        for i in range(3):
            Chow_set = []
            # Decide whether can Chow or not
            '''
            +----+----+----+----+
            |\ i |    |    |    |
            | \  | -0 | -1 | -2 |
            |j \ |    |    |    |
            +----+----+----+----+
            | +0 |  0 | -1 | -2 |
            +----+----+----+----+
            | +1 |  1 |  0 | -1 |
            +----+----+----+----+
            | +2 |  2 |  1 |  0 |
            +----+----+----+----+
            '''
            for j in range(3):
                can_Chow = True
                if tile_index-i+j >= 0 and tile_index-i+j <= 8:
                    if tile_type[tile_index-i+j] in hand:
                        Chow_set.append(tile_type[tile_index-i+j])
                    else:
                        can_Chow = False
                else:
                    can_Chow = False

                if not can_Chow:
                    Chow_set = []
                    break
            
            # 有可以吃的組合
            if len(Chow_set) > 0:
                if tile in Chow_set:
                    Chow_sets.append(Chow_set)


        if len(Chow_sets) > 0:
            print("玩家{0}是否要吃牌: (1)否 ".format(next_player), end="")
            for i in range(len(Chow_sets)):
                print("({0})".format(i+2, end=""))
                for j in range(3):
                    print(Chow_sets[i][j], end=" ")
            decision = random.randint(1, len(Chow_sets)+1)
            print(decision)
            '''
            decision = print("玩家{0}是否要吃牌: (1)是 (2)否: ".format(next_player), end='')
            # random choose action 
            decision = random.randint(1, 2)
            print(decision)
            '''
            # player chooses Chow
            if decision != 1:
                '''
                print("玩家{0}選擇吃: ".format(next_player), end="")
                for i in range(len(Chow_sets)):
                    print("({0})".format(i+1), end="")
                    for j in range(3):
                        print(Chow_sets[i][j], end=" ")
                print(": ", end='')
                # Random choose action
                Chow_decision = random.randint(1, len(Chow_sets))
                print(Chow_decision)
                '''
                Chow_decision = decision

                Chow_type_sl = [0] * 34
                for i in Chow_sets[Chow_decision-2]:
                    Chow_type_sl[self.all_tiles.index(i)] += 1
                self.Chow_data.loc[len(self.Chow_data.index)]=[throw_sl,hand_sl,open_hand_1_sl,open_hand_2_sl,open_hand_3_sl,open_hand_4_sl,
                                                               discard_hand_1_sl,discard_hand_2_sl,discard_hand_3_sl,discard_hand_4_sl,
                                                               decision,Chow_type_sl]

                for i in range(3):
                    self.open_hands[next_player].append(Chow_sets[Chow_decision-2][i])   # Append Chow set into the player's open hand

                    hand.remove(Chow_sets[Chow_decision-2][i])

                # Player change
                self.current_player = next_player

                return True
            # player chooses not Chow
            else:
                Chow_type_sl = [0] * 34
                self.Chow_data.loc[len(self.Chow_data.index)]=[throw_sl,hand_sl,open_hand_1_sl,open_hand_2_sl,open_hand_3_sl,open_hand_4_sl,
                                                               discard_hand_1_sl,discard_hand_2_sl,discard_hand_3_sl,discard_hand_4_sl,
                                                               decision,Chow_type_sl]

            
        hand.remove(tile)
        return False

    def sort_all_hands(self):
        for player in self.players:
            self.hands[player].sort()

    def draw_tile(self):
        self.hands[self.current_player].append(self.tiles.pop(0))
        tile = self.hands[self.current_player][-1]
        return tile

    def discard_tile(self):
        hand = self.hands[self.current_player]
        hand.sort()
        while True:
            self.display_hand()
            print('\nEnter a tile to discard: ', end='')
            # Random choose action
            tile_index = random.randint(1, len(self.hands[self.current_player]))
            print(tile_index)
            tile_index -= 1
            
            if tile_index >= len(hand):
                print('Tile not found in hand. Please try again.')
            else:
                print('\nPlayer {0} 丟 {1}\n'.format(self.current_player, hand[tile_index]))

                throw_sl = [0] * 34
                throw_sl[self.all_tiles.index(hand[tile_index])] = 1
                hand_sl = [0] * 34
                for i in hand:
                    hand_sl[self.all_tiles.index(i)] += 1
                open_hand_sl = []
                discard_hand_sl = []
                discard_player_index = self.players.index(self.current_player)
                for p in range(discard_player_index, discard_player_index+4):
                    player_index = p % 4
                    player = self.players[player_index]
                    open_hand = self.open_hands[player]
                    discard_hand = self.discard_hand[player]
                    
                    open_hand_array = [0] * 34
                    for i in open_hand:
                        open_hand_array[self.all_tiles.index(i)] += 1
                    open_hand_sl.append(open_hand_array)
                    discard_hand_array = [0] * 34
                    for i in discard_hand:
                        discard_hand_array[self.all_tiles.index(i)] += 1
                    discard_hand_sl.append(discard_hand_array)
                
                open_hand_1_sl = open_hand_sl[0]
                open_hand_2_sl = open_hand_sl[1]
                open_hand_3_sl = open_hand_sl[2]
                open_hand_4_sl = open_hand_sl[3]
                discard_hand_1_sl = discard_hand_sl[0]
                discard_hand_2_sl = discard_hand_sl[1]
                discard_hand_3_sl = discard_hand_sl[2]
                discard_hand_4_sl = discard_hand_sl[3]

                self.discard_data.loc[len(self.discard_data.index)]=[throw_sl,hand_sl,open_hand_1_sl,open_hand_2_sl,open_hand_3_sl,open_hand_4_sl,
                                                                  discard_hand_1_sl,discard_hand_2_sl,discard_hand_3_sl,discard_hand_4_sl]



                discard_tile = hand[tile_index]
                hand.remove(hand[tile_index])
                self.discard_hand[self.current_player].append(discard_tile)
                self.discard_hand[self.current_player].sort()
                return discard_tile

    def check_win(self, tile, player, discard=False):
        hand = self.hands[player].copy()
        if discard:
            hand.append(tile)
        hand.sort()
        eyes = []
        for i in range(len(hand) - 1):
            if hand[i] == hand[i+1] and eyes.count(hand[i]) == 0:
                eyes.append(hand[i])

        if len(eyes) == 0:
            return False

        for eye in eyes:
            hand = self.hands[player].copy()
            if discard:
                hand.append(tile)
            hand.sort()
            hand.remove(eye)
            hand.remove(eye)
            
            while True:
                # Win 
                if len(hand) == 0:
                    print("Player {0} win!!!".format(player))
                    global num_wins
                    num_wins += 1

                    self.Chow_data.to_csv('Chow_data.csv', mode='a')
                    self.Pong_data.to_csv('Pong_data.csv', mode='a')
                    self.Kong_data.to_csv('Kong_data.csv', mode='a')
                    self.discard_data.to_csv('discard_data.csv', mode='a')
                    exit()
                    return True
                    exit()
                # The first tile in hand
                i = hand[0]
                # Remove Pong first
                if hand.count(i) >= 3:
                    hand.remove(i)
                    hand.remove(i)
                    hand.remove(i)
                    continue
                
                if self.all_tiles.index(i) > 26:    # 字牌
                    break
                
                tile_type = []  # 哪種牌(萬or薯條or薯餅)
                tile_index = self.all_tiles.index(i)
                # 萬
                if tile_index < 9:
                    tile_type = self.w_tiles
                    tile_index %= 9
                # 條
                elif tile_index < 18:
                    tile_type = self.t_tiles
                    tile_index %= 9
                # 餅
                elif tile_index < 27:
                    tile_type = self.b_tiles
                    tile_index %= 9

                # Check Chow (start from 1 to 7, e.g. "'1'23", "'5'67")
                if tile_type.index(i) < 7:
                    chow_index = tile_type.index(i)
                    chow_mid = tile_type[chow_index + 1]
                    chow_last = tile_type[chow_index + 2]

                    # Remove Chow
                    if hand.count(chow_mid) != 0 and hand.count(chow_last) != 0:
                        hand.remove(i)
                        hand.remove(chow_mid)
                        hand.remove(chow_last)
                        continue
                # This tile isn't able to form a set.
                break
        return False
    
    # 流局
    def check_draw(self):
        
        if len(self.tiles) <= 14:
            print("流局!")
            self.Chow_data.to_csv('Chow_data.csv', mode='a')
            self.Pong_data.to_csv('Pong_data.csv', mode='a')
            self.Kong_data.to_csv('Kong_data.csv', mode='a')
            self.discard_data.to_csv('discard_data.csv', mode='a')
            global num_draws
            num_draws += 1
            return True
            exit()

    def play(self):
        first_turn = True
        while True:
            # Sort all players' hands
            self.sort_all_hands()
            if first_turn:
                self.display_all_hands()
                first_turn = False
            # Continue to next turn
            next_turn = False
            do = False

            # Current player's turn
            discard_tile = self.current_player_turn()

            # Other player's turn
            while((next_turn or not do) and not self.Kong_this_round):
                next_turn = self.check_other_player_move(discard_tile)
                if next_turn and not self.Kong_this_round:
                    discard_tile = self.discard_tile()
                do = True

            if self.win or self.draw:
                break
            
            # Someone Kong this round -> This player still has their turn.
            if self.Kong_this_round == True:
                self.Kong_this_round = False
                continue
            
            # Player change
            self.player_change()



# Set up game
num_players = 4

num_wins = 0
num_draws = 0


for i in range(50):
    game = Mahjong(num_players)

    # Play game
    game.play()

print("贏的次數: {0}".format(num_wins))
print("和局次數: {0}".format(num_draws))