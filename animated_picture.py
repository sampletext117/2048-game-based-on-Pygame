import pygame
import os

class Coin(pygame.sprite.Sprite):
    def __init__(self, group, image_num):
        super().__init__(group)
        self.number = image_num
        self.image = load_image("star" + str(self.number) + ".png")
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 10

    def update(self):
        if self.number < 6:
            self.number += 1
        if self.number >= 6:
            self.number = 1
        self.image = load_image("star" + str(self.number) + ".png")

def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    try:
        image = pygame.image.load(fullname)
        return image
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
