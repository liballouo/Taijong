from network import Network
import pygame
from setting import *
from tileSprite import TileSprite
from tileSprite import OpenTile
from button import Button
from tileImg import background

pygame.init()
pygame.mixer.init()

win = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Mahjong')
x = WIDTH//4
y = (HEIGHT*5)//6

def main():
    run = True

    n = Network()
    player = int(n.getP())
    print("You are player", player)

    # pygame settings
    update = True
    tileReceive = False # receive tile input
    buttonReceive = False # receive button input

    client_update_count = -1

    #手牌
    hand = []
    handSprite = []

    #open hand [自己, 下家, 對家, 上家]
    openHands = [[], [], [], []]

    #discard hand [自己, 下家, 對家, 上家]
    discardHands = [[], [], [], []]

    #others hand [下家, 對家, 上家]
    othersHandsLength = [0, 0, 0]

    while run:
        # get game from network
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            continue
        
        
        tileReceive = False # receive tile input
        buttonReceive = False # receive button input
        
        if game.ready:
            # pygame part
            # -----------------
            clock.tick(FPS)

            # if there's a move, then update
            if client_update_count != game.update_count:
                client_update_count = game.update_count
                update = True

            if(update):

                #update hand
                hand = game.players[player].hand
                handSprite = updateHandSprite(hand)

                #update discard hands
                discardHands = [game.players[player%4].discardhand, game.players[(player+1)%4].discardhand, 
                                game.players[(player+2)%4].discardhand, game.players[(player+3)%4].discardhand]

                #update open hands
                openHands = [game.players[player%4].openhand, game.players[(player+1)%4].openhand, 
                                game.players[(player+2)%4].openhand, game.players[(player+3)%4].openhand]

                #update others hand length
                othersHandsLength = [len(game.players[(player+1)%4].hand), len(game.players[(player+2)%4].hand), 
                                    len(game.players[(player+3)%4].hand)]
                
                
                    
                update = False
            # if win update others hand
            if game.win:
                othersHands = [game.players[(player+1)%4].hand, game.players[(player+2)%4].hand, 
                                game.players[(player+3)%4].hand]


            # input
            (mouseX, mouseY) = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.QUIT()

            # draw
            win.fill(BLACK)
            fill_background(win)
            drawHandSprite(win, handSprite)
            drawSelfOpenTiles(win, discardHands[0], openHands[0])
            if not game.win:
                drawDownOpenTiles(win, discardHands[1], openHands[1], othersHandsLength[0])
                drawAcrossOpenTiles(win, discardHands[2], openHands[2], othersHandsLength[1])
                drawUpOpenTiles(win, discardHands[3], openHands[3], othersHandsLength[2])
            else:
                drawDownWin(win, discardHands[1], openHands[1], othersHands[0])
                drawAcrossWin(win, discardHands[2], openHands[2], othersHands[1])
                drawUpWin(win, discardHands[3], openHands[3], othersHands[2])

            # update
            x = WIDTH // 4
            for i in handSprite:
                i.setX(x)
                x += TILE_WIDTH - 10

            if game.win == True:
                for i in game.players:
                    if i.win_or_not == True:
                        if i.player_number == player:
                            drawWin(win, "You win!!!")
                        elif (i.player_number - player) % 4 == 1:
                            drawWin(win, "下家 win!!!")
                        elif (i.player_number - player) % 4 == 2:
                            drawWin(win, "對家 win!!!")
                        elif (i.player_number - player) % 4 == 3:
                            drawWin(win, "上家 win!!!")
                            
            pygame.display.update()

            # --------------------
            # end pygame part

            # Win -> end game
            # if game.win == True:
            #     for i in game.players:
            #         if i.win_or_not == True:
            #             print(f"Player {i.player_number} win!!!")
                # break

def drawHandSprite(win, handSprite):
    for i in handSprite:
        i.drawTile(win)

def updateHandSprite(hand):
    handSprite = []
    x = (WIDTH*2.5)//10
    y = (HEIGHT*8.5)//10
    for i in hand:
        handSprite.append(TileSprite(i))
    for i in handSprite:
        i.setXY(x, y)
        x += TILE_WIDTH - 10
    return  handSprite

def drawSelfOpenTiles(win, discardHand, openHand):
    discardTiles = []
    x = (WIDTH*2.5)//10
    y = (HEIGHT*7.5)//10
    for i in discardHand:
        discardTiles.append(OpenTile(i, 0))
    for i in discardTiles:
        i.setXY(x, y)
        x += TILE_WIDTH - 10
    for i in discardTiles:
        i.drawTile(win)

    openTiles = []
    x = (WIDTH*1.75)//10
    y = (HEIGHT*9.5)//10
    for i in openHand:
        openTiles.append(OpenTile(i, 0))
    for i in openTiles:
        i.setXY(x, y)
        x += TILE_WIDTH - 10
    for i in openTiles:
        i.drawTile(win)

#下家
def drawDownOpenTiles(win, discardHand, openHand, handLength):
    discardTiles = []
    x = (WIDTH*8.3)//10
    y = (HEIGHT*6.5)//10
    for i in discardHand:
        discardTiles.append(OpenTile(i, 90))
    for i in discardTiles:
        i.setXY(x, y)
        y -= TILE_WIDTH - 10
    for i in discardTiles:
        i.drawTile(win)

    openTiles = []
    x = (WIDTH*9.5)//10
    y = (HEIGHT*9)//10
    for i in openHand:
        openTiles.append(OpenTile(i, 90))
    for i in openTiles:
        i.setXY(x, y)
        y -= TILE_WIDTH - 10
    for i in openTiles:
        i.drawTile(win)

    handTiles = []
    x = (WIDTH*8.9)//10
    y = (HEIGHT*8.5)//10
    for i in range(handLength):
        handTiles.append(OpenTile('back2', 0))
    for i in handTiles:
        i.setXY(x, y)
        y -= TILE_WIDTH - 10
    for i in handTiles:
        i.drawTile(win)

#對家
def drawAcrossOpenTiles(win, discardHand, openHand, handLength):
    discardTiles = []
    x = (WIDTH*7.5)//10
    y = (HEIGHT*2)//10
    for i in discardHand:
        discardTiles.append(OpenTile(i, 180))
    for i in discardTiles:
        i.setXY(x, y)
        x -= TILE_WIDTH - 10
    for i in discardTiles:
        i.drawTile(win)

    openTiles = []
    x = (WIDTH*8.5)//10
    y = (HEIGHT*0.5)//10
    for i in openHand:
        openTiles.append(OpenTile(i, 180))
    for i in openTiles:
        i.setXY(x, y)
        x -= TILE_WIDTH - 10
    for i in openTiles:
        i.drawTile(win)

    handTiles = []
    x = (WIDTH*7.5)//10
    y = (HEIGHT*1.25)//10
    for i in range(handLength):
        handTiles.append(OpenTile('back1', 0))
    for i in handTiles:
        i.setXY(x, y)
        x -= TILE_WIDTH - 8
    for i in handTiles:
        i.drawTile(win)

#上家
def drawUpOpenTiles(win, discardHand, openHand, handLength):
    discardTiles = []
    x = (WIDTH*1.7)//10
    y = (HEIGHT*2)//10
    for i in discardHand:
        discardTiles.append(OpenTile(i, -90))
    for i in discardTiles:
        i.setXY(x, y)
        y += TILE_WIDTH - 10
    for i in discardTiles:
        i.drawTile(win)

    openTiles = []
    x = (WIDTH*0.5)//10
    y = (HEIGHT*0.5)//10
    for i in openHand:
        openTiles.append(OpenTile(i, -90))
    for i in openTiles:
        i.setXY(x, y)
        y += TILE_WIDTH - 10
    for i in openTiles:
        i.drawTile(win)
    
    handTiles = []
    x = (WIDTH*1.1)//10
    y = (HEIGHT*1.5)//10
    for i in range(handLength):
        handTiles.append(OpenTile('back3', 0))
    for i in handTiles:
        i.setXY(x, y)
        y += TILE_WIDTH - 10
    for i in handTiles:
        i.drawTile(win)

#下家(贏顯示)
def drawDownWin(win, discardHand, openHand, hand):
    discardTiles = []
    x = (WIDTH*8.3)//10
    y = (HEIGHT*7.5)//10
    for i in discardHand:
        discardTiles.append(OpenTile(i, 90))
    for i in discardTiles:
        i.setXY(x, y)
        y -= TILE_WIDTH - 10
    for i in discardTiles:
        i.drawTile(win)

    openTiles = []
    x = (WIDTH*9.5)//10
    y = (HEIGHT*9)//10
    for i in openHand:
        openTiles.append(OpenTile(i, 90))
    for i in openTiles:
        i.setXY(x, y)
        y -= TILE_WIDTH - 10
    for i in openTiles:
        i.drawTile(win)

    handTiles = []
    x = (WIDTH*8.9)//10
    y = (HEIGHT*8.5)//10
    for i in hand:
        handTiles.append(OpenTile(i, 90))
    for i in handTiles:
        i.setXY(x, y)
        y -= TILE_WIDTH - 10
    for i in handTiles:
        i.drawTile(win)

#對家(贏顯示)
def drawAcrossWin(win, discardHand, openHand, hand):
    discardTiles = []
    x = (WIDTH*7.5)//10
    y = (HEIGHT*2)//10
    for i in discardHand:
        discardTiles.append(OpenTile(i, 180))
    for i in discardTiles:
        i.setXY(x, y)
        x -= TILE_WIDTH - 10
    for i in discardTiles:
        i.drawTile(win)

    openTiles = []
    x = (WIDTH*8.5)//10
    y = (HEIGHT*0.5)//10
    for i in openHand:
        openTiles.append(OpenTile(i, 180))
    for i in openTiles:
        i.setXY(x, y)
        x -= TILE_WIDTH - 10
    for i in openTiles:
        i.drawTile(win)

    handTiles = []
    x = (WIDTH*7.5)//10
    y = (HEIGHT*1.25)//10
    for i in hand:
        handTiles.append(OpenTile(i, 180))
    for i in handTiles:
        i.setXY(x, y)
        x -= TILE_WIDTH - 8
    for i in handTiles:
        i.drawTile(win)

#上家(贏顯示)
def drawUpWin(win, discardHand, openHand, hand):
    discardTiles = []
    x = (WIDTH*1.7)//10
    y = (HEIGHT*1.6)//10
    for i in discardHand:
        discardTiles.append(OpenTile(i, -90))
    for i in discardTiles:
        i.setXY(x, y)
        y += TILE_WIDTH - 10
    for i in discardTiles:
        i.drawTile(win)

    openTiles = []
    x = (WIDTH*0.5)//10
    y = (HEIGHT*0.5)//10
    for i in openHand:
        openTiles.append(OpenTile(i, -90))
    for i in openTiles:
        i.setXY(x, y)
        y += TILE_WIDTH - 10
    for i in openTiles:
        i.drawTile(win)
    
    handTiles = []
    x = (WIDTH*1.1)//10
    y = (HEIGHT*1.5)//10
    for i in hand:
        handTiles.append(OpenTile(i, -90))
    for i in handTiles:
        i.setXY(x, y)
        y += TILE_WIDTH - 10
    for i in handTiles:
        i.drawTile(win)


def fill_background(win):
    for y in range(0, HEIGHT, background.get_height()):
        for x in range(0, WIDTH, background.get_width()):
            win.blit(background, (x, y))

def drawWin(win, text):
    font = pygame.font.Font('msjh.ttc', 30)
    textSurface = font.render(text, True, WHITE)
    winRect = pygame.Rect(WIDTH//2 - 75, HEIGHT//2, 50, 50)
    win.blit(textSurface, winRect)
    
    pass


main()