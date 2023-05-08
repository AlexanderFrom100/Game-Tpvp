import pygame 
from copy import deepcopy
from random import choice, randrange

w = 10
h = 20
Tile = 35
screen = w * Tile, h * Tile
res = 584, 732
fps = 60

pygame.init()
scr = pygame.display.set_mode(res)
game_screen = pygame.Surface(screen)
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

fall_count = 0
fall_speed = 60
fall_limit = 2000

bg = pygame.image.load('tetris1.jpg').convert()

main_font = pygame.font.Font('font.ttf', 45)
font = pygame.font.Font('font.ttf', 35)

title = main_font.render('TETRIS', True, pygame.Color('cyan'))
t_score = font.render('money:', True, pygame.Color('green'))

get_color = lambda : (randrange(30,256), randrange(30,256), randrange(30,256))

figure = deepcopy(choice(figures))
next_figure = deepcopy(choice(figures))
color = get_color()
next_color = get_color()

money = 0
lines = 0
score = {0:0, 1:1, 2:3, 3:7, 4:15}

pygame.mixer.music.load('Tetris.mp3')
pygame.mixer.music.play()
    
def check_borders():
    if figure[i].x<0 or figure[i].x>w-1:
        return False
    elif figure[i].y>h-1 or field[figure[i].y][figure[i].x]:
        return False
    return True

while True:
    if pygame.mixer.music.get_busy() == False:
        pygame.mixer.music.play()
    game_over = 0
    dx = 0
    rotate = False
    scr.blit(bg, (0, 0))
    scr.blit(game_screen, (20,20))
    game_screen.fill(pygame.Color('black'))
    
    for i in range(lines):
        pygame.time.wait(200)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
            if event.key == pygame.K_RIGHT:
                dx = 1
            if event.key == pygame.K_DOWN:
                fall_limit = 100
            if event.key == pygame.K_UP:
                rotate = True
        else:
            fall_limit = 2000
            
    
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
                    field[figure_old[i].y][figure_old[i].x] = color
                figure = next_figure
                color = next_color
                next_figure = deepcopy(choice(figures))
                next_color = get_color()
                fall_limit = 2000
                break
    
    center = figure[0]
    figure_old = deepcopy(figure)
    for i in range(4):
        if rotate:
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_borders():
                figure = deepcopy(figure_old)
                break
    
    line = h-1
    lines = 0
    for row in range(h-1, -1, -1):
        count = 0
        for i in range(w):
            if field[row][i]:
                count+=1
            field[line][i] = field[row][i]
        if count < w:
            line -= 1
        else:
            fall_speed += 3
            lines += 1
    
    money += score[lines]
    
    [pygame.draw.rect(game_screen, (100,100,100), i_rect, 1) for i_rect in grid]
    
    for i in range(4):
        figures_rect.x = figure[i].x * Tile
        figures_rect.y = figure[i].y * Tile
        pygame.draw.rect(game_screen, color,figures_rect)
        
    for y, row in enumerate(field):
        for x, col in enumerate(row):
            if col:
                figures_rect.x, figures_rect.y = x*Tile, y*Tile
                pygame.draw.rect(game_screen, col, figures_rect)
        
    for i in range(4):            
        figures_rect.x = next_figure[i].x * Tile + 300
        figures_rect.y = next_figure[i].y * Tile + 105
        pygame.draw.rect(scr, next_color,figures_rect)
                
    scr.blit(title, (395, 20))
    scr.blit(t_score, (395, 600))
    scr.blit(font.render(str(money), True, pygame.Color('white')), (440, 650))
    
    for i in range(w):
        if field[0][i]:
            pygame.mixer.music.pause()
            field = [[0 for i in range(w)] for i in range(h)]
            fall_count = 0
            fall_speed = 60
            fall_limit = 2000
            money = 0
            game_over += 1
            for i_rect in grid:
                pygame.draw.rect(game_screen, get_color(), i_rect)
                scr.blit(game_screen, (20, 20))
                pygame.display.flip()
                clock.tick(200)
    if game_over:
        pygame.mixer.music.unpause()
        pygame.mixer.music.rewind()
            
    pygame.display.flip()
    clock.tick(fps)