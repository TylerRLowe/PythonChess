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
class board:
    def __init__(self,surface):
        self.surface = surface
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
            moves = self.layout[xSquare+ySquare*8].validMoves(xSquare,ySquare,self.layout,self.surface)
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