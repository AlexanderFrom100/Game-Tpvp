import pygame 

w = 10
h = 20
Tile = 35
screen = w * Tile, h * Tile
fps = 60

pygame.init()
game_screen = pygame.display.set_mode(screen)
clock = pygame.time.Clock()

grid = [pygame.Rect(x * Tile, y * Tile, Tile, Tile) for x in range(w) for y in range(h)]

figure_pos = [[(-1,0),(-2,0),(0,0),(1,0)],
              [(0,-1),(-1,-1),(-1,0),(0,0)],
              [(-1,0),(-1,1),(0,0),(0,-1)],
              [(0,0),(-2,0),(0,0),(1,0)],
              [(0,0),(-2,0),(0,0),(1,0)],
              [(0,0),(-2,0),(0,0),(1,0)],
              [(0,0),(-2,0),(0,0),(1,0)]]

while True:
    game_screen.fill(pygame.Color(200,200,200))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    
    [pygame.draw.rect(game_screen, (100,100,100), i_rect, 1) for i_rect in grid]
            
    pygame.display.flip()
    clock.tick(fps)