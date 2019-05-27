import pygame  # Pygame as core

state = 'wait'
pygame.font.init()
font = pygame.font.SysFont('Arial', 30)
playrect = pygame.Rect(220, 350, 224, 54)
playbtn = pygame.Surface((224, 54))
playbtnh = pygame.Surface((224, 54))
playbtn.fill((225, 225, 225))
playbtnh.fill((200, 200, 200))
playbtn.blit(font.render('Replay', False, (0, 0, 0)), (10, 10))
playbtnh.blit(font.render('Replay', False, (0, 0, 0)), (10, 10))

logo = pygame.image.load('img/logo.png')

def draw(screen: pygame.display, coins):
    global state
    screen.blit(logo, (100, 50))
    screen.blit(font.render('Coins: ' + str(coins), False, (0, 0, 0)), (270, 270))
    if playrect.collidepoint(pygame.mouse.get_pos()):
        screen.blit(playbtnh, (220, 350))
        if pygame.mouse.get_pressed()[0] == 1:
            state = 'move'
    else:
        screen.blit(playbtn, (220, 350))