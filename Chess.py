import pygame 
import piece
from pygame.locals import *
import Engine
import board
pygame.init()
surface = pygame.display.set_mode((600,600))
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
cream = pygame.Color(235,230,208)
green = pygame.Color(0,80,0)
lightBlue = pygame.Color(230,255,60)
blue = pygame.Color(0,0,225)
grey = pygame.Color(84,84,84,200)
surface.fill(green)
pygame.display.set_caption("Chess")
FPS = 60
FramePerSec = pygame.time.Clock()
piece.surface = surface
hasPieceSelected= False
pieceSelectedLocation =[]
playerTurn = True
Check = False
# pices
Radius = 25
circle = pygame.Surface((Radius*2, Radius*2), pygame.SRCALPHA)
bRook = piece.bRook()
bKnight = piece.bKnight()
bBishop = piece.bBishop()
bQueen = piece.bQueen()
bKing = piece.bKing()
bPawn = piece.bPawn()
empty = piece.empty()
wRook = piece.wRook()
wKnight = piece.wKnight()
wBishop= piece.wBishop()
wQueen = piece.wQueen()
wKing = piece.wKing()
wPawn = piece.wPawn()
        
board = board.board(surface)   
board.layout = [bRook,bKnight,bBishop,bQueen,bKing,bBishop,bKnight,bRook]
for i in range(8):
    board.layout.append(bPawn)
for i in range(10):
    board.layout.append(empty)
board.layout.append(wKing)
for i in range(21):
    board.layout.append(empty)
for i in range(8):
    board.layout.append(wPawn)
board.layout += [wRook,wKnight,wBishop,wQueen,wKing,wBishop,wKnight,wRook]
##game
piece = empty
board.create(hasPieceSelected,[])



while True:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        held = pygame.mouse.get_pressed()
        mouse = pygame.mouse.get_pos()
        trueX = mouse[0]
        trueY = mouse[1]
        x = round((trueX - 32.5) / 75) 
        y = round((trueY - 32.5) / 75) 
        #converting from the x and y coords, into the square that is located there
        #this allows accsess to the underlying array
        if playerTurn == False:
            engine.move(board.layout)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            spot = board.layout[x + y*8]
            if spot != empty and spot.color != black:
                hasPieceSelected = True
                #yellow square designates the square the person has selected; and will
                #stay yellow untill they pick another square or complete a move
                board.create(hasPieceSelected,[x,y])

            
    #pygame.draw.circle(DISPLAYSURF,BLACK,(0,0),500)
    x = 0
    y = 0
    

    #end of frame
    
    FramePerSec.tick(FPS)


        