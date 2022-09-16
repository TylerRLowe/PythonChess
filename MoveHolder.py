allMoves =[]
for x in range(1001):
    allMoves.append(None)
def clear():
    for x in range(1001):
        allMoves[x] = None

def MoveHolder():
    moves = []
    for i in range(1000,0,-1):
        move = allMoves[i]
        while move != None:
            moves.append(move)
            move = move.next
    return moves
    
def moveAdder(playerMove,piece,location,value):
    move = moves(playerMove,piece,location,value)
    value = int(value*10) + 500
    if(allMoves[value] == None):
        allMoves[value] = move
    else:
        move.next = allMoves[value]
        allMoves[value] = move
   
class moves():
    def __init__(self,move,piece,location,value):
        self.next = None
        self.value = value
        self.move = move
        self.piece = piece
        self.location = location