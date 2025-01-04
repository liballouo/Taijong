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
        """檢查其他玩家對於當前打出的牌的反應"""
        self._sort_all_players_hands()
        
        if self._check_win_reaction(tile):
            return True
            
        self._reset_and_check_actions(tile)
        return self._handle_player_decisions(tile)

    def _sort_all_players_hands(self):
        """整理所有玩家手牌"""
        for player in self.players:
            player.hand.sort()

    def _check_win_reaction(self, tile):
        """檢查是否有玩家可以胡牌"""
        for player_num, player in enumerate(self.players):
            if self._handle_player_win(player_num, player, tile):
                return True
        return False

    def _handle_player_win(self, player_num, player, tile):
        """處理玩家胡牌"""
        player.check_fang_qiang(tile)
        if player.win_move:
            self.receive(player_num)
            if player.win_or_not:
                self._process_win(player, tile)
                return True
        return False

    def _process_win(self, player, tile):
        """處理勝利相關操作"""
        player.hand.append(tile)
        player.hand.sort()
        self.players[self.last_player].discard_hand.pop()
        self.win = True

    def _reset_and_check_actions(self, tile):
        """重置並檢查可能的動作"""
        for player_num, player in enumerate(self.players):
            self._reset_decision_types(player)
            if player_num != self.last_player and not player.ting_or_not:
                self._check_player_actions(player_num, player, tile)

        # 檢查下家是否可以吃牌
        next_player = self.players[(self.last_player+1)%4]
        if not next_player.ting_or_not:
            next_player.check_chow(tile)

    def _reset_decision_types(self, player):
        """重置玩家的決策類型"""
        for key in player.decision_types:
            player.decision_types[key] = 0

    def _check_player_actions(self, player_num, player, tile):
        """檢查玩家可能的動作"""
        if player_num != (self.last_player+1)%4:
            player.check_kong(tile)
        player.check_pong(tile)

    def _handle_player_decisions(self, tile):
        """處理玩家的決策"""
        self._ask_players_for_decisions(tile)
        
        if self._handle_kong_decision():
            return True
            
        if self._handle_pong_decision():
            return True
            
        if self._handle_chow_decision():
            return True
            
        return True

    def _ask_players_for_decisions(self, tile):
        """詢問玩家是否要進行動作"""
        for player in self.players:
            if any(player.decision_types[action] for action in ["kong", "pong", "chow"]):
                player.ask_kong_pong_chow(tile)

    def _handle_kong_decision(self):
        """處理槓牌決策"""
        for player_num, player in enumerate(self.players):
            if player.decision_types["kong"]:
                decision, _ = self.split_result(player_num)
                if decision == "kong":
                    self._process_kong(player_num, player)
                    return True
        return False

    def _process_kong(self, player_num, player):
        """處理槓牌操作"""
        self.players[self.last_player].discard_hand.pop()
        player.do_kong()
        self.next_player = player_num

    def _handle_pong_decision(self):
        """處理碰牌決策"""
        for player_num, player in enumerate(self.players):
            if player.decision_types["pong"]:
                decision, _ = self.split_result(player_num)
                if decision == "pong":
                    self._process_pong(player_num, player)
                    return True
        return False

    def _process_pong(self, player_num, player):
        """處理碰牌操作"""
        self.draw = False
        self.players[self.last_player].discard_hand.pop()
        player.do_pong()
        self.next_player = player_num

    def _handle_chow_decision(self):
        """處理吃牌決策"""
        next_player = self.players[(self.last_player+1)%4]
        if next_player.decision_types["chow"]:
            decision, num = self.split_result((self.last_player+1)%4)
            if decision == "chow":
                self._process_chow(next_player, num)
                return True
        return False

    def _process_chow(self, player, num):
        """處理吃牌操作"""
        self.draw = False
        self.players[self.last_player].discard_hand.pop()
        player.do_chow(num)
        self.next_player = (self.last_player+1)%4

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
