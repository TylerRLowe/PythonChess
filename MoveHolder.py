class MoveHolder:
    def __init__(self) -> None:
        self.allMoves =[]
        for x in range(1001):
            self.allMoves.append(None)
    def clear(self):
        for x in range(1001):
            self.allMoves[x] = None
    #returns the moves in order of best to worst
    def getter(self):
        moves = []
        for i in range(1000,0,-1):
            move = self.allMoves[i]
            while move != None:
                moves.append(move)
                move = move.next
        return moves
    #takes the details of the move and holds on, including the value
    def moveAdder(self,playerMove,piece,location,value,bKing,wKing):
        move = self.moves(playerMove,piece,location,value,bKing,wKing)
        value = value//10 + 500
        if(self.allMoves[value] == None):
            self.allMoves[value] = move
        else:
            move.next = self.allMoves[value]
            self.allMoves[value] = move
    def updateMoveValue(self,move,value):
        self.allMoves[value//10 + 500] = move
    #Kind of an array of linked list, value pretty much is sorting them
    #but sometimes two moves have the same value
    #it is initialized as None, but after adding a move
    #.next being None indicates that is the final move at that value
    class moves():
        def __init__(self,move,piece,location,value,bKing,wKing):
            self.next = None
            self.value = value
            self.move = move
            self.piece = piece
            self.location = location
            self.bKing = bKing
            self.wKing = wKing