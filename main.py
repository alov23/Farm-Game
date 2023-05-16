import game_functionality
from game_functionality import pygame

print(game_functionality.WINDOW_SIZE)

class Crop(pygame.Surface, pygame.sprite.Sprite):
    def __init__(self, crop_name, crop_image_name):
        self.image = pygame.image.load(f"sprites/crops/{crop_image_name}.png")
        super().__init__((self.image.get_width(), self.image.get_height()))

# format: {"name_of_animation_state": (
#             fps,
#             pygame.image.load("path/to/spritesheet.png")
#         )}
#try:
test_animated = game_functionality.Animateable_Sprite({"waving": (1, pygame.image.load("crops/wheat/anim_spritesheets/waving.png"))})
#except Exception as e:
#    log = open("log.txt", "w")
#    log.write(str(e))
#    log.close()

game_functionality.game(test_animated)