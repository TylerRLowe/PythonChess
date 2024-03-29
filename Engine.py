from distutils.log import error
from sre_constants import JUMP
import pygame
import Piece
import board
import random
import time
import copy
import MoveHolder
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
cream = pygame.Color(235,230,208)
green = pygame.Color(0,80,0)
grey = pygame.Color(84,84,84,200)
pygame.init()
empty = Piece.emptyPiece()
bQueen = Piece.bQueen()
def move(layout,playerColor):
    return(evaluation(layout,black))
    
    moves ={}
    #keeps track of black pieces and their locations in the array
    #this is used to find the piece later, for ex the piece at pieces[1] index in the main layout
    #is locs[1]
    enemies = None
    i = 0
    for piece in layout:
        square = Piece.numToSquare(i)
        if piece.color != playerColor and piece.name() != "Empty":
            moves[i] = piece.thisPieceCanMove(square[0],square[1],layout,Piece.surface,enemies) 
            if not moves[i]: moves.pop(i,None)
            i += 1
    keys = list(moves.keys())

    if not moves or not keys: 
        return "error"
    movingPieceLocation = keys[random.randint(0,len(moves)-1)]
    possibleMoves = list(moves[movingPieceLocation])
    movingPiece = layout[movingPieceLocation]
    move = possibleMoves[random.randint(0,len(possibleMoves)-1)]
    if movingPiece.name() == "Pawn" and move[0] + move[1]*8 >= 56:
        layout[move[0]+move[1]*8] = bQueen
    else:
        layout[move[0]+move[1]*8] = movingPiece
    if movingPiece.name() == "King":    
        Piece.bKingSquare = move[0] + move[1] * 8
    if Piece.numToSquare(Piece.wKingSquare) in layout[move[0]+move[1]*8].validMoves(move[0],move[1],layout,Piece.surface):
        Piece.wKingCheck= True
    layout[movingPieceLocation] = empty
    return(layout)

def evaluation(layout,color):
    depth = 1
    moveHolder = MoveHolder.MoveHolder()
    start = time.time()
    bestLayout = board.emptyLayoutBlack
    i = 0
    x = 0
    #keeps track of where the king should actually be as it is altered each use of board changer
    trueBKing = Piece.bKingSquare
    trueWKing = Piece.wKingSquare
    for piece in layout:
        square = Piece.numToSquare(i)
        if piece.color != color:
            pass
        else:
            #resseting the square
            Piece.bKingSquare = trueBKing
            Piece.wKingSquare = trueWKing
            #looking at all moves for the piece, and finding out which one gives the best value
            moves = piece.thisPieceCanMove(square[0],square[1],layout,Piece.surface,None)
            for move in moves:
                x += 1
                tempLayout = boardChanger(layout, piece,i, move)
                value = board.score(tempLayout,color)
                #finds the value of each position, adds to a move holder to we can look at them in order
                moveHolder.moveAdder(move,piece,i,value,Piece.bKingSquare,Piece.wKingSquare)
                if value >= board.score(bestLayout,color):
                    #if the value is > the the best layout, it replaces it as best layout
                    bestLayout = tempLayout
        i +=1
    Piece.bKingSquare = trueBKing
    #checking the player moves to check what will happen next
    if color == black:
        return playerEvaluation(layout, white,moveHolder)
    else:
        return playerEvaluation(layout, black,moveHolder)

    while time.time() - start < 10:
        pass
#evaluating the other way, this time finding the best move the player can do
#evauliting step by step should allow me to evaulate positions in
#an order that will hopefully cut down on the number of positions evauluated rather then going to a set depth
def playerEvaluation(layout,color,moveHolder):
    moves = moveHolder.getter()
    moveHolder.clear()
    bestLayout = board.emptyLayoutBlack
    bestValue = -1000
    value = -10000
    trueBKing = Piece.bKingSquare
    trueWKing = Piece.wKingSquare
    finalWKingSquare =0
    finalBKingSquare =0
    for move in moves:
        #setting worst value to abitrary constant, so it is always reset on first run
        worstValue = 1000
        #badMove is used as we need to break out of two loops with an unsecsusful move
        badMove = False
        tempLayout = boardChanger(layout, move.piece, move.location, move.move)
        if move.piece.color != color:
            pass
        for x  in range(64):
            piece = tempLayout[x]
            if piece.name() == "Empty" or piece.color != white:
                pass
            else:
                #slightly altered version of the other evaluation, will get rid of moves faster
                square =Piece.numToSquare(x)
                playerMoves = piece.thisPieceCanMove(square[0],square[1],tempLayout,Piece.surface,None)
                for playerMove in playerMoves:
                    #resseting king square every move
                    Piece.bKingSquare = move.bKing
                    Piece.wKingSquare = move.wKing
                    judgingLayout = boardChanger(tempLayout, piece, x, playerMove)
                    #inveriting the board score, should have made color invertable
                    value =   - board.score(judgingLayout,color)
                    if value > bestValue:
                        if value < worstValue:
                            worstValue = value
                        #we need to continue checking the rest of the moves to see if there is somthing
                        #worst value keeping track of the worst case scenario
                        

                    else:
                        #if there is a better move white can make, we do not have to check the rest of this pieces moves
                        badMove = True
                        break
                if badMove:
                        #if there is a better move white can make, we also dont have to check other pieces move
                        break
        if worstValue > bestValue and badMove == False:
            
            #This is needed to not update the best layout before we should
            bestLayout = tempLayout
            finalBKingSquare = move.bKing
            finalWKingSquare = move.wKing
            #setting the bset value to worst possibility
            bestValue = worstValue
    Piece.bKingSquare = finalBKingSquare
    Piece.wKingSquare = finalWKingSquare
    return bestLayout
                

        
#takes the original layout, the move being made, and the piece
#edits and returns the
def boardChanger(layout,movingPiece,movingPieceLocation,move):
    newLayout = copy.copy(layout)
    if movingPiece.name() == "Pawn" and move[0] + move[1]*8 >= 56:
        newLayout[move[0]+move[1]*8] = bQueen
    else:
        newLayout[move[0]+move[1]*8] = movingPiece
    if movingPiece.name() == "King" and movingPiece.color == black:    
        Piece.bKingSquare = move[0] + move[1] * 8
    elif movingPiece.name() == "King" and movingPiece.color == white:
        Piece.wKingSquare = move[0] + move[1] * 8
    #if Piece.numToSquare(Piece.wKingSquare) in newLayout[move[0]+move[1]*8].validMoves(move[0],move[1],layout,Piece.surface):
     #   Piece.wKingCheck= True
    newLayout[movingPieceLocation] = empty
    
    return newLayout