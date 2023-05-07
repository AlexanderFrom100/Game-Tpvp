import pygame 
from copy import deepcopy
from random import choice, randrange

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
field = [[0 for i in range(w)]for j in range(h)]

fall_count,fall_speed,fall_limit = 0, 60, 2000

figure = deepcopy(choice(figures))

def check_borders():
    if figure[i].x<0 or figure[i].x>w-1:
        return False
    elif figure[i].y>h-1 or field[figure[i].y][figure[i].x]:
        return False
    return True

while True:
    dx = 0
    game_screen.fill(pygame.Color('black'))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
                fall_limit = 2000
            elif event.key == pygame.K_RIGHT:
                dx = 1
                fall_limit = 2000
            elif event.key == pygame.K_DOWN:
                fall_limit = 100
            
    
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not check_borders():
            figure = deepcopy(figure_old)
            break
        
    fall_count += fall_speed
    if fall_count > fall_limit:
        fall_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not check_borders():
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = pygame.Color('white')
                figure = deepcopy(choice(figures))
                fall_limit = 2000
                break
    
    [pygame.draw.rect(game_screen, (100,100,100), i_rect, 1) for i_rect in grid]
    
    for i in range(4):
        figures_rect.x = figure[i].x * Tile
        figures_rect.y = figure[i].y * Tile
        pygame.draw.rect(game_screen, pygame.Color('white'),figures_rect)
        
    for y, row in enumerate(field):
        for x, col in enumerate(row):
            if col:
                figures_rect.x, figures_rect.y = x*Tile, y*Tile
                pygame.draw.rect(game_screen, col, figures_rect)
            
    pygame.display.flip()
    clock.tick(fps)