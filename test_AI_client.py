import unittest
from src.Taijong.AI_client import *

class TestAIClient(unittest.TestCase):
    # Check if the hand sprite is no the reight position
    def test_update_hand_sprite(self):
        test_hand = ['萬1', '萬2', '萬3']
        sprites = update_hand_sprite(test_hand)

        for i in range(0, len(sprites)):
            # WIDTH = 1200 ; Height = 700 ; TILE_WIDTH = 44
            self.assertEqual(sprites[i].rect.centerx, 300 + 34*i)
            self.assertEqual(sprites[i].rect.centery, 595)
    
if __name__ == '__main__':
    unittest.main()