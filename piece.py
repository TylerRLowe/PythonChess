import pygame 
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
cream = pygame.Color(235,230,208)
green = pygame.Color(0,80,0)
grey = pygame.Color(84,84,84,200)
from pygame.locals import *
Radius = 75/2
circle = pygame.Surface((Radius*2, Radius*2), pygame.SRCALPHA)
surface = None
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


##king

class king(piece):
    def __init__(self):
        super().__init__()
        self.value = 1000
    def name(self):
        return "King"
    def validMoves(self,x,y,layout,surface):
        enemyMoves = set()
        enemies = []
        moves = []
        i = 0
        for piece in layout:
            if piece.color != self.color and piece.name == "Pawn":
                pass
            elif piece.color != self.color and piece.name() != "King":
                square = numToSquare(i)
                tempMove = piece.validMoves(square[0],square[1],layout,surface)
                for move in tempMove:
                    enemyMoves.add(move[0]+move[1]*8)
            i+=1
        #check each square indidually aginst the hashset containing possible enemy moves
        #may be worth optimizing by creating new method the test specifacally towards the king and add
        #those moves, pruning at each step; will add later
        if x < 7:
            if y < 7:
                if (x+y*8) in enemyMoves:
                    pass
                elif layout[(x+1)+(y+1)*7].name() != "Empty":
                    if layout[(x+1),(y+1)].color != this.color:
                        enemies.append([x+1,y+1])
                else:
                    moves.append([x+1,y+1])
        while None in enemies:
            enemies.remove(None)
        return moves + enemies

class wKing(king):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("whiteKing.png"),(75,75))
        self.color = white
#wKing = wKing()
class bKing(king):
    def __init__(self):
        super().__init__()
        self.color = black
        self.image = pygame.transform.scale(pygame.image.load("blackKing.png"),(75,75))
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
        elif y == 1:
            #make this upgrade pawn to queen
            pass
        else: 
             if layout[x + (y-1)*8].name() == "Empty":
                moves.append([x,y-1])
        return moves
#wPawn = wPawn()
class bPawn(pawn):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("blackPawn.png"),(75,75))
        self.color = black
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
        value = 3
    def name(self):
        return "Knight"
    def validMoves(self,x,y,layout,sruface):
        return knightMoves(self,x,y,layout,surface)

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

class empty(piece):
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
def diagonalChecks(this,x,y,layout,surface):
    moves = []
    enemies = []
    r = y
    for c in range(x-1,-1,-1):
        r-= 1
        if(r < 0):
            break
        if(layout[c + r*8].name() != "Empty"):
            enemies.append(enemyCheck(this,c,r,layout,surface))
            break
        moves.append([c,r])
    r = y
    for c in range(x-1,-1,-1):
        r+=1
        if(r > 7):
            break
        if(layout[c +r*8].name() != "Empty"):
            enemies.append(enemyCheck(this,c,r,layout,surface))
            break
        moves.append([c,r])

    r = y
    for c in range(x+1,8,+1):
        r -=1
        if(r < 0):
            break
        if(layout[c + r*8].name() != "Empty"):
            enemies.append(enemyCheck(this,c,r,layout,surface))
            break
        moves.append([c,r])
    r = y
    for c in range(x+1,8,+1):
        r +=1
        if(r > 7):
            break
        if(layout[c + r*8].name() != "Empty"):
            enemies.append(enemyCheck(this,c,r,layout,surface))
            break
        moves.append([c,r])
    while None in enemies:
        enemies.remove(None)
    return moves + enemies

def rookMoveChecks(this,x,y,layout,surface):
    moves =[]
    enemies =[]
    for c in range(x-1,-1,-1):
        if(layout[c + y*8].name() != "Empty"):
            enemies.append(enemyCheck(this,c,y,layout,surface))
            break
        moves.append([c,y])
    for c in range(x+1,8,+1):
        if(layout[c + y*8].name() != "Empty"):
            enemies.append(enemyCheck(this,c,y,layout,surface))
            break
        moves.append([c,y])
    for r in range(y+1,8,+1):
        if(layout[x + r*8].name() != "Empty"):
            enemies.append(enemyCheck(this,x,r,layout,surface))
            break
        moves.append([x,r])
    for r in range(y-1,-1,-1):
        if(layout[x + r*8].name() != "Empty"):
            enemies.append(enemyCheck(this,x,r,layout,surface))
            break
        moves.append([x,r])
    r = y
    while None in enemies:
        enemies.remove(None)
    return moves + enemies

def knightMoves(this,x,y,layout,surface):
    moves =[]
    enemies = []
    c = x+1
    r = y+2
    if c < 8 and r < 8:
        if layout[c + r*8].name() != "Empty":
            enemies.append(enemyCheck(this,c,r,layout,surface))
        else:
            moves.append([c,r])
    c = x-1
    r = y+2
    if c > -1 and r < 8:
        if layout[c + r*8].name() != "Empty":
            enemies.append(enemyCheck(this,c,r,layout,surface))
        else:
            moves.append([c,r])
    c = x+1
    r = y-2
    if c < 8 and r > -1:
        if layout[c + r*8].name() != "Empty":
            enemies.append(enemyCheck(this,c,r,layout,surface))
        else:
            moves.append([c,r])
    c = x-1
    r = y-2
    if c >-1  and r > -1:
        if layout[c + r*8].name() != "Empty":
            enemies.append(enemyCheck(this,c,r,layout,surface))
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

def enemyCheck(this,x,y,layout,surface):
    if layout[x+y*8].color != this.color:
        return [x,y]
    return None
def numToSquare(num):
    return[num%8, int(num /8)] 

#could optimize slightly by pruning enemy squares, not worth it for just drawing 
def circlePlacer(self,array,color,layout,surface):
    for move in array:
        if layout[move[0]+move[1]*8].name() == "Empty":
            drawCircle(move[0],move[1])
        elif layout[move[0]+move[1]*8].color != color:
            hollowCircle(move[0],move[1])
