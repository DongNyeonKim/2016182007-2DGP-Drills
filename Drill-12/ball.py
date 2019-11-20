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

    def get_bb(self):
        return self.x -10, self.y -10, self.x +10, self.y +10

    def draw(self):
        draw_rectangle(*self.get_bb())
        self.image.clip_draw(0, 0, 21, 21, self.x, self.y)

