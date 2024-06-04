import pygame
from random import randint
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join(FILEPATH,'images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
        self.direction = pygame.Vector2(0,0)
        self.speed = 500

    def update(self,dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE]:
            print('fire laser')
        # player
        p.rect.center += p.direction * p.speed * dt
        if p.rect.right > WINDOW_WIDTH:
            p.rect.right = WINDOW_WIDTH
        if p.rect.left < 0:
            p.rect.left = 0
        if p.rect.top < 0:
            p.rect.top = 0
        if p.rect.bottom > WINDOW_HEIGHT:
            p.rect.bottom = WINDOW_HEIGHT

class Star(pygame.sprite.Sprite):
    def __init__(self, speed, groups):
        super().__init__(groups)
        self.speed = speed
        self.image = pygame.image.load(join(FILEPATH,'images','star.png')).convert_alpha()
        self.rect = self.image.get_frect(center=(randint(0,WINDOW_WIDTH),randint(0,WINDOW_HEIGHT)))
        

    def update(self,dt):
        # linear star
        self.rect.y += (self.speed*dt)
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.top = 0
            self.rect.x = randint(0,WINDOW_WIDTH)
        

        # stochastic star   
        # for i in range(5):
        #     xrand = randint(0,WINDOW_WIDTH)
        #     yrand = randint(0,WINDOW_HEIGHT)
        #     display_surface.blit(self.image, (xrand,yrand)) 



# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720
display_surface  = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('Shooter')
running = True
clock = pygame.time.Clock()
FILEPATH = 'space shooter'

# initialization
all_sprites = pygame.sprite.Group()
p = Player(all_sprites)
for i in range(20):
    s = Star(p.speed,all_sprites)

meteor_surf = pygame.image.load(join(FILEPATH,'images','meteor.png')).convert_alpha()
meteor_rect = meteor_surf.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))

laser_surf = pygame.image.load(join(FILEPATH,'images','laser.png')).convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft = (20,WINDOW_HEIGHT-20))

while running:
    dt = clock.tick()/1000
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # enable quit
            running = False

    all_sprites.update(dt)

    # draw the game, order matters, last will be top
    display_surface.fill('black') 

    for i in range(2):
        display_surface.blit(meteor_surf, (randint(0,WINDOW_WIDTH),randint(0,WINDOW_HEIGHT)))
    
    all_sprites.draw(display_surface)

   
    
    pygame.display.update() # flip() update some part of the window
    
pygame.quit()