import random

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
        self.check_win(draw_tile, self.current_player)

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
                self.check_win(discard_tile, player, True)

        # Check draw
        self.check_draw()

        # Check Kong
        status = self.check_Kong(discard_tile, True)

        # Check Pong
        if not status:
            status = self.check_Pong(discard_tile)

        # Check Chow
        if not status:
            status = self.check_Chow(discard_tile)

        return status

    def check_Kong(self, tile, discard=False):
        hand = self.hands[self.current_player]
        
        count_hand = hand.count(tile)   # Count for the same tile

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
                    decision = int(input("玩家{0}是否要暗槓({1}): (1)是 (2)否: ".format(self.current_player, i)))
                    if decision == 1:
                        for j in range(4):
                            hand.remove(i)
                        Kong_tile_4 = []
                        for j in range(4):
                            Kong_tile_4.append(i)
                        self.open_hands[self.current_player].append(Kong_tile_4)  # append Kong tiles to the player's open hand
                        self.Kong_this_round = True
                        return True
                    return False
            # add Kong
            if is_in_open_hand:
                decision = int(input("玩家{0}是否要加槓: (1)是 (2)否: ".format(self.current_player)))
                if decision == 1:
                    hand.remove(tile)   # remove the tile from player's hand 
                    # adjust the set in open hand from 3 tiles to 4 tiles
                    tile_index = self.open_hands[self.current_player].index(Kong_tile_3)
                    self.open_hands[self.current_player][tile_index].append(tile)
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
                        decision = int(input("玩家{0}是否要明槓: (1)是 (2)否: ".format(player)))
                        if decision == 1:
                            for i in range(3):
                                hand.remove(tile)   # remove tiles from player's hand
                            self.open_hands[player].append(Kong_tile_4)  # append Kong tiles to the player's open hand
                            self.Kong_this_round = True
                            # Player change
                            self.current_player = player
                            return True
                        return False
        return False

    def check_Pong(self, tile):
        Pong_tile = []
        for i in range(3):
            Pong_tile.append(tile)
        
        for player in self.players:
            if player != self.current_player:
                hand = self.hands[player]
                count_hand = hand.count(tile)   # count for the same tile
                
                # Pong
                if count_hand == 2:
                    decision = int(input("玩家{0}是否要碰牌: (1)是 (2)否: ".format(player)))
                    if decision == 1:
                        for i in range(2):
                            hand.remove(tile)   # remove tiles from player's hand
                        self.open_hands[player].append(Pong_tile)  # append Pong tiles to the player's open hand
                        # Player change
                        self.current_player = player
                        '''
                        # Display your hand
                        self.display_hand()
                        '''
                        return True
        return False

    def check_Chow(self, tile):
        current_player_index = self.players.index(self.current_player)
        next_player_index = (current_player_index + 1) % 4
        next_player = self.players[next_player_index]
        hand = self.hands[next_player]
        hand.append(tile)
        
        tile_index = self.all_tiles.index(tile)
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
            decision = int(input("玩家{0}是否要吃牌: (1)是 (2)否: ".format(next_player)))
            if decision == 1:
                print("玩家{0}選擇吃: ".format(next_player), end="")
                for i in range(len(Chow_sets)):
                    print("({0})".format(i+1), end="")
                    for j in range(3):
                        print(Chow_sets[i][j], end=" ")
                Chow_decision = int(input(": "))

                self.open_hands[next_player].append(Chow_sets[Chow_decision-1])   # Append Chow set into the player's open hand
                for i in range(3):
                    hand.remove(Chow_sets[Chow_decision-1][i])

                # Player change
                self.current_player = next_player
                '''
                # display player's hand
                self.display_hand()
                # Discard a tile
                self.discard_tile()
                '''
                return True
            '''
            # 不吃可吃
            else:
                hand.remove(tile)
            '''
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
            tile_index = int(input('\nEnter a tile to discard: ')) - 1
            if tile_index >= len(hand):
                print('Tile not found in hand. Please try again.')
            else:
                print('\nPlayer {0} 丟 {1}\n'.format(self.current_player, hand[tile_index]))
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
        '''
        for player in self.players:
            print("Player {0} 的丟牌: {1}".format(player, self.discard_hand[player]))
        '''
        if len(self.tiles) <= 14:
            print("流局!")
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
            
            # Someone Kong this round -> This player still has their turn.
            if self.Kong_this_round == True:
                self.Kong_this_round = False
                continue
            
            # Player change
            self.player_change()

# Set up game
num_players = 4
game = Mahjong(num_players)

# Play game
game.play()
