import game_functionality
from game_functionality import pygame

print(game_functionality.WINDOW_SIZE)

class Crop(pygame.Surface, pygame.sprite.Sprite):
    def __init__(self, crop_name, crop_image_name):
        self.image = pygame.image.load(f"sprites/crops/{crop_image_name}.png")
        super().__init__((self.image.get_width(), self.image.get_height()))