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

    def move(self, oldPos: int, newPos: int) -> None:
        """Déplace un pion d'une case (oldPos) a une autre case vide (newPos)

        Précondition: oldPos est un entier
                      newPos est un entier

        Postcondition: Aucune
        """

        if (self.grid[newPos] != 0):
            return ValueError("Un pion existe déja sur cette case!")
        
        self.grid[oldPos], self.grid[newPos] = self.grid[newPos], self.grid[oldPos]
        return

    
    def getCase(self, casePos: int) -> int:
        """Recupere le type de pion sur la case demande

        Précondition: casePos est un entier

        Postcondition: Renvoie un entier
        """
        return self.grid[casePos]