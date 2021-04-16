import board, render, sys, game, _thread, time

grid = board.Plateau()
selected = -1
available = []
turnCount = 0
boards = []
timerWhite = 900
timerBlack = 900
timerWhite = 100
timerBlack = 100

def timerloop():
    """Fonction lancé sur un autre thread, toutes
    les secondes elle retire 1 seconde au joueur devant
    jouer et l'affiche sur le render

    Préconditions: Aucune

    Postconditions: Aucune
    """
    global timerWhite, timerBlack, turnCount
    while timerWhite > 0 and timerBlack > 0:
        time.sleep(1)
        if timerWhite > 0 and timerBlack > 0:
            if turnCount%2 == 0:
                timerWhite -= 1
            else:
                timerBlack -= 1

            render.setState("timerWhite", "{:02d}:{:02d} ".format(timerWhite//60, timerWhite%60))
            render.setState("timerBlack", "{:02d}:{:02d} ".format(timerBlack//60, timerBlack%60))

        if timerBlack == 0:
            render.setState("end", 3) # 0 => Timeout white
            return

        if timerWhite == 0:
            render.setState("end", 4) # 0 => Timeout black
            return

def checkState(grid: board.Plateau, isWhite: bool):
    """Regarde si la partie est finie selon le plateau donné
    pour le joueur séléctioné.
    Si la partie n'est pas terminé, False est retouré
    Si la partie est terminé d'un quelconque manière cette fonction
    renvoie True et l'affiche sur la fenetre.  

    Préconditions: grid est un Plateau
                   isWhite est une booléaine

    Postconditions: Renvoie une booléaine
    """
    global boards, timerWhite, timerBlack
    # On verifie si la partie n'est pas nulle selon la regle des 3 plateaux.
    count = 0
    for b in boards:
        if (grid.grid == b):
            count += 1

    if count >= 3:
        render.removeHighlights()
        render.render(grid, turnCount%2==0)
        render.setState("end", 0) # 0 => Match nul
    else:
        boards.append(grid.copy().grid)

    # On regarde tout les déplacements possibles pour vérifier s'ils sont légaux.
    e = -1
    for i in range(64):
        if not grid.isEmpty(i):
            pieceWhite = grid.getCase(i) > 0
            if pieceWhite == isWhite:
                for move in game.getMoves(grid, i):
                    testGrid = grid.copy()
                    testGrid.move(i, move)
                    e = game.lookForCheck(testGrid, not isWhite)
                    if (e == -1):
                        return False
    
    # Si aucun déplacement n'est dispo on previent le render de la fin "échec et mat"
    timerWhite = -1
    timerBlack = -1
    render.removeHighlights()
    render.render(grid, turnCount%2==0)
    render.setState("end", turnCount%2+1)
    return True

def onClick(pos):
    """Appelé quand une case est cliqué ou quand un bouton est cliqué
    Si pos est positif c'est la position cliqué sur la grille or
    s'il est négatif c'est l'ID du bouton cliqué.

    Préconditions: pos est la position cliqué

    Postconditions: Aucune
    """
    global grid, available, selected, turnCount, boards, timerWhite, timerBlack
    if (pos < 0): # Un bouton a été cliqué.

        if (pos == -1): # Bouton: Abandon
            timerWhite = -1
            timerBlack = -1
            render.setState("end", turnCount%2+5)
            
        if (pos == -2): # Bouton: Proposer la nulle
            render.setState("null", 2)
        if (pos == -3): # Bouton: Refuser la nulle
            render.setState("null", 0)
            render.render(grid, turnCount%2==0)
            
        if (pos == -4): # Bouton: Accepter la nulle
            timerWhite = -1
            timerBlack = -1
            render.render(grid, turnCount%2==0)
            render.setState("null", 0)
            render.setState("end", 0)
        return

    # Sinon le code continue car une case a été cliquée. 
    if (selected == -1 and not grid.isEmpty(pos) and ((grid.getCase(pos) < 0) == (turnCount%2==1))):
        selected = pos
        
        render.addHighlight(pos, 0)
        for i in game.getMoves(grid, selected):

            testGrid = grid.copy()
            testGrid.move(pos, i)

            if (game.lookForCheck(testGrid, grid.getCase(pos) < 0) == -1):

                if (grid.isEmpty(i)):
                    render.addHighlight(i, 1)
                else:
                    render.addHighlight(i, 2)
                available.append(i)
        
    else:
        if (available.__contains__(pos)):
            turnCount += 1
            if (turnCount > 100):
                render.setState("fiftymoves", True)

            # On réinitialise la règle des 50 tours si un pion est déplacé
            if (abs(grid.getCase(selected)) == 1):
                turnCount = turnCount%2
                boards = []
            # Ou si un pion est capturé
            if (not grid.isEmpty(pos)):
                turnCount = turnCount%2
                boards = []

            grid.move(selected, pos)
            if checkState(grid, turnCount%2==0): return

        selected = -1
        available = []
        render.removeHighlights()

    render.render(grid, turnCount%2==0)

if __name__ == "__main__":
    render.init()
    render.registerCallback("onClick", onClick)
    render.render(grid, True)
    _thread.start_new_thread(timerloop, ())
    while 1:
        if render._isAlive == False: sys.exit()