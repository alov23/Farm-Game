import game_functionality
from game_functionality import pygame

print(game_functionality.WINDOW_SIZE)

class Crop(pygame.Surface, pygame.sprite.Sprite):
    def __init__(self, crop_name, crop_image_name):
        self.image = pygame.image.load(f"sprites/crops/{crop_image_name}.png")
        super().__init__((self.image.get_width(), self.image.get_height()))

game_functionality.game()

# read from crop_locations.json to find places player can interact with to place crops
# [
#     (100, 200)
# ]
# = player can place a crop at x = 100, y = 200
#
# potentially have unlock conditions, also maybe just numbered for ease of modification
# [
#    ((100, 200), [1, 3, 4])
# ]
# = player has to finish the map-specific conditions 1, 3, and 4 before this spot is availabe
# can use for things like plant spots inside a greenhouse that has to be built