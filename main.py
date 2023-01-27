import sys
import pygame
from pygame.locals import *

pygame.init()
DISPLAY_SIZE = (pygame.display.Info().current_w, pygame.display.Info().current_h)
print(DISPLAY_SIZE[0]) # print display width
print(DISPLAY_SIZE[1]) # print display height
WINDOW_SIZE = (int((DISPLAY_SIZE[0] *7)/8), int(( ((DISPLAY_SIZE[0]/16)*9) *7)/8)) # makes window 3/4 the width of the users display and keeps it 16:9 aspect ratio
print(WINDOW_SIZE[0]) # print window width
print(WINDOW_SIZE[1]) # print window height
game_screen = pygame.display.set_mode(tuple(WINDOW_SIZE))
clock = pygame.time.Clock()

#player_sprite = pygame.image.load("sprites/player.png")



# idea for screen scaling
# instead of objects -> camera
# do objects -> new_surface -> camera
# this way the new_surface can be scale transformed before forcing camera boundaries

class Camera(pygame.Surface):
    def __init__(self, width, height):
        super().__init__((width, height))
        self.position = [0, 0]
        self.rect = pygame.Rect((0, 0), (width, height))

game_camera = Camera(WINDOW_SIZE[0], WINDOW_SIZE[1])



class Ground(pygame.Surface, pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.image.load("sprites/ground.png")
        super().__init__((self.image.get_width(), self.image.get_height()))
        self.position = [0, 0]
        self.rect = pygame.Rect(self.position[0], self.position[1], self.image.get_width(), self.image.get_height())

ground = Ground()


class World(pygame.Surface):
    def __init__(self, width, height):
        super().__init__((width, height))
        self.position = [0, 0]
        self.rect = pygame.Rect((0, 0), (width, height))

game_world = World(ground.get_width(), ground.get_height())



class Player(pygame.Surface, pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.image.load("sprites/player.png")
        super().__init__((self.image.get_width(), self.image.get_height()))
        self.position = [
            (ground.get_width() / 2) - (self.image.get_width() / 2),
            (ground.get_height() / 2) - (self.image.get_height() / 2)
        ]
        self.rect = pygame.Rect(self.position[0], self.position[1], self.image.get_width(), self.image.get_height())
        self.facing = 0 # self.facing == 0 means facing right, self.facing == 1 means facing left
    
    def get_rect(self):
        return self.rect
    
    # moves sprite when frame updates
    def update_position(self, update_x, update_y):
        # add code here to change sprite based on direction player is facing
        
        if self.position[0] + update_x < 0:
            self.position[0] = 0
        elif self.position[0] + update_x > ground.get_width() - self.get_width():
            self.position[0] = ground.get_width() - self.get_width()
        else:
            self.position[0] += update_x
        
        if self.position[1] + update_y < 0:
            self.position[1] = 0
        elif self.position[1] + update_y > ground.get_height() - self.get_height():
            self.position[1] = ground.get_height() - self.get_height()
        else:
            self.position[1] += update_y

player = Player()


class Crop(pygame.Surface, pygame.sprite.Sprite):
    def __init__(self, crop_name):
        #self.image =
        super().__init__((self.image.get_width(), self.image.get_height()))


# update world
# move camera to new player position
# update screen to show new camera position

#def update_camera_position(camera:Camera, player:Player):
#    player_x, player_y = player.position
#    player_w, player_h = player.get_rect().size
#    camera_w, camera_h = camera.get_rect().size
#
#    camera_x = player_x+player_w/2 - camera_w/2
#    camera_y = player_y+player_h/2 - camera_h/2
#
#    if camera_x < 0:
#        camera.position[0] = 0
#    elif camera_x > ground.rect.width - WINDOW_SIZE[0]:
#        camera.position[0] = ground.rect.width - WINDOW_SIZE[0]
#    else:
#        camera.position[0] = camera_x
#    
#    if camera_y < 0:
#        camera.position[1] = 0
#    elif camera_y > ground.rect.height - WINDOW_SIZE[1]:
#        camera.position[1] = ground.rect.height - WINDOW_SIZE[1]
#    else:
#        camera.position[1] = camera_y




def update_camera_position(camera:Camera, world:World, player:Player):
    camera.fill((150, 150, 150))

    player_w, player_h = player.get_rect().size
    player_x, player_y = player.position
    camera_w, camera_h = camera.get_rect().size

    #world_x_offset, world_y_offset = ((player_x / 2) + (player_w / 2), (player_y / 2) + (player_h / 2)) # use math to make offset have player in center
    #world_x_offset, world_y_offset = (0, 0)
    world_x_offset, world_y_offset = (# maybe have global variable of camera transformation size percent i.e. 1.0 as default, 2.0 two times zoom, then multiply all camera width and height values used here by it (also multiply values in update_screen())
        ( (-(player_x)) - (player_w / 2) ) + (camera_w / 2),
        ( (-(player_y)) - (player_h / 2) ) + (camera_h / 2)
        )

    camera.blit(world, (world_x_offset, world_y_offset))
#
#    camera_x = player_x+player_w/2 - camera_w/2
#    camera_y = player_y+player_h/2 - camera_h/2
#
#    if camera_x < 0:
#        camera.position[0] = 0
#    elif camera_x > ground.rect.width - WINDOW_SIZE[0]:
#        camera.position[0] = ground.rect.width - WINDOW_SIZE[0]
#    else:
#        camera.position[0] = camera_x
#    
#    if camera_y < 0:
#        camera.position[1] = 0
#    elif camera_y > ground.rect.height - WINDOW_SIZE[1]:
#        camera.position[1] = ground.rect.height - WINDOW_SIZE[1]
#    else:
#        camera.position[1] = camera_y




#def update_camera(camera:Camera, surfaces):
#    camera.fill((150, 150, 150))
#    camera_x, camera_y = camera.position
#
#    for surface in surfaces:
#        surface_x, surface_y = surface.position
#
#        result = (surface_x-camera_x, surface_y-camera_y)
#        camera.blit(surface.image, result)

def update_screen(screen:pygame.Surface, camera:Camera):
    screen.blit(pygame.transform.scale(camera, (camera.get_width()*2, camera.get_height()*2)), (-(camera.get_width()/2), -(camera.get_height()/2)))
    #screen.blit(camera, (0, 0))

def update_world(world:World, camera:Camera, ground:Ground, sprites:list):
    world.fill((150, 150, 150))
#    sprites_on_screen = []

    world.blit(ground.image, (0, 0))

    for sprite in sprites:
        if sprite.rect.colliderect(camera.rect):
            world.blit(sprite.image, (sprite.position[0], sprite.position[1]))
#            sprites_on_screen.append(sprite)


movementSpeedVariable = 4
movementSpeedRunMultiplier = 2

while True:
    player_update_x, player_update_y = 0, 0

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_w]:
        player_update_y -= movementSpeedVariable
    if pressed_keys[K_s]:
        player_update_y += movementSpeedVariable
    if pressed_keys[K_a]:
        player_update_x -= movementSpeedVariable
    if pressed_keys[K_d]:
        player_update_x += movementSpeedVariable
    if pressed_keys[K_LSHIFT]:
        player_update_x *= movementSpeedRunMultiplier
        player_update_y *= movementSpeedRunMultiplier
    
    player.update_position(player_update_x, player_update_y)
    
    update_camera_position(game_camera, game_world, player)
    update_world(game_world, game_camera, ground, [player])
#    update_camera(game_camera, [ground, player])
    update_screen(game_screen, game_camera)

    print(player.position)

    pygame.display.flip()
    clock.tick(60)

# notes
#screen = pygame.display.set_mode((75*16, 75*9)) # can change window size like this


#                  Crops json layout
#------------------------------------------------------
# crop name: [
#  1) price to buy seeds per season
#      1) spring
#      2) summer
#      3) fall
#      4) winter
#  2) can buy seeds in which seasons
#      1) spring
#      2) summer
#      3) fall
#      4) winter
#  3) plant sell price per season
#      1) spring
#          1) live price
#          2) dead price
#      2) summer
#          1) live price
#          2) dead price
#      3) fall
#          1) live price
#          2) dead price
#      4) winter
#          1) live price
#          2) dead price
#  4) crop sell price per season
#      1) spring
#      2) summer
#      3) fall
#      4) winter
#  5) plant can grow in which seasons
#      1) spring
#      2) summer
#      3) fall
#      4) winter
#  6) plant can produce crops in which seasons
#      1) spring
#      2) summer
#      3) fall
#      4) winter
#  7) plant dies in which seasons
#      1) spring
#      2) summer
#      3) fall
#      4) winter
#  8) plant growth stages
#      1)
#          1) starting stage
#          2) first stage sprite path
#      2)
#          1) 2nd stage - x plant age to reach
#          2) second stage sprite path
#      etc...
#  9) plant age growth per season
#      1) spring
#      2) summer
#      3) fall
#      4) winter
# 10) crop grow time per season (possibly in days)
#      1) spring
#      2) summer
#      3) fall
#      4) winter
# 11) does the entire plant get harvested when harvesting (for things like wheat)
# 12) amount of seeds gained when harvesting (for things like wheat)
#]