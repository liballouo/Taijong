import sys
from pathlib import Path
# 將專案根目錄加入系統路徑
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from main.AI_client import *

import unittest

class TestAIClient(unittest.TestCase):
    # Check if the hand sprite is no the right position
    def test_update_hand_sprite(self):
        test_hand = ['萬1', '萬2', '萬3']
        sprites = update_hand_sprite(test_hand)

        for i in range(0, len(sprites)):
            # WIDTH = 1200 ; Height = 700 ; TILE_WIDTH = 44
            self.assertEqual(sprites[i].rect.centerx, 300 + 34*i)
            self.assertEqual(sprites[i].rect.centery, 595)
    
if __name__ == '__main__':
    unittest.main()