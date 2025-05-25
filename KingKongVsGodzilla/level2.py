import random
import pygame

pygame.init()

#Screen
info = pygame.display.Info()
width, height = info.current_w, info.current_h
window_w, window_h = width - 800, height - 300
screen = pygame.display.set_mode([window_w, window_h])
pygame.display.set_caption('King Kong vs. Mech Godzilla!')

#state
class GameState:
    def __init__(self):
        self.reset()
    #reset if die    
    def reset(self):
        self.active_level = 0
        self.counter = 0
        self.score = 0
        self.high_score = 0
        self.lives = 3
        self.bonus = 6000
        self.first_rock_trigger = False
        self.victory = False
        self.reset_game = False
        self.game_over = False
        self.beam_Spawn = 360
        self.beam_Count = self.beam_Spawn // 2
        self.beam_time = 360
        self.rock_trigger = False

state = GameState()

timer = pygame.time.Clock()
fps = 60

pygame.mixer.init()
#Volume
theme_vol = 0.5
volume = 0.7
#Sounds
theme = pygame.mixer.Sound('assets/sounds/theme2.mp3')
theme.set_volume(theme_vol)
beam_sound = pygame.mixer.Sound('assets/sounds/beam2.mp3')
beam_sound.set_volume(volume)
jump_sound = pygame.mixer.Sound('assets/sounds/jump.mp3')
jump_sound.set_volume(volume)
club_sound = pygame.mixer.Sound('assets/sounds/club.mp3') 
club_sound.set_volume(volume)
death_sound = pygame.mixer.Sound('assets/sounds/death.mp3')
death_sound.set_volume(volume)
victory_sound = pygame.mixer.Sound('assets/sounds/victory.mp3')
victory_sound.set_volume(volume)
rock_sound = pygame.mixer.Sound('assets/sounds/rock.mp3')
rock_sound.set_volume(volume)
#Fonts for GUI
font = pygame.font.Font('assets/fonts/Boldonse-Regular.ttf', 50)
font2 = pygame.font.Font('assets/fonts/Boldonse-Regular.ttf', 30)
#Monitor Dimensions
section_w = window_w // 32
section_h = window_h // 32
sect = section_h // 8
#Rows for the levels
r1 = window_h - 2 * section_h
r2 = r1 - 4 * section_h
r3 = r2 - 7 * sect - 3 * section_h
r4 = r3 - 4 * section_h
r5 = r4 - 7 * sect - 3 * section_h
r6 = r5 - 4 * section_h
#Horizontal for each row (coloumn)
row6_top = r6 - 4 * sect
row5_top = r5 - 8 * sect
row4_top = r4 - 8 * sect
row3_top = r3 - 8 * sect
row2_top = r2 - 8 * sect
row1_top = r1 - 5 * sect
#background image
wallpaper = pygame.transform.scale(pygame.image.load('assets/images/wallpaper/wall2.png'), (window_w, window_h))
#mechgodzilla
zilla1 = pygame.transform.scale(pygame.image.load('assets/images/mech/mech_godzilla1.png'), (section_w * 5, section_h * 5))
zilla2 = pygame.transform.scale(pygame.image.load('assets/images/mech/mech_godzilla2.png'), (section_w * 5, section_h * 5))
zilla3 = pygame.transform.scale(pygame.image.load('assets/images/mech/mech_godzilla3.png'), (section_w * 5, section_h * 5))
#godzilla attack
beam_img = pygame.transform.scale(pygame.image.load('assets/images/mech/beam2.png'), (section_w * 2, section_h * 1.5))
#baby kong
baby1 = pygame.transform.scale(pygame.image.load('assets/images/baby/babykong.png'), (2 * section_w, 3 * section_h))
baby2 = pygame.transform.scale(pygame.image.load('assets/images/baby/babykong.png'), (2 * section_w, 3 * section_h))
#rocks
rocks = pygame.transform.scale(pygame.image.load('assets/images/rocks/rocks.png'), (3 * section_w, 4 * section_h))
rock = pygame.transform.scale(pygame.image.load('assets/images/rocks/rock1.png'), (1 * section_w, 1.5 * section_h))
rock2 = pygame.transform.scale(pygame.image.load('assets/images/rocks/rock2.png'), (1 * section_w, 1.5 * section_h))
#king kong
standing = pygame.transform.scale(pygame.image.load('assets/images/kingkong/kong_idle.png'), (2 * section_w, 2.5 * section_h))
jumping = pygame.transform.scale(pygame.image.load('assets/images/kingkong/kong_jumping.png'), (2 * section_w, 2.5 * section_h))
running = pygame.transform.scale(pygame.image.load('assets/images/kingkong/kong_running.png'), (2 * section_w, 2.5 * section_h))
climb = pygame.transform.scale(pygame.image.load('assets/images/kingkong/kong_idle.png'), (2 * section_w, 2.5 * section_h))
climb2 = pygame.transform.scale(pygame.image.load('assets/images/kingkong/kong_idle.png'), (2 * section_w, 2.5 * section_h))
Club_Idle = pygame.transform.scale(pygame.image.load('assets/images/kingkong/kong_idle.png'), (2.5 * section_w, 2.5 * section_h))
Club_Jump = pygame.transform.scale(pygame.image.load('assets/images/kingkong/kong_stickjump.png'), (2.5 * section_w, 2.5 * section_h))
Club_Attack = pygame.transform.scale(pygame.image.load('assets/images/kingkong/kong_stickattack.png'), (2.5 * section_w, 3.5 * section_h))
#king kong weapon
Stick = pygame.transform.scale(pygame.image.load('assets/images/kingkong/club.png'), (1 * section_w, 2 * section_h))

section_w = window_w // 32
section_h = window_h // 32
sect = section_h // 8

#Level design
levels = [{
    'rows': [
        (1, r1, 15), (16, r1 - sect, 3), (19, r1 - 2 * sect, 3), (22, r1 - 3 * sect, 3),
        (25, r1 - 4 * sect, 3), (28, r1 - 5 * sect, 3), (25, r2, 3), (22, r2 - sect, 3),
        (19, r2 - 2 * sect, 3), (16, r2 - 3 * sect, 3), (13, r2 - 4 * sect, 3), (10, r2 - 5 * sect, 3),
        (7, r2 - 6 * sect, 3), (4, r2 - 7 * sect, 3), (2, r2 - 8 * sect, 2), (4, r3, 3),
        (7, r3 - sect, 3), (10, r3 - 2 * sect, 3), (13, r3 - 3 * sect, 3), (16, r3 - 4 * sect, 3),
        (19, r3 - 5 * sect, 3), (22, r3 - 6 * sect, 3), (25, r3 - 7 * sect, 3), (28, r3 - 8 * sect, 2),
        (25, r4, 3), (22, r4 - sect, 3), (19, r4 - 2 * sect, 3), (16, r4 - 3 * sect, 3),
        (13, r4 - 4 * sect, 3), (10, r4 - 5 * sect, 3), (7, r4 - 6 * sect, 3), (4, r4 - 7 * sect, 3),
        (2, r4 - 8 * sect, 2), (4, r5, 3), (7, r5 - sect, 3), (10, r5 - 2 * sect, 3),
        (13, r5 - 3 * sect, 3), (16, r5 - 4 * sect, 3), (19, r5 - 5 * sect, 3), (22, r5 - 6 * sect, 3),
        (25, r5 - 7 * sect, 3), (28, r5 - 8 * sect, 2), (25, r6, 3), (22, r6 - sect, 3),
        (19, r6 - 2 * sect, 3), (16, r6 - 3 * sect, 3), (2, r6 - 4 * sect, 14), (13, r6 - 4 * section_h, 6),
        (10, r6 - 3 * section_h, 3)],
    'columns': [
        (12, r2 + 6 * sect, 2), (12, r2 + 26 * sect, 2), (25, r2 + 11 * sect, 4), (6, r3 + 11 * sect, 3),
        (14, r3 + 8 * sect, 4), (10, r4 + 6 * sect, 1), (10, r4 + 24 * sect, 2), (16, r4 + 6 * sect, 5),
        (25, r4 + 9 * sect, 4), (6, r5 + 11 * sect, 3), (11, r5 + 8 * sect, 4), (23, r5 + 4 * sect, 1),
        (23, r5 + 24 * sect, 2), (25, r6 + 9 * sect, 4), (13, r6 + 5 * sect, 2), (13, r6 + 25 * sect, 2),
        (18, r6 - 27 * sect, 4), (12, r6 - 17 * sect, 2), (10, r6 - 17 * sect, 2), (12, -5, 13), (10, -5, 13)],
    'Clubs': [(4, row6_top + section_h), (25, row6_top - section_h), (4, row4_top + section_h), (27, row5_top + section_h)],
    'target': (13, r6 - 4 * section_h, 3)}]

#King KONG
class King_Kong(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.y_change = 0
        self.x_speed = 3
        self.x_change = 0
        self.landed = False
        self.pos = 0
        self.dir = 1
        self.count = 0
        self.climbing = False
        self.image = standing
        self.Club = False
        self.max_Club = 450
        self.Club_len = self.max_Club
        self.Club_pos = 1
        self.rect = self.image.get_rect()
        self.hitbox = self.rect
        self.Club_box = self.rect
        self.rect.center = (x_pos, y_pos)
        self.over_beams = False
        self.bottom = pygame.Rect(self.rect.left, self.rect.bottom - 20, self.rect.width, 20)
        self.club_channel = None
    #update king kong
    def update(self):
        self.landed = False
        for plat in plats:
            if self.bottom.colliderect(plat):
                self.landed = True
                if not self.climbing:
                    self.rect.centery = plat.top - self.rect.height // 2 + 1
        
        if not self.landed and not self.climbing:
            self.y_change += 0.25
        
        self.rect.x += self.x_change * self.x_speed
        self.rect.y += self.y_change
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > window_w:
            self.rect.right = window_w
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > window_h:
            self.rect.bottom = window_h
            self.landed = True
            self.y_change = 0
        
        self.bottom = pygame.Rect(self.rect.left, self.rect.bottom - 20, self.rect.width, 20)
        
        if self.x_change != 0 or (self.climbing and self.y_change != 0):
            if self.count < 3:
                self.count += 1
            else:
                self.count = 0
                if self.pos == 0:
                    self.pos += 1
                else:
                    self.pos = 0
        else:
            self.pos = 0
        
        if self.Club:
            self.Club_pos = (self.Club_len // 30) % 2
            self.Club_len -= 1
            if self.Club_len <= 0:
                self.Club = False
                self.Club_len = self.max_Club
                if self.club_channel:
                    self.club_channel.stop()
    #hitbox of KingKong
    def calc_hitbox(self):
        if not self.Club:
            self.hitbox = pygame.Rect(self.rect.left + 15, self.rect.top + 5, self.rect.width - 30, self.rect.height - 10)
            self.Club_box = pygame.Rect(0, 0, 0, 0)
        elif self.Club_pos == 0:
            if self.dir == 1:
                self.hitbox = pygame.Rect(self.rect.left + 15, self.rect.top + 5,self.rect.width - 30, self.rect.height - 10)
                self.Club_box = pygame.Rect(self.rect.right - 10, self.rect.top + 5,section_w, self.rect.height - 10)
            else:
                self.hitbox = pygame.Rect(self.rect.left + 15, self.rect.top + 5, self.rect.width - 30, self.rect.height - 10)
                self.Club_box = pygame.Rect(self.rect.left - section_w + 10, self.rect.top + 5,section_w, self.rect.height - 10)
        else:
            self.hitbox = pygame.Rect(self.rect.left + 15, self.rect.top + 5,self.rect.width - 30, self.rect.height - 10)
            self.Club_box = pygame.Rect(self.rect.left + 15, self.rect.top - section_h,self.rect.width - 30, section_h)
    #animate king kong through images
    def draw(self):
        if not self.Club:
            if not self.climbing and self.landed:
                if self.pos == 0:
                    self.image = standing
                else:
                    self.image = running
            elif not self.landed and not self.climbing:
                self.image = jumping
            elif self.climbing:
                if self.pos == 0:
                    self.image = climb
                else:
                    self.image = climb2
        else:
            if self.Club_pos == 0:
                self.image = Club_Jump
            else:
                self.image = Club_Attack
        if not isinstance(self.image, pygame.Surface):
            self.image = standing         
        if self.dir == -1:
            self.image = pygame.transform.flip(self.image, True, False)    
        self.calc_hitbox()   
        if self.Club_pos == 1 and self.Club:
            screen.blit(self.image, (self.rect.left, self.rect.top - section_h))
        else:
            screen.blit(self.image, self.rect)
#Club stick weapon
class Club(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = Stick
        self.rect = self.image.get_rect()
        self.rect.topleft = (x_pos * section_w, y_pos)
        self.used = False
    #when king kong touch club
    def draw(self):
        if not self.used:
            screen.blit(self.image, self.rect)
            if self.rect.colliderect(kong.hitbox):
                self.used = True
                kong.Club = True
                kong.Club_len = kong.max_Club
                club_sound.play()
                self.kill()
#beam class
class Beam(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = beam_img
        self.image = self.original_image  
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos, y_pos)
        self.y_change = 0
        self.x_change = random.choice([-3, 3])
        self.Beamd_collision = False
        self.falling = False
        self.check_lad = False
        self.bottom = pygame.Rect(self.rect.left, self.rect.bottom - 5, self.rect.width, 5)
        self.hitbox = pygame.Rect(0, 0, self.rect.width * 0.8, self.rect.height * 0.8)
        self.hitbox.center = self.rect.center
        self.current_row = None  
        self.flipped = False  
    #update beams
    def update(self, beam_trig):
        self.falling = True
        self.hitbox.center = self.rect.center
        #if new rows, flip
        new_row = None
        if self.rect.bottom < r6:
            new_row = 6
        elif self.rect.bottom < r5:
            new_row = 5
        elif self.rect.bottom < r4:
            new_row = 4
        elif self.rect.bottom < r3:
            new_row = 3
        elif self.rect.bottom < r2:
            new_row = 2
        else:
            new_row = 1
            
        if new_row != self.current_row and self.current_row is not None and new_row != 1:
            self.flipped = not self.flipped
            self.image = pygame.transform.flip(self.original_image, False, self.flipped)
            
        self.current_row = new_row
        
        for plat in plats:
            if self.bottom.colliderect(plat):
                self.falling = False
                self.y_change = 0
                self.rect.bottom = plat.top + 1
                break
        
        if self.falling:
            self.y_change = min(self.y_change + 0.5, 8)
        
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        
        if self.rect.left < 0:
            self.rect.left = 0
            self.x_change *= -1
            self.image = pygame.transform.flip(self.original_image, self.x_change < 0, self.flipped)
        if self.rect.right > window_w:
            self.rect.right = window_w
            self.x_change *= -1
            self.image = pygame.transform.flip(self.original_image, self.x_change < 0, self.flipped)
        
        if self.rect.colliderect(Beamd_drum) and not self.Beamd_collision:
            self.Beamd_collision = True
            if random.randint(0, 4) == 4:
                beam_trig = True
        
        self.bottom = pygame.Rect(self.rect.left, self.rect.bottom - 5, self.rect.width, 5)
        
        if self.rect.top > window_h:
            self.kill()
        
        return beam_trig
    #will check if it fell
    def check_fall(self):
        if not self.falling:
            below = pygame.Rect(self.rect.left, self.rect.bottom, self.rect.width, 5)
            for lad in lads:
                if below.colliderect(lad) and random.randint(0, 60) == 60:
                    self.falling = True
                    self.y_change = 2
                    break

    def draw(self):
        screen.blit(self.image, self.rect)
#rocks
class Crystal(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = rock
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos, y_pos)
        self.pos = 1
        self.count = 0
        self.x_count = 0
        self.x_change = 2
        self.x_max = 4
        self.y_change = 0
        self.row = 1
        self.check_lad = False
        self.climbing = False
    #update rocks
    def update(self):
        if self.y_change < 3 and not self.climbing:
            self.y_change += 0.25
        
        for plat in plats:
            if self.rect.colliderect(plat):
                self.climbing = False
                self.y_change = -4
                break
        
        if self.count < 15:
            self.count += 1
        else:
            self.count = 0
            self.pos *= -1
            if self.x_count < self.x_max:
                self.x_count += 1
            else:
                self.x_count = 0
                if self.row in [1, 3, 5]:
                    self.x_max = random.randint(3, 6) if self.x_change > 0 else random.randint(6, 10)
                else:
                    self.x_max = random.randint(6, 10) if self.x_change > 0 else random.randint(3, 6)
                self.x_change *= -1
        
        if self.pos == 1:
            self.image = rock if self.x_change > 0 else pygame.transform.flip(rock, True, False)
        else:
            self.image = rock2 if self.x_change > 0 else pygame.transform.flip(rock2, True, False)
        
        if not isinstance(self.image, pygame.Surface):
            self.image = rock
        
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        
        if self.rect.top > window_h or self.rect.top < 0:
            self.kill()

    def check_climb(self):
        if not self.climbing:
            for lad in lads:
                if self.rect.colliderect(lad) and random.randint(0, 120) == 120:
                    self.climbing = True
                    self.y_change = -4
                    break
        
        if self.rect.bottom < r6:
            self.row = 6
        elif self.rect.bottom < r5:
            self.row = 5
        elif self.rect.bottom < r4:
            self.row = 4
        elif self.rect.bottom < r3:
            self.row = 3
        elif self.rect.bottom < r2:
            self.row = 2
        else:
            self.row = 1
#platform starting with the floor (rows)
class Floor:
    def __init__(self, x_pos, y_pos, length):
        self.x_pos = x_pos * section_w
        self.y_pos = y_pos
        self.length = length
        self.top = self.draw()
    #draw the floors
    def draw(self):
        line_width = 7
        platform_color = (255,255,0)
        #create floors
        for i in range(self.length):
            left = self.x_pos + (section_w * i)
            mid = left + (section_w * 0.5)
            right = left + section_w
            top = self.y_pos
            bottom = top + section_h
            #floors
            pygame.draw.line(screen, platform_color, (left, top), (right, top), line_width)
            pygame.draw.line(screen, platform_color, (left, bottom), (right, bottom), line_width)
            pygame.draw.line(screen, platform_color, (left, bottom), (mid, top), line_width)
            pygame.draw.line(screen, platform_color, (mid, top), (right, bottom), line_width)
        
        return pygame.Rect(self.x_pos, self.y_pos, self.length * section_w, 2)
#ladder class
class Ladder:
    def __init__(self, x_pos, y_pos, length):
        self.x_pos = x_pos * section_w
        self.y_pos = y_pos
        self.length = length
        self.body = self.draw()
    #draw ladders
    def draw(self):
        line_width = 3
        lad_color = (0,0,0)
        lad_height = 0.6
        #create ladder
        for i in range(self.length):
            top = self.y_pos + lad_height * section_h * i
            mid = top + (lad_height / 2) * section_h
            bottom = top + lad_height * section_h
            left = self.x_pos
            right = left + section_w
            #create ladder    
            pygame.draw.line(screen, lad_color, (left, top), (left, bottom), line_width)
            pygame.draw.line(screen, lad_color, (right, top), (right, bottom), line_width)
            pygame.draw.line(screen, lad_color, (left, mid), (right, mid), line_width)
        
        return pygame.Rect(self.x_pos, self.y_pos - section_h,
                         section_w, (lad_height * self.length * section_h + section_h))
#screen for the full 
def draw_screen():
    platforms = []
    climbers = []
    for ladder in levels[state.active_level]['columns']:
        lad = Ladder(*ladder)
        if ladder[2] >= 3:
            climbers.append(lad.body)
    for floor in levels[state.active_level]['rows']:
        br = Floor(*floor)
        platforms.append(br.top)
    return platforms, climbers

#GUI
def draw_extras():
    screen.blit(font.render(f'I•{state.score}', True, 'black'), (3*section_w, 2*section_h))
    screen.blit(font.render(f'TOP•{state.high_score}', True, 'black'), (14 * section_w, 2 * section_h))
    screen.blit(font.render(f'[  ][        ]', True, 'black'), (20 * section_w, 4 * section_h))
    screen.blit(font2.render(f'  M    BONUS ', True, 'black'), (20 * section_w + 5, 4 * section_h))
    screen.blit(font2.render(f'  {state.lives}       {state.bonus}  ', True, 'black'),
                (20 * section_w + 5, 5 * section_h))
    if state.beam_Count < state.beam_Spawn // 2:
        screen.blit(baby1, (10 * section_w, r6 - 6 * section_h))
    else:
        screen.blit(baby2, (10 * section_w, r6 - 6 * section_h))
    Beamd = draw_rocks()
    draw_zilla()
    return Beamd

#draw the rocks
def draw_rocks():
    x, y = 2 * section_w, window_h - 4.5 * section_h
    Beamd = pygame.Rect(x, y, 2 * section_w, 2.5 * section_h)
    screen.blit(rocks, (x + 0.5 * section_w, y - 1 * section_h))
    return Beamd

#draw godzilla
def draw_zilla():
    phase_time = state.beam_time // 4
    if state.beam_Spawn - state.beam_Count > 3 * phase_time:
        zilla_img = zilla1 
    elif state.beam_Spawn - state.beam_Count > 2 * phase_time:
        zilla_img = zilla2
    elif state.beam_Spawn - state.beam_Count > phase_time:
        zilla_img = zilla3
    else:
        zilla_img = pygame.transform.flip(zilla1, True, False)
        screen.blit(beam_img, (250, 250))
    screen.blit(zilla_img, (3.5 * section_w, r6 - 5.5 * section_h))

#will check if king kong climbs
def check_climb():
    can_climb = False
    climb_down = False
    under = pygame.Rect(kong.rect.left, kong.rect.bottom, kong.rect.width, 2 * section_h)
    for lad in lads:
        if kong.hitbox.colliderect(lad):
            can_climb = True
        if under.colliderect(lad):
            climb_down = True
    if (not can_climb and (not climb_down or kong.y_change < 0)) or \
       (kong.landed and can_climb and kong.y_change > 0 and not climb_down):
        kong.climbing = False
    return can_climb, climb_down

#beam collision
def beam_collide(reset):
    under = pygame.Rect(kong.rect.left, kong.rect.bottom, kong.rect.width, 2 * section_h)
    for bms in beam_s:
        if bms.hitbox.colliderect(kong.hitbox):
            reset = True
        elif not kong.landed and not kong.over_beams and under.colliderect(bms.hitbox):
            kong.over_beams = True
            state.score += 100
    if kong.landed:
        kong.over_beams = False
    return reset

#reset level conditions
def reset_level():
    global kong
    pygame.time.delay(1000)
    death_sound.play() #death sound play 
    beam_s.empty()
    aura.empty()
    Clubs.empty()
    kong.kill()
    kong = King_Kong(250, window_h - 130)
    if state.active_level < len(levels) and 'Clubs' in levels[state.active_level]:
        for stick in levels[state.active_level]['Clubs']:
            Clubs.add(Club(*stick))
    state.lives -= 1
    state.bonus = 6000
    state.first_rock_trigger = False
    state.beam_Spawn = 360
    state.beam_Count = state.beam_Spawn // 2
    state.reset_game = False

def check_victory():
    if state.active_level >= len(levels):
        return False
    target = levels[state.active_level]['target']
    target_rect = pygame.Rect(target[0] * section_w, target[1], section_w * target[2], 1)
    return kong.bottom.colliderect(target_rect)
#if victory will show screen and play music and go next level
def next_level():
    victory_sound.play()
    screen.blit(font.render('NEXT LEVEL!', True, 'white'), (window_w//2 - 100, window_h//2 - 50))
    pygame.display.flip()
    pygame.time.delay(2000)
    state.lives += 1
    state.score += state.bonus
    if state.score > state.high_score:
        state.high_score = state.score
    if state.active_level + 1 < len(levels):
        state.active_level += 1
        reset_level()
    else:
        return False
    return True
#reset everything
def reset_game_completely():
    global kong, beam_s, aura, Clubs
    #reset game
    state.reset()
    #reset the sprites
    beam_s.empty()
    aura.empty()
    Clubs.empty()
    # Recreate Kong
    kong = King_Kong(250, window_h - 130)
    
    #re init the clubs
    if levels and state.active_level < len(levels) and 'Clubs' in levels[state.active_level]:
        for stick in levels[state.active_level]['Clubs']:
            Clubs.add(Club(*stick))
#if all lives are gone
def show_game_over_screen():
    screen.blit(wallpaper, (0, 0))
    screen.blit(font.render('GAME OVER!', True, 'red'), (window_w//2 - 100, window_h//2 - 100))
    screen.blit(font2.render('Press R to Restart', True, 'white'), (window_w//2 - 100, window_h//2))
    screen.blit(font2.render('Press Q to Quit', True, 'white'), (window_w//2 - 100, window_h//2 + 50))
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game_completely()
                    return True
                elif event.key == pygame.K_q:
                    return False
        timer.tick(fps)
    return False

#Init objects
beam_s = pygame.sprite.Group()
aura = pygame.sprite.Group()
Clubs = pygame.sprite.Group()
#Initiliaze Kong
kong = King_Kong(250, window_h - 130)
#Initalize Clubs for the level
if levels and state.active_level < len(levels) and 'Clubs' in levels[state.active_level]:
    for stick in levels[state.active_level]['Clubs']:
        Clubs.add(Club(*stick))

#Play music indefinitely until lives reset or proceeds to next level
theme.play(-1)
#Game Loop
run = True
while run:
    if state.game_over:
        if not show_game_over_screen():
            run = False
        continue    
    #Background
    screen.blit(wallpaper, (0, 0))
    timer.tick(fps)   
    #Updates the counter
    if state.counter < 60:
        state.counter += 1
    else:
        state.counter = 0
        if state.bonus > 0:
            state.bonus -= 100   
    #Draws the full platform
    plats, lads = draw_screen()
    Beamd_drum = draw_extras()
    climb, down = check_climb() 
    #Beam spawn count
    if state.beam_Count < state.beam_Spawn:
        state.beam_Count += 1
    else:
        state.beam_Count = random.randint(0, 120)
        state.beam_time = state.beam_Spawn - state.beam_Count
        beam_s.add(Beam(3.5 * section_w + zilla1.get_width()//2, r6 - 5.5 * section_h))
        beam_sound.play()   
        if not state.first_rock_trigger:
            aura.add(Crystal(5 * section_w, window_h - 4 * section_h))
            state.first_rock_trigger = True
    #Update beams 
    for beams in beam_s:
        beams.draw()
        beams.check_fall()
        state.rock_trigger = beams.update(state.rock_trigger)  
        if kong.Club and (beams.hitbox.colliderect(kong.Club_box) or beams.rect.colliderect(kong.Club_box)):
            beams.kill()
            state.score += 500
    #Rock spawn
    if state.rock_trigger:
        aura.add(Crystal(5 * section_w, window_h - 4 * section_h))
        rock_sound.play()
        state.rock_trigger = False 
    #Rock check for collision with king kong
    for crystal_obj in aura:
        crystal_obj.check_climb()
        if crystal_obj.rect.colliderect(kong.hitbox):
            state.reset_game = True
    #rock update
    aura.update()
    aura.draw(screen)
    #draws kong and updates his character
    kong.update()
    kong.draw()
    #place clubs
    for stick in Clubs:
        stick.draw()
    # Check for collisions
    state.reset_game = beam_collide(state.reset_game)
    # Check for victory
    state.victory = check_victory()
    #Will check to reset
    if state.reset_game:
        if state.lives > 0:
            reset_level()
            state.reset_game = False
        else:
            state.game_over = True
            continue
    #If not victory
    if state.victory:
        if not next_level():
            run = False
    #Keyboard controls when controlling king kong
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and not kong.climbing:
                kong.x_change = 1
                kong.dir = 1
            if event.key == pygame.K_LEFT and not kong.climbing:
                kong.x_change = -1
                kong.dir = -1
            if event.key == pygame.K_SPACE and kong.landed:
                kong.landed = False
                kong.y_change = -6
                jump_sound.play()
            if event.key == pygame.K_UP and climb:
                kong.y_change = -2
                kong.x_change = 0
                kong.climbing = True
            if event.key == pygame.K_DOWN and down:
                kong.y_change = 2
                kong.x_change = 0
                kong.climbing = True
        
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_RIGHT, pygame.K_LEFT):
                kong.x_change = 0
            if event.key == pygame.K_UP and climb:
                kong.y_change = 0
                if kong.landed:
                    kong.climbing = False
            if event.key == pygame.K_DOWN and down:
                kong.y_change = 0
                if kong.landed:
                    kong.climbing = False
    
    pygame.display.flip()

pygame.quit()
