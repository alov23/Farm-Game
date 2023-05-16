import game_framework
from game_framework import pygame

print(game_framework.WINDOW_SIZE)

class Crop(pygame.Surface, pygame.sprite.Sprite):
    def __init__(self, crop_name, crop_image_name):
        self.image = pygame.image.load(f"sprites/crops/{crop_image_name}.png")
        super().__init__((self.image.get_width(), self.image.get_height()))

# format: {"name_of_animation_state": (
#             amount_of_frames_to_show_each_frame,
#             pygame.image.load("path/to/spritesheet.png")
#         )}
#try:
test_animated = game_framework.Animateable_Sprite({"waving": (10, pygame.image.load("crops/wheat/anim_spritesheets/waving.png"))}, (500, 500))
#except Exception as e:
#    log = open("log.txt", "w")
#    log.write(str(e))
#    log.close()

game_framework.game(test_animated)