from tile import *
from deck import Deck
# from .tile import *
# from .deck import Deck

class Player:
    number_of_player = 0

    def __init__(self):
        self.deck = Deck()
        self.hand = []
        self.open_hand = []
        self.discard_hand = []
        self.player_number = Player.number_of_player
        Player.number_of_player += 1
        self.draw_tile = ""
        self.jia_kong_tile = ""
        self.an_kong_tile = ""
        self.discard_tile = ""
        self.kong_tile = ""
        self.pong_tile = ""
        self.chow_sets = []
        self.ting_tiles = []
        self.win_or_not = False
        self.jia_kong_or_not = False
        self.an_kong_or_not = False
        self.ting_or_not = False
        self.decision_types = {"kong": 0, "pong": 0, "chow": 0}
        self.decision_results = ""
        
    def draw(self, tile):
        self.hand.append(tile)
        return tile

    def show_hand(self):
        # print(*self.hand)
        for i in range(len(self.hand)):
            print(f"({i+1}){self.hand[i]}", end = " ")
        print("")

    def check_win(self):
        hand = self.hand.copy()
        hand.sort()
        eyes = []
        for i in range(len(hand) - 1):
            if hand.count(hand[i]) == 2 and eyes.count(hand[i]) == 0:
                eyes.append(hand[i])

        if len(eyes) == 0:
            return False

        for eye in eyes:
            hand = self.hand.copy()
            hand.sort()
            hand.remove(eye)
            hand.remove(eye)
            
            while True:
                # Win 
                if len(hand) == 0:
                    return True
                # The first tile in hand
                i = hand[0]
                # Remove Pong first
                if hand.count(i) >= 3:
                    hand.remove(i)
                    hand.remove(i)
                    hand.remove(i)
                    continue
                
                if ALL_TILES.index(i) > 26: # 字牌
                    break
                
                tile_index, tile_type = self.deck.find_tile_type_index(i)

                # Check Chow (start from 1 to 7, e.g. "'1'23", "'5'67")
                if tile_type.index(i) < 7:

                    chow_set = tile_type[tile_index:tile_index+3]

                    # Remove Chow
                    if hand.count(chow_set[1]) != 0 and hand.count(chow_set[2]) != 0:
                        for tile in chow_set:
                            hand.remove(tile)
                        continue
                # This tile isn't able to form a set.
                break
        return False
    
    def check_fang_qiang(self, discard_tile):
        hand = self.hand.copy()
        hand.append(discard_tile)
        hand.sort()
        eyes = []
        for i in range(len(hand) - 1):
            if hand.count(hand[i]) == 2 and eyes.count(hand[i]) == 0:
                eyes.append(hand[i])

        if len(eyes) == 0:
            return False

        for eye in eyes:
            hand = self.hand.copy()
            hand.append(discard_tile)
            hand.sort()
            hand.remove(eye)
            hand.remove(eye)
            
            while True:
                # Win 
                if len(hand) == 0:
                    return True
                # The first tile in hand
                i = hand[0]
                # Remove Pong first
                if hand.count(i) >= 3:
                    hand.remove(i)
                    hand.remove(i)
                    hand.remove(i)
                    continue
                
                if ALL_TILES.index(i) > 26: # 字牌
                    break
                
                tile_index, tile_type = self.deck.find_tile_type_index(i)

                # Check Chow (start from 1 to 7, e.g. "'1'23", "'5'67")
                if tile_type.index(i) < 7:

                    chow_set = tile_type[tile_index:tile_index+3]

                    # Remove Chow
                    if hand.count(chow_set[1]) != 0 and hand.count(chow_set[2]) != 0:
                        for tile in chow_set:
                            hand.remove(tile)
                        continue
                # This tile isn't able to form a set.
                break
        return False
    
    def check_ting(self):
        self.ting_tiles = []
        hand = self.hand.copy()
        hand.sort()
        for k in hand:
            ting_tile = k
            ting_hand = hand.copy()
            ting_hand.remove(k)
            for j in ALL_TILES:
                win_hand = ting_hand.copy()
                win_hand.append(j)
                win_hand.sort()
                eyes = []
                for i in range(len(win_hand) - 1):
                    if win_hand.count(win_hand[i]) == 2 and eyes.count(win_hand[i]) == 0:
                        eyes.append(win_hand[i])

                if len(eyes) == 0:
                    continue

                for eye in eyes:
                    win_hand = ting_hand.copy()
                    win_hand.append(j)
                    win_hand.sort()
                    win_hand.remove(eye)
                    win_hand.remove(eye)
                    
                    while True:
                        # Ting
                        if len(win_hand) == 0:
                            if ting_tile not in self.ting_tiles:
                                self.ting_tiles.append(ting_tile)
                                # return True
                                break
                            break
                        # The first tile in hand
                        i = win_hand[0]
                        # Remove Pong first
                        if win_hand.count(i) >= 3:
                            win_hand.remove(i)
                            win_hand.remove(i)
                            win_hand.remove(i)
                            continue
                        
                        if ALL_TILES.index(i) > 26: # 字牌
                            break
                        
                        tile_index, tile_type = self.deck.find_tile_type_index(i)

                        # Check Chow (start from 1 to 7, e.g. "'1'23", "'5'67")
                        if tile_type.index(i) < 7:

                            chow_set = tile_type[tile_index:tile_index+3]

                            # Remove Chow
                            if win_hand.count(chow_set[1]) != 0 and win_hand.count(chow_set[2]) != 0:
                                for tile in chow_set:
                                    win_hand.remove(tile)
                                continue
                        # This tile isn't able to form a set.
                        break
        if len(self.ting_tiles) != 0:
            return True
        else:
            return False
        
    def do_ting(self, tile_index):
        discard_tile = self.do_discard(tile_index)
        return discard_tile

    def check_jia_kong(self, tile):
        count_open_hand = self.open_hand.count(tile)
        if count_open_hand == 3:
            self.jia_kong_tile = tile
            return True
        return False

    def do_jia_kong(self):
        tile = self.jia_kong_tile
        hand = self.hand
        hand.remove(tile)
        self.open_hand.append(tile)
        self.jia_kong_tile = ""
        return True

    def check_an_kong(self):
        hand = self.hand
        for i in range(len(hand)-3):
            tile = hand[i]            
            count_hand = hand.count(tile)
            if count_hand == 4:
                self.an_kong_tile = tile
                return True
        return False

    def do_an_kong(self):
        tile = self.an_kong_tile
        hand = self.hand
        for i in range(4):
            # remove tiles from player's hand
            hand.remove(tile)
        for i in range(4):
            # append Kong tiles to the player's open hand
            self.open_hand.append(tile)
        self.an_kong_tile = ""
        return True

    def check_discard(self):
        self.hand.sort()
        return True

    def do_discard(self, tile_index):
        hand = self.hand
        discard_tile = hand[tile_index]
        hand.remove(discard_tile)
        self.discard_hand.append(discard_tile)
        # self.discard_tile = discard_tile
        return discard_tile

    def check_kong(self, tile):
        
        self.kong_tile = ""
        hand = self.hand
        # calculate the number of the same tile
        count_hand = hand.count(tile)

        if count_hand == 3:
            self.kong_tile = tile
            self.decision_types["kong"] = 1
            return True
        self.decision_types["kong"] = 0
        return False
                
    def do_kong(self):
        tile = self.kong_tile
        hand = self.hand
        for i in range(3):
                # remove tiles from player's hand
            hand.remove(tile)
        for i in range(4):
                # append Kong tiles to the player's open hand
            self.open_hand.append(tile)
        return True

    def check_pong(self, tile):
        hand = self.hand
        # calculate the number of the same tile
        count_hand = hand.count(tile)
        if count_hand >= 2:
            self.pong_tile = tile
            self.decision_types["pong"] = 1
            return True
        self.decision_types["pong"] = 0
        return False

    def do_pong(self):
        tile = self.pong_tile
        hand = self.hand
        # remove tiles from player's hand
        for i in range(2):
            hand.remove(tile)
        # append Pong tiles to the player's open hand
        for i in range(3):
            self.open_hand.append(tile)
        return True

    def check_chow(self, tile):
        hand = self.hand.copy()
        hand.append(tile)
        Chow_sets = []  # 紀錄可以吃的組合
        tile_type = []  # 哪種牌(萬or條or餅)

        tile_index, tile_type = self.deck.find_tile_type_index(tile)

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
                can_Chow = True # 應該不用
                if tile_index-i+j >= 0 and tile_index-i+j <= 8:
                    if tile_type[tile_index-i+j] in hand:
                        Chow_set.append(tile_type[tile_index-i+j])
                    else: # 應該不用
                        can_Chow = False # 應該不用
                else: # 應該不用
                    can_Chow = False # 應該不用

                if not can_Chow: # 應該不用
                    Chow_set = [] # 應該不用
                    break # 應該不用
            
            # 有可以吃的組合
            if len(Chow_set) > 0:
                # 將可以吃的組合放入Chow sets
                if tile in Chow_set:
                    Chow_sets.append(Chow_set)

        # 用來做決定的list [吃左, 吃中, 吃右]
        self.chow_sets = [[], [], []]

        for i in range(len(Chow_sets)):
            index = Chow_sets[i].index(tile)           
            self.chow_sets[index] = Chow_sets[i]

        if len(Chow_sets) > 0:
            self.decision_types["chow"] = 1
            return True
        self.decision_types["chow"] = 0
        return False

    def do_chow(self, decision):
            # do chow
            # player chooses Chow
        hand = self.hand
        if decision in [2, 3, 4]:
            # 2, 3, 4 -> == [] -> invalid -> redecision
            for i in range(3):
                chow_tile = self.chow_sets[decision-2][i]
                self.open_hand.append(chow_tile) # Append Chow set into the player's open hand
                if i != decision-2:
                    hand.remove(chow_tile)
            if decision == 2:
                temp = self.open_hand[-2]
                self.open_hand[-2] = self.open_hand[-3]
                self.open_hand[-3] = temp
            elif decision == 4:
                temp = self.open_hand[-2]
                self.open_hand[-2] = self.open_hand[-1]
                self.open_hand[-1] = temp
            return True
        return False
    
    def ask_kong_pong_chow(self, tile):
        pass