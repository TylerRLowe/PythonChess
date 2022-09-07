#the piece can by found in the array by using board.layout[x+y*8] when represents the square\
import pygame
import Piece
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
cream = pygame.Color(235,230,208)
green = pygame.Color(0,80,0)
lightBlue = pygame.Color(0,50,200)
blue = pygame.Color(72,166,255)
grey = pygame.Color(84,84,84,200)
pygame.init()
font = pygame.font.Font(None, 70)
text = font.render('White wins: checkmate', True, pygame.Color(0,0,0), pygame.Color(255,255,255))
textRect = text.get_rect()
textRect.center = (300,300)
knightPoints = [-.50,-.40,-.30,-.30,-.30,-.30,-.40,-.50,
    -.40,-.20,  0,  0,  0,  0,-.20,-.40,
    -.30,  0, .10, .15, .15, .10,  0,-.30,
    -.30,  .05, .15, .20, .20, .15,  .05,-.30,
    -.30,  0, .15, .20, .20, .15,  0,-.30,
    -.30,  .05, .10, .15, .15, .10,  .05,-.30,
    -.40,-.20,  0,  .05,  .05,  0,-.20,-.40,
    -.50,-.40,-.20,-.30,-.30,-.20,-.40,-.50]
whitePawnPoints = [0,  0,  0,  0,  0,  0,  0,  0,
    .50, .50, .50, .50, .50, .50, .50, .50,
    .10, .10, .20, .30, .30, .20, .10, .10,
     .05,  .05, .10, .27, .27, .10,  .05,  .05,
     0,  0,  0, .25, .25,  0,  0,  0,
     .05, -.05,-.10,  0,  0,-.10, -.05,  .05,
     .05, .10, .10,-.25,-.25, .10, .10,  .05,
     0,  0,  0,  0,  0,  0,  0,  0]
kingPoints = [ -.30, -.40, -.40, -.50, -.50, -.40, -.40, -.30,
  -.30, -.40, -.40, -.50, -.50, -.40, -.40, -.30,
  -.30, -.40, -.40, -.50, -.50, -.40, -.40, -.30,
  -.30, -.40, -.40, -.50, -.50, -.40, -.40, -.30,
  -.20, -.30, -.30, -.40, -.40, -.30, -.30, -.20,
  -.10, -.20, -.20, -.20, -.20, -.20, -.20, -.10, 
   .20,  .20,   0,   0,   0,   0,  .20,  .20,
   .20,  .30,  .10,   0,   0,  .10,  .30,  .20]
lateKingPoints = [-.50,-.40,-.30,-.20,-.20,-.30,-.40,-.50,
    -.30,-.20,-.10,  0,  0,-.10,-.20,-.30,
    -.30,-.10, .20, .30, .30, .20,-.10,-.30,
    -.30,-.10, .30, .40, .40, .30,-.10,-.30,
    -.30,-.10, .30, .40, .40, .30,-.10,-.30,
    -.30,-.10, .20, .30, .30, .20,-.10,-.30,
    -.30,-.30,  0,  0,  0,  0,-.30,-.30,
    -.50,-.30,-.30,-.30,-.30,-.30,-.30,-.50]
class board:
    def __init__(self,surface):
        self.surface = surface
        self.whiteValue = 1039.2
        self.blackValue = 1039.2

    def layout(self):
        pass
    def create(self,hasPieceSelected,pieceSelectedLocation):
        x = 0
        y = 0
        #wiping the screen (removes previous pieces)
        self.surface.fill(blue)
        for i in range(32):
            if x == 600:
                y +=75
                x = 75
            elif x == 675:
                x = 0
                y+=75
            pygame.draw.rect(self.surface,cream,(x,y,75,75))
            x += 150
        if hasPieceSelected:
            #yellow square is an array that carries the x and y square; multiplying by 75 gives pos
            #circles show where the player can move
            xSquare = pieceSelectedLocation[0]
            ySquare = pieceSelectedLocation[1]
            pygame.draw.rect(self.surface,lightBlue,(xSquare*75,ySquare*75,75,75))
            moves = self.layout[xSquare+ySquare*8].thisPieceCanMove(xSquare,ySquare,self.layout,self.surface,None)
            Piece.circlePlacer(moves,self.layout[xSquare + ySquare*8].color,self.layout,self.surface)          
        self.populate()
         ##placing the pieces
    def populate(self):
        x=0
        y=0
        for placer in self.layout:
            placer.place(self.surface,x,y)
            x += 75
            if(x == 600):
                x = 0 
                y +=75
    def comCheckMate(self):
        self.surface.blit(text, textRect)
def score(layout,color):
    #this can be called to iterate through the board and find the vlaue of each piece
    #will probably instead manually change the score of the layout when the computer moves for search purposes
    #after more thinking this may be a useless method but atleaast i can use it at the start to avoid
    #manually calculating
    whiteScore = 0
    blackScore = 0
    pointsWhiteKingSquare = 0 
    i = 0
    pointsBlackKingSquare = 0
    for piece in layout:
        if piece.name() == "Empty":
            pass
        elif piece.color == white:
            if piece.name() == "Knight":
                whiteScore += knightPoints[i]
            elif piece.name() == "Pawn":
                whiteScore += whitePawnPoints[i]
            elif piece.name() == "King":
                pointsWhiteKingSquare = i
            whiteScore += piece.value
        elif piece.color == black:
            if piece.name() == "Knight":
                blackScore += knightPoints[i]
            elif piece.name() == "Pawn":
                blackScore += whitePawnPoints[63-i]
            elif piece.name() == "King":
                pointsBlackKingSquare = i
            blackScore += piece.value
        i +=1
    if blackScore + whiteScore < 40:
        blackScore += lateKingPoints[63-pointsBlackKingSquare]
        whiteScore += lateKingPoints[pointsWhiteKingSquare]
    else:
        blackScore += kingPoints[63-pointsBlackKingSquare]
        whiteScore += kingPoints[pointsWhiteKingSquare]
    if color == black:
        return blackScore - whiteScore