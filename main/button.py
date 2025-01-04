import pygame
from setting import *
from main.tile_img import *

class Button:
    def __init__(self, x, y, width, height, text, move):
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.center = (x, y)
        self.frame = None
        self.font = pygame.font.Font('msjh.ttc', 30)
        self.textSurface = self.font.render(text, True, WHITE)
        self.move = move
        self.textOffsetX = 0
        self.textOffsetY = 6
        self.activate = False
        # self.btnImg = pygame.image.load("Image/Btn.png")

    def clicked(self, x: int, y: int) -> bool:
        if self.rect.collidepoint(x, y):
            return True
        return False

    def createFrame(self, x: int, y: int):
        """if cursor position is on the button, create button frame"""
        if self.clicked(x, y):
            x, y, w, h = self.rect
            self.frame = pygame.Rect(x - 2, y - 2, w + 4, h + 4)
        else:
            self.frame = None

    def drawFrame(self, win):
        if self.frame is not None:
            pygame.draw.rect(win, WHITE, self.frame, 2)

    def drawText(self, win):
        textRect = self.rect.copy()
        textRect.y += self.textOffsetY
        textRect.x += self.textOffsetX
        win.blit(self.textSurface, textRect)
    
    def drawButton(self, win):
        self.btnImg = pygame.transform.scale(self.btnImg, (self.rect.width, self.rect.height))
        win.blit(self.btnImg, self.rect)

    def draw(self, win, mouseX, mouseY):
        pass

class ChowBtn(Button):
    def __init__(self, x, y, tile, move):
        super().__init__(x, y, 130, 50, '吃', move)
        self.numOfImg = 4
        self.tile = tile
        self.tileImg = []

    def setTile(self, tile):
        self.tile = []
        self.tile = tile

    def setTileImg(self):
        self.tileImg = []
        for i in self.tile:
            tileImg = imgDict[i]
            tileImg = pygame.transform.scale(tileImg, ((9*TILE_WIDTH)//10, (9*TILE_HEIGHT)//10))
            self.tileImg.append(tileImg)
        
    def drawTile(self, win):
        self.setTileImg()
        k = 30
        for i in self.tileImg:
            tileImgRect = i.get_rect()
            tileImgRect.centery = self.rect.centery
            tileImgRect.left = self.rect.left + k
            k += 0.9*TILE_WIDTH - 9
            win.blit(i, tileImgRect)
    
    def draw(self, win, mouseX, mouseY):
        self.createFrame(mouseX, mouseY)
        # chowBtn.drawButton(win)
        self.drawFrame(win)
        self.drawText(win)
        self.drawTile(win)

class PongBtn(Button):
    def __init__(self, x, y, tile):
        super().__init__(x, y, 75, 50, '碰', 'pong')
        self.numOfImg = 2
        self.tile = tile
        self.tileImg = None

    def setTileImg(self):
        self.tileImg = imgDict[self.tile]
        
    def drawTile(self, win):
        self.setTileImg()
        k = 30
        tileImgRect = self.tileImg.get_rect()
        tileImgRect.centery = self.rect.centery
        tileImgRect.left = self.rect.left + k
        k += 0.9*TILE_WIDTH - 9
        win.blit(self.tileImg, tileImgRect)

    def draw(self, win, mouseX, mouseY):
        self.createFrame(mouseX, mouseY)
        # chowBtn.drawButton(win)
        self.drawFrame(win)
        self.drawText(win)
        self.drawTile(win)

class KongBtn(Button):
    def __init__(self, x, y, tile):
        super().__init__(x, y, 75, 50, '槓', 'kong')
        self.numOfImg = 2
        self.tile = tile
        self.tileImg = []

    def setTileImg(self):
        self.tileImg = imgDict[self.tile]
        
    def drawTile(self, win):
        self.setTileImg()
        k = 30
        tileImgRect = self.tileImg.get_rect()
        tileImgRect.centery = self.rect.centery
        tileImgRect.left = self.rect.left + k
        k += 0.9*TILE_WIDTH - 9
        win.blit(self.tileImg, tileImgRect)

    def draw(self, win, mouseX, mouseY):
        self.createFrame(mouseX, mouseY)
        # chowBtn.drawButton(win)
        self.drawFrame(win)
        self.drawText(win)
        self.drawTile(win)

class TingBtn(Button):
    def __init__(self, x, y, tile):
        super().__init__(x, y, 75, 50, '聽', 'ting')
        self.numOfImg = 2
        self.textOffsetY = -3
        self.tile = tile
        self.tileImg = None

    def setTileImg(self):
        self.tileImg = imgDict[self.tile]
        
    def drawTile(self, win):
        self.setTileImg()
        k = 30
        tileImgRect = self.tileImg.get_rect()
        tileImgRect.centery = self.rect.centery
        tileImgRect.left = self.rect.left + k
        k += 0.9*TILE_WIDTH - 9
        win.blit(self.tileImg, tileImgRect)

    def draw(self, win, mouseX, mouseY):
        self.createFrame(mouseX, mouseY)
        # chowBtn.drawButton(win)
        self.drawFrame(win)
        self.drawText(win)
        self.drawTile(win)


class WinBtn(Button):
    def __init__(self, x, y):
        super().__init__(x, y, 32, 32, '贏', 'win')
        self.numOfImg = 1
        self.textOffsetY = -3

    def draw(self, win, mouseX, mouseY):
        self.createFrame(mouseX, mouseY)
        # chowBtn.drawButton(win)
        self.drawFrame(win)
        self.drawText(win)
    
class NoMoveBtn(Button):
    def __init__(self, x, y):
        super().__init__(x, y, 32, 32, 'X', 'no_move')
        self.numOfImg = 1
        self.textOffsetY = -3
        self.textOffsetX = 5
        self.btnImg = pygame.image.load("Image/X.png")
        self.btnImg = pygame.transform.scale(self.btnImg, (32, 32))

    def draw(self, win, mouseX, mouseY):
        self.createFrame(mouseX, mouseY)
        self.drawFrame(win)
        self.drawButton(win)