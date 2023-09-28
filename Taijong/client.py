from network import Network
import pygame
from setting import *
from tileSprite import TileSprite
from tileSprite import OpenTile
from button import *
from tileImg import background

pygame.init()
pygame.mixer.init()

win = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Mahjong')
x = WIDTH//4
y = (HEIGHT*5)//6

chowBtn = []
chowBtn.append(ChowBtn((WIDTH*2.5)//10, (HEIGHT*6.5)//10, ['萬1', '萬2', '萬3'], 'chow 2'))
chowBtn.append(ChowBtn((WIDTH*2.5)//10 + 135, (HEIGHT*6.5)//10, ['萬1', '萬2', '萬3'], 'chow 3'))
chowBtn.append(ChowBtn((WIDTH*2.5)//10 + 270, (HEIGHT*6.5)//10, ['萬1', '萬2', '萬3'], 'chow 4'))

pongBtn = PongBtn((WIDTH*2.5)//10 + 375, (HEIGHT*6.5)//10, '萬1')
kongBtn = KongBtn((WIDTH*2.5)//10 + 450, (HEIGHT*6.5)//10, '萬1')
tingBtn = TingBtn((WIDTH*2.5)//10, (HEIGHT*6.5)//10, '萬1')
winBtn = WinBtn((WIDTH*2.5)//10, (HEIGHT*6.5)//10)
noMoveBtn = NoMoveBtn((WIDTH*2.5)//10 + 500, (HEIGHT*6.5)//10)

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

    #others hand length [下家, 對家, 上家]
    othersHandsLength = [0, 0, 0]

    #others hands
    othersHands = [[], [], []]

    #Button List
    buttonList = [chowBtn[0], chowBtn[1]]

    while run:
        # get game from network
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break
        
        
        tileReceive = False # receive tile input
        buttonReceive = False # receive button input

        buttonList = btnListAppend(game, player)
        
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
                    run = False
                    pygame.QUIT()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in handSprite:
                        i.cursorOnOrNot(mouseX, mouseY)
                        if i.cursorOn:
                            tileReceive = True
                            decision = handSprite.index(i)
                            break
                    for i in buttonList:
                        if i.clicked(mouseX, mouseY):
                            decision = i.move
                            buttonReceive = True
                            break
                if game.players[player].discard_move:
                    for i in handSprite:
                        i.cursorOnOrNot(mouseX, mouseY)

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
            
            for i in buttonList:
                i.draw(win, mouseX, mouseY)
            
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

            # Win
            if game.players[player].win_move == True:
                # button is clicked
                if buttonReceive:
                    buttonReceive = False
                    if decision == "win":
                        n.send("win")
                    else:
                        n.send("no_move")
            # Ting
            elif game.players[player].ting_move == True:
                if buttonReceive:
                    if decision != "no_move":
                        message = "ting " + str(decision)
                        n.send(message)
                    else:
                        n.send("no_move")
            # jia_kong
            elif game.players[player].jia_kong_move == True:
                if buttonReceive:
                    if decision == "kong":
                        n.send("jia_kong")
                    else:
                        n.send("no_move")
            # an_kong
            elif game.players[player].an_kong_move == True:
                if buttonReceive:
                    if decision == "kong":
                        n.send("an_kong")
                    else:
                        n.send("no_move")
            # discard
            elif game.players[player].discard_move == True:
                if game.players[player].ting_or_not == False:
                    if tileReceive:
                        tileReceive = False
                        tile_index = decision
                        # print(f"Player {game.players[player].player_number} 丟 {game.players[player].hand[tile_index]}")
                        n.send("discard " + str(tile_index))
                else:
                    # 聽的話只能丟摸到的牌
                    tile_index = game.players[player].hand.index(game.players[player].draw_tile)
                    n.send("discard " + str(tile_index))

            # 改
            elif game.players[player].ask_move == True:
                if buttonReceive:
                    if decision == 'no_move':
                        n.send("no_move")
                    elif decision == 'chow 2':
                        n.send("chow 2")
                    elif decision == 'chow 3':
                        n.send("chow 3")
                    elif decision == 'chow 4':
                        n.send("chow 4")
                    elif decision == 'pong':
                        n.send("pong ")
                    elif decision == 'kong':
                        n.send("kong ")
                    else:
                        n.send("no_move")
                
            else:
                pass

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

def btnListAppend(game, player):# Win
    btnList = []
    if game.players[player].win_move == True:
        noMoveBtn.rect.centerx = (WIDTH*2.5)//10 + 50
        btnList.append(winBtn)
        btnList.append(noMoveBtn)
    # Ting
    elif game.players[player].ting_move == True:
        widthOffset = 0
        for i in range(len(game.players[player].ting_tiles)):
            tingBtn = TingBtn((WIDTH*2.5)//10 + widthOffset, (HEIGHT*6.5)//10, game.players[player].ting_tiles[i])
            tingBtn.move = i
            btnList.append(tingBtn)
            widthOffset += 75
        noMoveBtn.rect.centerx = (WIDTH*2.5)//10 + widthOffset
        btnList.append(noMoveBtn)
        
    # jia_kong
    elif game.players[player].jia_kong_move == True:
        kongBtn.rect.centerx = (WIDTH*2.5)//10
        kongBtn.tile = game.players[player].jia_kong_tile
        btnList.append(kongBtn)
        noMoveBtn.rect.centerx = (WIDTH*2.5)//10 + 75
        btnList.append(noMoveBtn)
    # an_kong
    elif game.players[player].an_kong_move == True:
        kongBtn.rect.centerx = (WIDTH*2.5)//10
        kongBtn.tile = game.players[player].an_kong_tile
        btnList.append(kongBtn)
        noMoveBtn.rect.centerx = (WIDTH*2.5)//10 + 75
        btnList.append(noMoveBtn)

    # 改
    elif game.players[player].ask_move == True:
        widthOffset = 0
        if game.players[player].decision_types["chow"]: # 應該要跟78行對調
            for i in range(len(game.players[player].chow_sets)): 
                if game.players[player].chow_sets[i] != []:
                    chowBtn[i].rect.centerx = (WIDTH*2.5)//10 + widthOffset
                    chowBtn[i].setTile(game.players[player].chow_sets[i])
                    btnList.append(chowBtn[i])
                    widthOffset += 135
        if game.players[player].decision_types["pong"]:
            pongBtn.rect.centerx = (WIDTH*2.5)//10 + widthOffset
            pongBtn.tile  = game.players[player].pong_tile
            btnList.append(pongBtn)
            widthOffset += 75
        if game.players[player].decision_types["kong"]:
            kongBtn.rect.centerx = (WIDTH*2.5)//10 + widthOffset
            kongBtn.tile = game.players[player].kong_tile
            btnList.append(kongBtn)
            widthOffset += 75
        
        noMoveBtn.rect.centerx = (WIDTH*2.5)//10 + widthOffset
        btnList.append(noMoveBtn)
        
    return btnList

def drawWin(win, text):
    font = pygame.font.Font('msjh.ttc', 30)
    textSurface = font.render(text, True, WHITE)
    winRect = pygame.Rect(WIDTH//2 - 75, HEIGHT//2, 50, 50)
    win.blit(textSurface, winRect)
    
    pass

main()