from tileImg import *

class TileSprite:
    def __init__(self, tile):
        self.tile = tile
        self.image = imgDict[self.tile]
        self.rect = self.image.get_rect()
        self.cursorOn = False
        self.bottom = None
    
    def set_x_y(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y
        self.bottom = self.rect.bottom
    
    def set_x(self, x):
        self.rect.centerx = x

    def cursor_on_or_not(self, mouseX, mouseY):
        if self.rect.left < mouseX < self.rect.right - 10 and self.rect.top < mouseY < self.bottom:
            if not self.cursorOn:
                self.rect.centery -= 10
            self.cursorOn = True
        elif self.cursorOn:
            self.cursorOn = False
            self.rect.centery += 10
        return self.cursorOn

    def draw_tile(self, win):
        win.blit(self.image, self.rect)

class OpenTile:
    def __init__(self, tile, angle):
        self.tile = tile
        self.image = imgDict[self.tile]
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()
        self.bottom = None
    
    def set_x_y(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y
        self.bottom = self.rect.bottom
    
    def set_x(self, x):
        self.rect.centerx = x

    def draw_tile(self, win):
        win.blit(self.image, self.rect)

#目前還沒用到
# class HandTiles:
#     def __init__(self, hand):
#         self.tileSprites = []
#         self.setTileSprites(hand)

#     def setTileSprites(self, hand):
#         for i in hand:
#             self.tileSprites.append(TileSprite(i))

#     def updateTile(self, hand):
#         self.tileSprites = []
#         self.setTileSprites(hand)

#     def checkCursor(self, mouseX, mouseY):
#         for i in self.tileSprites:
#             if i.cursorOnOrNot(mouseX, mouseY):
#                 return i