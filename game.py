import board

def lookForCheck(grid: board.Plateau, isWhite: bool):
    """on regarde si oui ou non si le roi des menacé par
    le joueur demandé et renvoie la pion menaçant.

    Préconditions: grid est un Plateau

    Postconditions: Renvoie une ID
    """
    for i in range(64):
        if not grid.isEmpty(i):
            pieceWhite = grid.getCase(i) > 0
            if pieceWhite == isWhite:
                for move in getMoves(grid, i):
                    
                    k = 5
                    if isWhite: k = -5

                    if grid.getCase(move) == k:
                        return i
    return -1

def getMoves(grid: board.Plateau, pieceId: int):
    """Renvoie toutes les possibilités de mouvement
    pour la pièce demandé

    Préconditions: grid est un Plateau
                   pieceId est un entier

    Postconditions: Renvoie un tableau d'entiers
    """

    # ID & Names Pairs
    #
    # 0 Vide - Empty
    # 1 Pion - Pawn
    # 2 Tour - Rook
    # 3 Cavalier - Knight
    # 4 Fou - Bishop
    # 5 Roi - King
    # 6 Dame - Queen
    #
    # Négatif = énemmi

    possibilities = []
    pieceType = grid.getCase(pieceId)
    isAlly = pieceType == abs(pieceType)

    # Type Pion Blanc (haut)
    if (pieceType == 1):

        if (grid.isEmpty(pieceId+8)):
            possibilities.append(pieceId+8)
            if (pieceId < 16 and grid.isEmpty(pieceId+16)):
                possibilities.append(pieceId+16)
        
        x = (pieceId%8)

        if (x < 7 and grid.isAvailable(pieceId+9, isAlly)):
            if not grid.isEmpty(pieceId+9):
                possibilities.append(pieceId+9)

        if (x > 0 and grid.isAvailable(pieceId+7, isAlly)):
            if not grid.isEmpty(pieceId+7):
                possibilities.append(pieceId+7)

    # Type Pion Noir (bas)
    if (pieceType == -1):
    
        if (grid.isEmpty(pieceId-8)):
            possibilities.append(pieceId-8)
            if (pieceId > 47 and grid.isEmpty(pieceId-16)):
                possibilities.append(pieceId-16)
        
        x = (pieceId%8)

        if (x < 7 and grid.isAvailable(pieceId-7, isAlly)):
            if not grid.isEmpty(pieceId-7):
                possibilities.append(pieceId-7)

        if (x > 0 and grid.isAvailable(pieceId-9, isAlly)):
            if not grid.isEmpty(pieceId-9):
                possibilities.append(pieceId-9)
                
    # Type Tour ou Dame
    if (abs(pieceType) == 2 or abs(pieceType) == 6):
        
        i = 1
        while True:
            if (grid.isAvailable(pieceId+8*i, isAlly)):
                possibilities.append(pieceId+8*i)
                if (not grid.isEmpty(pieceId+8*i)): break
            else:
                break
            i+=1
            
        i = 1
        while True:
            if (grid.isAvailable(pieceId-8*i, isAlly)):
                possibilities.append(pieceId-8*i)
                if (not grid.isEmpty(pieceId-8*i)): break
            else: break
            i+=1
            
        for i in range(1, pieceId%8+1):
            if (grid.isAvailable(pieceId-i, isAlly)):
                possibilities.append(pieceId-i)
                if (not grid.isEmpty(pieceId-i)): break
            else: break
            
        for i in range(1, 8-(pieceId%8)):
            if (grid.isAvailable(pieceId+i, isAlly)):
                possibilities.append(pieceId+i)
                if (not grid.isEmpty(pieceId+i)): break
            else: break

    # Type Cavalier
    if (abs(pieceType) == 3):
        x = (pieceId%8)

        if (x < 7 and grid.isAvailable(pieceId+17, isAlly)):
            possibilities.append(pieceId+17)
        if (x < 7 and grid.isAvailable(pieceId-15, isAlly)):
            possibilities.append(pieceId-15)

        if (x > 0 and grid.isAvailable(pieceId-17, isAlly)):
            possibilities.append(pieceId-17)
        if (x > 0 and grid.isAvailable(pieceId+15, isAlly)):
            possibilities.append(pieceId+15)

        if (x < 6 and grid.isAvailable(pieceId+10, isAlly)):
            possibilities.append(pieceId+10)
        if (x < 6 and grid.isAvailable(pieceId-6, isAlly)):
            possibilities.append(pieceId-6)

        if (x > 1 and grid.isAvailable(pieceId-10, isAlly)):
            possibilities.append(pieceId-10)
        if (x > 1 and grid.isAvailable(pieceId+6, isAlly)):
            possibilities.append(pieceId+6)
            
    # Type Fou ou Dame
    if (abs(pieceType) == 4 or abs(pieceType) == 6):

        for i in range(1, pieceId%8+1):
            if (grid.isAvailable(pieceId-9*i, isAlly)):
                possibilities.append(pieceId-9*i)
                if (not grid.isEmpty(pieceId-9*i)): break
            else: break
            
        for i in range(1, 8-(pieceId%8)):
            if (grid.isAvailable(pieceId+9*i, isAlly)):
                possibilities.append(pieceId+9*i)
                if (not grid.isEmpty(pieceId+9*i)): break
            else: break

        for i in range(1, pieceId%8+1):
            if (grid.isAvailable(pieceId+7*i, isAlly)):
                possibilities.append(pieceId+7*i)
                if (not grid.isEmpty(pieceId+7*i)): break
            else: break
            
        for i in range(1, 8-(pieceId%8)):
            if (grid.isAvailable(pieceId-7*i, isAlly)):
                possibilities.append(pieceId-7*i)
                if (not grid.isEmpty(pieceId-7*i)): break
            else: break

    # Type Roi
    if (abs(pieceType) == 5):

        if (grid.isAvailable(pieceId+8, isAlly)):
            possibilities.append(pieceId+8)
        if (grid.isAvailable(pieceId-8, isAlly)):
            possibilities.append(pieceId-8)

        x = (pieceId%8)

        if (x < 7):
            if (grid.isAvailable(pieceId+9, isAlly)):
                possibilities.append(pieceId+9)
            if (grid.isAvailable(pieceId-7, isAlly)):
                possibilities.append(pieceId-7)
            if (grid.isAvailable(pieceId+1, isAlly)):
                possibilities.append(pieceId+1)

        if (x > 0):
            if (grid.isAvailable(pieceId-9, isAlly)):
                possibilities.append(pieceId-9)
            if (grid.isAvailable(pieceId+7, isAlly)):
                possibilities.append(pieceId+7)
            if (grid.isAvailable(pieceId-1, isAlly)):
                possibilities.append(pieceId-1)


    # Roque - Blanc Gauche Tour
    if (pieceId == 0 and not grid.tlRookMoved and not grid.tKingMoved and isAlly):
        if (grid.isEmpty(1) and grid.isEmpty(2)):
            possibilities.append(3)
            print("Roque - Blanc Gauche Tour")
            
    # Roque - Blanc Droite Tour
    if (pieceId == 7 and not grid.trRookMoved and not grid.tKingMoved and isAlly):
        if (grid.isEmpty(4) and grid.isEmpty(5) and grid.isEmpty(6)):
            possibilities.append(3)
            print("Roque - Blanc Droite Tour")

    # Roque - Noir Gauche Tour
    if (pieceId == 56 and not grid.blRookMoved and not grid.bKingMoved and not isAlly):
        if (grid.isEmpty(57) and grid.isEmpty(58) and grid.isEmpty(59)):
            possibilities.append(60)
            print("Roque - Noir Gauche Tour")
            
    # Roque - Noir Droite Tour
    if (pieceId == 63 and not grid.brRookMoved and not grid.bKingMoved and not isAlly):
        if (grid.isEmpty(61) and grid.isEmpty(62)):
            possibilities.append(60)
            print("Roque - Noir Droite Tour")

    return possibilities
