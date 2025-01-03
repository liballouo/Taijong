from tile import *
# from deck import Deck
from player import Player

class Human_Player(Player):
    def __init__(self):
        super().__init__()
        self.win_move = False
        self.ting_move = False
        self.jia_kong_move = False
        self.an_kong_move = False
        self.discard_move = False
        self.ask_move = False # 觸發client問吃碰槓
        # self.kong_move = False
        # self.pong_move = False
        # self.chow_move = False
        self.receive_or_not = False

    def draw(self, tile):
        return super().draw(tile)
    
    def show_hand(self):
        return super().show_hand()

    def check_win(self):
        self.win_move = super().check_win()
        return self.win_move
    
    def check_fang_qiang(self, discard_tile):
        self.win_move = super().check_fang_qiang(discard_tile)
        return self.win_move
    
    def check_ting(self):
        self.ting_move = super().check_ting()
        return self.ting_move
    
    def do_ting(self, tile_index):
        discard_tile = super().do_ting(tile_index)
        self.ting_move = False
        return discard_tile

    def check_jia_kong(self, tile):
        self.jia_kong_move = super().check_jia_kong(tile)
        return self.jia_kong_move
    
    def do_jia_kong(self):
        super().do_jia_kong()
        self.jia_kong_move = False
        return

    def check_an_kong(self):
        self.an_kong_move = super().check_an_kong()
        return self.an_kong_move

    def do_an_kong(self):
        super().do_an_kong()
        self.an_kong_move = False
        return

    def check_discard(self):
        self.discard_move = super().check_discard()
        return

    def do_discard(self, tile_index):
        discard_tile = super().do_discard(tile_index)
        self.discard_move = False
        return discard_tile

    def check_kong(self, tile):
        return super().check_kong(tile)
        self.decision_types["kong"] = int(super().check_kong(tile))
        return True
        # self.kong_move = super().check_kong(tile)
        # return self.kong_move

    def do_kong(self):
        super().do_kong()
        # self.kong_move = False
        return
    
    def check_pong(self, tile):
        return super().check_pong(tile)
        self.decision_types["pong"] = int(super().check_pong(tile))
        return True
        # self.pong_move = super().check_pong(tile)
        # return self.pong_move

    def do_pong(self):
        super().do_pong()
        # self.pong_move = False
        return

    def check_chow(self, tile):
        return super().check_chow(tile)
        self.decision_types["chow"] = int(super().check_chow(tile))
        return True
        # self.chow_move = super().check_chow(tile)
        # return self.chow_move
    
    def do_chow(self, decision):
        super().do_chow(decision)
        # self.chow_move = False
        return

    def ask_kong_pong_chow(self, tile):
        super().ask_kong_pong_chow(tile)
        self.ask_move = True
        self.receive()
        return

    def receive(self):
        i=0
        while not self.receive_or_not:
            i+=1
        self.receive_or_not = False