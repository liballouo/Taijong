import pygame

pygame.init()

file_path = "Image/"

#萬
w1 = pygame.image.load(f"{file_path}w1.gif")
w2 = pygame.image.load(f"{file_path}w2.gif")
w3 = pygame.image.load(f"{file_path}w3.gif")
w4 = pygame.image.load(f"{file_path}w4.gif")
w5 = pygame.image.load(f"{file_path}w5.gif")
w6 = pygame.image.load(f"{file_path}w6.gif")
w7 = pygame.image.load(f"{file_path}w7.gif")
w8 = pygame.image.load(f"{file_path}w8.gif")
w9 = pygame.image.load(f"{file_path}w9.gif")

#條
t1 = pygame.image.load(f"{file_path}t1.gif")
t2 = pygame.image.load(f"{file_path}t2.gif")
t3 = pygame.image.load(f"{file_path}t3.gif")
t4 = pygame.image.load(f"{file_path}t4.gif")
t5 = pygame.image.load(f"{file_path}t5.gif")
t6 = pygame.image.load(f"{file_path}t6.gif")
t7 = pygame.image.load(f"{file_path}t7.gif")
t8 = pygame.image.load(f"{file_path}t8.gif")
t9 = pygame.image.load(f"{file_path}t9.gif")

#餅
b1 = pygame.image.load(f"{file_path}b1.gif")
b2 = pygame.image.load(f"{file_path}b2.gif")
b3 = pygame.image.load(f"{file_path}b3.gif")
b4 = pygame.image.load(f"{file_path}b4.gif")
b5 = pygame.image.load(f"{file_path}b5.gif")
b6 = pygame.image.load(f"{file_path}b6.gif")
b7 = pygame.image.load(f"{file_path}b7.gif")
b8 = pygame.image.load(f"{file_path}b8.gif")
b9 = pygame.image.load(f"{file_path}b9.gif")

#東南西北中發白
E = pygame.image.load(f"{file_path}E.gif")
S = pygame.image.load(f"{file_path}S.gif")
W = pygame.image.load(f"{file_path}W.gif")
N = pygame.image.load(f"{file_path}N.gif")
C = pygame.image.load(f"{file_path}C.gif")
F = pygame.image.load(f"{file_path}F.gif")
P = pygame.image.load(f"{file_path}P.gif")

#背面
back0 = pygame.image.load(f"{file_path}back0.gif")
back1 = pygame.image.load(f"{file_path}back1.gif")
back2 = pygame.image.load(f"{file_path}back2.gif")
back3 = pygame.image.load(f"{file_path}back3.gif")

# 背景
background = pygame.image.load(f"{file_path}background.jpg")

imgDict = {'萬1': w1, '萬2': w2, '萬3': w3, '萬4': w4, '萬5': w5, '萬6': w6, '萬7': w7, '萬8': w8, '萬9': w9, 
           '條1': t1, '條2': t2, '條3': t3, '條4': t4, '條5': t5, '條6': t6, '條7': t7, '條8': t8, '條9': t9, 
           '餅1': b1, '餅2': b2, '餅3': b3, '餅4': b4, '餅5': b5, '餅6': b6, '餅7': b7, '餅8': b8, '餅9': b9, 
           'E': E, 'S': S, 'W': W, 'N': N, 'C': C, 'F': F, 'P': P, 'back0': back0, 'back1': back1, 
           'back2': back2, 'back3': back3}