import bagchal

def movestoAction(source, target):

    addition = 0

    x, y = target

    if source == None:
        action = 5 * x + y
        return action
    
    singleDiag = 24
    doubleDiag = 40

    singleStHori = 50
    singleStVert = 70

    doubleStHori = 90
    doubleStVert = 105

    m, n = source

    delX = x - m
    delY = y - n

    minX = min([x, m])
    minY = min([y, n])

    maxX = max([x, m])
    maxY = max([y, n])

    if abs(delX) == 1 and abs(delY) == 1:
        
        if delX < 0:
            addition = 96

        return singleDiag + 4 * minX + maxY + addition

    elif abs(delX) == 2 and abs(delY) == 2:

        slope = delY/delX

        if slope == 1:
            if m == 1:
                return 49
            elif m == 3:
                return 145
            action = 2
        else:
            if m == 1:
                return 50
            elif m == 3:
                return 146
            action = 1

        if delX < 0:
            addition = 96

        action = action + doubleDiag + 4 * int(minX / 2) + minY + addition
        return action

    elif (abs(delX) == 1 and abs(delY) == 0) or (abs(delY) == 1 and abs(delX) == 0):
        
        if abs(delX) == 0:
            if delY < 0:
                addition = 96
            return singleStHori + 4 * minX + maxY + addition
        
        elif abs(delY) == 0:
            if delX < 0:
                addition = 96
            return singleStVert + 4 * minY + maxX + addition

    elif (abs(delX) == 2 and abs(delY) == 0) or (abs(delY) == 2 and abs(delX) == 0):
        
        if abs(delX) == 0:
            if delY < 0:
                addition = 96
            return doubleStHori + 3 * minX + minY + 1 + addition
        elif abs(delY) == 0:
            if delX < 0:
                addition = 96
            return doubleStVert + 3 * minY + minX + 1 + addition

    else:
        print("Not Valid Move")
        return None

    
# movestoActionMapper = [{'move': [None, [0, 0]], 'action': 0} ,
# {'move': [None, [0, 1]], 'action': 1} ,
# {'move': [None, [0, 2]], 'action': 2} ,
# {'move': [None, [0, 3]], 'action': 3} ,
# {'move': [None, [0, 4]], 'action': 4} ,
# {'move': [None, [1, 0]], 'action': 5} ,
# {'move': [None, [1, 1]], 'action': 6} ,
# {'move': [None, [1, 2]], 'action': 7} ,
# {'move': [None, [1, 3]], 'action': 8} ,
# {'move': [None, [1, 4]], 'action': 9} ,
# {'move': [None, [2, 0]], 'action': 10} ,
# {'move': [None, [2, 1]], 'action': 11} ,
# {'move': [None, [2, 2]], 'action': 12} ,
# {'move': [None, [2, 3]], 'action': 13} ,
# {'move': [None, [2, 4]], 'action': 14} ,
# {'move': [None, [3, 0]], 'action': 15} ,
# {'move': [None, [3, 1]], 'action': 16} ,
# {'move': [None, [3, 2]], 'action': 17} ,
# {'move': [None, [3, 3]], 'action': 18} ,
# {'move': [None, [3, 4]], 'action': 19} ,
# {'move': [None, [4, 0]], 'action': 20} ,
# {'move': [None, [4, 1]], 'action': 21} ,
# {'move': [None, [4, 2]], 'action': 22} ,
# {'move': [None, [4, 3]], 'action': 23} ,
# {'move': [None, [4, 4]], 'action': 24} ,
# {'move': [[1, 1], [0, 0]], 'action': 25} ,
# {'move': [[0, 0], [1, 1]], 'action': 25} ,
# {'move': [[1, 1], [0, 2]], 'action': 26} ,
# {'move': [[0, 2], [1, 1]], 'action': 26} ,
# {'move': [[1, 3], [0, 2]], 'action': 27} ,
# {'move': [[0, 2], [1, 3]], 'action': 27} ,
# {'move': [[1, 3], [0, 4]], 'action': 28} ,
# {'move': [[0, 4], [1, 3]], 'action': 28} ,
# {'move': [[2, 0], [1, 1]], 'action': 29} ,
# {'move': [[1, 1], [2, 0]], 'action': 29} ,
# {'move': [[2, 2], [1, 1]], 'action': 30} ,
# {'move': [[1, 1], [2, 2]], 'action': 30} ,
# {'move': [[2, 2], [1, 3]], 'action': 31} ,
# {'move': [[1, 3], [2, 2]], 'action': 31} ,
# {'move': [[2, 4], [1, 3]], 'action': 32} ,
# {'move': [[1, 3], [2, 4]], 'action': 32} ,
# {'move': [[3, 1], [2, 0]], 'action': 33} ,
# {'move': [[2, 0], [3, 1]], 'action': 33} ,
# {'move': [[3, 1], [2, 2]], 'action': 34} ,
# {'move': [[2, 2], [3, 1]], 'action': 34} ,
# {'move': [[3, 3], [2, 2]], 'action': 35} ,
# {'move': [[2, 2], [3, 3]], 'action': 35} ,
# {'move': [[3, 3], [2, 4]], 'action': 36} ,
# {'move': [[2, 4], [3, 3]], 'action': 36} ,
# {'move': [[4, 0], [3, 1]], 'action': 37} ,
# {'move': [[3, 1], [4, 0]], 'action': 37} ,
# {'move': [[4, 2], [3, 1]], 'action': 38} ,
# {'move': [[3, 1], [4, 2]], 'action': 38} ,
# {'move': [[4, 2], [3, 3]], 'action': 39} ,
# {'move': [[3, 3], [4, 2]], 'action': 39} ,
# {'move': [[4, 4], [3, 3]], 'action': 40} ,
# {'move': [[3, 3], [4, 4]], 'action': 40} ,
# {'move': [[2, 0], [0, 2]], 'action': 41} ,
# {'move': [[0, 2], [2, 0]], 'action': 41} ,
# {'move': [[2, 2], [0, 0]], 'action': 42} ,
# {'move': [[0, 0], [2, 2]], 'action': 42} ,
# {'move': [[2, 2], [0, 4]], 'action': 43} ,
# {'move': [[0, 4], [2, 2]], 'action': 43} ,
# {'move': [[2, 4], [0, 2]], 'action': 44} ,
# {'move': [[0, 2], [2, 4]], 'action': 44} ,
# {'move': [[4, 0], [2, 2]], 'action': 45} ,
# {'move': [[2, 2], [4, 0]], 'action': 45} ,
# {'move': [[4, 2], [2, 0]], 'action': 46} ,
# {'move': [[2, 0], [4, 2]], 'action': 46} ,
# {'move': [[4, 2], [2, 4]], 'action': 47} ,
# {'move': [[2, 4], [4, 2]], 'action': 47} ,
# {'move': [[4, 4], [2, 2]], 'action': 48} ,
# {'move': [[2, 2], [4, 4]], 'action': 48} ,
# {'move': [[1, 1], [3, 3]], 'action': 49} ,
# {'move': [[3, 3], [1, 1]], 'action': 49} ,
# {'move': [[3, 1], [1, 3]], 'action': 50} ,
# {'move': [[1, 3], [3, 1]], 'action': 50} ,
# {'move': [[0, 1], [0, 0]], 'action': 51} ,
# {'move': [[0, 0], [0, 1]], 'action': 51} ,
# {'move': [[0, 2], [0, 1]], 'action': 52} ,
# {'move': [[0, 1], [0, 2]], 'action': 52} ,
# {'move': [[0, 3], [0, 2]], 'action': 53} ,
# {'move': [[0, 2], [0, 3]], 'action': 53} ,
# {'move': [[0, 4], [0, 3]], 'action': 54} ,
# {'move': [[0, 3], [0, 4]], 'action': 54} ,
# {'move': [[1, 1], [1, 0]], 'action': 55} ,
# {'move': [[1, 0], [1, 1]], 'action': 55} ,
# {'move': [[1, 2], [1, 1]], 'action': 56} ,
# {'move': [[1, 1], [1, 2]], 'action': 56} ,
# {'move': [[1, 3], [1, 2]], 'action': 57} ,
# {'move': [[1, 2], [1, 3]], 'action': 57} ,
# {'move': [[1, 4], [1, 3]], 'action': 58} ,
# {'move': [[1, 3], [1, 4]], 'action': 58} ,
# {'move': [[2, 1], [2, 0]], 'action': 59} ,
# {'move': [[2, 0], [2, 1]], 'action': 59} ,
# {'move': [[2, 2], [2, 1]], 'action': 60} ,
# {'move': [[2, 1], [2, 2]], 'action': 60} ,
# {'move': [[2, 3], [2, 2]], 'action': 61} ,
# {'move': [[2, 2], [2, 3]], 'action': 61} ,
# {'move': [[2, 4], [2, 3]], 'action': 62} ,
# {'move': [[2, 3], [2, 4]], 'action': 62} ,
# {'move': [[3, 1], [3, 0]], 'action': 63} ,
# {'move': [[3, 0], [3, 1]], 'action': 63} ,
# {'move': [[3, 2], [3, 1]], 'action': 64} ,
# {'move': [[3, 1], [3, 2]], 'action': 64} ,
# {'move': [[3, 3], [3, 2]], 'action': 65} ,
# {'move': [[3, 2], [3, 3]], 'action': 65} ,
# {'move': [[3, 4], [3, 3]], 'action': 66} ,
# {'move': [[3, 3], [3, 4]], 'action': 66} ,
# {'move': [[4, 1], [4, 0]], 'action': 67} ,
# {'move': [[4, 0], [4, 1]], 'action': 67} ,
# {'move': [[4, 2], [4, 1]], 'action': 68} ,
# {'move': [[4, 1], [4, 2]], 'action': 68} ,
# {'move': [[4, 3], [4, 2]], 'action': 69} ,
# {'move': [[4, 2], [4, 3]], 'action': 69} ,
# {'move': [[4, 4], [4, 3]], 'action': 70} ,
# {'move': [[4, 3], [4, 4]], 'action': 70} ,
# {'move': [[1, 0], [0, 0]], 'action': 71} ,
# {'move': [[0, 0], [1, 0]], 'action': 71} ,
# {'move': [[2, 0], [1, 0]], 'action': 72} ,
# {'move': [[1, 0], [2, 0]], 'action': 72} ,
# {'move': [[3, 0], [2, 0]], 'action': 73} ,
# {'move': [[2, 0], [3, 0]], 'action': 73} ,
# {'move': [[4, 0], [3, 0]], 'action': 74} ,
# {'move': [[3, 0], [4, 0]], 'action': 74} ,
# {'move': [[1, 1], [0, 1]], 'action': 75} ,
# {'move': [[0, 1], [1, 1]], 'action': 75} ,
# {'move': [[2, 1], [1, 1]], 'action': 76} ,
# {'move': [[1, 1], [2, 1]], 'action': 76} ,
# {'move': [[3, 1], [2, 1]], 'action': 77} ,
# {'move': [[2, 1], [3, 1]], 'action': 77} ,
# {'move': [[4, 1], [3, 1]], 'action': 78} ,
# {'move': [[3, 1], [4, 1]], 'action': 78} ,
# {'move': [[1, 2], [0, 2]], 'action': 79} ,
# {'move': [[0, 2], [1, 2]], 'action': 79} ,
# {'move': [[2, 2], [1, 2]], 'action': 80} ,
# {'move': [[1, 2], [2, 2]], 'action': 80} ,
# {'move': [[3, 2], [2, 2]], 'action': 81} ,
# {'move': [[2, 2], [3, 2]], 'action': 81} ,
# {'move': [[4, 2], [3, 2]], 'action': 82} ,
# {'move': [[3, 2], [4, 2]], 'action': 82} ,
# {'move': [[1, 3], [0, 3]], 'action': 83} ,
# {'move': [[0, 3], [1, 3]], 'action': 83} ,
# {'move': [[2, 3], [1, 3]], 'action': 84} ,
# {'move': [[1, 3], [2, 3]], 'action': 84} ,
# {'move': [[3, 3], [2, 3]], 'action': 85} ,
# {'move': [[2, 3], [3, 3]], 'action': 85} ,
# {'move': [[4, 3], [3, 3]], 'action': 86} ,
# {'move': [[3, 3], [4, 3]], 'action': 86} ,
# {'move': [[1, 4], [0, 4]], 'action': 87} ,
# {'move': [[0, 4], [1, 4]], 'action': 87} ,
# {'move': [[2, 4], [1, 4]], 'action': 88} ,
# {'move': [[1, 4], [2, 4]], 'action': 88} ,
# {'move': [[3, 4], [2, 4]], 'action': 89} ,
# {'move': [[2, 4], [3, 4]], 'action': 89} ,
# {'move': [[4, 4], [3, 4]], 'action': 90} ,
# {'move': [[3, 4], [4, 4]], 'action': 90} ,
# {'move': [[0, 2], [0, 0]], 'action': 91} ,
# {'move': [[0, 0], [0, 2]], 'action': 91} ,
# {'move': [[0, 3], [0, 1]], 'action': 92} ,
# {'move': [[0, 1], [0, 3]], 'action': 92} ,
# {'move': [[0, 4], [0, 2]], 'action': 93} ,
# {'move': [[0, 2], [0, 4]], 'action': 93} ,
# {'move': [[1, 2], [1, 0]], 'action': 94} ,
# {'move': [[1, 0], [1, 2]], 'action': 94} ,
# {'move': [[1, 3], [1, 1]], 'action': 95} ,
# {'move': [[1, 1], [1, 3]], 'action': 95} ,
# {'move': [[1, 4], [1, 2]], 'action': 96} ,
# {'move': [[1, 2], [1, 4]], 'action': 96} ,
# {'move': [[2, 2], [2, 0]], 'action': 97} ,
# {'move': [[2, 0], [2, 2]], 'action': 97} ,
# {'move': [[2, 3], [2, 1]], 'action': 98} ,
# {'move': [[2, 1], [2, 3]], 'action': 98} ,
# {'move': [[2, 4], [2, 2]], 'action': 99} ,
# {'move': [[2, 2], [2, 4]], 'action': 99} ,
# {'move': [[3, 2], [3, 0]], 'action': 100} ,
# {'move': [[3, 0], [3, 2]], 'action': 100} ,
# {'move': [[3, 3], [3, 1]], 'action': 101} ,
# {'move': [[3, 1], [3, 3]], 'action': 101} ,
# {'move': [[3, 4], [3, 2]], 'action': 102} ,
# {'move': [[3, 2], [3, 4]], 'action': 102} ,
# {'move': [[4, 2], [4, 0]], 'action': 103} ,
# {'move': [[4, 0], [4, 2]], 'action': 103} ,
# {'move': [[4, 3], [4, 1]], 'action': 104} ,
# {'move': [[4, 1], [4, 3]], 'action': 104} ,
# {'move': [[4, 4], [4, 2]], 'action': 105} ,
# {'move': [[4, 2], [4, 4]], 'action': 105} ,
# {'move': [[2, 0], [0, 0]], 'action': 106} ,
# {'move': [[0, 0], [2, 0]], 'action': 106} ,
# {'move': [[3, 0], [1, 0]], 'action': 107} ,
# {'move': [[1, 0], [3, 0]], 'action': 107} ,
# {'move': [[4, 0], [2, 0]], 'action': 108} ,
# {'move': [[2, 0], [4, 0]], 'action': 108} ,
# {'move': [[2, 1], [0, 1]], 'action': 109} ,
# {'move': [[0, 1], [2, 1]], 'action': 109} ,
# {'move': [[3, 1], [1, 1]], 'action': 110} ,
# {'move': [[1, 1], [3, 1]], 'action': 110} ,
# {'move': [[4, 1], [2, 1]], 'action': 111} ,
# {'move': [[2, 1], [4, 1]], 'action': 111} ,
# {'move': [[2, 2], [0, 2]], 'action': 112} ,
# {'move': [[0, 2], [2, 2]], 'action': 112} ,
# {'move': [[3, 2], [1, 2]], 'action': 113} ,
# {'move': [[1, 2], [3, 2]], 'action': 113} ,
# {'move': [[4, 2], [2, 2]], 'action': 114} ,
# {'move': [[2, 2], [4, 2]], 'action': 114} ,
# {'move': [[2, 3], [0, 3]], 'action': 115} ,
# {'move': [[0, 3], [2, 3]], 'action': 115} ,
# {'move': [[3, 3], [1, 3]], 'action': 116} ,
# {'move': [[1, 3], [3, 3]], 'action': 116} ,
# {'move': [[4, 3], [2, 3]], 'action': 117} ,
# {'move': [[2, 3], [4, 3]], 'action': 117} ,
# {'move': [[2, 4], [0, 4]], 'action': 118} ,
# {'move': [[0, 4], [2, 4]], 'action': 118} ,
# {'move': [[3, 4], [1, 4]], 'action': 119} ,
# {'move': [[1, 4], [3, 4]], 'action': 119} ,
# {'move': [[4, 4], [2, 4]], 'action': 120} ,
# {'move': [[2, 4], [4, 4]], 'action': 120} ]

def movestoAction(source, target):

    x, y = target

    if source == None:
        action = 5 * x + y
        return action
    
    singleDiag = 24
    doubleDiag = 40

    singleStHori = 50
    singleStVert = 70

    doubleStHori = 90
    doubleStVert = 105

    m, n = source

    delX = x - m
    delY = y - n

    minX = min([x, m])
    minY = min([y, n])

    maxX = max([x, m])
    maxY = max([y, n])

    if abs(delX) == 1 and abs(delY) == 1:
        return singleDiag + 4 * minX + maxY

    elif abs(delX) == 2 and abs(delY) == 2:

        slope = delY/delX 

        if slope == 1:
            if minX == 1:
                return 49
            action = 2
        else:
            if minX == 1:
                return 50
            action = 1

        action = action + doubleDiag + 4 * int(minX / 2) + minY
        return action

    elif (abs(delX) == 1 and abs(delY) == 0) or (abs(delY) == 1 and abs(delX) == 0):
        
        if abs(delX) == 0:
            return singleStHori + 4 * minX + maxY
        elif abs(delY) == 0:
            return singleStVert + 4 * minY + maxX

    elif (abs(delX) == 2 and abs(delY) == 0) or (abs(delY) == 2 and abs(delX) == 0):
        
        if abs(delX) == 0:
            return doubleStHori + 3 * minX + minY + 1
        elif abs(delY) == 0:
            return doubleStVert + 3 * minY + minX + 1

    else:
        print("Not Valid Move")
        return None

# def actionToMove(action: int):
#     moves = []
#     for mappers in movestoActionMapper:
#         if mappers["action"] == action:
#             moves.append(mappers["action"][0])

#     return moves

# def actionToDoableMove(game:bagchal, action: int):
#     for mappers in movestoActionMapper:
#         if mappers["action"] == action:
#             if game.check_move(mappers["move"][0])["is_valid"]:
#                 return mappers["action"][0]


    