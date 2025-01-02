from deck import Deck
from player import Player
from human_player import Human_Player
from AI_player import AI_Player

class Majhong:
    def __init__(self, human_player_num):
        self.human_player_num = human_player_num
        self.deck = Deck()
        self.players = []

        for i in range(human_player_num):
            self.players.append(Human_Player())
        
        for i in range(4 - human_player_num):
            self.players.append(AI_Player())
        
        self.draw = True
        self.win = False
        self.jia_kong = False
        self.an_kong = False
        # self.discard_tile = ""
        self.last_player = 0
        self.next_player = 0
        # for pygame update
        self.update_count = 0
        self.ready = False

    def initialize(self):
        self.deck.shuffle()
        # self.deck.print_tiles() # 之後刪掉
        self.deal()
        for i in self.players:
            i.hand.sort()

    # 發牌
    def deal(self):
        for i in range(16):
            for i in range(4):
                self.players[i].draw(self.deck.draw())

    # 顯示剩餘牌庫
    def show_deck(self):
        self.deck.print_tiles()

    # 顯示玩家手牌
    def show_hand(self, player):
        print(f"player{player+1}: ")
        self.players[player].show_hand()

    # 顯示所有玩家手牌
    def show_hands(self):
        for i in range(4):
            self.show_hand(i)

    def liu_ju(self):
        if self.deck.number_tile_left_in_deck() <= 8:
            return True
        else:
            return False
        
    # 吃碰槓決定之字串處理
    def split_result(self, player_num):
        num = 0
        result = self.players[player_num].decision_results
        result_split = result.split()
        decision = result_split[0]
        if len(result_split) == 2:
            num = int(result_split[1])
        return decision, num

    def check_other_player_move(self, tile):
        for i in self.players:
            i.hand.sort()
        # 看要不要do_win和do_fang_qiang，用來顯示結束遊戲的牌型和誰放槍，還沒寫別人放槍要不要胡
        for player_num in range(len(self.players)):
            self.players[player_num].check_fang_qiang(tile)
            if self.players[player_num].win_move == True:
                self.receive(player_num)
                if self.players[player_num].win_or_not == True:
                    self.players[player_num].hand.append(tile)
                    self.players[player_num].hand.sort()
                    self.players[self.last_player].discard_hand.pop()
                    self.win = True
                    return True
            
        # check
        for player_num in range(len(self.players)):
            # initial the permission of decision types
            for key in self.players[player_num].decision_types:
                self.players[player_num].decision_types[key] = 0
            if player_num != self.last_player and self.players[player_num].ting_or_not == False:
                if player_num != (self.last_player+1)%4:
                    self.players[player_num].check_kong(tile)
                self.players[player_num].check_pong(tile)
        if self.players[(self.last_player+1)%4].ting_or_not == False:
            self.players[(self.last_player+1)%4].check_chow(tile)
        
        # ask
        for player_num in range(len(self.players)):
            if self.players[player_num].decision_types["kong"] or self.players[player_num].decision_types["pong"] or self.players[player_num].decision_types["chow"]:
                self.players[player_num].ask_kong_pong_chow(tile)

        # do
        for player_num in range(len(self.players)):
            if self.players[player_num].decision_types["kong"]:
            # if self.players[player_num].decision_results != "":
                decision, num = self.split_result(player_num)
                if decision == "kong":
                    self.players[self.last_player].discard_hand.pop() # 丟的牌被槓->把她從discard hand刪掉
                    self.players[player_num].do_kong()
                    self.next_player = player_num
                    return True
        for player_num in range(len(self.players)):
            if self.players[player_num].decision_types["pong"]:
                decision, num = self.split_result(player_num)
                if decision == "pong":
                    self.draw = False
                    self.players[self.last_player].discard_hand.pop() # 丟的牌被碰->把她從discard hand刪掉
                    self.players[player_num].do_pong()
                    self.next_player = player_num
                    return True
        if self.players[(self.last_player+1)%4].decision_types["chow"]:
            decision, num = self.split_result((self.last_player+1)%4)
            if decision == "chow":
                self.draw = False
                self.players[self.last_player].discard_hand.pop() # 丟的牌被吃->把她從discard hand刪掉
                self.players[(self.last_player+1)%4].do_chow(num)
                self.next_player = (self.last_player+1)%4
                return True
        return True

        # for player_num in range(len(self.players)):
        #     if player_num != self.last_player and player_num != (self.last_player+1)%4 and self.players[player_num].ting_or_not == False:
        #         kong = self.players[player_num].check_kong(tile)
        #         if kong == True:
        #             self.receive(player_num)
        #             # self.next_player = player_num
        #             # self.draw = False
        #             return True
        # for player_num in range(len(self.players)):
        #     if player_num != self.last_player and self.players[player_num].ting_or_not == False:
        #         pong = self.players[player_num].check_pong(tile)
        #         if pong == True:
        #             self.receive(player_num)
        #             # self.next_player = player_num
        #             # self.draw = False
        #             return True
        # if self.players[(self.last_player+1)%4].ting_or_not == False:
        #     chow = self.players[(self.last_player+1)%4].check_chow(tile)
        #     if chow == True:
        #         self.receive((self.last_player+1)%4)
        #         # self.next_player = (self.last_player+1)%4
        #         # self.draw = False
        #         return True

    def player_turn(self):
        # 空值是為了沒有摸牌有東西放check jia an kong
        self.players[self.next_player].draw_tile = ''
        if self.draw == True:
            self.players[self.next_player].draw_tile = self.players[self.next_player].draw(self.deck.draw())
        self.draw = True
        self.last_player = self.next_player
        self.next_player = (self.next_player+1)%4
        self.players[self.last_player].hand.sort()
        # 改self.win成self.win_move
        self.players[self.last_player].check_win()
        if self.players[self.last_player].win_move == True:
            self.receive(self.last_player)
            if self.players[self.last_player].win_or_not == True:
                self.win = True
                return True
        if self.players[self.last_player].ting_or_not == False:
            # next_player有問題改成last_player
            self.jia_kong = self.players[self.last_player].check_jia_kong(self.players[self.last_player].draw_tile)
            if self.jia_kong == True:
                self.receive(self.last_player)
                if self.players[self.last_player].jia_kong_or_not == True:
                    self.players[self.last_player].jia_kong_or_not = False
                    self.next_player = self.last_player
                    return True
            self.an_kong = self.players[self.last_player].check_an_kong()
            if self.an_kong == True:
                self.receive(self.last_player)
                if self.players[self.last_player].an_kong_or_not == True:
                    self.players[self.last_player].an_kong_or_not = False
                    self.next_player = self.last_player
                    return True
            ting = self.players[self.last_player].check_ting()
            if ting == True:
                self.receive(self.last_player)
                if self.players[self.last_player].ting_or_not == True:
                    return True
                else:
                    self.players[self.last_player].check_discard()
                    self.receive(self.last_player)
            else:
                self.players[self.last_player].check_discard()
                self.receive(self.last_player)
            return True
        else:
            self.players[self.last_player].check_discard()
            self.receive(self.last_player)
            return True
    
    def receive(self, p):
        i=0
        while not self.players[p].receive_or_not:
            i+=1
        self.players[p].receive_or_not = False


# majhong = Majhong(4)
# majhong.initialize()
# while majhong.win != True:
#     majhong.player_turn()
#     if majhong.win == True:
#         break
#     if majhong.jia_kong == True:
#         majhong.jia_kong = False
#         continue
#     if majhong.an_kong == True:
#         majhong.an_kong = False
#         continue
#     majhong.check_other_player_move(majhong.discard_tile)

# print(f"Player {majhong.last_player} win!!!")
# print("exit")
# exit()