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