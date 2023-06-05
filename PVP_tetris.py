import pygame
import sys
from copy import deepcopy
from random import choice, randrange

pygame.init()

dollars = [3000, 3000]

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
    
    g_o_scr = pygame.image.load('game_over.jpg').convert()

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

    money = dollars
    lines = 0
    score = {0:0, 1:100, 2:200, 3:600, 4:1200}

    minutes = 2
    seconds = 1
    milseconds = 0
    
    player_over = 0
    player_over2 = 0

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
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    fall_limit = 2000
                if event.key == pygame.K_DOWN:
                    fall_limit2 = 2000
                
        
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
            figures_rect.x = next_figure[i].x * Tile - 110
            figures_rect.y = next_figure[i].y * Tile + 105
            if player_over:
                pygame.draw.rect(scr, 'white',figures_rect)
            else:
                pygame.draw.rect(scr, next_color,figures_rect)
            
        for i in range(4):            
            figures_rect2.x = next_figure2[i].x * Tile + 950
            figures_rect2.y = next_figure2[i].y * Tile + 105
            if player_over2:
                pygame.draw.rect(scr, 'white',figures_rect2)
            else:
                pygame.draw.rect(scr, next_color2,figures_rect2)
                    
        scr.blit(title, (512, 20))
        scr.blit(t_score, (5, 600))
        scr.blit(t_score, (1050, 600))
        
        n = len(str(money[0]))
        n2 = len(str(money[1]))
        scr.blit(font.render(str(money[0]), True, pygame.Color('white')), (105 - n*23, 650))
        scr.blit(font.render(str(money[1]), True, pygame.Color('white')), (1145 - n2*23, 650))
        
        scr.blit(next, (10,190))
        scr.blit(next2, (1050,190))
        scr.blit(time, (527, 300))
        scr.blit(font.render(str(minutes), True, pygame.Color('white')), (537, 350))
        scr.blit(font.render(':', True, pygame.Color('white')), (567, 345))
        scr.blit(font.render('$', True, pygame.Color('green')), (108, 650))
        scr.blit(font.render('$', True, pygame.Color('green')), (1148, 650))
        
        if seconds < 10:
            scr.blit(font.render('0', True, pygame.Color('white')), (577, 350))
            scr.blit(font.render(str(seconds), True, pygame.Color('white')), (602, 350))
        else:
            scr.blit(font.render(str(seconds), True, pygame.Color('white')), (577, 350))
        
        if milseconds == 0:
            if seconds == 0:
                if minutes == 0:
                    player_over += 1
                    player_over2 += 1
                else:
                    seconds = 60
                    minutes -= 1
            milseconds = 60
            seconds -= 1
        milseconds -= 1
        
        for i in range(w):
            if player_over2:
                scr.blit(g_o_scr, (695,20))
            if player_over:
                scr.blit(g_o_scr, (137,20))
                break
            if field[0][i]:
                player_over += 1
                game_o.play()
                for i_rect in grid:
                    pygame.draw.rect(game_screen, get_color(), i_rect)
                    scr.blit(game_screen, (137,20))
                    pygame.display.flip()
                    clock.tick(200)
                    pygame.time.wait(6)
                
        for i in range(w):
            if player_over2:
                scr.blit(g_o_scr, (695,20))
                break
            if field2[0][i]:
                player_over2 += 1
                game_o.play()
                for i_rect in grid:
                    pygame.draw.rect(game_screen2, get_color(), i_rect)
                    scr.blit(game_screen2, (695,20))
                    pygame.display.flip()
                    clock.tick(200)
                    pygame.time.wait(6)
                break

        if player_over and player_over2:
            game_over += 1
        
        if game_over:
            pygame.mixer.music.pause()
            dollars = money
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
    sh_pl = font.render('Player turn:', True, pygame.Color('green'))
    money = o_font.render('Money:', True, pygame.Color('blue'))
    button_b = pygame.Rect(170, 206,50,40)
    button_b2 = pygame.Rect(558, 206,50,40)
    button_b3 = pygame.Rect(350, 366,50,40)
    buy = o_font.render('Buy', True, pygame.Color('white'))
    buy2 = o_font.render('Buy', True, pygame.Color('white'))
    buy3 = o_font.render('Buy', True, pygame.Color('white'))
    button_e = pygame.Rect(40, 475,70,40)
    equip = o_font.render('Equip', True, pygame.Color('white'))
    next_p = o_font.render('Next Player', True, pygame.Color('white'))
    button_n = pygame.Rect(628, 20,150,40)
    gun = pygame.image.load('Makarov2.png')
    Ak_gun = pygame.image.load('Ak-47.png')
    pump = pygame.image.load('pump.png')
    
    g_equip = pygame.image.load('Makarov_eqip.png')
    
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
        scr.blit(buy, (170, 206))
        scr.blit(buy2, (558, 206))
        scr.blit(buy3, (350, 366))
        scr.blit(next_p, (628, 20))
        scr.blit(Ak_gun, (325, 60))
        scr.blit(pump, (50, 230))
        
        scr.blit(g_equip, (30, 400))
        scr.blit(equip, (40, 475))
        scr.blit(o_font.render('1000', True, pygame.Color('white')), (253, 366))
        scr.blit(o_font.render('$', True, pygame.Color('green')), (325, 366))
        scr.blit(o_font.render('100', True, pygame.Color('white')), (93, 206))
        scr.blit(o_font.render('$', True, pygame.Color('green')), (145, 206))
        scr.blit(o_font.render('800', True, pygame.Color('white')), (475, 206))
        scr.blit(o_font.render('$', True, pygame.Color('green')), (528, 206))
        scr.blit(o_font.render('$', True, pygame.Color('green')), (195, 20))
        scr.blit(sh_pl, (460, 700))
        if player_c:
            scr.blit(font.render('2', True, pygame.Color('orange')), (720, 705))
        else:
            scr.blit(font.render('1', True, pygame.Color('orange')), (720, 705))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_c > 0:
                    if button_n.collidepoint(event.pos):
                        play_tet(dollars)
                else:
                    if button_n.collidepoint(event.pos):
                        player_c += 1
                if dollars[player_c] < price or dollars[player_c] <= 0:
                    break
                if button_b.collidepoint(event.pos):
                    dollars[player_c] -= price
                if button_b2.collidepoint(event.pos):
                    dollars[player_c] -= price
                if button_b3.collidepoint(event.pos):
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
           
        if button_e.x <= a <= button_e.x + 70 and button_e.y <= b <= button_e.y + 40:
           equip = o_font.render('Equip', True, pygame.Color('yellow'))
        else:
           equip = o_font.render('Equip', True, pygame.Color('white'))
           
        if button_b3.x <= a <= button_b3.x + 50 and button_b3.y <= b <= button_b3.y + 40:
           buy3 = o_font.render('Buy', True, pygame.Color('yellow'))
           price = 1000
        else:
           buy3 = o_font.render('Buy', True, pygame.Color('white'))
        
        if player_c != 0:
            money = o_font.render('Money:', True, pygame.Color('red'))
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

def twodshoot():
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 750
    clock = pygame.time.Clock()
    FPS = 60
    GRAVITY = 0.75
    moving_left = False
    moving_right = False
    moving_left2 = False
    moving_right2 = False
    BG = (144, 201, 120)
    shoot = False
    shoot2 = False
    
    bullet_img = pygame.image.load('bullet.png')

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('2dShooter')

    class Soldier(pygame.sprite.Sprite):
        def __init__(self, char_type, x, y, scale, speed, ammo):
            pygame.sprite.Sprite.__init__(self)
            self.alive = True
            self.char_type = char_type
            self.speed = speed
            self.ammo = ammo
            self.start_ammo = ammo
            self.shoot_cooldown = 0
            self.health = 100
            self.max_health = self.health
            self.direction = 1
            self.flip = False
            self.vel_y = 0
            self.in_air = True
            self.jump = False
            img = pygame.image.load(f'{self.char_type}.png')
            self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)


        def move(self, moving_left, moving_right):
            dx = 0
            dy = 0
            
            self.vel_y += GRAVITY
            if self.vel_y > 10:
                self.vel_y
            dy += self.vel_y

            if self.jump == True and self.in_air == False:
                self.vel_y = -11
                self.jump = False
                self.in_air = True
                
            if self.rect.x < 2:
                moving_left = False
            if self.rect.x > SCREEN_WIDTH-self.image.get_width()-2:
                moving_right = False

            if moving_left:
                dx = -self.speed
                self.flip = True
                self.direction = -1
            if moving_right:
                dx = self.speed
                self.flip = False
                self.direction = 1
                
            if self.rect.bottom + dy > 300:
                dy = 300 - self.rect.bottom
                self.in_air = False



            self.rect.x += dx
            self.rect.y += dy
            
        def shoot(self):
            if self.shoot_cooldown == 0 and self.ammo > 0:
                self.shoot_cooldown = 20
                bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
                bullet_group.add(bullet)
                self.ammo -= 1


        def draw(self):
            screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
            
    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y, direction):
            pygame.sprite.Sprite.__init__(self)
            self.speed = 10
            self.image = bullet_img
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.direction = direction

        def update(self):
            self.rect.x += (self.direction * self.speed)
            if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
                self.kill()

            if pygame.sprite.spritecollide(player, bullet_group, False):
                if player.alive:
                    player.health -= 10
                    self.kill()
            if pygame.sprite.spritecollide(player2, bullet_group, False):
                if player2.alive:
                    player2.health -= 10
                    print(player2.health)
                    self.kill()


    bullet_group = pygame.sprite.Group()

            
    player = Soldier('1x4', 200, 200, 3, 5, 20)
    player2 = Soldier('1x4r', 400, 200, 3, 5, 20)

    run = True
    while run:
        clock.tick(FPS)
        screen.fill(BG)
        pygame.draw.line(screen, (255,0,0), (0, 300), (SCREEN_WIDTH, 300))
        player.draw()
        player2.draw()
        player.move(moving_left, moving_right)
        player2.move(moving_left2, moving_right2)
        bullet_group.update()
        bullet_group.draw(screen)
        if player.shoot_cooldown > 0:
                player.shoot_cooldown -= 1
        if player2.shoot_cooldown > 0:
                player2.shoot_cooldown -= 1
        if player.health <= 0:
            player.alive = False 
        if player2.health <= 0:
            player2.alive = False 
        
        if player.alive:
            run = True
        else:
            run = False
            break
        if player2.alive:
            run = True
        else:
            run = False
            break
        if shoot:
            player.shoot()
        if shoot2:
            player2.shoot()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    moving_left = True
                if event.key == pygame.K_d:
                    moving_right = True
                if event.key == pygame.K_w:
                    player.jump = True
                if event.key == pygame.K_f:
                    shoot = True
                if event.key == pygame.K_LEFT:
                    moving_left2 = True
                if event.key == pygame.K_RIGHT:
                    moving_right2 = True
                if event.key == pygame.K_UP:
                    player2.jump = True
                if event.key == pygame.K_RCTRL:
                    shoot2 = True
                if event.key == pygame.K_ESCAPE:
                    run = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    moving_left = False
                if event.key == pygame.K_d:
                    moving_right = False
                if event.key == pygame.K_f:
                    shoot = False
                if event.key == pygame.K_LEFT:
                    moving_left2 = False
                if event.key == pygame.K_RIGHT:
                    moving_right2 = False
                if event.key == pygame.K_RCTRL:
                    shoot2 = False

        pygame.display.update()
    return
        
twodshoot()
pygame.quit()