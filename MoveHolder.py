allMoves =[]
for x in range(1000):
    allMoves.append(None)

def MoveHolder():
    return allMoves
    
def moveAdder(playerMove,value):
    move = moves(playerMove,value)
    value = int(value*10) + 500
    if(allMoves[value] == None):
        allMoves[value] = move
    else:
        allMoves[value].next = allMoves[value]
        allMoves[value] = move
        
class moves():
    def __init__(self,move,value):
        self.next = None
        self.value = value
        self.move = move