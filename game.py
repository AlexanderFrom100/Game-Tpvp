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

figures_pos = [[(-1,0),(-2,0),(0,0),(1,0)],
              [(0,-1),(-1,-1),(-1,0),(0,0)],
              [(-1,0),(-1,1),(0,0),(0,-1)],
              [(0,0),(-1,0),(0,1),(-1,-1)],
              [(0,0),(0,-1),(0,1),(-1,-1)],
              [(0,0),(0,-1),(0,1),(1,-1)],
              [(0,0),(0,-1),(0,1),(-1,0)]]

figures = [[pygame.Rect(x+w//2, y+1, 1, 1)for x,y in fig_pos] for fig_pos in figures_pos]
figures_rect = pygame.Rect(0,0,Tile-2,Tile-2)

figure = figures[0]

while True:
    game_screen.fill(pygame.Color('black'))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    
    [pygame.draw.rect(game_screen, (100,100,100), i_rect, 1) for i_rect in grid]
    
    for i in range(4):
        figures_rect.x = figure[i].x * Tile
        figures_rect.y = figure[i].y * Tile
        pygame.draw.rect(game_screen, pygame.Color('white'),figures_rect)
            
    pygame.display.flip()
    clock.tick(fps)