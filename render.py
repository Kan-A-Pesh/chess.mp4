import pygame, sys, plateau, _thread

_grid = None
_isAlive = True

def init():
    """Initialise la fenetre et affiche le menu.

    Précondition: Aucune

    Postcondition: Aucune
    """
    _thread.start_new_thread(_render_loop, ())

def _render_loop():
    """Function hors-thread principal, ce dernier ne doit pas etre
    éxécuté dans le thread principal!
    Toujours actif, détermine les éventuels événement sur la fenetre
    ainsi que les demande de 'render'
    """
    global _grid, _isAlive

    pygame.init()

    size = 500, 500
    _screen = pygame.display.set_mode(size)

    # Chargement des images
    white = []
    white.append(pygame.image.load("assets/white/pawn.png"))
    white.append(pygame.image.load("assets/white/rook.png"))
    white.append(pygame.image.load("assets/white/knight.png"))
    white.append(pygame.image.load("assets/white/bishop.png"))
    white.append(pygame.image.load("assets/white/king.png"))
    white.append(pygame.image.load("assets/white/queen.png"))

    black = []
    black.append(pygame.image.load("assets/black/pawn.png"))
    black.append(pygame.image.load("assets/black/rook.png"))
    black.append(pygame.image.load("assets/black/knight.png"))
    black.append(pygame.image.load("assets/black/bishop.png"))
    black.append(pygame.image.load("assets/black/king.png"))
    black.append(pygame.image.load("assets/black/queen.png"))

    emptyA = pygame.image.load("assets/emptyA.png")
    emptyB = pygame.image.load("assets/emptyB.png")

    while True:
        # Détéction des evenements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _isAlive = False
                sys.exit()

        # Détéction d'une demande de 'render'
        if _grid != None:

            _screen.fill((0,0,0))
            _screen.blit(white[0], white[0].get_rect())
            pygame.display.flip()

            _grid = None

def render(grid: plateau.Plateau):
    """Rafraichis la fenêtre et affiche le plateau de jeu demandé
    
    Précondition: grid est un Plateau

    Postcondition: Aucune
    """
    global _grid
    _grid = grid

if __name__ == "__main__":
    init()
    render(plateau.Plateau())
    while 1:
        if _isAlive == False: sys.exit()