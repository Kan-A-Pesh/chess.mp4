import pygame, sys, board, _thread, math

_grid = None
_isAlive = True
_callbacks = {}
_highlights = {}

def init():
    """Initialise la fenetre et affiche le menu.

    Précondition: Aucune

    Postcondition: Aucune
    """
    _thread.start_new_thread(_render_loop, ())

def registerCallback(name, callback):
    """Assigne l'événement de nom 'name' a la fonction 'callback'

    Précondition: name est un string
                  callback est une function

    Postcondition: Aucune
    """
    _callbacks[name] = callback

def _render_loop():
    """Function hors-thread principal, ce dernier ne doit pas etre
    éxécuté dans le thread principal!
    Toujours actif, détermine les éventuels événement sur la fenetre
    ainsi que les demande de 'render'
    """
    global _grid, _isAlive, _callbacks, _highlights

    pygame.init()

    size = 500, 500
    offset = 70, 70
    case_size = 45, 45
    piece_offset = 2, 2
    _screen = pygame.display.set_mode(size)

    # Chargement des images
    white = []
    white.append(pygame.image.load("assets/white/empty.png"))
    white.append(pygame.image.load("assets/white/pawn.png"))
    white.append(pygame.image.load("assets/white/rook.png"))
    white.append(pygame.image.load("assets/white/knight.png"))
    white.append(pygame.image.load("assets/white/bishop.png"))
    white.append(pygame.image.load("assets/white/king.png"))
    white.append(pygame.image.load("assets/white/queen.png"))

    black = []
    black.append(pygame.image.load("assets/black/empty.png"))
    black.append(pygame.image.load("assets/black/pawn.png"))
    black.append(pygame.image.load("assets/black/rook.png"))
    black.append(pygame.image.load("assets/black/knight.png"))
    black.append(pygame.image.load("assets/black/bishop.png"))
    black.append(pygame.image.load("assets/black/king.png"))
    black.append(pygame.image.load("assets/black/queen.png"))

    highlights = []
    highlights.append(pygame.image.load("assets/hl_selected.png"))
    highlights.append(pygame.image.load("assets/hl_move.png"))
    highlights.append(pygame.image.load("assets/hl_capture.png"))

    while True:
        # Détéction des evenements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _isAlive = False
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if (_callbacks.__contains__("onClick")):
                    pos_x = pos[0] - offset[0]
                    pos_y = pos[1] - offset[1]

                    pos_x = math.floor(pos_x / case_size[0]) 
                    pos_y = math.floor(pos_y / case_size[1]) 

                    if (pos_x < 8 and pos_x >= 0) and (pos_y < 8 and pos_y >= 0):
                        _callbacks["onClick"](pos_x + pos_y * 8)

        # Détéction d'une demande de 'render'
        if _grid != None:

            _screen.fill((0,0,0))
            for x in range(8):
                for y in range(8):

                    image = white[0]
                    if (x+y)%2:
                        image = black[0]

                    caseId = _grid.getCase(y*8+x)
                    
                    if ((y*8+x) in _highlights):
                        _screen.blit(highlights[_highlights[(y*8+x)]], (offset[0]+45*x, offset[1]+45*y))
                    else:
                        _screen.blit(image, (offset[0]+45*x, offset[1]+45*y))

                    if (caseId > 0):
                        _screen.blit(white[caseId], (piece_offset[0]+offset[0]+45*x, piece_offset[1]+offset[1]+45*y))
                        pass
                    elif (caseId < 0):
                        _screen.blit(black[-caseId], (piece_offset[0]+offset[0]+45*x, piece_offset[1]+offset[1]+45*y))
                        pass
            
            pygame.display.flip()

            _grid = None

def addHighlight(pos: int, color: int):
    """Ajoute des cases en surbriance qui seront affiché au
    prochain rafraichisement de la fenêtre.
    
    Précondition: pos est un entier
                  color est un entier

    Postcondition: Aucune
    """
    global _highlights
    _highlights[pos] = color

def removeHighlights():
    """Retire toutes les cases en surbriance précédement définis
    qui seront retirées au prochain rafraichisement de la fenêtre.
    
    Précondition: Aucune

    Postcondition: Aucune
    """
    global _highlights
    _highlights = {}

def render(grid: board.Plateau):
    """Rafraichis la fenêtre et affiche le plateau de jeu demandé
    
    Précondition: grid est un Plateau

    Postcondition: Aucune
    """
    global _grid
    _grid = grid