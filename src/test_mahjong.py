import sys
import os
# 將專案根目錄加入系統路徑
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from main.mahjong import Majhong
from main.tile import ALL_TILES
from main.human_player import Human_Player
from main.AI_player import AI_Player

class TestMajhong(unittest.TestCase):
    def setUp(self):
        # 創建一個包含1個人類玩家的遊戲
        self.game = Majhong(1)
        # 初始化遊戲
        self.game.initialize()

    def test_initialization(self):
        """測試遊戲初始化"""
        # 總人數應為4
        self.assertEqual(len(self.game.players), 4)
        # 分別為人類, AI, AI, AI玩家
        self.assertIsInstance(self.game.players[0], Human_Player)
        self.assertIsInstance(self.game.players[1], AI_Player)
        self.assertIsInstance(self.game.players[2], AI_Player)
        self.assertIsInstance(self.game.players[3], AI_Player)
        # 針對初始化參數的判斷
        self.assertTrue(self.game.draw)
        self.assertFalse(self.game.win)
        self.assertFalse(self.game.jia_kong)
        self.assertFalse(self.game.an_kong)
        self.assertFalse(self.game.ready)
        
    def test_player_count(self):
        """測試玩家數量改變"""
        # 創建一個包含4個人類玩家的遊戲
        game_4_human = Majhong(4)
        # 總人數應為4
        self.assertEqual(len(game_4_human.players), 4)
        # 皆為人類玩家
        self.assertTrue(all(isinstance(p, Human_Player) for p in game_4_human.players))

        # 創建一個包含2個人類玩家的遊戲
        game_2_human = Majhong(2)
        # 總人數應為4
        self.assertEqual(len(game_2_human.players), 4)
        # 分別為人類, 人類, AI, AI玩家
        self.assertTrue(isinstance(game_2_human.players[0], Human_Player))
        self.assertTrue(isinstance(game_2_human.players[1], Human_Player))
        self.assertTrue(isinstance(game_2_human.players[2], AI_Player))
        self.assertTrue(isinstance(game_2_human.players[3], AI_Player))

    def test_deal(self):
        """測試發牌功能"""
        for player in self.game.players:
            # 每一個玩家應該要有16張手牌
            self.assertEqual(len(player.hand), 16)  

    def test_liu_ju(self):
        """測試流局判定"""
        # 初始狀態下不會流局
        self.assertFalse(self.game.liu_ju())
        
        # 模擬牌庫只剩下8張
        self.game.deck.tiles = self.game.deck.tiles[:8]
        # 應要流局
        self.assertTrue(self.game.liu_ju())

    def test_split_result(self):
        """測試決策的字串結果分割是否正確"""
        self.game.players[0].decision_results = "pong 1"
        decision, num = self.game.split_result(0)
        self.assertEqual(decision, "pong")
        self.assertEqual(num, 1)

    def test_draw(self):
        """測試抽牌功能"""
        # 設置玩家手牌
        player = self.game.players[0]
        player.hand = [
            '萬1', '萬1'
        ]
        
        player.draw('萬9')
        self.assertEqual(['萬1', '萬1', '萬9'], player.hand)

    def test_pong(self):
        """測試碰牌判定"""
        # 設置玩家手牌
        player = self.game.players[0]
        player.hand = [
            '萬1', '萬1', '條5', '條6'
        ]
        
        # 測試可以碰
        discard_tile = '萬1'
        self.assertTrue(player.check_pong(discard_tile))
        
        # 測試不能碰
        discard_tile = '萬2'
        self.assertFalse(player.check_pong(discard_tile))

    def test_check_chow(self):
        """測試吃牌判定"""
        player = self.game.players[0]
        player.hand = [
            '萬1', '萬2', '條5', '條6'
        ]
        
        # 測試可以吃
        discard_tile = '萬3'
        self.assertTrue(player.check_chow(discard_tile))
        
        # 測試不能吃
        discard_tile = '萬4'
        self.assertFalse(player.check_chow(discard_tile))

    def test_check_kong(self):
        """測試槓牌判定"""
        player = self.game.players[0]
        player.hand = [
            '萬1', '萬1', '萬1'
        ]
        
        # 測試暗槓
        # 無法暗槓
        self.assertFalse(player.check_an_kong())
        # 可以暗槓
        player.hand.append('萬1')
        self.assertTrue(player.check_an_kong())
        
        # 測試加槓
        # 無法加槓
        player.open_hand = ['條5', '條5', '條5']
        self.assertFalse(player.check_jia_kong('條6'))
        # 可以加槓
        self.assertTrue(player.check_jia_kong('條5'))

    def test_check_ting(self):
        """測試聽牌判定"""
        player = self.game.players[0]
        # 設置一個(打掉其中一張後)可以聽牌的手牌組合
        player.hand = [
            '萬1', '萬1', '萬1', '萬2', '萬3', '萬4', 
            '條2', '條2', '條2','餅5', '餅5', '餅9', 'E', 'E'
        ]
        
        self.assertTrue(player.check_ting())
        
        # 設置一個(打掉其中一張後)無法聽牌的手牌組合
        player.hand = [
            '萬1', '萬1', '萬1', '萬2', '萬3', '萬4', 
            '條2', '條2', '條2','餅1', '餅5', '餅9', 'E', 'E'
        ]
        
        self.assertFalse(player.check_ting())
        

    def test_check_win(self):
        """測試胡牌判定"""
        player = self.game.players[0]
        # 設置一個可以胡牌的手牌組合
        player.hand = [
            '萬1', '萬1', '萬1', '萬2', '萬3', '萬4', 
            '條2', '條2', '條2','餅5', '餅5', '餅5', 'E', 'E'
        ]
        
        self.assertTrue(player.check_win())
    
if __name__ == '__main__':
    unittest.main()