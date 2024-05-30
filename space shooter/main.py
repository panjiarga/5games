import pygame
from random import randint
from os.path import join

# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720
display_surface  = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('Shooter')
running = True
clock = pygame.time.Clock()
FILEPATH = 'space shooter'

# surface

# converting image, if no transparent pixels: convert(), if has transparent pixels convert_alpha()
player_surf = pygame.image.load(join(FILEPATH,'images', 'player.png')).convert_alpha()
player_rect = player_surf.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
x_player = 100
player_direction = -1
player_speed = 3

star_surf = pygame.image.load(join(FILEPATH,'images','star.png')).convert_alpha()
star_positions = [(randint(0,WINDOW_WIDTH),randint(0,WINDOW_HEIGHT)) for i in range(20)]
x_star = randint(0,1280)
y_star = randint(0,720)

meteor_surf = pygame.image.load(join(FILEPATH,'images','meteor.png')).convert_alpha()
meteor_rect = meteor_surf.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))

laser_surf = pygame.image.load(join(FILEPATH,'images','laser.png')).convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft = (20,WINDOW_HEIGHT-20))

while running:
    clock.tick()
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # enable quit
            running = False

    # draw the game, order matters, last will be top
    display_surface.fill('cyan4')
    for pos in star_positions:
        display_surface.blit(star_surf, (pos[0],pos[1])) 
        # x_star = random.randint(0,WINDOW_WIDTH)
        # y_star = random.randint(0,WINDOW_HEIGHT)

    for i in range(5):
        x_star = randint(0,WINDOW_WIDTH)
        y_star = randint(0,WINDOW_HEIGHT)
        display_surface.blit(star_surf, (x_star,y_star)) 

    display_surface.blit(meteor_surf, meteor_rect)
    display_surface.blit(laser_surf, laser_rect)


    player_rect.left += player_direction * player_speed
    if (player_rect.left <0) or (player_rect.right > WINDOW_WIDTH) : 
        player_direction *= -1
    display_surface.blit(player_surf, player_rect)
   
    
    pygame.display.update() # flip() update some part of the window
    


pygame.quit()