from tile import *
from deck import Deck
# from .tile import *
# from .deck import Deck

from dataclasses import dataclass, field
from typing import List, Dict
from enum import Enum

class ActionType(Enum):
    """動作類型列舉"""
    KONG = "kong"
    PONG = "pong"
    CHOW = "chow"

@dataclass
class Player:
    # 玩家相關
    deck: Deck = field(default_factory=Deck)
    hand: List[str] = field(default_factory=list)
    open_hand: List[str] = field(default_factory=list)
    discard_hand: List[str] = field(default_factory=list)
    player_number: int = 0
    draw_tile: str = ""
    decision_types: Dict[str, int] = field(default_factory=lambda: {t.value: 0 for t in ActionType})
    
    # 狀態相關屬性
    win_or_not: bool = False
    jia_kong_or_not: bool = False
    an_kong_or_not: bool = False
    ting_or_not: bool = False
    win_move: bool = False
    receive_or_not: bool = False
    
    # 動作相關屬性
    jia_kong_tile: str = ""
    an_kong_tile: str = ""
    discard_tile: str = ""
    kong_tile: str = ""
    pong_tile: str = ""
    chow_sets: List[List[str]] = field(default_factory=list)
    ting_tiles: List[str] = field(default_factory=list)
    decision_results: str = ""    
        
    def draw(self, tile):
        self.hand.append(tile)
        return tile

    def show_hand(self):
        for i in range(len(self.hand)):
            print(f"({i+1}){self.hand[i]}", end = " ")

    def check_win(self) -> bool:
        """檢查是否胡牌"""
        return self._check_win_with_hand(self.hand.copy())

    def check_fang_qiang(self, discard_tile: str) -> bool:
        """檢查是否可以放槍胡"""
        test_hand = self.hand.copy()
        test_hand.append(discard_tile)
        return self._check_win_with_hand(test_hand)

    def _check_win_with_hand(self, hand: List[str]) -> bool:
        """檢查指定手牌是否可以胡牌"""
        hand.sort()
        eyes = self._find_possible_eyes(hand)
        
        if not eyes:
            return False

        return any(self._can_win_with_eye(hand.copy(), eye) for eye in eyes)

    def _find_possible_eyes(self, hand: List[str]) -> List[str]:
        """找出所有可能的對子"""
        eyes = []
        for i in range(len(hand) - 1):
            current_tile = hand[i]
            if (hand.count(current_tile) >= 2 and 
                current_tile not in eyes):
                eyes.append(current_tile)
        return eyes

    def _can_win_with_eye(self, hand: List[str], eye: str) -> bool:
        """使用指定對子檢查是否可以胡牌"""
        # 移除對子
        hand.remove(eye)
        hand.remove(eye)
        
        while hand:
            if not self._try_remove_set(hand):
                return False
        return True

    def _try_remove_set(self, hand: List[str]) -> bool:
        """嘗試從手牌中移除一組順子或刻子"""
        if not hand:
            return True
            
        first_tile = hand[0]
        
        # 嘗試移除刻子
        if self._try_remove_pung(hand, first_tile):
            return True
            
        # 字牌只能組成刻子
        if self._is_honor_tile(first_tile):
            return False
            
        # 嘗試移除順子
        return self._try_remove_chow(hand, first_tile)

    def _try_remove_pung(self, hand: List[str], tile: str) -> bool:
        """嘗試移除刻子"""
        if hand.count(tile) >= 3:
            for _ in range(3):
                hand.remove(tile)
            return True
        return False

    def _try_remove_chow(self, hand: List[str], first_tile: str) -> bool:
        """嘗試移除順子"""
        tile_index, tile_type = self.deck.find_tile_type_index(first_tile)
        
        if tile_type.index(first_tile) >= 7:  # 不能組成順子
            return False
            
        chow_set = tile_type[tile_index:tile_index+3]
        if self._can_form_chow(hand, chow_set):
            self._remove_chow(hand, chow_set)
            return True
        return False

    def _can_form_chow(self, hand: List[str], chow_set: List[str]) -> bool:
        """檢查是否能夠形成順子"""
        return all(tile in hand for tile in chow_set)

    def _remove_chow(self, hand: List[str], chow_set: List[str]) -> None:
        """從手牌中移除順子"""
        for tile in chow_set:
            hand.remove(tile)

    def _is_honor_tile(self, tile: str) -> bool:
        """判斷是否為字牌"""
        return ALL_TILES.index(tile) > 26
    
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
        for _ in range(4):
            # remove tiles from player's hand
            hand.remove(tile)
        for _ in range(4):
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