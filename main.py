from PIL import Image
import game_framework
from game_framework import pygame

print(game_framework.WINDOW_SIZE)

test_image = Image.open("crops/wheat/anim_spritesheets/waving.png")
test_image = test_image.convert("RGBA")
d = test_image.getdata()
pixels = [[]]

x = 0
y = 0
for pixel in d:
    if x == (32*6):
        x = 0
        y += 1
        pixels.append([])
    #print(f"{x}, {y}")
    #
    #print(f"{pixel[:3]} - {type(pixel[:3])}")
    pixels[y].append(pixel[:3])
    
    x += 1
print(pixels)
#print(str(test_image.getdata()))

class Crop(pygame.Surface, pygame.sprite.Sprite):
    def __init__(self, crop_name, crop_image_name):
        self.image = pygame.image.load(f"sprites/crops/{crop_image_name}.png")
        super().__init__((self.image.get_width(), self.image.get_height()))

# format: {"name_of_animation_state": (
#             amount_of_frames_to_show_each_frame,
#             pygame.image.load("path/to/spritesheet.png")
#         )}
#try:
test_animated = game_framework.Animateable_Sprite({"waving": (10, pygame.image.load("crops/wheat/anim_spritesheets/waving.png"))}, (780, 390))
test_paletted = game_framework.Animateable_Sprite_Paletted(pygame.image.load("player/img/player_palette.png"), {"waving": (10, pygame.image.load("player/img/player_1.png"))}, (700, 390))
#except Exception as e:
#    log = open("log.txt", "w")
#    log.write(str(e))
#    log.close()

game_framework.game(test_animated, test_paletted)