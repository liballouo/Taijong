import torch
import torch.nn as nn
from tile import *
from player import Player
from response import *
# from .tile import *
# from .player import Player
# from .response import *
import time

class AI_Player(Player):
    def __init__(self):
        super().__init__()
        #複製的
        self.win_move = False
        self.ting_move = False
        self.jia_kong_move = False
        self.an_kong_move = False
        self.discard_move = False
        self.ask_move = False 
        self.receive_or_not = True

        self.decision_points = {"kong": 0, "no_kong": 0, "pong": 0, "no_pong": 0, 
                                "no_chow": 0, "chow 2": 0, "chow 3": 0, "chow 4": 0,}

    def draw(self, tile):
        return super().draw(tile)
    
    def show_hand(self):
        return super().show_hand()
    
    def check_win(self):
        self.receive_or_not = True
        win = super().check_win()
        if win:
            self.win_move = True
            self.win_or_not = True
        return 
    
    def check_fang_qiang(self, discard_tile):
        self.receive_or_not = True
        win = super().check_fang_qiang(discard_tile)
        if win:
            self.win_move = True
            self.win_or_not = True
        return
    
    def check_ting(self):
        self.receive_or_not = True
        # decision = 1 永遠不聽
        return False
    
    # def do_ting(self, tile_index):
    #     return super().do_ting(tile_index)
    
    def check_jia_kong(self, tile):
        self.receive_or_not = True
        jia_kong = super().check_jia_kong(tile)
        if jia_kong:
            hand = self.hand.copy()
            for i in range(3):
                hand.append(tile)
            hand_tiles = self.deck.tile_to_list(hand)
            throw = self.deck.tile_to_list([tile])
            points = Kong(throw, hand_tiles)
            if points[0][1] > points[0][0]:
                self.do_jia_kong()
        return 
    
    def do_jia_kong(self):
        # call the function in response.py
        # sleep for 2 seconds
        time.sleep(2)
        return super().do_jia_kong()
    
    #要寫AI判斷
    def check_an_kong(self):
        self.receive_or_not = True
        an_kong = super().check_an_kong()
        if an_kong:
            hand = self.hand.copy()
            hand.remove(self.an_kong_tile)
            hand_tiles = self.deck.tile_to_list(hand)
            throw = self.deck.tile_to_list([self.an_kong_tile])
            points = Kong(throw, hand_tiles)
            if points[0][1] > points[0][0]:
                self.do_an_kong()
        return 
    
    def do_an_kong(self):
        # call the function in response.py
        # sleep for 2 seconds
        time.sleep(2)
        return super().do_an_kong()
    
    def check_discard(self):
        self.receive_or_not = True
        self.do_discard()
        return super().check_discard()
    
    def do_discard(self):
        # call the function in response.py
        hand = self.hand
        print(f"player{self.player_number}: ", hand)
        hand_tiles = self.deck.tile_to_list(hand)
        tile = discard_tile(hand_tiles)
        tile = ALL_TILES[tile.indices]
        print(f"player{self.player_number}丟: ", tile)
        self.discard_tile = tile
        tile_index = hand.index(tile)

        # sleep for 2 seconds
        time.sleep(2)
        return super().do_discard(tile_index)
    
    def check_kong(self, tile):
        return super().check_kong(tile)
    
    def do_kong(self):
        # sleep for 2 seconds
        time.sleep(2)
        return super().do_kong()
    
    def check_pong(self, tile):
        return super().check_pong(tile)
    
    def do_pong(self):
        # sleep for 2 seconds
        time.sleep(2)
        return super().do_pong()
    
    def check_chow(self, tile):
        return super().check_chow(tile)
    
    def do_chow(self, decision):
        # sleep for 2 seconds
        time.sleep(2)
        return super().do_chow(decision)
    
    def ask_kong_pong_chow(self, tile):
        print(f"player{self.player_number}: ", tile)
        super().ask_kong_pong_chow(tile)
        for key in self.decision_points:
                self.decision_points[key] = 0
        hand = self.hand.copy()
        print(f"player{self.player_number}: ", hand)
        hand_tiles = self.deck.tile_to_list(hand)
        throw = self.deck.tile_to_list([tile])
        if self.decision_types["kong"]:
            points = Kong(throw, hand_tiles)
            self.decision_points["kong"] = points[0][1]
            self.decision_points["no_kong"] = points[0][0]
        if self.decision_types["pong"]:
            points = Pong(throw, hand_tiles)
            self.decision_points["pong"] = points[0][1]
            self.decision_points["no_pong"] = points[0][0]
        if self.decision_types["chow"]:
            points = Chow(throw, hand_tiles)
            self.decision_points["no_chow"] = points[0][0]
            self.decision_points["chow 2"] = points[0][1]
            self.decision_points["chow 3"] = points[0][2]
            self.decision_points["chow 4"] = points[0][3]
        result = max(self.decision_points, key=lambda k: self.decision_points[k])
        print(f"player{self.player_number}: ", result)
        # if result == "no_kong" or result == "no_pong" or result == "no_chow":
        #     result = "no_move"
        self.decision_results = result

        return
    
