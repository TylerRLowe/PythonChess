
from distutils.log import error
import pygame
import Piece
import board
import random
import time
import copy
pygame.init()
empty = Piece.emptyPiece()
bQueen = Piece.bQueen()
def move(layout,playerColor,wKing,bKing):
    return(evaluation(layout,bKing.color,wKing,bKing))
    
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

def evaluation(layout,color,wKing,bKing):
    start = time.time()
    bestLayout = layout
    i = 0
    for piece in layout:
        square = Piece.numToSquare(i)
        if piece.color != color:
            pass
        else:
            moves = piece.thisPieceCanMove(square[0],square[1],layout,Piece.surface,None)
            for move in moves:
                tempLayout = boardChanger(layout, piece,i, move)
                if board.score(tempLayout,color)>= board.score(bestLayout,color):
                    bestLayout = tempLayout
        i +=1
        
    return bestLayout
    while time.time() - start < 10:
        pass

#takes the original layout, the move being made, and the piece
#edits and returns the
def boardChanger(layout,movingPiece,movingPieceLocation,move):
    newLayout = copy.copy(layout)
    if movingPiece.name() == "Pawn" and move[0] + move[1]*8 >= 56:
        newLayout[move[0]+move[1]*8] = bQueen
    else:
        newLayout[move[0]+move[1]*8] = movingPiece
    if movingPiece.name() == "King":    
        Piece.bKingSquare = move[0] + move[1] * 8
    if Piece.numToSquare(Piece.wKingSquare) in newLayout[move[0]+move[1]*8].validMoves(move[0],move[1],layout,Piece.surface):
        Piece.wKingCheck= True
    newLayout[movingPieceLocation] = empty
    return newLayout