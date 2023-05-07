import pygame 

screen = 800, 600

pygame.init()
game_screen = pygame.display.set_mode(screen)
clock = pygame.time.Clock()

while True:
    game_screen.fill(pygame.Color(200,200,200))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
            
    pygame.display.flip()
    clock.tick()