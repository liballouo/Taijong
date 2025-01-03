from network import Network
import pygame
from setting import *
from tileSprite import TileSprite
from tileSprite import OpenTile
from tileImg import *

def main():
    pygame.init()
    pygame.mixer.init()

    win = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Mahjong')
    x = WIDTH//4
    
    run = True

    n = Network()
    player = int(n.getP())
    print("You are player", player)

    # pygame settings
    update = True

    client_update_count = -1

    #手牌
    hand = []
    hand_sprite = []

    #open hand [自己, 下家, 對家, 上家]
    open_hands = [[], [], [], []]

    #discard hand [自己, 下家, 對家, 上家]
    discard_hands = [[], [], [], []]

    #others hand [下家, 對家, 上家]
    others_hands_length = [0, 0, 0, 0]

    while run:
        # get game from network
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            continue
        
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
                hand_sprite = update_hand_sprite(hand)

                #update discard hands
                discard_hands = [game.players[player%4].discard_hand, game.players[(player+1)%4].discard_hand, 
                                game.players[(player+2)%4].discard_hand, game.players[(player+3)%4].discard_hand]

                #update open hands
                open_hands = [game.players[player%4].open_hand, game.players[(player+1)%4].open_hand, 
                                game.players[(player+2)%4].open_hand, game.players[(player+3)%4].open_hand]

                #update others hand length
                others_hands_length = [0, len(game.players[(player+1)%4].hand), len(game.players[(player+2)%4].hand), 
                                    len(game.players[(player+3)%4].hand)]
                
                update = False
                
            # if win update others hand
            if game.win:
                others_hands = [game.players[(player+0)%4].hand, game.players[(player+1)%4].hand, game.players[(player+2)%4].hand, 
                                game.players[(player+3)%4].hand]


            # input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.QUIT()

            # draw
            win.fill(BLACK)
            fill_background(win)
            draw_hand_sprite(win, hand_sprite)
            draw_self_tiles(win, discard_hands[0], open_hands[0])
            
            if not game.win:
                draw_down_open_tiles(win, discard_hands[1], open_hands[1], others_hands_length[1])
                draw_across_open_tiles(win, discard_hands[2], open_hands[2], others_hands_length[2])
                draw_up_open_tiles(win, discard_hands[3], open_hands[3], others_hands_length[3])
            else:
                draw_down_win(win, discard_hands[1], open_hands[1], others_hands[1])
                draw_across_win(win, discard_hands[2], open_hands[2], others_hands[2])
                draw_up_win(win, discard_hands[3], open_hands[3], others_hands[3])

            # update
            x = WIDTH // 4
            for i in hand_sprite:
                i.set_x(x)
                x += TILE_WIDTH - 10

            if game.win == True:
                for i in game.players:
                    if i.win_or_not == True:
                        if i.player_number == player:
                            draw_win(win, "You win!!!")
                        elif (i.player_number - player) % 4 == 1:
                            draw_win(win, "下家 win!!!")
                        elif (i.player_number - player) % 4 == 2:
                            draw_win(win, "對家 win!!!")
                        elif (i.player_number - player) % 4 == 3:
                            draw_win(win, "上家 win!!!")
                            
            pygame.display.update()
            # --------------------
            # end pygame part

def draw_hand_sprite(win, hand_sprite):
    for i in hand_sprite:
        i.draw_tile(win)

def update_hand_sprite(hand):
    hand_sprite = []
    x = (WIDTH*2.5)//10
    y = (HEIGHT*8.5)//10
    for i in hand:
        hand_sprite.append(TileSprite(i))
    for i in hand_sprite:
        i.set_x_y(x, y)
        x += TILE_WIDTH - 10
    return hand_sprite

def draw_discard_tiles(window, player_idx, discard_hand, x_offset, y_offset, discard_angle):
    discard_tiles = []
    x = (WIDTH*x_offset)//10
    y = (HEIGHT*y_offset)//10
    for i in discard_hand:
        discard_tiles.append(OpenTile(i, discard_angle))
    for i in discard_tiles:
        i.set_x_y(x, y)
        if player_idx == 0:
            x += TILE_WIDTH - 10
        elif player_idx == 1:
            y -= TILE_WIDTH - 10
        elif player_idx == 2:
            x -= TILE_WIDTH - 10
        elif player_idx == 3:
            y += TILE_WIDTH - 10
    for i in discard_tiles:
        i.draw_tile(window)

def draw_open_tiles(window, player_idx, open_hand, x_offset, y_offset, open_angle):
    open_tiles = []
    x = (WIDTH*x_offset)//10
    y = (HEIGHT*y_offset)//10
    for i in open_hand:
        open_tiles.append(OpenTile(i, open_angle))
    for i in open_tiles:
        i.set_x_y(x, y)
        if player_idx == 0:
            x += TILE_WIDTH - 10
        elif player_idx == 1:
            y -= TILE_WIDTH - 10
        elif player_idx == 2:
            x -= TILE_WIDTH - 10
        elif player_idx == 3:
            y += TILE_WIDTH - 10
    for i in open_tiles:
        i.draw_tile(window)

def draw_hand_tiles(window, player_idx, x_offset, y_offset, hand_tile_index, hand_angle, hand_length):
    hand_tiles = []
    x = (WIDTH*x_offset)//10
    y = (HEIGHT*y_offset)//10
    for i in range(hand_length):
        hand_tiles.append(OpenTile(hand_tile_index, hand_angle))
    for i in hand_tiles:
        i.set_x_y(x, y)
        if player_idx == 0:
            x += TILE_WIDTH - 10
        elif player_idx == 1:
            y -= TILE_WIDTH - 10
        elif player_idx == 2:
            x -= TILE_WIDTH - 10
        elif player_idx == 3:
            y += TILE_WIDTH - 10
    for i in hand_tiles:
        i.draw_tile(window)

# 自己
def draw_self_tiles(window, discard_hand, open_hand):
    draw_discard_tiles(window, 0, discard_hand, x_offset=2.5, y_offset=7.5, discard_angle=0)
    draw_open_tiles(window, 0, open_hand, x_offset=1.75, y_offset=9.5, open_angle=0)
    
#下家
def draw_down_open_tiles(window, discard_hand, open_hand, hand_length):
    draw_discard_tiles(window, 1, discard_hand, x_offset=8.3, y_offset=6.5, discard_angle=90)
    draw_open_tiles(window, 1, open_hand, x_offset=9.5, y_offset=9, open_angle=90)
    draw_hand_tiles(window, 1, x_offset=8.9, y_offset=8.5, hand_tile_index='back2', hand_angle=0, hand_length=hand_length)

#對家
def draw_across_open_tiles(window, discard_hand, open_hand, hand_length):
    draw_discard_tiles(window, 2, discard_hand, x_offset=7.5, y_offset=2, discard_angle=180)
    draw_open_tiles(window, 2, open_hand, x_offset=8.5, y_offset=0.5, open_angle=180)
    draw_hand_tiles(window, 2, x_offset=7.5, y_offset=1.25, hand_tile_index='back1', hand_angle=0, hand_length=hand_length)

#上家
def draw_up_open_tiles(window, discard_hand, open_hand, hand_length):
    draw_discard_tiles(window, 3, discard_hand, x_offset=1.7, y_offset=2, discard_angle=-90)
    draw_open_tiles(window, 3, open_hand, x_offset=0.5, y_offset=0.5, open_angle=-90)
    draw_hand_tiles(window, 3, x_offset=1.1, y_offset=1.5, hand_tile_index='back3', hand_angle=0, hand_length=hand_length)

#下家(贏顯示)
def draw_down_win(win, discard_hand, open_hand, hand):
    discard_tiles = []
    x = (WIDTH*8.3)//10
    y = (HEIGHT*7.5)//10
    for i in discard_hand:
        discard_tiles.append(OpenTile(i, 90))
    for i in discard_tiles:
        i.set_x_y(x, y)
        y -= TILE_WIDTH - 10
    for i in discard_tiles:
        i.draw_tile(win)

    open_tiles = []
    x = (WIDTH*9.5)//10
    y = (HEIGHT*9)//10
    for i in open_hand:
        open_tiles.append(OpenTile(i, 90))
    for i in open_tiles:
        i.set_x_y(x, y)
        y -= TILE_WIDTH - 10
    for i in open_tiles:
        i.draw_tile(win)

    handTiles = []
    x = (WIDTH*8.9)//10
    y = (HEIGHT*8.5)//10
    for i in hand:
        handTiles.append(OpenTile(i, 90))
    for i in handTiles:
        i.set_x_y(x, y)
        y -= TILE_WIDTH - 10
    for i in handTiles:
        i.draw_tile(win)

#對家(贏顯示)
def draw_across_win(win, discard_hand, open_hand, hand):
    discard_tiles = []
    x = (WIDTH*7.5)//10
    y = (HEIGHT*2)//10
    for i in discard_hand:
        discard_tiles.append(OpenTile(i, 180))
    for i in discard_tiles:
        i.set_x_y(x, y)
        x -= TILE_WIDTH - 10
    for i in discard_tiles:
        i.draw_tile(win)

    open_tiles = []
    x = (WIDTH*8.5)//10
    y = (HEIGHT*0.5)//10
    for i in open_hand:
        open_tiles.append(OpenTile(i, 180))
    for i in open_tiles:
        i.set_x_y(x, y)
        x -= TILE_WIDTH - 10
    for i in open_tiles:
        i.draw_tile(win)

    handTiles = []
    x = (WIDTH*7.5)//10
    y = (HEIGHT*1.25)//10
    for i in hand:
        handTiles.append(OpenTile(i, 180))
    for i in handTiles:
        i.set_x_y(x, y)
        x -= TILE_WIDTH - 8
    for i in handTiles:
        i.draw_tile(win)

#上家(贏顯示)
def draw_up_win(win, discard_hand, open_hand, hand):
    discard_tiles = []
    x = (WIDTH*1.7)//10
    y = (HEIGHT*1.6)//10
    for i in discard_hand:
        discard_tiles.append(OpenTile(i, -90))
    for i in discard_tiles:
        i.set_x_y(x, y)
        y += TILE_WIDTH - 10
    for i in discard_tiles:
        i.draw_tile(win)

    open_tiles = []
    x = (WIDTH*0.5)//10
    y = (HEIGHT*0.5)//10
    for i in open_hand:
        open_tiles.append(OpenTile(i, -90))
    for i in open_tiles:
        i.set_x_y(x, y)
        y += TILE_WIDTH - 10
    for i in open_tiles:
        i.draw_tile(win)
    
    handTiles = []
    x = (WIDTH*1.1)//10
    y = (HEIGHT*1.5)//10
    for i in hand:
        handTiles.append(OpenTile(i, -90))
    for i in handTiles:
        i.set_x_y(x, y)
        y += TILE_WIDTH - 10
    for i in handTiles:
        i.draw_tile(win)

def fill_background(win):
    for y in range(0, HEIGHT, background.get_height()):
        for x in range(0, WIDTH, background.get_width()):
            win.blit(background, (x, y))

def draw_win(win, text):
    font = pygame.font.Font('msjh.ttc', 30)
    textSurface = font.render(text, True, WHITE)
    winRect = pygame.Rect(WIDTH//2 - 75, HEIGHT//2, 50, 50)
    win.blit(textSurface, winRect)
    
    pass

if __name__ == '__main__':
    main()