import pygame 
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
cream = pygame.Color(235,230,208)
green = pygame.Color(0,80,0)
grey = pygame.Color(84,84,84,200)
from pygame.locals import *
import copy
Radius = 75/2
bKingSquare = 4
wKingSquare = 60
wCastle = True
bCastle = True
bKingCheck = False
wKingCheck = False
circle = pygame.Surface((Radius*2, Radius*2), pygame.SRCALPHA)
surface = None
class enemyMoveListClass():
    ## this class stores all the enemy moves, in an array keeping track of how many times the enemy can move to a given square
    def __init__(self):
        self.moves = []
        for i in range(64):
            self.moves.append(0)
    def reset(self):
        for i in range(63):
            self.moves[i] = 0
    def add(self,num):
        if(num < 64 and num > -1):
            self.moves[num] = self.moves[num] + 1
    def find(self,num):
        return self.moves[num]
enemyMoveList = enemyMoveListClass()
class piece():
    def __init__(self):
        self.color = None
        pass
    def place(self, surface, x, y):
        surface.blit(self.image,(x,y))
    def validMoves(self,x,y,layout,surface):
        #returns a 2d array of pairs that are available to be moved to
        return None
    def name(self):
        return None
    def thisPieceCanMove(self,x,y,layout,surface,enemies):
        return self.validMoves(x, y, layout, surface)


##king

class king(piece):
    def __init__(self):
        super().__init__()
        self.value = 50
        #self.value = 1000
    def name(self):
        return "King"
    def validMoves(self,x,y,layout,surface):
        enemies = []
        moves = []
        #check each square indidually aginst the hashset containing possible enemy moves
        #may be worth optimizing by creating new method the test specifacally towards the king and add
        #those moves, pruning at each step; will add later
        if x < 7:
            if y < 7:
                if safeForKingMove(self,[x+1,y+1],[x,y],layout,surface):
                    if layout[(x+1)+(y+1)*8].name() != "Empty":
                        if layout[(x+1)+(y+1)*8].color != self.color:
                            enemies.append([x+1,y+1])
                    else:
                        moves.append([x+1,y+1])
            if y > 0:
                if safeForKingMove(self,[x+1,y-1],[x,y],layout,surface):
                    if layout[(x+1)+(y-1)*8].name() != "Empty":
                        if layout[(x+1)+(y-1)*8].color != self.color:
                            enemies.append([x+1,y-1])
                    else:
                        moves.append([x+1,y-1])
            if safeForKingMove(self,[x+1,y],[x,y],layout,surface):
                if layout[(x+1)+(y)*8].name() != "Empty":
                    if layout[(x+1)+(y)*8].color != self.color:
                        enemies.append([x+1,y])
                else:
                    moves.append([x+1,y])
        if x > 0:
            if y < 7:
                if safeForKingMove(self,[x-1,y+1],[x,y],layout,surface):
                    if layout[(x-1)+(y+1)*8].name() != "Empty":
                        if layout[(x-1)+(y+1)*8].color != self.color:
                            enemies.append([x-1,y+1])
                    else:
                        moves.append([x-1,y+1])
            if y > 0:
                if safeForKingMove(self,[x-1,y-1],[x,y],layout,surface):
                    if layout[(x-1)+(y-1)*8].name() != "Empty":
                        if layout[(x-1)+(y-1)*8].color != self.color:
                            enemies.append([x-1,y-1])
                    else:
                        moves.append([x-1,y-1])
            if safeForKingMove(self,[x-1,y],[x,y],layout,surface):
                if layout[(x-1)+(y)*8].name() != "Empty":
                    if layout[(x-1)+(y)*8].color != self.color:
                        enemies.append([x-1,y])
                else:
                    moves.append([x-1,y])
        if y < 7:
            if safeForKingMove(self,[x,y+1],[x,y],layout,surface):
                if layout[(x)+(y+1)*8].name() != "Empty":
                    if layout[(x)+(y+1)*8].color != self.color:
                        enemies.append([x,y+1])
                else:
                    moves.append([x,y+1]) 
        if y > 0:
            if safeForKingMove(self,[x,y-1],[x,y],layout,surface):
                if layout[(x)+(y-1)*8].name() != "Empty":
                    if layout[(x)+(y-1)*8].color != self.color:
                        enemies.append([x,y-1])
                else:
                    moves.append([x,y-1])
        moves += enemies
        return moves

class wKing(king):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("whiteKing.png"),(75,75))
        self.color = white
        self.canCastle = True
        self.check = False
#wKing = wKing()
class bKing(king):
    def __init__(self):
        super().__init__()
        self.color = black
        self.image = pygame.transform.scale(pygame.image.load("blackKing.png"),(75,75))
        self.canCastle = True
        self.check = False
#bKing = bKing()


##pawn

class pawn(piece):
    def __init__(self):
        super().__init__()
        self.value = 1
    def name(self):
        return "Pawn"

class wPawn(pawn):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("whitePawn.png"),(75,75))
        self.color = white
        
    def validMoves(self,x,y, layout,surface):
        moves = []
        #first chech if pawn has not yet moved by checking if in 7th row
        if y == 6:
            if layout[x + 5*8].name() == "Empty":
                moves.append([x,5])
                if layout[x + 4*8].name() == "Empty":
                    moves.append([x,4])
        else: 
            if layout[x + (y-1)*8].name() == "Empty":
                moves.append([x,y-1])
        return moves + self.potentialKillSpots(x,y,layout,surface)
    def killSpots(self,x,y,layout,surface):
        moves =[]
        if y > 0:
            if x < 7:
                if layout[x+1 + (y-1)*8].name() != "Empty" and (layout[x+1 + (y-1)*8].color != self.color):
                    if safe(self,[x+1,y-1],[x,y],layout,surface,None):
                        moves.append([x+1,y-1])
            if x > 0:
                if layout[x-1 + (y-1)*8].name() != "Empty" and (layout[x-1 + (y-1)*8].color != self.color):
                    if safe(self,[x-1,y-1],[x,y],layout,surface,None):
                        moves.append([x-1,y-1])
        return moves
    def potentialKillSpots(self,x,y,layout,surface):
        moves =[]
        if y > 0:
            if x < 7:
                moves.append([x+1,y-1])
            if x > 0:
                moves.append([x-1,y-1])
        return moves
    def thisPieceCanMove(self,x,y,layout,surface,enemies):
        enemies = None
        moves = []
        #first chech if pawn has not yet moved by checking if in 7th row
        if y == 6:
            if layout[x + 5*8].name() == "Empty":
                if safe(self,[x,5],[x,y],layout,surface,enemies):moves.append([x,5])
                if layout[x + 4*8].name() == "Empty":
                    if safe(self,[x,4],[x,y],layout,surface,enemies):moves.append([x,4])
        else: 
            if layout[x + (y-1)*8].name() == "Empty":
                if safe(self,[x,y-1],[x,y],layout,surface,enemies):moves.append([x,y-1])
        if y > 0:
            if x < 7:
                if layout[x+1 + (y-1)*8].name() != "Empty" and (layout[x+1 + (y-1)*8].color != self.color):
                    if safe(self,[x+1,y-1],[x,y],layout,surface,enemies):moves.append([x+1,y-1])
            if x > 0:
                if layout[x-1 + (y-1)*8].name() != "Empty" and (layout[x-1 + (y-1)*8].color != self.color):
                    if safe(self,[x+1,y-1],[x,y],layout,surface,enemies):moves.append([x-1,y-1])
        return moves + self.killSpots(x,y,layout,surface)

class bPawn(pawn):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("blackPawn.png"),(75,75))
        self.color = black
    def killSpots(self,x,y,layout,surface):
        moves = []
        if y < 7:
            if x < 7:
                if layout[x+1 + (y+1)*8].name() != "Empty" and (layout[x+1 + (y+1)*8].color != self.color):
                    if safe(self,[x+1,y+1],[x,y],layout,surface,None):
                        moves.append([x+1,y+1])
            if x > 0:
                if layout[x-1 + (y+1)*8].name() != "Empty" and (layout[x-1 + (y+1)*8].color != self.color):
                    if safe(self,[x-1,y+1],[x,y],layout,surface,None):
                        moves.append([x-1,y+1])
        return moves
    def validMoves(self,x,y, layout,surface):
        moves = []
        if y == 1: 
            if layout[x + 2*8].name() == "Empty":
                moves.append([x,2])
                if layout[x + 3*8].name() == "Empty":
                    moves.append([x,3])
        else: 
            if layout[x + (y+1)*8].name() == "Empty":
                moves.append([x,y+1])
        return moves + self.potentialKillSpots(x,y,layout,surface)
    def potentialKillSpots(self,x,y,layout,surface):
        moves = []
        if y < 7:
            if x < 7:
                moves.append([x+1,y+1])
            if x > 0:
                moves.append([x-1,y+1])
        return moves
    def thisPieceCanMove(self,x,y,layout,surface,enemies):
        moves = []
        enemies = None
        if y == 1: 
            if layout[x + 2*8].name() == "Empty":
                if safe(self,[x,2],[x,y],layout,surface,enemies): moves.append([x,2])
                if layout[x + 3*8].name() == "Empty":
                    if safe(self,[x,3],[x,y],layout,surface,enemies): moves.append([x,3])
        else: 
            if layout[x + (y+1)*8].name() == "Empty":
                if safe(self,[x,y+1],[x,y],layout,surface,enemies): moves.append([x,y+1])
        if x < 7:
            if layout[x+1 + (y+1)*8].name() != "Empty" and (layout[x+1 + (y+1)*8].color != self.color):
                if safe(self,[x+1,y+1],[x,y],layout,surface,enemies): moves.append([x+1,y+1])
        if x > 0:
            if layout[x-1 + (y+1)*8].name() != "Empty" and (layout[x-1 + (y+1)*8].color != self.color):
                if safe(self,[x-1,y+1],[x,y],layout,surface,enemies): moves.append([x-1,y+1])
        return moves + self.killSpots(x,y,layout,surface)
        

#bPawn = bPawn()


##rook

class rook(piece):
    def __init__(self):
        super().__init__()
        self.value = 5
    def name(self):
        return "Rook"
    def validMoves(self,x,y,layout,surface):
        return rookMoveChecks(self,x,y,layout,surface)
    def thisPieceCanMove(self,x,y,layout,surface,enemies):
        return rookMoveChecksMainPiece(self, x, y, layout, surface)

class wRook(rook):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("whiteRook.png"),(75,75))
        self.color = white
    #moves are the same for both rooks, may have to edit when i add removing peices
#wRook = wRook()
class bRook(rook):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("blackRook.png"),(75,75))
        self.color = black
#bRook = bRook()

##queen

class queen(piece):
    def __init__(self):
        super().__init__()
        self.value = 10
    def name(self):
        return "Queen"
    def validMoves(self,x,y,layout,surface):
        return diagonalChecks(self,x,y,layout,surface) + rookMoveChecks(self,x,y,layout,surface)
    def thisPieceCanMove(self,x,y,layout,surface,enemies):
        return diagonalChecksMainPiece(self, x, y, layout, surface) + rookMoveChecksMainPiece(self,x,y,layout,surface)

class wQueen(queen):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("whiteQueen.png"),(75,75))
        self.color = white
#wQueen = wQueen()
class bQueen(queen):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("blackQueen.png"),(75,75))
        self.color = black
#bQueen = bQueen()

##bishop

class bishop(piece):
    def __init__(self):
        super().__init__()
        self.value = 3
    def name(self):
        return "Bishop"
    def validMoves(self,x,y,layout,surface):
        return diagonalChecks(self,x,y,layout,surface)
    def thisPieceCanMove(self,x,y,layout,surface,enemies):
        return diagonalChecksMainPiece(self, x, y, layout, surface)

class wBishop(bishop):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("whiteBishop.png"),(75,75))
        self.color = white
#wBishop = wBishop()
class bBishop(bishop):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("blackBishop.png"),(75,75))
        self.color = black
#bBishop = bBishop()

##knight

class knight(piece):
    def __init__(self):
        super().__init__()
        self.value = 3
    def name(self):
        return "Knight"
    def validMoves(self,x,y,layout,sruface):
        return knightMoves(self,x,y,layout,surface)
    def thisPieceCanMove(self,x,y,layout,surface,enemies):
        return knightMovesMainPiece(self, x, y, layout, surface)

class wKnight(knight):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("whiteKnight.png"),(75,75))
        self.color = white
#wKnight = wKnight()
class bKnight(knight):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("blackKnight.png"),(75,75))
        self.color = black
#bKnight = bKnight()

#empty

class emptyPiece(piece):
    def __init__(self):
        super().__init__()
        self.value = 0
        self.image = False
    def place(self,surface,x,y):
        pass
    def name(self):
        return "Empty"
#used for queen and bishop, checking empty squares on the four diagnols, stop on edge or peice, if enemy 
#peice, while circle returns list of vaible moves, enemys always at the end 2d array
def diagonalChecks(self,x,y,layout,surface):
    moves = []
    enemies = []
    r = y
    for c in range(x-1,-1,-1):
        r-= 1
        if(r < 0):
            break
        if(layout[c + r*8].name() != "Empty"):
            enemies.append(enemyCheck(self,c,r,layout,surface))
            break
        moves.append([c,r])
    r = y
    for c in range(x-1,-1,-1):
        r+=1
        if(r > 7):
            break
        if(layout[c +r*8].name() != "Empty"):
            enemies.append(enemyCheck(self,c,r,layout,surface))
            break
        moves.append([c,r])

    r = y
    for c in range(x+1,8,+1):
        r -=1
        if(r < 0):
            break
        if(layout[c + r*8].name() != "Empty"):
            enemies.append(enemyCheck(self,c,r,layout,surface))
            break
        moves.append([c,r])
    r = y
    for c in range(x+1,8,+1):
        r +=1
        if(r > 7):
            break
        if(layout[c + r*8].name() != "Empty"):
            enemies.append(enemyCheck(self,c,r,layout,surface))
            break
        moves.append([c,r])
    while None in enemies:
        enemies.remove(None)
    return moves + enemies
#only need to check the oppents moves for the piece that is clicked on, big optimization
#cannot figure out how to maximaze efficency without re doing alot or reusing code, should have planned ahead and proofed for this
def diagonalChecksMainPiece(self,x,y,layout,surface):
    enemyMoves = None # enemyMoveCheker(self, layout, None,None)
    moves = []
    enemies = []
    r = y
    for c in range(x-1,-1,-1):
        r-= 1
        if(r < 0):
            break
        if(layout[c + r*8].name() != "Empty"):
            if safe(self,[c,r],[x,y],layout,surface,enemyMoves): enemies.append(enemyCheck(self,c,r,layout,surface))
            break
        if safe(self,[c,r],[x,y],layout,surface,enemyMoves):  moves.append([c,r])
    r = y
    for c in range(x-1,-1,-1):
        r+=1
        if(r > 7):
            break
        if(layout[c +r*8].name() != "Empty"):
            if safe(self,[c,r],[x,y],layout,surface,enemyMoves): enemies.append(enemyCheck(self,c,r,layout,surface))
            break
        if safe(self,[c,r],[x,y],layout,surface,enemyMoves): moves.append([c,r])

    r = y
    for c in range(x+1,8,+1):
        r -=1
        if(r < 0):
            break
        if(layout[c + r*8].name() != "Empty"):
            if safe(self,[c,r],[x,y],layout,surface,enemyMoves): enemies.append(enemyCheck(self,c,r,layout,surface))
            break
        if safe(self,[c,r],[x,y],layout,surface,enemyMoves): moves.append([c,r])
    r = y
    for c in range(x+1,8,+1):
        r +=1
        if(r > 7):
            break
        if(layout[c + r*8].name() != "Empty"):
            if safe(self,[c,r],[x,y],layout,surface,enemyMoves): enemies.append(enemyCheck(self,c,r,layout,surface))
            break
        if safe(self,[c,r],[x,y],layout,surface,enemyMoves): moves.append([c,r])
    while None in enemies:
        enemies.remove(None)
    return moves + enemies


def rookMoveChecks(self,x,y,layout,surface):
    moves =[]
    enemies =[]
    for c in range(x-1,-1,-1):
        if(layout[c + y*8].name() != "Empty"):
            enemies.append(enemyCheck(self,c,y,layout,surface))
            break
        moves.append([c,y])
    for c in range(x+1,8,+1):
        if(layout[c + y*8].name() != "Empty"):
            enemies.append(enemyCheck(self,c,y,layout,surface))
            break
        moves.append([c,y])
    for r in range(y+1,8,+1):
        if(layout[x + r*8].name() != "Empty"):
            enemies.append(enemyCheck(self,x,r,layout,surface))
            break
        moves.append([x,r])
    for r in range(y-1,-1,-1):
        if(layout[x + r*8].name() != "Empty"):
            enemies.append(enemyCheck(self,x,r,layout,surface))
            break
        moves.append([x,r])
    r = y
    while None in enemies:
        enemies.remove(None)
    return moves + enemies

def knightMoves(self,x,y,layout,surface):
    moves =[]
    enemies = []
    c = x+1
    r = y+2
    if c < 8 and r < 8:
        if layout[c + r*8].name() != "Empty":
            enemies.append(enemyCheck(self,c,r,layout,surface))
        else:
            moves.append([c,r])
    c = x-1
    r = y+2
    if c > -1 and r < 8:
        if layout[c + r*8].name() != "Empty":
            enemies.append(enemyCheck(self,c,r,layout,surface))
        else:
            moves.append([c,r])
    c = x+1
    r = y-2
    if c < 8 and r > -1:
        if layout[c + r*8].name() != "Empty":
            enemies.append(enemyCheck(self,c,r,layout,surface))
        else:
            moves.append([c,r])
    c = x-1
    r = y-2
    if c >-1  and r > -1:
        if layout[c + r*8].name() != "Empty":
            enemies.append(enemyCheck(self,c,r,layout,surface))
        else:
            moves.append([c,r])
    c = x+2
    r = y+1
    if c < 8 and r < 8:
        if layout[c + r*8].name() != "Empty":
            enemies.append(enemyCheck(self,c,r,layout,surface))
        else:
            moves.append([c,r])
    c = x-2
    r = y+1
    if c > -1 and r < 8:
        if layout[c + r*8].name() != "Empty":
            enemies.append(enemyCheck(self,c,r,layout,surface))
        else:
            moves.append([c,r])
    c = x+2
    r = y-1
    if c < 8 and r > -1:
        if layout[c + r*8].name() != "Empty":
            enemies.append(enemyCheck(self,c,r,layout,surface))
        else:
            moves.append([c,r])
    c = x-2
    r = y-1
    if c >-1  and r > -1:
        if layout[c + r*8].name() != "Empty":
            enemies.append(enemyCheck(self,c,r,layout,surface))
        else:
            moves.append([c,r])
    while None in enemies:
        enemies.remove(None)
    return moves + enemies

def knightMovesMainPiece(self,x,y,layout,surface):
    moves =[]
    enemies = []
    enemyMoves = None
    c = x+1
    r = y+2
    if c < 8 and r < 8:
        if layout[c + r*8].name() != "Empty":
            if safe(self,[c,r],[x,y],layout,surface,enemyMoves):enemies.append(enemyCheck(self,c,r,layout,surface))
        else:
            if safe(self,[c,r],[x,y],layout,surface,enemyMoves):moves.append([c,r])
    c = x-1
    r = y+2
    if c > -1 and r < 8:
        if layout[c + r*8].name() != "Empty":
            if safe(self,[c,r],[x,y],layout,surface,enemyMoves):enemies.append(enemyCheck(self,c,r,layout,surface))
        else:
            if safe(self,[c,r],[x,y],layout,surface,enemyMoves):moves.append([c,r])
    c = x+1
    r = y-2
    if c < 8 and r > -1:
        if layout[c + r*8].name() != "Empty":
            if safe(self,[c,r],[x,y],layout,surface,enemyMoves):enemies.append(enemyCheck(self,c,r,layout,surface))
        else:
            if safe(self,[c,r],[x,y],layout,surface,enemyMoves):moves.append([c,r])
    c = x-1
    r = y-2
    if c >-1  and r > -1:
        if layout[c + r*8].name() != "Empty":
            if safe(self,[c,r],[x,y],layout,surface,enemyMoves):enemies.append(enemyCheck(self,c,r,layout,surface))
        else:
            if safe(self,[c,r],[x,y],layout,surface,enemyMoves):moves.append([c,r])
    c = x+2
    r = y+1
    if c < 8 and r < 8:
        if layout[c + r*8].name() != "Empty":
            if safe(self,[c,r],[x,y],layout,surface,enemyMoves):enemies.append(enemyCheck(self,c,r,layout,surface))
        else:
            if safe(self,[c,r],[x,y],layout,surface,enemyMoves):moves.append([c,r])
    c = x-2
    r = y+1
    if c > -1 and r < 8:
        if layout[c + r*8].name() != "Empty":
            if safe(self,[c,r],[x,y],layout,surface,enemyMoves):enemies.append(enemyCheck(self,c,r,layout,surface))
        else:
            if safe(self,[c,r],[x,y],layout,surface,enemyMoves):moves.append([c,r])
    c = x+2
    r = y-1
    if c < 8 and r > -1:
        if layout[c + r*8].name() != "Empty":
            if safe(self,[c,r],[x,y],layout,surface,enemyMoves):enemies.append(enemyCheck(self,c,r,layout,surface))
        else:
            if safe(self,[c,r],[x,y],layout,surface,enemyMoves):moves.append([c,r])
    c = x-2
    r = y-1
    if c >-1  and r > -1:
        if layout[c + r*8].name() != "Empty":
            if safe(self,[c,r],[x,y],layout,surface,enemyMoves):enemies.append(enemyCheck(self,c,r,layout,surface))
        else:
            if safe(self,[c,r],[x,y],layout,surface,enemyMoves):moves.append([c,r])
    while None in enemies:
        enemies.remove(None)
    return moves + enemies
def rookMoveChecksMainPiece(self,x,y,layout,surface):
    moves =[]
    enemies =[]
    enemyMoves = None
    r = y
    for c in range(x-1,-1,-1):
        if(layout[c + y*8].name() != "Empty"):
            if safe(self,[c,r],[x,y],layout,surface,enemyMoves):enemies.append(enemyCheck(self,c,y,layout,surface))
            break
        if safe(self,[c,r],[x,y],layout,surface,enemyMoves):moves.append([c,y])
    for c in range(x+1,8,+1):
        if(layout[c + y*8].name() != "Empty"):
            if safe(self,[c,r],[x,y],layout,surface,enemyMoves):enemies.append(enemyCheck(self,c,y,layout,surface))
            break
        if safe(self,[c,r],[x,y],layout,surface,enemyMoves):moves.append([c,y])
    c = x
    for r in range(y+1,8,+1):
        if(layout[x + r*8].name() != "Empty"):
            if safe(self,[c,r],[x,y],layout,surface,enemyMoves):enemies.append(enemyCheck(self,x,r,layout,surface))
            break
        if safe(self,[c,r],[x,y],layout,surface,enemyMoves):moves.append([x,r])
    for r in range(y-1,-1,-1):
        if(layout[x + r*8].name() != "Empty"):
            if safe(self,[c,r],[x,y],layout,surface,enemyMoves):enemies.append(enemyCheck(self,x,r,layout,surface))
            break
        if safe(self,[c,r],[x,y],layout,surface,enemyMoves):moves.append([x,r])
    r = y
    while None in enemies:
        enemies.remove(None)
    return moves + enemies

def knightMoves(self,x,y,layout,surface):
    moves =[]
    enemies = []
    c = x+1
    r = y+2
    if c < 8 and r < 8:
        if layout[c + r*8].name() != "Empty":
            enemies.append(enemyCheck(self,c,r,layout,surface))
        else:
            moves.append([c,r])
    c = x-1
    r = y+2
    if c > -1 and r < 8:
        if layout[c + r*8].name() != "Empty":
            enemies.append(enemyCheck(self,c,r,layout,surface))
        else:
            moves.append([c,r])
    c = x+1
    r = y-2
    if c < 8 and r > -1:
        if layout[c + r*8].name() != "Empty":
            enemies.append(enemyCheck(self,c,r,layout,surface))
        else:
            moves.append([c,r])
    c = x-1
    r = y-2
    if c >-1  and r > -1:
        if layout[c + r*8].name() != "Empty":
            enemies.append(enemyCheck(self,c,r,layout,surface))
        else:
            moves.append([c,r])
    c = x+2
    r = y+1
    if c < 8 and r < 8:
        if layout[c + r*8].name() != "Empty":
            enemies.append(enemyCheck(self,c,r,layout,surface))
        else:
            moves.append([c,r])
    c = x-2
    r = y+1
    if c > -1 and r < 8:
        if layout[c + r*8].name() != "Empty":
            enemies.append(enemyCheck(self,c,r,layout,surface))
        else:
            moves.append([c,r])
    c = x+2
    r = y-1
    if c < 8 and r > -1:
        if layout[c + r*8].name() != "Empty":
            enemies.append(enemyCheck(self,c,r,layout,surface))
        else:
            moves.append([c,r])
    c = x-2
    r = y-1
    if c >-1  and r > -1:
        if layout[c + r*8].name() != "Empty":
            enemies.append(enemyCheck(self,c,r,layout,surface))
        else:
            moves.append([c,r])
    while None in enemies:
        enemies.remove(None)
    return moves + enemies

def drawCircle(x,y):
    Radius = 25
    circle = pygame.Surface((Radius*2, Radius*2), pygame.SRCALPHA)
    pygame.draw.circle(circle, grey, (Radius, Radius), Radius)
    surface.blit(circle,(x*75+Radius/2,y*75+Radius/2))
def hollowCircle(x,y):
    Radius = 75/2
    circle = pygame.Surface((Radius*2, Radius*2), pygame.SRCALPHA)
    pygame.draw.circle(circle, grey, (Radius, Radius), Radius,10)
    surface.blit(circle,(x*75,y*75))

def enemyCheck(self,x,y,layout,surface):
    if layout[x+y*8].color != self.color:
        return [x,y]
    return None
def numToSquare(num):
    return[num%8, int(num /8)] 

#could optimize slightly by pruning enemy squares, not worth it for just drawing 
def circlePlacer(array,color,layout,surface):
    if(array == None or len(array)==0):
        return
    for move in array:
        if layout[move[0]+move[1]*8].name() == "Empty":
            drawCircle(move[0],move[1])
        elif layout[move[0]+move[1]*8].color != color:
            hollowCircle(move[0],move[1])
#takes the piece for color, but sends piece for future proofing since i antipate having a seperate check for king at some point
#
"""def enemyMoveCheker(self,layout,move,orgin):
    if move != None:
        layout = copy.copy(layout)
        layout[move[0] + move[1]*8] = layout[orgin[0] + orgin[1]*8]
        layout[orgin[0] + orgin[1]*8] = emptyPiece()
    enemyMoves = set()
    i =0
    for piece in layout:
        if piece.color != self.color and piece.name() == "Pawn":
            moves = piece.potentialKillSpots(numToSquare(i)[0],numToSquare(i)[1],layout,surface)
            for move in moves:
                enemyMoves.add(move[0] + move[1]*8)
        elif piece.color != self.color and piece.name() == "King":
            moves = []
            square = numToSquare(i)
            x = square[0]
            y = square[1]
            if x < 7:
                if y < 7:
                    moves.append([x+1,y+1])
                if y > 0:
                    moves.append([x+1,y-1])
                moves.append([x+1,y])
            if x > 0:
                if y < 7:
                    moves.append([x-1,y+1])
                if y > 0:
                    moves.append([x-1,y-1])
                moves.append([x-1,y])
            if y < 7:
                moves.append([x,y+1]) 
            if y > 0:
                moves.append([x,y-1])
            for move in moves:
                enemyMoves.add(move[0]+move[1]*8)
        elif piece.color != self.color:
            square = numToSquare(i)
            tempMove = piece.validMoves(square[0],square[1],layout,surface)
            if tempMove:
                for move in tempMove:
                    enemyMoves.add(move[0]+move[1]*8)
        i+=1
    return enemyMoves"""
## original enemy move checker, for better efficency i will now create a hashmap so it keeps tack of times a square can be moved to 
## this will greatly boost the efficency of checking legal moves

        
#return array of times each square can be moved to by enemy, can also accept a move and orgin to check what will happen after a certain move
def enemyMoveCheker(self,layout,move,orgin):
    if move != None:
        layout = copy.copy(layout)
        layout[move[0] + move[1]*8] = layout[orgin[0] + orgin[1]*8]
        layout[orgin[0] + orgin[1]*8] = emptyPiece()
    enemyMoveList.reset()
    i =0
    for piece in layout:
        if piece.color != self.color and piece.name() == "Pawn":
            moves = piece.potentialKillSpots(numToSquare(i)[0],numToSquare(i)[1],layout,surface)
            for move in moves:
                enemyMoveList.add(move[0] + move[1]*8)
        elif piece.color != self.color and piece.name() == "King":
            # will get stuck in loop, does not allow king to move withing one square of the other king
            moves = []
            square = numToSquare(i)
            x = square[0]
            y = square[1]
            if x < 7:
                if y < 7:
                    moves.append([x+1,y+1])
                if y > 0:
                    moves.append([x+1,y-1])
                moves.append([x+1,y])
            if x > 0:
                if y < 7:
                    moves.append([x-1,y+1])
                if y > 0:
                    moves.append([x-1,y-1])
                moves.append([x-1,y])
            if y < 7:
                moves.append([x,y+1]) 
            if y > 0:
                moves.append([x,y-1])
            for move in moves:
                enemyMoveList.add(move[0]+move[1]*8)
        elif piece.color != self.color:
            square = numToSquare(i)
            tempMove = piece.validMoves(square[0],square[1],layout,surface)
            if tempMove:
                for move in tempMove:
                    enemyMoveList.add(move[0]+move[1]*8)
        i+=1
    return enemyMoveList.moves
def safe(piece,move,orgin,layout,surface,enemies):
    #passing in enemies is only down when checking moves, would save time to check once
    if enemies == None:
        enemies = enemyMoveCheker(piece, layout,move,orgin)
    copyLayout =  copy.copy(layout)
    #creating a tempory layout to check if the king is safe from check after this move
    copyLayout[orgin[0] + orgin[1]*8] = emptyPiece()
    copyLayout[move[0] + move[1]*8] = piece
    if piece.color == white:
        if enemies[wKingSquare] != 0:
            return False
        return True
    if enemies[bKingSquare] != 0:
        return False
    return True
def safeForKingMove(piece,move,orgin,layoutCopy,surface):
    layout =  copy.copy(layoutCopy)
    enemies = enemyMoveCheker(piece, layout,move,orgin)
    #creating a tempory layout to check if the king is safe from check after this move
    if piece.color == white:
        if enemies[move[0]+move[1]*8] != 0:
            return False
        return True
    if enemies[move[0]+move[1]*8] != 0:
        return False
    return True
def bKingMove(num):
    bCastle = False
    bKingSquare = num
def wKingMove(num):
    wCastle = False
    wKingSquare = num


