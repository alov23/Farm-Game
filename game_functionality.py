import sys
import pygame
from pygame.locals import *

import config

pygame.init()
DISPLAY_SIZE = (pygame.display.Info().current_w, pygame.display.Info().current_h)
print(f"DISPLAY_SIZE[0]: {DISPLAY_SIZE[0]}") # print display width
print(f"DISPLAY_SIZE[1]: {DISPLAY_SIZE[1]}") # print display height
WINDOW_SIZE = (int((DISPLAY_SIZE[0] *7)/8), int(( ((DISPLAY_SIZE[0]/16)*9) *7)/8)) # makes window 3/4 the width of the users display and keeps it 16:9 aspect ratio
print(f"WINDOW_SIZE[0]: {WINDOW_SIZE[0]}") # print window width
print(f"WINDOW_SIZE[1]: {WINDOW_SIZE[1]}") # print window height
game_screen = pygame.display.set_mode(tuple(WINDOW_SIZE))
clock = pygame.time.Clock()

#player_sprite = pygame.image.load("sprites/player.png")


class Camera(pygame.Surface):
    def __init__(self, width, height):
        super().__init__((width, height))
        self.position = [0, 0]
        self.rect = pygame.Rect((0, 0), (width, height))

game_camera = Camera(WINDOW_SIZE[0], WINDOW_SIZE[1])

scaled_game_camera = Camera(WINDOW_SIZE[0], WINDOW_SIZE[1])

def scale(old_surface:pygame.Surface, new_width:int, new_height:int):
    global scaled_game_camera
    scaled_game_camera = Camera(new_width, new_height)
    pygame.transform.scale(old_surface, (new_width, new_height), scaled_game_camera)

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


# update world
# move camera to new player position
# update screen to show new camera position

def set_zoom_level(camera:Camera, newZoomLevel:int):
    if (newZoomLevel > 1):
        config.CAMERA_ZOOM_AMOUNT = newZoomLevel
        config.CAMERA_AREA_WIDTH_MODIFIER = -(camera.get_width() / (2/(newZoomLevel-1)))
        config.CAMERA_AREA_HEIGHT_MODIFIER = -(camera.get_height() / (2/(newZoomLevel-1)))
        scale(camera, camera.get_width() / config.CAMERA_ZOOM_AMOUNT, camera.get_height() / config.CAMERA_ZOOM_AMOUNT)
    elif (newZoomLevel == 1):
        config.CAMERA_ZOOM_AMOUNT = newZoomLevel
        config.CAMERA_AREA_WIDTH_MODIFIER = 0
        config.CAMERA_AREA_HEIGHT_MODIFIER = 0
        scale(camera, WINDOW_SIZE[0], WINDOW_SIZE[1])
    else:
        raise Exception(f"Can not have {newZoomLevel}x zoom")

def zoom_in(camera:Camera, zoomAmount:int):
    set_zoom_level(camera, config.CAMERA_ZOOM_AMOUNT + zoomAmount)

def zoom_out(camera:Camera, zoomAmount:int):
    set_zoom_level(camera, config.CAMERA_ZOOM_AMOUNT - zoomAmount)


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
#    ------------------------------------- change all this to change world_offset variables instead of setting camera.position -------------------------------------
#    this stuff makes it so the camera wont show stuff thats out of bounds
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



def update_screen(screen:pygame.Surface, camera:Camera):
    #print(camera.get_width())
    #print(camera.get_width() / 1, end=" - ")
    #print(f"({camera.get_width()} -> ({scaled_game_camera.get_width()}), {camera.get_height()} -> ({scaled_game_camera.get_height()}))", end=" - ")
    #screen.blit(
    #    pygame.transform.scale(camera, (camera.get_width()*config.CAMERA_ZOOM_AMOUNT, camera.get_height()*config.CAMERA_ZOOM_AMOUNT)),
    #    (config.CAMERA_AREA_WIDTH_MODIFIER, config.CAMERA_AREA_HEIGHT_MODIFIER)
    #    )
    screen.blit(
        pygame.transform.scale(camera, (camera.get_width()*config.CAMERA_ZOOM_AMOUNT, camera.get_height()*config.CAMERA_ZOOM_AMOUNT)),
        (0, 0)
        )
    #screen.blit(camera, (0, 0))

def update_world(world:World, camera:Camera, ground:Ground, sprites:list):
    world.fill((150, 150, 150))
#    sprites_on_screen = []

    world.blit(ground.image, (0, 0))

    for sprite in sprites:
        #if sprite.rect.colliderect(camera.rect): !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! NEED TO FIX SOMEHOW !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #print(sprite == player)
        print(f"{camera.rect.center} - {camera.position}")
        world.blit(sprite.image, (sprite.position[0], sprite.position[1]))
#            sprites_on_screen.append(sprite)

while True:
    player_update_x, player_update_y = 0, 0

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                zoom_out(game_camera, 1)
                #CURRENT_ZOOM_LEVEL -= 1
                #if CURRENT_ZOOM_LEVEL <= -1:
                #    CURRENT_ZOOM_LEVEL = len(config.ZOOM_LEVELS)-1
                #config.CAMERA_ZOOM_AMOUNT = config.ZOOM_LEVELS[CURRENT_ZOOM_LEVEL][0]
                #config.UPDATE_SCREEN_DIV_DENOM = config.ZOOM_LEVELS[CURRENT_ZOOM_LEVEL][1]
            if event.key == K_RIGHT:
                zoom_in(game_camera, 1)
                #CURRENT_ZOOM_LEVEL += 1
                #if CURRENT_ZOOM_LEVEL >= len(config.ZOOM_LEVELS):
                #    CURRENT_ZOOM_LEVEL = 0
                #config.CAMERA_ZOOM_AMOUNT = config.ZOOM_LEVELS[CURRENT_ZOOM_LEVEL][0]
                #config.UPDATE_SCREEN_DIV_DENOM = config.ZOOM_LEVELS[CURRENT_ZOOM_LEVEL][1]

    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_w]:
        player_update_y -= config.MOVEMENT_SPEED_VARIABLE
    if pressed_keys[K_s]:
        player_update_y += config.MOVEMENT_SPEED_VARIABLE
    if pressed_keys[K_a]:
        player_update_x -= config.MOVEMENT_SPEED_VARIABLE
    if pressed_keys[K_d]:
        player_update_x += config.MOVEMENT_SPEED_VARIABLE
    if pressed_keys[K_LSHIFT]:
        player_update_x *= config.MOVEMENT_SPEED_RUN_MULTIPLIER
        player_update_y *= config.MOVEMENT_SPEED_RUN_MULTIPLIER
    
    player.update_position(player_update_x, player_update_y)

    scaled_game_camera.position = player.position
    
    update_camera_position(scaled_game_camera, game_world, player)
    update_world(game_world, scaled_game_camera, ground, [player])
    #game_world.blit(player.image, (camera.position[0], camera.position[1]))
#    update_camera(game_camera, [ground, player])
    update_screen(game_screen, scaled_game_camera)

    #print(player.position)
    #print(f"zoom: {config.CAMERA_ZOOM_AMOUNT} - ({config.CAMERA_AREA_WIDTH_MODIFIER}, {config.CAMERA_AREA_HEIGHT_MODIFIER})", end="")

    #if (scaled_game_camera.get_width() % ((DISPLAY_SIZE[0] *7)/8)/config.CAMERA_ZOOM_AMOUNT == 0 and scaled_game_camera.get_height() % (( ((DISPLAY_SIZE[0]/16)*9) *7)/8)/config.CAMERA_ZOOM_AMOUNT == 0):
    #    print(f" - true!")
    #else:
    #    print(f" - {((DISPLAY_SIZE[0] *7)/8)/config.CAMERA_ZOOM_AMOUNT}, {(( ((DISPLAY_SIZE[0]/16)*9) *7)/8)/config.CAMERA_ZOOM_AMOUNT}")

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
#  9) plant amount of time to age per season
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