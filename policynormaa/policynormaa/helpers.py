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
        slope = delY / delX

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
