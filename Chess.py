import pygame 
import Piece
from pygame.locals import *
import Engine
import board
pygame.init()
font = pygame.font.Font('freesansbold.ttf', 32)
surface = pygame.display.set_mode((600,600))
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
cream = pygame.Color(235,230,208)
green = pygame.Color(0,80,0)
lightBlue = pygame.Color(0,50,200)
blue = pygame.Color(0,0,225)
grey = pygame.Color(84,84,84,200)
surface.fill(green)
pygame.display.set_caption("Chess")
FPS = 60
pygame.font.init() 
my_font = pygame.font.SysFont('Comic Sans MS', 30)
Piece.surface = surface
FramePerSec = pygame.time.Clock()
hasPieceSelected= False
playerTurn = True
check = False
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('CheckMate', True, pygame.Color(0,0,0), pygame.Color(255,255,255))
textRect = text.get_rect()
textRect.center = (350,350)
# pices
Radius = 25
circle = pygame.Surface((Radius*2, Radius*2), pygame.SRCALPHA)
bRook = Piece.bRook()
bKnight = Piece.bKnight()
bBishop = Piece.bBishop()
bQueen = Piece.bQueen()
bKing = Piece.bKing()
bPawn = Piece.bPawn()
empty = Piece.emptyPiece()
wRook = Piece.wRook()
wKnight = Piece.wKnight()
wBishop= Piece.wBishop()
wQueen = Piece.wQueen()
wKing = Piece.wKing()
wPawn = Piece.wPawn()      
board = board.board(surface)  
Piece.surface = surface
#layout could be 2d array to more easily convert to squares, but harder to traverse
#I went with 1d array, but in hindsight a 2d array may be easier to deal with
board.layout = [bRook,bKnight,bBishop,bQueen,bKing,bBishop,bKnight,bRook]
for i in range(8):
    board.layout.append(bPawn)
for i in range(32):
    board.layout.append(empty)

for i in range(8):
    board.layout.append(wPawn)
board.layout += [wRook,wKnight,wBishop,wQueen,wKing,wBishop,wKnight,wRook]
##game
piece = empty
font = pygame.font.Font('freesansbold.ttf', 32)
playing = True
def main():
    hasPieceSelected= False
    playerTurn = True
    playerColor = white
    debug = start()
    board.create(hasPieceSelected,[])
    while playing:
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
            if playerTurn == False and debug == False:
                board.layout = Engine.move(board.layout,black)
                if board.layout == "error":
                    board.comCheckMate()
                    pygame.display.update()
                    pause()
                board.create(hasPieceSelected,selectedPieceLocation)
                playerTurn = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if y > 7 or y < 0 or x > 7 or x < 0:
                    pass
                else:
                    piece = board.layout[x + y*8]
                    #in debug, player controls both sides
                    if piece.name() != "Empty" and (piece.color == playerColor or debug ==True):
                        hasPieceSelected = True
                        #yellow square designates the square the person has selected; and will
                        #stay yellow untill they pick another square or complete a move
                        board.create(hasPieceSelected,[x,y])
                        selectedPiece = board.layout[x+y*8]
                        selectedPieceLocation = [x,y]
                    elif hasPieceSelected and [x,y] in selectedPiece.thisPieceCanMove(selectedPieceLocation[0],selectedPieceLocation[1],board.layout,surface,None):
                        playerTurn = False
                        hasPieceSelected = False
                        board.layout[selectedPieceLocation[0]+selectedPieceLocation[1]*8] = empty
                        selectedPieceLocation=[]
                        #auto queens on a pawn getting to the other side
                        if selectedPiece.name() == "Pawn" and x + y*8 <= 7 and selectedPiece.color ==white:
                            selectedPiece = wQueen
                        if selectedPiece.name() == "Pawn" and x == 1 and selectedPiece.color ==white and debug == True:
                            selectedPiece = bQueen
                        board.layout[x + y*8] = selectedPiece
                        if selectedPiece.name() == "King" and selectedPiece.color == white:
                            Piece.wKingSquare = x + y*8
                        if selectedPiece.name() == "King" and selectedPiece.color == black and debug == True:
                            Piece.bKingSquare = x + y*8
                        board.create(hasPieceSelected, selectedPieceLocation)
                    


                
        #pygame.draw.circle(DISPLAYSURF,BLACK,(0,0),500)
        x = 0
        y = 0
        

        #end of frame
        
        FramePerSec.tick(FPS)

def pause():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
def start():
    while playing:
        surface.fill(black)
        pygame.draw.rect(surface,pygame.Color(72,166,255),(100,100,400,400))
        text = font.render('Main Menu', True, lightBlue, cream)
        pygame.draw.rect(surface,  pygame.Color(235,230,208),(100,150,400,32))
        rect = text.get_rect()
        rect.center = (300,166)
        surface.blit(text,rect)
        text = font.render('Start', True, lightBlue, cream)
        pygame.draw.rect(surface,  pygame.Color(235,230,208),(250,250,100,32))
        rect = text.get_rect()
        rect.center = (300,266)
        surface.blit(text,rect)
        text = font.render('Debug', True, lightBlue, cream)
        pygame.draw.rect(surface,  pygame.Color(235,230,208),(250,350,100,32))
        rect = text.get_rect()
        rect.center = (300,366)
        surface.blit(text,rect)
        pygame.display.update()
        held = pygame.mouse.get_pressed()
        mouse = pygame.mouse.get_pos()
        trueX = mouse[0]
        trueY = mouse[1]
        x = round((trueX - 32.5) / 75) 
        y = round((trueY - 32.5) / 75) 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if y > 7 or y < 0 or x > 7 or x < 0:
                    pass
                else:
                    #if the x coord of the mouse is withen the start or debug box
                    if trueX <=350 and trueX >= 250:
                        #checking if y in start box returning to the game if true
                        if trueY <= 282 and trueY >= 250:
                            return False
                        #Enterting debug mode if debug is hit
                        if trueY <=382 and trueY >=350:
                            return True
    

if __name__ == "__main__":
    main()