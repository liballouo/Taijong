from deck import Deck
from human_player import Human_Player
from AI_player import AI_Player
# from .deck import Deck
# from .human_player import Human_Player
# from .AI_player import AI_Player

class Majhong:
    def __init__(self, human_player_num):
        self.human_player_num = human_player_num
        self.deck = Deck()
        self.players = []

        # 依照指定人類玩家人數加入人類/AI玩家
        for _ in range(human_player_num):
            self.players.append(Human_Player())
        
        for _ in range(4 - human_player_num):
            self.players.append(AI_Player())
        
        # 初始化參數
        self.draw = True
        self.win = False
        self.jia_kong = False
        self.an_kong = False
        self.last_player = 0
        self.next_player = 0
        # for pygame update
        self.update_count = 0
        self.ready = False

    # 發牌
    def deal(self):
        for i in range(16):
            for i in range(4):
                self.players[i].draw(self.deck.draw())
    
    # 初始化遊戲: 洗牌 -> 發牌
    def initialize(self):
        # 洗牌
        self.deck.shuffle()
        # 發牌
        self.deal()
        for i in self.players:
            # 整理手牌
            i.hand.sort()

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

    # 是否流局判斷
    def liu_ju(self):
        # 供牌小於等於8張，即流局
        if self.deck.number_tile_left_in_deck() <= 8:
            return True
        else:
            return False
        
    # 吃碰槓決定之字串處理
    def split_result(self, player_num):
        num = 0
        # decision_results: e.g. "pong 1"
        result = self.players[player_num].decision_results
        result_split = result.split()
        decision = result_split[0]
        if len(result_split) == 2:
            num = int(result_split[1])
        return decision, num

    def check_other_player_move(self, tile):
        # 整理每個玩家的手牌
        for i in self.players:
            i.hand.sort()
        # 看要不要do_win和do_fang_qiang，用來顯示結束遊戲的牌型和誰放槍，還沒寫別人放槍要不要胡
        for player_num in range(len(self.players)):
            self.players[player_num].check_fang_qiang(tile)
            # 某玩家選擇贏
            if self.players[player_num].win_move == True:
                self.receive(player_num)
                if self.players[player_num].win_or_not == True:
                    self.players[player_num].hand.append(tile)
                    self.players[player_num].hand.sort()
                    self.players[self.last_player].discard_hand.pop()
                    self.win = True
                    return True
            
        # 檢查
        for player_num in range(len(self.players)):
            # initial the permission of decision types
            for key in self.players[player_num].decision_types:
                self.players[player_num].decision_types[key] = 0
            # 檢查聽牌，若無 -> 槓 -> 碰
            if player_num != self.last_player and self.players[player_num].ting_or_not == False:
                if player_num != (self.last_player+1)%4:
                    self.players[player_num].check_kong(tile)
                self.players[player_num].check_pong(tile)
        # 檢察廳牌，若無 -> 吃
        if self.players[(self.last_player+1)%4].ting_or_not == False:
            self.players[(self.last_player+1)%4].check_chow(tile)
        
        # 詢問玩家是否要進行 槓/碰/吃
        for player_num in range(len(self.players)):
            if self.players[player_num].decision_types["kong"] or self.players[player_num].decision_types["pong"] or self.players[player_num].decision_types["chow"]:
                self.players[player_num].ask_kong_pong_chow(tile)

        # 玩家選擇 
        # 槓
        for player_num in range(len(self.players)):
            if self.players[player_num].decision_types["kong"]:
                decision, num = self.split_result(player_num)
                if decision == "kong":
                    self.players[self.last_player].discard_hand.pop() # 丟的牌被槓 -> 把它從discard hand刪掉
                    self.players[player_num].do_kong()
                    self.next_player = player_num
                    return True
        # 碰
        for player_num in range(len(self.players)):
            if self.players[player_num].decision_types["pong"]:
                decision, num = self.split_result(player_num)
                if decision == "pong":
                    self.draw = False
                    self.players[self.last_player].discard_hand.pop() # 丟的牌被碰->把她從discard hand刪掉
                    self.players[player_num].do_pong()
                    self.next_player = player_num
                    return True
        # 吃
        if self.players[(self.last_player+1)%4].decision_types["chow"]:
            decision, num = self.split_result((self.last_player+1)%4)
            if decision == "chow":
                self.draw = False
                self.players[self.last_player].discard_hand.pop() # 丟的牌被吃->把她從discard hand刪掉
                self.players[(self.last_player+1)%4].do_chow(num)
                self.next_player = (self.last_player+1)%4
                return True
        return True

    def player_turn(self):
        """處理玩家回合"""
        self._prepare_player_turn()
        
        if self._handle_win_check():
            return True
            
        if not self.players[self.last_player].ting_or_not:
            if self._handle_kong_actions():
                return True
                
            if self._handle_ting():
                return True
        
        self._handle_discard()
        return True

    def _prepare_player_turn(self):
        """準備玩家回合"""
        self.players[self.next_player].draw_tile = '' # 空值是為了沒有摸牌有東西放check jia/an kong
        if self.draw:
            self.players[self.next_player].draw_tile = self._draw_new_tile()
        self.draw = True
        self.last_player = self.next_player
        self.next_player = (self.next_player + 1) % 4
        self.players[self.last_player].hand.sort()

    def _draw_new_tile(self):
        """從牌堆抽一張新牌"""
        return self.players[self.next_player].draw(self.deck.draw())

    def _handle_win_check(self):
        """處理玩家胡牌檢查"""
        self.players[self.last_player].check_win()
        if self.players[self.last_player].win_move:
            self.receive(self.last_player)
            if self.players[self.last_player].win_or_not:
                self.win = True
                return True
        return False

    def _handle_kong_actions(self):
        """處理槓牌相關動作"""
        # 處理加槓
        if self._handle_jia_kong():
            return True
            
        # 處理暗槓
        if self._handle_an_kong():
            return True
            
        return False

    def _handle_jia_kong(self):
        """處理加槓"""
        self.jia_kong = self.players[self.last_player].check_jia_kong(
            self.players[self.last_player].draw_tile
        )
        if self.jia_kong:
            self.receive(self.last_player)
            if self.players[self.last_player].jia_kong_or_not:
                self.players[self.last_player].jia_kong_or_not = False
                self.next_player = self.last_player
                return True
        return False

    def _handle_an_kong(self):
        """處理暗槓"""
        self.an_kong = self.players[self.last_player].check_an_kong()
        if self.an_kong:
            self.receive(self.last_player)
            if self.players[self.last_player].an_kong_or_not:
                self.players[self.last_player].an_kong_or_not = False
                self.next_player = self.last_player
                return True
        return False

    def _handle_ting(self):
        """處理聽牌"""
        ting = self.players[self.last_player].check_ting()
        if ting:
            self.receive(self.last_player)
            if self.players[self.last_player].ting_or_not:
                return True
            self._handle_normal_discard()
        return False

    def _handle_discard(self):
        """處理一般打牌"""
        if not self.players[self.last_player].ting_or_not:
            self.players[self.last_player].check_discard()
        else:
            self.players[self.last_player].check_discard()
        self.receive(self.last_player)
    
    def receive(self, p):
        i=0
        while not self.players[p].receive_or_not:
            i+=1
        self.players[p].receive_or_not = False
