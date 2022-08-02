import pygame
import Piece
import board
import random
surface = Piece.surface
empty = Piece.emptyPiece()
bQueen = Piece.bQueen()
def move(layout,playerColor,wKing,bKing):
    pieces = []
    locs = []
    #keeps track of black pieces and their locations in the array
    #this is used to find the piece later, for ex the piece at pieces[1] index in the main layout
    #is locs[1]
    i = 0
    for piece in layout:
        square = Piece.numToSquare(i)
        if piece.color != playerColor and piece.validMoves(square[0],square[1],layout,surface):
            pieces.append(piece)
            locs.append(i)
        i += 1
    mover = random.randint(0,len(pieces)-1)
    square = Piece.numToSquare(locs[mover])
    moves = pieces[mover].validMoves(square[0],square[1],layout,surface)
    move = moves[random.randint(0, len(moves)-1)]
    if pieces[mover].name() == "Pawn" and move[0] + move[1]*8 >= 56:
        layout[move[0]+move[1]*8] = bQueen
    else:
        layout[move[0]+move[1]*8] = pieces[mover]
    if pieces[mover].name() == "King":
        Piece.bKingMove(move[0]+move[1]*8)
    if Piece.numToSquare(Piece.bKingSquare) in layout[move[0]+move[1]*8].validMoves(move[0],move[1],layout,surface):
        piece.bKingCheck= TrueS
    layout[square[0] + square[1]*8] = empty
    return(layout)