import random

class Mahjong:
    def __init__(self, num_players):
        self.tiles = [  '萬1', '萬2', '萬3', '萬4', '萬5', '萬6', '萬7', '萬8', '萬9',
                        '條1', '條2', '條3', '條4', '條5', '條6', '條7', '條8', '條9',
                        '索1', '索2', '索3', '索4', '索5', '索6', '索7', '索8', '索9',
                        'E', 'S', 'W', 'N', 'C', 'F', 'P']      # E:東, S:南, W:西, N:北, C:中, F: 發, P:白
        self.tiles *= 4
        self.players = ['East', 'South', 'West', 'North']
        self.hands = {player :[self.tiles.pop(random.randint(0, len(self.tiles) - 1)) for i in range(16)] for player in self.players}
        self.open_hands = {player :[] for player in self.players}
        self.current_player = 'East'
        self.fisrt_round = True

    def display_hand(self, hand):
        print('\n你的手牌: ')
        index = 1
        for tile in hand:
            print('({0}){1:^2}'.format(index, tile), end=' ')
            index += 1
        print('\n\n')

    def display_open_hand(self):
        for player in self.players:
            print('玩家{0:5}: {1}\n'.format(player, self.open_hands[player]))

    def choose_action(self, hand):
        while True:
            action = int(input('玩家{0}請選擇動作 (1)丟牌, (2)吃, (3)碰, (4)槓, (5)聽, (6)胡, (7)查看open hand, (8)end: '.format(self.current_player)))
            print('\n')
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

    def discard_tile(self, hand):
        while True:
            tile_index = int(input('\nEnter tile to discard: ')) - 1
            if tile_index >= len(hand):
                print('Tile not found in hand. Please try again.')
            else:
                print('{0}丟{1}'.format(self.current_player, hand[tile_index]))
                hand.remove(hand[tile_index])
                return hand
            
    def Kong(self, hand):
        pass

    def Pong(self, hand):
        pass

    def Chow(self, hand):
        pass

    def Ting(self, hand):
        pass

    def win(self, hand):
        pass

    def play(self):
        while True:
            if self.fisrt_round == True and self.current_player == 'East':            # 開門
                self.hands[self.current_player].append(self.tiles.pop(0))
                self.fisrt_round = False

            print('\nPlayer', self.current_player + '\'s turn.')
            self.hands[self.current_player].sort()
            self.display_hand(self.hands[self.current_player])

            # Check for a winning hand
            if self.is_winning_hand(self.hands[self.current_player]):
                print('Congratulations, you win!')
                break
            
            # Choose action
            action = self.choose_action(self.hands[self.current_player])
            '''
            # Ask player to discard a tile
            discard = self.discard_tile(self.hands[self.current_player])
            print('Player', self.current_player, 'discards', discard)
            '''

            # Update hands and next player
            for i in range(len(self.players)):
                if self.players[i] == self.current_player:
                    self.current_player = self.players[(i+1)%len(self.players)]
                    self.hands[self.current_player].append(self.tiles.pop(0))
                    break
            

# Set up game
num_players = 4
game = Mahjong(num_players)

# Play game
game.play()
