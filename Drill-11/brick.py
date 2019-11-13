from pico2d import *
import game_world
import game_framework

MIN_FALL_SPEED = 50
MAX_FALL_SPEED = 200

class Brick:
    image = None

    def __init__(self):
        if Brick.image == None:
            Brick.image = load_image('brick180x40.png')
        self.x, self.y, self.speed = 200,200,300
        self.dir=0

    def get_bb(self):
        return self.x - 90, self.y - 20, self.x + 90, self.y + 20

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())
        # fill here for draw

    def update(self):
        if self.x <= 0+90:
            self.dir = 0
        if self.x >= 1600-90:
            self.dir = 1
        if self.dir==0:
            self.x += self.speed * game_framework.frame_time
        elif self.dir==1:
            self.x -= self.speed * game_framework.frame_time

