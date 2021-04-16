import pygame, sys, board, _thread, math

_grid = None
_isAlive = True
_callbacks = {}
_highlights = {}
_isWhiteTurn = True
_states = {}

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

def setState(name, state):
    """Assigne l'état de nom 'name' a la valeur 'state'

    Précondition: name est un string
                  state n'est pas nul

    Postcondition: Aucune
    """
    global _states
    _states[name] = state

def _render_loop():
    """Function hors-thread principal, ce dernier ne doit pas etre
    éxécuté dans le thread principal!
    Toujours actif, détermine les éventuels événement sur la fenetre
    ainsi que les demande de 'render'
    """
    global _grid, _isAlive, _callbacks, _highlights, _isWhiteTurn, _states

    pygame.init()
    pygame.font.init()

    txtFont = pygame.font.SysFont('Comic Sans MS', 20)
    _states["_timerWhite"] = -1
    _states["_timerBlack"] = -1

    size = 500, 500
    offset = 70, 70
    case_size = 45, 45
    piece_offset = 2, 2
    _screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Chess.mp4')

    # Chargement des images
    white = []
    white.append(pygame.image.load("assets/white/empty.png"))
    white.append(pygame.image.load("assets/white/pawn.png"))
    white.append(pygame.image.load("assets/white/rook.png"))
    white.append(pygame.image.load("assets/white/knight.png"))
    white.append(pygame.image.load("assets/white/bishop.png"))
    white.append(pygame.image.load("assets/white/king.png"))
    white.append(pygame.image.load("assets/white/queen.png"))
    white.append(pygame.image.load("assets/white/turn.png"))

    black = []
    black.append(pygame.image.load("assets/black/empty.png"))
    black.append(pygame.image.load("assets/black/pawn.png"))
    black.append(pygame.image.load("assets/black/rook.png"))
    black.append(pygame.image.load("assets/black/knight.png"))
    black.append(pygame.image.load("assets/black/bishop.png"))
    black.append(pygame.image.load("assets/black/king.png"))
    black.append(pygame.image.load("assets/black/queen.png"))
    black.append(pygame.image.load("assets/black/turn.png"))

    highlights = []
    highlights.append(pygame.image.load("assets/hl_selected.png"))
    highlights.append(pygame.image.load("assets/hl_move.png"))
    highlights.append(pygame.image.load("assets/hl_capture.png"))

    states = []
    states.append(pygame.image.load("assets/stt_null.png"))
    states.append(pygame.image.load("assets/stt_black.png"))
    states.append(pygame.image.load("assets/stt_white.png"))
    states.append(pygame.image.load("assets/stt_timeout_white.png"))
    states.append(pygame.image.load("assets/stt_timeout_black.png"))
    states.append(pygame.image.load("assets/stt_surrender_white.png"))
    states.append(pygame.image.load("assets/stt_surrender_black.png"))

    nulBtn = pygame.image.load("assets/null.png")
    fnulBtn= pygame.image.load("assets/null_force.png")
    ffBtn  = pygame.image.load("assets/surrender.png")
    timer  = pygame.image.load("assets/timer.png")
    ffPanel= pygame.image.load("assets/surrender_panel.png")

    while True:
        # Détéction des evenements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _isAlive = False
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP and (not "end" in _states or _states["end"] != -1):
                pos = pygame.mouse.get_pos()
                if (_callbacks.__contains__("onClick")):
                    
                    # Assignation des positions selon la fenetre
                    pos_x = pos[0]
                    pos_y = pos[1]

                    # Fenetre "nulle"
                    if ("null" in _states and _states["null"] == 1):
                        if size[0]/2 - 150 < pos_x and pos_x < size[0]/2 and size[1]/2 + 5 < pos_y and pos_y < size[1]/2 + 40:
                            # Bouton "accepter"
                            _callbacks["onClick"](-4)
                        if size[0]/2 < pos_x and pos_x < size[0]/2 + 150 and size[1]/2 + 5 < pos_y and pos_y < size[1]/2 + 40:
                            # Bouton "refuser"
                            _callbacks["onClick"](-3)
                        continue

                    # Boutons "nulle"
                    if 5 < pos_x and pos_x < 35 and 5 < pos_y and pos_y < 35:
                        # Bouton "nulle" coté blanc
                        if "fiftymoves" in _states and _states["fiftymoves"]:
                            _callbacks["onClick"](-4)
                        else:
                            _callbacks["onClick"](-2)

                    if size[0] - 35 < pos_x and pos_x < size[0] - 5 and size[1] - 35 < pos_y and pos_y < size[1] - 5:
                        # Bouton "nulle" coté noir
                        if "fiftymoves" in _states and _states["fiftymoves"]:
                            _callbacks["onClick"](-4)
                        else:
                            _callbacks["onClick"](-2)

                    # Boutons "abandon"
                    if 40 < pos_x and pos_x < 70 and 5 < pos_y and pos_y < 35:
                        # Bouton "abandon" coté blanc
                        _callbacks["onClick"](-1)

                    if size[0] - 70 < pos_x and pos_x < size[0] - 40 and size[1] - 35 < pos_y and pos_y < size[1] - 5:
                        # Bouton "abandon" coté noir
                        _callbacks["onClick"](-1)

                    # Assignation des positions selon la grille
                    pos_x = pos[0] - offset[0]
                    pos_y = pos[1] - offset[1]

                    pos_x = math.floor(pos_x / case_size[0]) 
                    pos_y = math.floor(pos_y / case_size[1]) 

                    if (pos_x < 8 and pos_x >= 0) and (pos_y < 8 and pos_y >= 0):
                        _callbacks["onClick"](pos_x + pos_y * 8)

        # Détéction d'une demande de 'render'
        if _grid != None and (not "end" in _states or _states["end"] != -1):

            _screen.fill((0,0,0))
            for x in range(8):
                for y in range(8):

                    image = white[0]
                    if (x+y)%2:
                        image = black[0]

                    caseId = _grid.getCase(y*8+x)
                    
                    if ((y*8+x) in _highlights):
                        _screen.blit(highlights[_highlights[(y*8+x)]], (offset[0]+case_size[0]*x, offset[1]+case_size[1]*y))
                    else:
                        _screen.blit(image, (offset[0]+45*x, offset[1]+45*y))

                    if (caseId > 0):
                        _screen.blit(white[caseId], (piece_offset[0]+offset[0]+case_size[0]*x, piece_offset[1]+offset[1]+case_size[1]*y))
                    elif (caseId < 0):
                        _screen.blit(black[-caseId], (piece_offset[0]+offset[0]+case_size[0]*x, piece_offset[1]+offset[1]+case_size[1]*y))
            
            # Affichage du tour actuel
            if _isWhiteTurn:
                _screen.blit(white[7], (offset[0], (offset[1]/2 - 12.5)))
            else:
                _screen.blit(black[7], (offset[0], size[1] - (offset[1]/2 + 12.5)))
                
            # Affichage du bouton "nulle" (diffère selon la règle des 50 coups)
            if "fiftymoves" in _states and _states["fiftymoves"]:
                _screen.blit(fnulBtn, (5, 5))
                _screen.blit(fnulBtn, (size[0] - 35, size[1] - 35))
            else:
                _screen.blit(nulBtn, (5, 5))
                _screen.blit(nulBtn, (size[0] - 35, size[1] - 35))

            _screen.blit(ffBtn, (40, 5))
            _screen.blit(ffBtn, (size[0] - 70, size[1] - 35))

            pygame.display.flip()
            _states["_timerWhite"] = -1
            _states["_timerBlack"] = -1

            _grid = None

        # Détéction d'un état de fin
        if "end" in _states and _states["end"] != -1:
            _screen.blit(states[_states["end"]], (size[0]/2 - 180, size[1]/2 - 27.5))
            pygame.display.flip()
            _states["end"] = -1

        if "null" in _states and _states["null"] == 2:
            _screen.blit(ffPanel, (size[0]/2 - 180, size[1]/2 - 50))
            pygame.display.flip()
            _states["null"] = 1

        if "timerWhite" in _states and _states["_timerWhite"] != _states["timerWhite"]:
            _screen.blit(txtFont.render(_states["timerWhite"], False, (255,255,255), (0,0,0)), (5, 40))
            _states["_timerWhite"] = _states["timerWhite"]
            pygame.display.flip()

        if "timerBlack" in _states and _states["_timerBlack"] != _states["timerBlack"]:
            _screen.blit(txtFont.render(_states["timerBlack"], False, (255,255,255), (0,0,0)), (size[0]-70, size[1] - 65))
            _states["_timerBlack"] = _states["timerBlack"]
            pygame.display.flip()

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

def render(grid: board.Plateau, isWhiteTurn: bool):
    """Rafraichis la fenêtre et affiche le plateau de jeu demandé
    
    Précondition: grid est un Plateau

    Postcondition: Aucune
    """
    global _grid, _isWhiteTurn
    _grid = grid
    _isWhiteTurn = isWhiteTurn