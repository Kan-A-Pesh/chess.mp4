from copy import deepcopy

class Plateau:

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

    grid = [
         2, 3, 4, 5, 6, 4, 3, 2,
         1, 1, 1, 1, 1, 1, 1, 1,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
        -1,-1,-1,-1,-1,-1,-1,-1,
        -2,-3,-4,-6,-5,-4,-3,-2
    ]

    tlRookMoved = False
    trRookMoved = False
    tKingMoved = False

    blRookMoved = False
    brRookMoved = False
    bKingMoved = False

    def move(self, oldPos: int, newPos: int):
        """Déplace un pion d'une case (oldPos) a une autre case vide (newPos)

        Précondition: oldPos est un entier
                      newPos est un entier

        Postcondition: Aucune
        """
        
        if (oldPos == 0 and newPos == 0):
            self.tlRookMoved = True
        if (oldPos == 7 and newPos == 7):
            self.trRookMoved = True
        if (oldPos == 3 and newPos == 3):
            self.tKingMoved = True
        
        if (oldPos == 56 and newPos == 56):
            self.blRookMoved = True
        if (oldPos == 63 and newPos == 63):
            self.brRookMoved = True
        if (oldPos == 60 and newPos == 60):
            self.bKingMoved = True

        # Roque - Blanc gauche
        if (oldPos == 0 and newPos == 3):
            self.grid[0] = 0
            self.grid[3] = 2
            self.grid[2] = 5
            return
        
        # Roque - Blanc droite
        if (oldPos == 7 and newPos == 3):
            self.grid[7] = 0
            self.grid[3] = 2
            self.grid[4] = 5
            return
        
        # Roque - Noir gauche
        if (oldPos == 56 and newPos == 60):
            self.grid[56] = 0
            self.grid[60] = -2
            self.grid[59] = -5
            return
        
        # Roque - Noir droite
        if (oldPos == 63 and newPos == 60):
            self.grid[63] = 0
            self.grid[60] = -2
            self.grid[61] = -5
            return

        self.grid[newPos] = self.grid[oldPos]
        self.grid[oldPos] = 0
        return

    def getCase(self, casePos: int):
        """Recupere le type de pion sur la case demande

        Précondition: casePos est un entier

        Postcondition: Renvoie un entier
        """
        return self.grid[casePos]

    def isEmpty(self, casePos: int):
        """Renvoie si la case demandé est vide ou non

        Précondition: casePos est un entier

        Postcondition: Renvoie une booléaine
        """
        if (casePos < 00): return False
        if (casePos > 63): return False

        return self.grid[casePos] == 0

    def isAvailable(self, casePos: int, isAlly: bool):
        """Renvoie si la case demandé est disponible ou non
        Renvoie True si la case est vide ou appartient a l'ennemi
        Sinon renvoie False

        Précondition: casePos est un entier
                      isAlly est une booléaine

        Postcondition: Renvoie une booléaine
        """
        if (casePos < 00): return False
        if (casePos > 63): return False

        if self.isEmpty(casePos): return True

        return (self.grid[casePos] == abs(self.grid[casePos])) != isAlly

    def copy(self):
        grid = Plateau()
        grid.grid = deepcopy(self.grid)
        
        grid.tlRookMoved = deepcopy(self.tlRookMoved)
        grid.trRookMoved = deepcopy(self.trRookMoved)
        grid.tKingMoved = deepcopy(self.tKingMoved)
        
        grid.blRookMoved = deepcopy(self.blRookMoved)
        grid.brRookMoved = deepcopy(self.brRookMoved)
        grid.bKingMoved = deepcopy(self.bKingMoved)
        return grid