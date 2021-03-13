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

    def move(self, oldPos: int, newPos: int):
        """Déplace un pion d'une case (oldPos) a une autre case vide (newPos)

        Précondition: oldPos est un entier
                      newPos est un entier

        Postcondition: Aucune
        """
        
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