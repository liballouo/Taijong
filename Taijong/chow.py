def check_chow(self, tile):
        hand = self.hand.copy()
        hand.append(tile)
        Chow_sets = []  # 紀錄可以吃的組合
        tile_type = []  # 哪種牌(萬or條or餅)

        tile_index, tile_type = self.deck.find_tile_type_index(tile)

        for i in range(3):
            Chow_set = []
            # Decide whether can Chow or not
            '''
            +----+----+----+----+
            |\ i |    |    |    |
            | \  | -0 | -1 | -2 |
            |j \ |    |    |    |
            +----+----+----+----+
            | +0 |  0 | -1 | -2 |
            +----+----+----+----+
            | +1 |  1 |  0 | -1 |
            +----+----+----+----+
            | +2 |  2 |  1 |  0 |
            +----+----+----+----+
            '''
            for j in range(3):
                can_Chow = True # 應該不用
                if tile_index-i+j >= 0 and tile_index-i+j <= 8:
                    if tile_type[tile_index-i+j] in hand:
                        Chow_set.append(tile_type[tile_index-i+j])
                    else: # 應該不用
                        can_Chow = False # 應該不用
                else: # 應該不用
                    can_Chow = False # 應該不用

                if not can_Chow: # 應該不用
                    Chow_set = [] # 應該不用
                    break # 應該不用
            
            # 有可以吃的組合
            if len(Chow_set) > 0:
                # 將可以吃的組合放入Chow sets
                if tile in Chow_set:
                    Chow_sets.append(Chow_set)

        # 用來做決定的list [吃左, 吃中, 吃右]
        Chow_decison_set = [[], [], []]

        for i in range(len(Chow_sets)):
            index = Chow_sets[i].index(tile)           
            Chow_decison_set[index] = Chow_sets[i]

        if len(Chow_sets) > 0:
            self.chow_sets = Chow_sets
            # ask chow
            print(f"玩家{self.player_number}是否要吃牌: (1)否 ", end="")
            for i in range(len(Chow_decison_set)): 
                print("({0})".format(i+2, end=""))
                if Chow_decison_set[i] != []:
                    for j in range(3):
                        print(Chow_decison_set[i][j], end=" ")
                    # pass
            decision = int(input())
            #print(decision)
            
            # do chow
            # player chooses Chow
            hand = self.hand
            if decision != 1:
                # 2, 3, 4 -> == [] -> invalid -> redecision
                for i in range(3):
                    chow_tile = Chow_decison_set[decision-2][i]
                    self.openhand.append(chow_tile)   # Append Chow set into the player's open hand
                    if chow_tile in hand:
                        hand.remove(chow_tile)
                return True
            # player chooses not Chow
            else: # 應該不用
                hand.remove(tile) # 應該不用
                return False # 應該不用
            
        hand.remove(tile)
        return False