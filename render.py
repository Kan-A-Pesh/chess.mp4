import pygame, sys

screen = None

def init():
    global screen

    pygame.init()

    size = 500, 500

    screen = pygame.display.set_mode(size)

ball = pygame.image.load("assets\white\king.png")
ballrect = ball.get_rect()

def render():
    global screen
    
    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()