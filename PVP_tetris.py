import pygame
import sys
from copy import deepcopy
from random import choice, randrange

pygame.init()

dollars = [1200, 3500]

def play_tet(dollars):
    w = 10
    h = 20
    Tile = 35
    screen = w * Tile, h * Tile
    res = 1208, 732
    fps = 60
    next_scr = 150, 150
    
    scr = pygame.display.set_mode(res)
    game_screen = pygame.Surface(screen)
    game_screen2 = pygame.Surface(screen)
    next_screen = pygame.Surface(next_scr)
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
    figures2 = [[pygame.Rect(x+w//2, y+1, 1, 1)for x,y in fig_pos] for fig_pos in figures_pos]
    figures_rect = pygame.Rect(0,0,Tile-2,Tile-2)
    figures_rect2 = pygame.Rect(0,0,Tile-2,Tile-2)
    field = [[0 for i in range(w)]for j in range(h)]
    field2 = [[0 for i in range(w)]for j in range(h)]

    fall_count = 0
    fall_speed = 60
    fall_limit = 2000
    fall_count2 = 0
    fall_speed2 = 60
    fall_limit2 = 2000

    bg = pygame.image.load('tetris1.jpg').convert()

    main_font = pygame.font.Font('font.ttf', 45)
    font = pygame.font.Font('font.ttf', 35)

    title = main_font.render('TETRIS', True, pygame.Color('cyan'))
    t_score = font.render('money:', True, pygame.Color('green'))
    next = font.render('Next:', True, pygame.Color('red'))
    next2 = font.render('Next:', True, pygame.Color('blue'))
    time = font.render('Time:', True, pygame.Color('orange'))

    get_color = lambda : (randrange(60,256), randrange(60,256), randrange(60,256))

    figure = deepcopy(choice(figures))
    figure2 = deepcopy(choice(figures2))
    next_figure = deepcopy(choice(figures))
    next_figure2 = deepcopy(choice(figures2))
    color = get_color()
    next_color = get_color()
    color2 = get_color()
    next_color2 = get_color()

    money = [0, 0]
    lines = 0
    score = {0:0, 1:100, 2:200, 3:600, 4:1200}

    minutes = 2
    seconds = 1
    milseconds = 0

    pygame.mixer.music.load('Tetris.mp3')
    pygame.mixer.music.play()

    line_com = pygame.mixer.Sound('line_complete.mp3')
    game_o = pygame.mixer.Sound('game-over.mp3')
        
    def check_borders():
        if figure[i].x<0 or figure[i].x>w-1:
            return False
        elif figure[i].y>h-1 or field[figure[i].y][figure[i].x]:
            return False
        return True
    
    def check_borders2():
        if figure2[i].x<0 or figure2[i].x>w-1:
            return False
        elif figure2[i].y>h-1 or field2[figure2[i].y][figure2[i].x]:
            return False
        return True

    pygame.display.set_caption('Tetris')
    
    while True:
        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.play()
        game_over = 0
        dx = 0
        dx2 = 0
        rotate = False
        rotate2 = False
        scr.blit(bg, (0, 0))
        scr.blit(game_screen, (137,20))
        scr.blit(game_screen2, (695,20))
        game_screen.fill(pygame.Color('black'))
        game_screen2.fill(pygame.Color('black'))
        scr.blit(next_screen, (-15,80))
        scr.blit(next_screen, (1048,80))
        next_screen.fill(pygame.Color('white'))
        
        for i in range(lines):
            pygame.time.wait(150)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    dx = -1
                if event.key == pygame.K_d:
                    dx = 1
                if event.key == pygame.K_s:
                    fall_limit = 100
                if event.key == pygame.K_w:
                    rotate = True
                if event.key == pygame.K_LEFT:
                    dx2 = -1
                if event.key == pygame.K_RIGHT:
                    dx2 = 1
                if event.key == pygame.K_DOWN:
                    fall_limit2 = 100
                if event.key == pygame.K_UP:
                    rotate2 = True
                
        
        figure_old = deepcopy(figure)
        figure_old2 = deepcopy(figure2)
        for i in range(4):
            figure[i].x += dx
            if not check_borders():
                figure = deepcopy(figure_old)
                break
            
        for i in range(4):
            figure2[i].x += dx2
            if not check_borders2():
                figure2 = deepcopy(figure_old2)
                break
            
        fall_count += fall_speed
        fall_count2 += fall_speed2
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
        
        if fall_count2 > fall_limit2:
            fall_count2 = 0
            figure_old2 = deepcopy(figure2)
            for i in range(4):
                figure2[i].y += 1
                if not check_borders2():
                    for i in range(4):
                        field2[figure_old2[i].y][figure_old2[i].x] = color2
                    figure2 = next_figure2
                    color2 = next_color2
                    next_figure2 = deepcopy(choice(figures2))
                    next_color2 = get_color()
                    fall_limit2 = 2000
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
                
        center2 = figure2[0]
        figure_old2 = deepcopy(figure2)
        for i in range(4):
            if rotate2:
                x = figure2[i].y - center2.y
                y = figure2[i].x - center2.x
                figure2[i].x = center2.x - x
                figure2[i].y = center2.y + y
                if not check_borders2():
                    figure2 = deepcopy(figure_old2)
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
                line_com.play()
                
        line2 = h-1
        lines2 = 0
        for row in range(h-1, -1, -1):
            count2 = 0
            for i in range(w):
                if field2[row][i]:
                    count2+=1
                field2[line2][i] = field2[row][i]
            if count2 < w:
                line2 -= 1
            else:
                fall_speed2 += 3
                lines2 += 1
                line_com.play()
        
        money[0] += score[lines]
        money[1] += score[lines2]
        
        [pygame.draw.rect(game_screen, (100,100,100), i_rect, 1) for i_rect in grid]
        [pygame.draw.rect(game_screen2, (100,100,100), i_rect, 1) for i_rect in grid]
        
        for i in range(4):
            figures_rect.x = figure[i].x * Tile
            figures_rect.y = figure[i].y * Tile
            pygame.draw.rect(game_screen, color,figures_rect)
            
        for i in range(4):
            figures_rect2.x = figure2[i].x * Tile
            figures_rect2.y = figure2[i].y * Tile
            pygame.draw.rect(game_screen2, color2,figures_rect2)

        for y, row in enumerate(field):
            for x, col in enumerate(row):
                if col:
                    figures_rect.x, figures_rect.y = x*Tile, y*Tile
                    pygame.draw.rect(game_screen, col, figures_rect)
                    
        for y, row in enumerate(field2):
            for x, col in enumerate(row):
                if col:
                    figures_rect2.x, figures_rect2.y = x*Tile, y*Tile
                    pygame.draw.rect(game_screen2, col, figures_rect2)
            
        for i in range(4):            
            figures_rect.x = next_figure[i].x * Tile - 100
            figures_rect.y = next_figure[i].y * Tile + 105
            pygame.draw.rect(scr, next_color,figures_rect)
            
        for i in range(4):            
            figures_rect2.x = next_figure2[i].x * Tile + 950
            figures_rect2.y = next_figure2[i].y * Tile + 105
            pygame.draw.rect(scr, next_color2,figures_rect2)
                    
        scr.blit(title, (512, 20))
        scr.blit(t_score, (5, 600))
        scr.blit(t_score, (1050, 600))
        if money[0] > 999:
            scr.blit(font.render(str(money[0]), True, pygame.Color('white')), (10, 650))
        elif money[0] > 99:
            scr.blit(font.render(str(money[0]), True, pygame.Color('white')), (35, 650))
        else:
            scr.blit(font.render(str(money[0]), True, pygame.Color('white')), (75, 650))
            
        if money[1] > 999:
            scr.blit(font.render(str(money[1]), True, pygame.Color('white')), (1050, 650))
        elif money[1] > 99:
            scr.blit(font.render(str(money[1]), True, pygame.Color('white')), (1075, 650))
        else:
            scr.blit(font.render(str(money[1]), True, pygame.Color('white')), (1105, 650))
        
        scr.blit(next, (10,190))
        scr.blit(next2, (1050,190))
        scr.blit(time, (527, 300))
        scr.blit(font.render(str(minutes), True, pygame.Color('white')), (537, 350))
        scr.blit(font.render(':', True, pygame.Color('white')), (567, 345))
        scr.blit(font.render('$', True, pygame.Color('green')), (105, 650))
        scr.blit(font.render('$', True, pygame.Color('green')), (1135, 650))
        
        if seconds < 10:
            scr.blit(font.render('0', True, pygame.Color('white')), (577, 350))
            scr.blit(font.render(str(seconds), True, pygame.Color('white')), (602, 350))
        else:
            scr.blit(font.render(str(seconds), True, pygame.Color('white')), (577, 350))
        
        if milseconds == 0:
            if seconds == 0:
                if minutes == 0:
                    game_over += 1
                else:
                    seconds = 60
                    minutes -= 1
            milseconds = 60
            seconds -= 1
        milseconds -= 1
            
        
        for i in range(w):
            if field[0][i]:
                game_over += 1
                
        for i in range(w):
            if field2[0][i]:
                game_over += 1
        
        if game_over:
            pygame.mixer.music.pause()
            game_o.play()
            field = [[0 for i in range(w)] for i in range(h)]
            dollars = money
            for i_rect in grid:
                pygame.draw.rect(game_screen, get_color(), i_rect)
                pygame.draw.rect(game_screen2, get_color(), i_rect)
                scr.blit(game_screen, (137,20))
                scr.blit(game_screen2, (695,20))
                pygame.display.flip()
                clock.tick(200)
                pygame.time.wait(6)
            shop(dollars)
                
        pygame.display.flip()
        clock.tick(fps)
        
def menu():
    font = pygame.font.SysFont('cambria', 50)
    button_p = pygame.Rect(260, 705,110,60)
    button_q = pygame.Rect(430, 705,110,60)
    play = font.render('PLAY', True, pygame.Color('white'))
    quit = font.render('QUIT', True, pygame.Color('white'))
    pygame.display.set_caption('Welcome to PVP TETRIS')
    Bg = pygame.image.load('GameLogo.jpg')
    res = 800, 800
    scr = pygame.display.set_mode(res)
    while True:
        scr.blit(Bg, (0, 0))
        scr.blit(play, (260, 705))
        scr.blit(quit, (430, 705))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_q.collidepoint(event.pos):
                    pygame.quit()
                if button_p.collidepoint(event.pos):
                    play_tet(dollars)
        a,b = pygame.mouse.get_pos()
        if button_p.x <= a <= button_p.x + 110 and button_p.y <= b <= button_p.y +60:
           play = font.render('PLAY', True, pygame.Color('cyan'))
        else:
            play = font.render('PLAY', True, pygame.Color('white'))
        if button_q.x <= a <= button_q.x + 110 and button_q.y <= b <= button_q.y +60:
           quit = font.render('QUIT', True, pygame.Color('red'))
        else:
            quit = font.render('QUIT', True, pygame.Color('white'))
        scr.blit(quit,(button_q.x, button_q.y))
        scr.blit(play,(button_p.x, button_p.y))
        pygame.display.update()
        
def shop(dollars):
    clock = pygame.time.Clock()
    res = 800, 800
    scr = pygame.display.set_mode(res)
    price = 0
    player_c = 0
    pygame.display.set_caption('Shop')
    font = pygame.font.SysFont('cambria', 50)
    o_font = pygame.font.SysFont('cambria', 30)
    money = o_font.render('Money:', True, pygame.Color('yellow'))
    button_b = pygame.Rect(220, 206,50,40)
    button_b2 = pygame.Rect(658, 206,50,40)
    buy = o_font.render('Buy', True, pygame.Color('white'))
    buy2 = o_font.render('Buy', True, pygame.Color('white'))
    next_p = o_font.render('Next Player', True, pygame.Color('white'))
    button_n = pygame.Rect(628, 20,150,40)
    gun = pygame.image.load('Makarov2.png')
    Ak_gun = pygame.image.load('Ak-47.png')
    
    def col_change(col, dir) -> None:
        for i in range(3):
            col[i] += 1 * dir[i]
            if col[i] >= 255 or col[i] <= 0:
                dir[i] *= -1
                
    col_dir = [-1, 1, 1]
    def_col = [120, 120, 240]
    
    while True:
        title = font.render('GUN SHOP', True, def_col)
        col_change(def_col, col_dir)
        pygame.time.wait(10)
        scr.fill((101, 67, 33))
        scr.blit(title, (300, 10))
        scr.blit(money, (30, 18))
        scr.blit(gun, (50, 60))
        scr.blit(buy, (220, 206))
        scr.blit(buy2, (658, 206))
        scr.blit(next_p, (628, 20))
        scr.blit(Ak_gun, (325, 60))
        scr.blit(o_font.render('100', True, pygame.Color('white')), (143, 206))
        scr.blit(o_font.render('$', True, pygame.Color('green')), (195, 206))
        scr.blit(o_font.render('800', True, pygame.Color('white')), (575, 206))
        scr.blit(o_font.render('$', True, pygame.Color('green')), (628, 206))
        scr.blit(o_font.render('$', True, pygame.Color('green')), (195, 20))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_n.collidepoint(event.pos):
                    if player_c >= 1:
                        break
                    player_c += 1
                if(dollars[player_c] < price or dollars[player_c] <= 0):
                    break
                if button_b.collidepoint(event.pos):
                    dollars[player_c] -= price
                if button_b2.collidepoint(event.pos):
                    dollars[player_c] -= price
                
        
        a,b = pygame.mouse.get_pos()        
        if button_b.x <= a <= button_b.x + 50 and button_b.y <= b <= button_b.y + 40:
           buy = o_font.render('Buy', True, pygame.Color('yellow'))
           price = 100
        else:
           buy = o_font.render('Buy', True, pygame.Color('white'))
           
        if button_b2.x <= a <= button_b2.x + 50 and button_b2.y <= b <= button_b2.y + 40:
           buy2 = o_font.render('Buy', True, pygame.Color('yellow'))
           price = 800
        else:
           buy2 = o_font.render('Buy', True, pygame.Color('white'))
        
        if player_c == 1:
            next_p = o_font.render('End Shop', True, pygame.Color('white'))
            button_n = pygame.Rect(628, 20,122,40)
            if button_n.x <= a <= button_n.x + 122 and button_n.y <= b <= button_n.y + 40:
                next_p = o_font.render('End Shop', True, pygame.Color('cyan'))
            else:
                next_p = o_font.render('End Shop', True, pygame.Color('white'))
        else:
            if button_n.x <= a <= button_n.x + 150 and button_n.y <= b <= button_n.y + 40:
                next_p = o_font.render('Next Player', True, pygame.Color('cyan'))
            else:
                next_p = o_font.render('Next Player', True, pygame.Color('white'))
           
        if dollars[player_c] > 999:
            scr.blit(o_font.render(str(dollars[player_c]), True, pygame.Color('white')), (127, 20))
        elif dollars[player_c] > 99:
            scr.blit(o_font.render(str(dollars[player_c]), True, pygame.Color('white')), (143, 20))
        else:
            scr.blit(o_font.render(str(dollars[player_c]), True, pygame.Color('white')), (177, 20))
        
        clock.tick()
        pygame.display.update()
        
shop(dollars)