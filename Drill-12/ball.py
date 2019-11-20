from pico2d import *
import random

class Ball:
    def __init__(self):
        self.image = load_image('ball21x21.png')
        self.x = random.randint(100, 1100)
        self.y = random.randint(100, 1000)
        self.hp = 100
    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, 21, 21, self.x, self.y)

