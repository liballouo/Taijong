import random
from tile import *

class Deck:
    def __init__(self):
        self.wan_tiles = WAN_TILES
        self.tiao_tiles = TIAO_TILES
        self.bing_tiles = BING_TILES
        self.zi_tiles = ZI_TILES
        # 牌
        self.all_tiles = (self.wan_tiles + self.tiao_tiles + self.bing_tiles + self.zi_tiles)
        # 牌庫
        self.tiles = 4 * self.all_tiles
        
    def print_all_tiles(self):
        print(*self.all_tiles, "\n")
    
    def print_tiles(self):
        print(*self.tiles, "\n")
        # print(len(self.tiles))

    def find_all_tiles_index(self, tile):
        return self.all_tiles.index(tile)
    
    def find_wan_tiles_index(self, tile):
        return self.wan_tiles.index(tile)

    def find_tiao_tiles_index(self, tile):
        return self.tiao_tiles.index(tile)
    
    def find_bing_tiles_index(self, tile):
        return self.bing_tiles.index(tile)
    
    def find_zi_tiles_index(self, tile):
        return self.zi_tiles.index(tile)

    def find_tile_type_index(self, tile):
        tile_index = self.find_all_tiles_index(tile)
        # 萬
        if tile_index < 9:
            tile_type = self.wan_tiles
            tile_index %= 9
        # 條
        elif tile_index < 18:
            tile_type = self.tiao_tiles
            tile_index %= 9
        # 餅
        elif tile_index < 27:
            tile_type = self.bing_tiles
            tile_index %= 9
        else:
            tile_type = self.zi_tiles
        return tile_index, tile_type

    def shuffle(self):
        random.shuffle(self.tiles)

    def draw(self):
        return self.tiles.pop()
    
    def number_tile_left_in_deck(self):
        return len(self.tiles)
    
    def tile_to_list(self, tile):
        list = [0] * 34
        for i in tile:
            list[self.all_tiles.index(i)] += 1
        return list

# deck = Deck()
# deck.shuffle()
# deck.print_all_tiles()
# deck.print_tiles()
# print(deck.draw())
# deck.print_tiles()