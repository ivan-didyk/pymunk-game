import pygame  # Pygame as core

logo = pygame.image.load('img/logo.png')
playbtn = pygame.image.load('img/btn-play.png')
playbtnh = pygame.image.load('img/btn-play-hover.png')
playbtn = pygame.transform.scale(playbtn, (224, 54))
playbtnh = pygame.transform.scale(playbtnh, (224, 54))
playrect = pygame.Rect(220, 300, 224, 54)

state = 'wait'

def draw(screen: pygame.display):
    global state
    screen.blit(logo, (100, 50))
    if playrect.collidepoint(pygame.mouse.get_pos()):
        screen.blit(playbtnh, (220, 300))
        if pygame.mouse.get_pressed()[0] == 1:
            state = 'move'
    else:
        screen.blit(playbtn, (220, 300))