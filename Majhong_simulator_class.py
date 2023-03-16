import random

class Mahjong:
    def __init__(self, num_players):
        self.tiles = [  '萬1', '萬2', '萬3', '萬4', '萬5', '萬6', '萬7', '萬8', '萬9',
                        '條1', '條2', '條3', '條4', '條5', '條6', '條7', '條8', '條9',
                        '餅1', '餅2', '餅3', '餅4', '餅5', '餅6', '餅7', '餅8', '餅9',
                        'E', 'S', 'W', 'N', 'C', 'F', 'P']      # E:東, S:南, W:西, N:北, C:中, F: 發, P:白
        self.w_tiles = ['萬1', '萬2', '萬3', '萬4', '萬5', '萬6', '萬7', '萬8', '萬9']
        self.t_tiles = ['條1', '條2', '條3', '條4', '條5', '條6', '條7', '條8', '條9']
        self.b_tiles = ['餅1', '餅2', '餅3', '餅4', '餅5', '餅6', '餅7', '餅8', '餅9']
        self.tiles *= 4
        self.players = ['1(East)', '2(South)', '3(West)', '4(North)']
        self.card_river = []    
        self.hands = {player :[self.tiles.pop(random.randint(0, len(self.tiles) - 1)) for i in range(16)] for player in self.players}
        self.open_hands = {player :[] for player in self.players}
        self.sets = {player :[] for player in self.players}
        self.pairs = {player :[] for player in self.players}
        self.current_player = '1(East)'
        self.fisrt_round = True

    def display_all_hands(self):
        for player in self.players:
            print('\nPlayer {0} 的手牌: '.format(player))
            index = 1
            for tile in self.hands[player]:
                print('({0}){1:^2}'.format(index, tile), end=' ')
                index += 1
            print('\n')

    def display_hand(self):
        print('\nPlayer', self.current_player + '\'s turn.')
        print('\n你的手牌: ')
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

    def choose_action(self, hand):
        while True:
            action = int(input('玩家{0}請選擇動作 (1)丟牌, (2)吃, (3)碰, (4)槓, (5)聽, (6)胡, (7)查看open hand, (8)end: '.format(self.current_player)))
            if action == 1:
                discard = self.discard_tile(hand)
                return discard
            elif action == 2:
                set = self.Chow(hand)
                return set
            elif action == 3:
                set = self.Pong(hand)
                return set
            elif action == 4:
                set = self.Kong(hand)
                return set
            elif action == 5:
                status = self.Ting(hand)
                return status
            elif action == 6:
                status = self.win(hand)
                return status
            elif action == 7:
                self.display_open_hand()
                continue
            elif action == 8:
                exit()
            else:
                print('Invalid action, please try again.')

    def is_winning_tile(self, hand, tile):
        hand_copy = hand[:]
        hand_copy.append(tile)
        hand_copy.sort()

        # Check for a pair
        pairs = [hand_copy[i] for i in range(0, len(hand_copy)-1, 2) if hand_copy[i] == hand_copy[i+1]]
        if len(pairs) != 1:
            return False

        # Check for sets
        sets = [hand_copy[i:i+3] for i in range(0, len(hand_copy)-2, 3) if hand_copy[i] == hand_copy[i+2]]
        if len(sets) != 4:
            return False

        # Check for eyes
        for i in range(len(hand_copy) - 1):
            if hand_copy[i] == hand_copy[i+1]:
                return True
        return False

    def is_winning_hand(self, hand):
        for tile in self.tiles:
            if self.is_winning_tile(hand, tile):
                return True
        return False
    
    def current_player_turn(self):
        # The turn starts
        # Draw a tile
        draw_tile = self.draw_tile()

        # Sort player's hand
        self.sort_all_hands()

        # Display player's hand
        self.display_hand()

        # Check win
        

        # Check Kong
        self.check_Kong(draw_tile)

        # Discard a tile
        discard_tile = self.discard_tile()

        return discard_tile

    def check_other_player_move(self, discard_tile):
        status = False # Determine whether continue other players' move

        # Check win

        # Check Kong
        status = self.check_Kong(discard_tile, True)

        # Check Pong
        status = self.check_Pong(discard_tile)

        # Check Chow


        return status

    def check_Kong(self, tile, discard=False):
        
        hand = self.hands[self.current_player]
        count_hand = hand.count(tile)   # count for the same tile

        Kong_tile_3 = []
        for i in range(3):
            Kong_tile_3.append(tile)
        Kong_tile_4 = []
        

        # check whether there's a set in play's open hand
        if Kong_tile_3 in self.open_hands[self.current_player]:
            is_in_open_hand = True
        else:
            is_in_open_hand = False
        
        # A player draws a tile.
        if not discard:
            # concealed Kong case 1:
            for i in range(len(hand)): # i is the tile in hand
                if hand.count(i) == 4:
                    decision = int(input("玩家{0}是否要槓牌: (1)是 (2)否: ".format(self.current_player)))
                    if decision == 1:
                        for j in range(4):
                            hand.remove(i)
                        for j in range(4):
                            Kong_tile_4.append(i)
                        self.open_hands[self.current_player].append(Kong_tile_4)  # append Kong tiles to the player's open hand
                        return True
            '''
            # concealed Kong case 2:
            if count_hand == 4:
                decision = int(input("玩家{0}是否要槓牌: (1)是 (2)否: ".format(self.current_player)))
                if decision == 1:
                    for i in range(4):
                        hand.remove(tile)   # remove tiles from player's hand
                    self.open_hands[self.current_player].append(Kong_tile_4)  # append Kong tiles to the player's open hand
                    return True
            '''
            # add Kong
            if is_in_open_hand:
                decision = int(input("玩家{0}是否要槓牌: (1)是 (2)否: ".format(self.current_player)))
                if decision == 1:
                    hand.remove(tile)   # remove the tile from player's hand 
                    # adjust the set in open hand from 3 tiles to 4 tiles
                    tile_index = self.open_hands[self.current_player].index(Kong_tile_3)
                    self.open_hands[self.current_player][tile_index] += tile
                    return True

        # A player discards a tile.
        if discard:
            for player in self.players:
                # exposed Kong
                if count_hand == 3:
                    decision = int(input("玩家{0}是否要槓牌: (1)是 (2)否: ".format(player)))
                    if decision == 1:
                        for i in range(3):
                            hand.remove(tile)   # remove tiles from player's hand
                        self.open_hands[player].append(Kong_tile_4)  # append Kong tiles to the player's open hand
                        # change player
                        self.current_player = player
                        self.player_change()
                        return True
        return False

    def check_Pong(self, tile):
        Pong_tile = []
        for i in range(3):
            Pong_tile.append(tile)
        
        for player in self.players:
            hand = self.hands[player]
            count_hand = hand.count(tile)   # count for the same tile
            
            # Pong
            if count_hand == 2:
                decision = int(input("玩家{0}是否要碰牌: (1)是 (2)否: ".format(player)))
                if decision == 1:
                    for i in range(2):
                        hand.remove(tile)   # remove tiles from player's hand
                    self.open_hands[player].append(Pong_tile)  # append Pong tiles to the player's open hand
                    # Change player
                    self.current_player = player
                    # Display your hand
                    self.display_hand()
                    # Discard a tile
                    self.discard_tile()
                    return True
        return False

    def check_Chow(self):
        pass

    def sort_all_hands(self):
        for player in self.players:
            self.hands[player].sort()

    def draw_tile(self):
        tile = self.hands[self.current_player].append(self.tiles.pop(0))
        return tile

    def discard_tile(self):
        hand = self.hands[self.current_player]
        while True:
            tile_index = int(input('\nEnter tile to discard: ')) - 1
            if tile_index >= len(hand):
                print('Tile not found in hand. Please try again.')
            else:
                print('\nPlayer {0} 丟 {1}\n'.format(self.current_player, hand[tile_index]))
                discard_tile = hand[tile_index]
                hand.remove(hand[tile_index])
                return discard_tile

    def check_win(self, tile):
            hand = self.hands[self.current_player]
            hand.append(tile)
            hand = hand.sort()
            eyes = []
            for i in range(len(hand) - 1):
                if hand[i] == hand[i+1] and eyes.count(hand[i]) == 0:
                    eyes.append(hand[i])
            
            if len(eyes) == 0:
                return False

            for eye in eyes:
                hand = self.hands[self.current_player]
                hand.remove(eye)
                hand.remove(eye)
                for i in hand:
                    if hand.count(i) >= 3:
                        hand.remove(i)
                        hand.remove(i)
                        hand.remove(i)
                        continue
                    
                    if self.w_tiles.count(i):
                        chow_index = self.w_tiles.index(i)
                        chow_mid = self.w_tiles[chow_index + 1]
                        chow_last = self.w_tiles[chow_index + 2]
                    elif self.t_tiles.count(i):
                        chow_index = self.t_tiles.index(i)
                        chow_mid = self.t_tiles[chow_index + 1]
                        chow_last = self.t_tiles[chow_index + 2]
                    elif self.b_tiles.count(i):
                        chow_index = self.b_tiles.index(i)
                        chow_mid = self.b_tiles[chow_index + 1]
                        chow_last = self.b_tiles[chow_index + 2]

                    if hand.count(chow_mid) != 0 and hand.count(chow_last) != 0:
                        hand.remove(i)
                        hand.remove(chow_mid)
                        hand.remove(chow_last)
                        continue
                    break
                if len(hand) == 0:
                    return True

    def play(self):
        first_turn = True
        while True:
            # Sort all players' hands
            self.sort_all_hands()
            if first_turn:
                self.display_all_hands()
                first_turn = False
            # continue to next turn
            next_turn = False
            do = False

            # current player's turn
            discard_tile = self.current_player_turn()

            # other player's turn
            while(next_turn or not do):
                next_turn = self.check_other_player_move(discard_tile)
                do = True
            
            # end or not
            end = int(input("end or not (1)yes (2)no: "))
            if end == 1:
                exit()

            #  Player change
            self.player_change()
            
            

# Set up game
num_players = 4
game = Mahjong(num_players)

# Play game
game.play()
