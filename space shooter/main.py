import pygame
from random import randint
from random import uniform
from os.path import join

# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720
display_surface  = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('Shooter')
running = True
timer = 0
global_speed = 0.5
clock = pygame.time.Clock()
FILEPATH = 'space shooter'
music = pygame.mixer.music.load(join(FILEPATH,'audio', 'visual.mp3'))

def second(i):
    return int(i*1000)

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join(FILEPATH,'images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
        self.direction = pygame.Vector2(0,0)
        self.speed = 600
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = second(0.5)
        self.laser_image = pygame.image.load(join(FILEPATH,'images','laser.png')).convert_alpha()

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            #print((current_time - self.laser_shoot_time))
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot=True

    def update(self,dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        if self.direction:
            self.direction = self.direction.normalize()
            #print(self.direction)
        else:
            self.direction

        # fire laser
        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(self.speed*2,self.laser_image,self.rect.midtop,all_sprites)
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            #print('fire laser ', self.laser_shoot_time)       

        self.laser_timer()

        # update position
        p.rect.center += p.direction * p.speed * dt
        if p.rect.right > WINDOW_WIDTH:
            p.rect.right = WINDOW_WIDTH
        if p.rect.left < 0:
            p.rect.left = 0
        if p.rect.top < 0:
            p.rect.top = 0
        if p.rect.bottom > WINDOW_HEIGHT:
            p.rect.bottom = WINDOW_HEIGHT

class Laser(pygame.sprite.Sprite):
    def __init__(self, speed, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
        self.speed = speed

    def update(self,dt):
        self.rect.centery -= self.speed*dt
        if self.rect.bottom <0:
            self.kill()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        #self.speed = speed
        #self.image = pygame.image.load(join(FILEPATH,'images','star.png')).convert_alpha()
        self.image = pygame.Surface((2,2))
        self.speed = 1000/randint(50,80)
        pygame.draw.circle(self.image,'white',(1,1),1)
        self.rect = self.image.get_frect(center=(randint(0,WINDOW_WIDTH),randint(0,WINDOW_HEIGHT)))
        
    def update(self,dt):
        # linear star
        self.rect.y += (self.speed*dt)
        if self.rect.top > WINDOW_HEIGHT:
            self.rect.bottom = 0
            self.rect.x = randint(0,WINDOW_WIDTH)
        # stochastic star   
        # for i in range(5):
        #     xrand = randint(0,WINDOW_WIDTH)
        #     yrand = randint(0,WINDOW_HEIGHT)
        #     display_surface.blit(self.image, (xrand,yrand)) 

class Meteor(pygame.sprite.Sprite):
    def __init__(self, speed, direction, groups):
        super().__init__(groups)
        self.speed = speed
        self.image = pygame.image.load(join(FILEPATH,'images','meteor.png')).convert_alpha()
        #self.image.fill('white')
        self.rect = self.image.get_frect(left=uniform(0,WINDOW_WIDTH),bottom=uniform(-500,-50))
        self.direction = direction
        #print(self.rect.x, self.rect.y, 'dir ', self.direction, 'speed ', self.speed)

    def update(self,dt):
        # linear diagonal meteor
        self.rect.center += self.speed * self.direction * dt
        #print(self.speed)
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()

# custom events => meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event,second(0.5))
meteor_belt = pygame.event.custom_type()
pygame.time.set_timer(meteor_belt,second(5))

# initialization
all_sprites = pygame.sprite.Group()
stars = pygame.sprite.Group()
for i in range(200):
    s = Star(stars)
p = Player(all_sprites)
pygame.mixer.music.play()
# run
while running:
    
    dt = clock.tick()/1000
    dt_stars = dt*global_speed
    if (timer <= int(pygame.time.get_ticks()/1000)):
        timer +=1
        print(timer)
        if (timer>=29):
            global_speed=2
        if (timer>=115):
            global_speed=0.8
            dt*=0.5
        if (timer>=152):
            global_speed=4
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # enable quit
            running = False
        if (timer>30) and (timer<118):
            if event.type == meteor_event:
            #print('meteor')
                m = Meteor(randint(500,1000),(pygame.Vector2(uniform(-0.5,0.5),1)), all_sprites)
            if event.type == meteor_belt:
                speed = randint(300,500)
                for i in range(10):
                    m = Meteor(speed,pygame.Vector2(0,1), all_sprites)

    all_sprites.update(dt)
    stars.update(dt_stars)

    # draw the game, order matters, last will be top
    display_surface.fill('black')
    stars.draw(display_surface)
    all_sprites.draw(display_surface)

    

    pygame.display.update() # flip() update some part of the window
    
pygame.quit()