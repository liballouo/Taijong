import pygame

pygame.init()

#萬
w1 = pygame.image.load("Image/w1.gif")
w2 = pygame.image.load("Image/w2.gif")
w3 = pygame.image.load("Image/w3.gif")
w4 = pygame.image.load("Image/w4.gif")
w5 = pygame.image.load("Image/w5.gif")
w6 = pygame.image.load("Image/w6.gif")
w7 = pygame.image.load("Image/w7.gif")
w8 = pygame.image.load("Image/w8.gif")
w9 = pygame.image.load("Image/w9.gif")

#條
t1 = pygame.image.load("Image/t1.gif")
t2 = pygame.image.load("Image/t2.gif")
t3 = pygame.image.load("Image/t3.gif")
t4 = pygame.image.load("Image/t4.gif")
t5 = pygame.image.load("Image/t5.gif")
t6 = pygame.image.load("Image/t6.gif")
t7 = pygame.image.load("Image/t7.gif")
t8 = pygame.image.load("Image/t8.gif")
t9 = pygame.image.load("Image/t9.gif")

#餅
b1 = pygame.image.load("Image/b1.gif")
b2 = pygame.image.load("Image/b2.gif")
b3 = pygame.image.load("Image/b3.gif")
b4 = pygame.image.load("Image/b4.gif")
b5 = pygame.image.load("Image/b5.gif")
b6 = pygame.image.load("Image/b6.gif")
b7 = pygame.image.load("Image/b7.gif")
b8 = pygame.image.load("Image/b8.gif")
b9 = pygame.image.load("Image/b9.gif")

#東南西北中發白
E = pygame.image.load("Image/E.gif")
S = pygame.image.load("Image/S.gif")
W = pygame.image.load("Image/W.gif")
N = pygame.image.load("Image/N.gif")
C = pygame.image.load("Image/C.gif")
F = pygame.image.load("Image/F.gif")
P = pygame.image.load("Image/P.gif")

#背面
back0 = pygame.image.load("Image/back0.gif")
back1 = pygame.image.load("Image/back1.gif")
back2 = pygame.image.load("Image/back2.gif")
back3 = pygame.image.load("Image/back3.gif")

# 背景
background = pygame.image.load("Image/background.jpg")

imgDict = {'萬1': w1, '萬2': w2, '萬3': w3, '萬4': w4, '萬5': w5, '萬6': w6, '萬7': w7, '萬8': w8, '萬9': w9, 
           '條1': t1, '條2': t2, '條3': t3, '條4': t4, '條5': t5, '條6': t6, '條7': t7, '條8': t8, '條9': t9, 
           '餅1': b1, '餅2': b2, '餅3': b3, '餅4': b4, '餅5': b5, '餅6': b6, '餅7': b7, '餅8': b8, '餅9': b9, 
           'E': E, 'S': S, 'W': W, 'N': N, 'C': C, 'F': F, 'P': P, 'back0': back0, 'back1': back1, 
           'back2': back2, 'back3': back3}