def MoveHolder(move,value):
    moves = []
    value  = int(value * 10)
    moveAdder(move,value)
    return moves
    
def moveAdder(playerMove,value):
    move = moves(playerMove,value)
    if(moves[value] == None):
        moves[value] = move
        moves[value].next = None
    else:
        move.next = moves[value]
        moves[value] = move
        
class moves(move,value):
    def __init__(self):
        self.next = None
        self.value = value
        self.move = move