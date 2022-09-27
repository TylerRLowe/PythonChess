allMoves =[]
for x in range(1001):
    allMoves.append(None)
def clear():
    for x in range(1001):
        allMoves[x] = None
#returns the moves in order of best to worst
def moveHolder():
    moves = []
    for i in range(1000,0,-1):
        move = allMoves[i]
        while move != None:
            moves.append(move)
            move = move.next
    return moves
#takes the details of the move and holds on, including the value
def moveAdder(playerMove,piece,location,value,bKing,wKing):
    move = moves(playerMove,piece,location,value,bKing,wKing)
    value = int(value*10) + 500
    if(allMoves[value] == None):
        allMoves[value] = move
    else:
        move.next = allMoves[value]
        allMoves[value] = move
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