import socket
from _thread import *
import pickle
from main.mahjong import Majhong

server = "192.168.150.199"
# server = ""
# server = "192.168.1.183"
port = 5550

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0

def threaded_client(conn, p): # 一場兩個，因為有兩個玩家
    global idCount
    conn.send(str.encode(str(p)))
    reply = ""
    while True:
        try:
            data = conn.recv(8192).decode()
            if not data:
                break
            else:
                data_split = data.split()
                move = data_split[0]
                #這行出問題 改成寫進聽(47)和丟(63)裡面 因為get經split不會有1
                # num = data_split[1]
                if move == "reset":
                    game.resetWent()
                elif move != "get":
                    if move == "win":
                        game.players[p].win_or_not = True
                        game.win = True
                        game.players[p].receive_or_not = True
                    elif move == "ting":
                        game.players[p].ting_or_not = True
                        tile = game.players[p].ting_tiles[int(data_split[1])]
                        tile_index = game.players[p].hand.index(tile)
                        game.players[p].discard_tile = game.players[p].do_ting(tile_index)
                        game.players[p].receive_or_not = True
                    elif move == "jia_kong":
                        game.players[p].jia_kong_or_not = True
                        game.players[p].do_jia_kong()
                        game.next_player = game.last_player
                        game.players[p].receive_or_not = True
                    elif move == "an_kong":
                        game.players[p].an_kong_or_not = True
                        game.players[p].do_an_kong()
                        game.next_player = game.last_player
                        game.players[p].receive_or_not = True
                    elif move == "discard":
                        tile_index = int(data_split[1])
                        game.players[p].discard_tile = game.players[p].do_discard(tile_index)
                        game.players[p].receive_or_not = True

                    elif move == "kong" or move == "pong" or move == "chow":
                        game.players[p].decision_results = data
                        game.players[p].ask_move = False
                        game.players[p].receive_or_not = True

                    elif move == "no_move":
                        game.players[p].decision_results = data
                        game.players[p].win_move = False
                        # 過水在靠邀
                        game.players[p].ting_move = False
                        game.players[p].jia_kong_move = False
                        game.players[p].an_kong_move = False
                        game.players[p].discard_move = False
                        # game.players[p].kong_move = False
                        # game.players[p].pong_move = False
                        # game.players[p].chow_move = False
                        game.players[p].ask_move = False
                        game.players[p].receive_or_not = True
                    else:
                        pass

                conn.sendall(pickle.dumps(game))
        except:
            break

    print("Lost connection")
    try:
        del games
        print("Closing Game")
    except:
        pass
    idCount -= 1
    conn.close()



while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    player_count = 4

    if idCount % player_count == 1:
        game = Majhong(1)
        print("Creating a new game...")
        p = 0
    elif idCount % player_count == 2:
        p = 1
        game.ready = True
    elif idCount % player_count == 3:
        p = 2
    elif idCount % player_count == 0:
        p = 3
 

    start_new_thread(threaded_client, (conn, p))

    if game.ready:
        break

game.initialize()
while game.win == False:
    game.update_count += 1
    if game.liu_ju():
        print("liu_ju")
        break
    game.player_turn()
    if game.win == True:
        for i in game.players:
            if i.win_or_not == True:
                print(f"Player {i.player_number} win!!!")
        break
    if game.jia_kong == True:
        game.jia_kong = False
        continue
    elif game.an_kong == True:
        game.an_kong = False
        continue
    game.update_count += 1
    game.check_other_player_move(game.players[game.last_player].discard_tile)
    if game.win == True:
        for i in game.players:
            if i.win_or_not == True:
                print(f"Player {i.player_number} win!!!")
        break

while True:
    i=0
print("exit")
# exit()