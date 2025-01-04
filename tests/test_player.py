import unittest
from main.player import Player
from main.tile import ALL_TILES

class TestPlayer(unittest.TestCase):
    def setUp(self):
        """每個測試案例前執行"""
        self.player = Player()

    def test_initialization(self):
        """測試玩家初始化"""
        self.assertEqual(len(self.player.hand), 0)
        self.assertEqual(len(self.player.open_hand), 0)
        self.assertEqual(len(self.player.discard_hand), 0)
        self.assertEqual(self.player.draw_tile, "")
        self.assertEqual(self.player.jia_kong_tile, "")
        self.assertEqual(self.player.an_kong_tile, "")
        self.assertEqual(self.player.discard_tile, "")
        self.assertEqual(self.player.kong_tile, "")
        self.assertEqual(self.player.pong_tile, "")
        self.assertEqual(len(self.player.chow_sets), 0)
        self.assertEqual(len(self.player.ting_tiles), 0)
        self.assertFalse(self.player.win_or_not)
        self.assertFalse(self.player.jia_kong_or_not)
        self.assertFalse(self.player.an_kong_or_not)
        self.assertFalse(self.player.ting_or_not)

    def test_draw(self):
        """測試抽牌功能"""
        tile = "萬1"
        self.player.draw(tile)
        self.assertEqual(len(self.player.hand), 1)
        self.assertEqual(self.player.hand[0], tile)

    def test_check_win(self):
        """測試胡牌判定"""
        # 測試一個可以胡牌的手牌組合
        self.player.hand = [
            '萬1', '萬1', '萬1',  # 刻子
            '萬2', '萬3', '萬4',  # 順子
            '條2', '條2', '條2',  # 刻子
            '餅5', '餅5', '餅5',  # 刻子
            'E', 'E'             # 眼
        ]
        self.assertTrue(self.player.check_win())

        # 測試不能胡牌的手牌組合
        self.player.hand = [
            '萬1', '萬2', '萬3',
            '條1', '條2', '條3',
            '餅1', '餅2', '餅3',
            'E', 'S', 'W', 'N', 'C'
        ]
        self.assertFalse(self.player.check_win())

    def test_check_fang_qiang(self):
        """測試放槍胡牌判定"""
        # 測試可以放槍胡的情況
        self.player.hand = [
            '萬1', '萬1', '萬1',
            '萬2', '萬3', '萬4',
            '條2', '條2', '條2',
            '餅5', '餅5', '餅5',
            'E'
        ]
        self.assertTrue(self.player.check_fang_qiang('E'))

        # 測試不能放槍胡的情況
        self.assertFalse(self.player.check_fang_qiang('W'))

    def test_check_ting(self):
        """測試聽牌判定"""
        # 測試可以聽牌的情況
        self.player.hand = [
            '萬1', '萬1', '萬1',
            '萬2', '萬3', '萬4',
            '條2', '條2', '條2',
            '餅5', '餅5', '餅9',
            'E', 'E'
        ]
        self.assertTrue(self.player.check_ting())
        self.assertGreater(len(self.player.ting_tiles), 0)

        # 測試不能聽牌的情況
        self.player.hand = [
            '萬1', '萬2', '萬3',
            '條1', '條2', '條3',
            '餅1', '餅2', '餅3',
            'E', 'S', 'W', 'N', 'C'
        ]
        self.assertFalse(self.player.check_ting())
        self.assertEqual(len(self.player.ting_tiles), 0)

    def test_check_jia_kong(self):
        """測試加槓判定"""
        # 測試可以加槓的情況
        self.player.open_hand = ['條5', '條5', '條5']
        self.assertTrue(self.player.check_jia_kong('條5'))

        # 測試不能加槓的情況
        self.assertFalse(self.player.check_jia_kong('條6'))

    def test_check_an_kong(self):
        """測試暗槓判定"""
        # 測試可以暗槓的情況
        self.player.hand = ['萬1', '萬1', '萬1', '萬1']
        self.assertTrue(self.player.check_an_kong())
        
        # 測試不能暗槓的情況
        self.player.hand = ['萬1', '萬1', '萬1']
        self.assertFalse(self.player.check_an_kong())

    def test_check_kong(self):
        """測試槓牌判定"""
        # 測試可以槓的情況
        self.player.hand = ['萬1', '萬1', '萬1']
        self.assertTrue(self.player.check_kong('萬1'))

        # 測試不能槓的情況
        self.assertFalse(self.player.check_kong('萬2'))

    def test_check_pong(self):
        """測試碰牌判定"""
        # 測試可以碰的情況
        self.player.hand = ['萬1', '萬1']
        self.assertTrue(self.player.check_pong('萬1'))

        # 測試不能碰的情況
        self.assertFalse(self.player.check_pong('萬2'))

    def test_check_chow(self):
        """測試吃牌判定"""
        # 測試可以吃的情況
        self.player.hand = ['萬1', '萬2']
        self.assertTrue(self.player.check_chow('萬3'))
        # 吃(的牌在)右邊
        self.assertEqual(self.player.chow_sets[2], ['萬1', '萬2', '萬3'])

        # 測試不能吃的情況
        self.player.hand = ['萬1', '萬2']
        self.assertFalse(self.player.check_chow('萬4'))

    def test_do_discard(self):
        """測試打牌功能"""
        self.player.hand = ['萬1', '萬2', '萬3']
        discarded_tile = self.player.do_discard(1)  # 打出第二張牌
        self.assertEqual(discarded_tile, '萬2')
        self.assertEqual(len(self.player.hand), 2)
        self.assertEqual(len(self.player.discard_hand), 1)

if __name__ == '__main__':
    unittest.main()