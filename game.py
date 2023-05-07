import pygame 

w = 10
h = 20
Tile = 45
screen = w * Tile, h * Tile
fps = 60

pygame.init()
game_screen = pygame.display.set_mode(screen)
clock = pygame.time.Clock()

grid = [pygame.Rect(x * Tile, y * Tile, Tile, Tile) for x in range(w) for y in range(h)]

while True:
    game_screen.fill(pygame.Color(200,200,200))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
            
    pygame.display.flip()
    clock.tick(fps)